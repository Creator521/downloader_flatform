"""Preview and Download API routes with Redis caching and proper error handling."""
import json
import subprocess
import sys
import os
import logging
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import StreamingResponse
from urllib.parse import quote
import yt_dlp

from app.proxy_utils import ProxyManager
from app.dependencies import limiter

logger = logging.getLogger(__name__)

router = APIRouter()
proxy_manager = ProxyManager()


def get_redis_client():
    """Get Redis client — returns None if Redis is unavailable (Point 7: fail-safe)."""
    try:
        import redis
        REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        client = redis.from_url(REDIS_URL, decode_responses=True)
        client.ping()
        return client
    except Exception as e:
        logger.warning(f"Redis unavailable, running without cache: {e}")
        return None


# Initialize Redis (fail-safe)
redis_client = get_redis_client()
CACHE_DURATION = 3600  # 1 Hour


def cache_get(key: str):
    """Safely get from Redis cache (Point 7: fail-safe)."""
    if redis_client is None:
        return None
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        logger.warning(f"Redis read error: {e}")
    return None


def cache_set(key: str, value: dict, ttl: int = CACHE_DURATION):
    """Safely set to Redis cache (Point 7: fail-safe)."""
    if redis_client is None:
        return
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception as e:
        logger.warning(f"Redis write error: {e}")


@router.post("/preview")
@limiter.limit("10/minute")
def preview(request: Request, url: str = Form(...)):
    # Check Cache (Redis) — Point 7: fail-safe
    cached_data = cache_get(url)
    if cached_data:
        return cached_data

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    cookie_file = proxy_manager.get_cookie_file()
    if cookie_file:
        ydl_opts["cookiefile"] = cookie_file

    proxy = proxy_manager.get_proxy()
    if proxy:
        ydl_opts["proxy"] = proxy

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # PROXY THUMBNAIL IF NEEDED
        thumb = info.get("thumbnail")
        if thumb and ("instagram.com" in thumb or "fbcdn" in thumb):
            thumb = f"/proxy-image?url={quote(thumb)}"

        data = {
            "title": info.get("title"),
            "thumbnail": thumb,
            "video_url": info.get("url"),
            "uploader": info.get("uploader"),
            "view_count": info.get("view_count"),
            "duration": info.get("duration")
        }

        # Save to Cache (Redis)
        cache_set(url, data)

        return data
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e).lower()
        logger.error(f"yt-dlp download error for {url}: {e}")
        if "sign in" in error_msg or "login" in error_msg:
            raise HTTPException(
                status_code=400,
                detail="This platform requires login/cookies to download video. Please provide valid cookies."
            )
        raise HTTPException(status_code=400, detail="Failed to process the video URL. Please check and try again.")
    except Exception as e:
        logger.error(f"Preview server error for {url}: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred. Please try again later.")


@router.post("/download")
@limiter.limit("5/minute")
def download(request: Request, url: str = Form(...), format: str = Form("video")):
    # 1. Get Metadata — Point 9: Try Redis cache first to avoid double yt-dlp extraction
    cached_data = cache_get(url)

    if cached_data and cached_data.get("title"):
        # Use cached metadata
        title = cached_data["title"]
        logger.info(f"Using cached metadata for download: {url}")
    else:
        # Fetch fresh metadata
        ydl_opts_meta = {
            "quiet": True,
            "skip_download": True,
        }

        cookie_file = proxy_manager.get_cookie_file()
        if cookie_file:
            ydl_opts_meta["cookiefile"] = cookie_file

        proxy = proxy_manager.get_proxy()
        if proxy:
            ydl_opts_meta["proxy"] = proxy

        try:
            with yt_dlp.YoutubeDL(ydl_opts_meta) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "video")
        except Exception as e:
            error_msg = str(e).lower()
            logger.error(f"Download metadata error for {url}: {e}")
            if "sign in" in error_msg or "login" in error_msg or "requested format is not available" in error_msg:
                raise HTTPException(
                    status_code=400,
                    detail="This platform requires login/cookies to download video. Please provide valid cookies."
                )
            raise HTTPException(status_code=400, detail="Could not fetch video metadata. Please check the URL and try again.")

    # Determine format code and extension
    if format == "audio":
        format_code = "bestaudio/best"
        ext = "m4a"
    else:
        format_code = "best[ext=mp4]/best"
        ext = "mp4"

    # Clean filename
    filename = f"{title}.{ext}"
    filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).strip()

    # 2. Start Streaming Subprocess
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--no-part",
        "--output", "-",
        "--format", format_code,
        "--quiet",
    ]

    # Add Cookie File
    cookie_file = proxy_manager.get_cookie_file()
    if cookie_file:
        cmd.extend(["--cookies", cookie_file])

    # Add Proxy
    proxy = proxy_manager.get_proxy()
    if proxy:
        cmd.extend(["--proxy", proxy])

    cmd.append(url)

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=10**7  # 10MB buffer
        )

        # 3. Create Generator
        def iterfile():
            try:
                while True:
                    data = proc.stdout.read(64 * 1024)  # Read 64KB chunks
                    if not data:
                        break
                    yield data
            except Exception:
                proc.kill()
            finally:
                proc.wait()

        # 4. Return Streaming Response
        media_type = "audio/mp4" if format == "audio" else "video/mp4"
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"'
        }

        return StreamingResponse(
            iterfile(),
            media_type=media_type,
            headers=headers
        )

    except Exception as e:
        logger.error(f"Streaming failed for {url}: {e}")
        raise HTTPException(status_code=500, detail="Download streaming failed. Please try again later.")
