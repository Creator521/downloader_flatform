"""Preview and Download API routes with Redis caching and proper error handling."""
import json
import subprocess
import sys
import os
import logging
import ipaddress
import time
import random
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import StreamingResponse
from urllib.parse import quote, urlparse
import yt_dlp

from app.proxy_utils import proxy_manager
from app.dependencies import limiter

logger = logging.getLogger(__name__)

router = APIRouter()


def validate_url(url: str) -> str:
    """Validate and sanitize URL to prevent SSRF attacks."""
    if not url or not url.strip():
        raise HTTPException(status_code=400, detail="URL is required.")
    
    url = url.strip()
    parsed = urlparse(url)
    
    # Only allow http and https schemes
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="Only HTTP and HTTPS URLs are allowed.")
    
    if not parsed.hostname:
        raise HTTPException(status_code=400, detail="Invalid URL: no hostname found.")
    
    # Block internal/private IPs
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private or ip.is_loopback or ip.is_reserved:
            raise HTTPException(status_code=400, detail="Internal URLs are not allowed.")
    except ValueError:
        # Not an IP address, it's a hostname — that's fine
        pass
    
    # Block common internal hostnames
    blocked_hosts = ["localhost", "0.0.0.0", "metadata.google.internal"]
    if parsed.hostname.lower() in blocked_hosts:
        raise HTTPException(status_code=400, detail="This URL is not allowed.")
    
    return url


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


def extract_info_with_retry(url: str, max_retries: int = 3) -> dict:
    """Attempts to extract video info using yt-dlp, retrying with different proxies on failure."""
    last_error = None
    for attempt in range(max_retries):
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
                if attempt > 0:
                    logger.info(f"Extraction succeeded on attempt {attempt + 1} for {url} using proxy {proxy}")
                return {"info": info, "proxy": proxy}
        except Exception as e:
            last_error = e
            logger.warning(f"yt-dlp extract error (attempt {attempt + 1}/{max_retries}) for {url}: {e}")
            if attempt < max_retries - 1:
                # Add a small delay before retrying with a new proxy
                time.sleep(random.uniform(1.0, 3.0))
            
    # All retries failed
    error_msg = str(last_error).lower()
    logger.error(f"Failed to extract info for {url} after {max_retries} attempts. Last error: {last_error}")
    
    if "sign in" in error_msg or "login" in error_msg or "requested format is not available" in error_msg:
        raise HTTPException(
            status_code=400,
            detail="Instagram/Platform requires login. We are experiencing high traffic from this platform. Please try again in a few moments."
        )
    raise HTTPException(status_code=400, detail="Failed to process the video URL. Please check and try again.")


@router.post("/preview")
@limiter.limit("10/minute")
def preview(request: Request, url: str = Form(...)):
    url = validate_url(url)
    # Check Cache (Redis) — Point 7: fail-safe
    cached_data = cache_get(url)
    if cached_data:
        return cached_data

    # Use the retry mechanism for metadata extraction
    try:
        extracted = extract_info_with_retry(url)
        info = extracted["info"]

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
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Preview server error for {url}: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred. Please try again later.")


@router.post("/download")
@limiter.limit("5/minute")
def download(request: Request, url: str = Form(...), format: str = Form("video")):
    url = validate_url(url)
    # 1. Get Metadata — Point 9: Try Redis cache first to avoid double yt-dlp extraction
    cached_data = cache_get(url)

    successful_proxy = None
    if cached_data and cached_data.get("title"):
        # Use cached metadata
        title = cached_data["title"]
        logger.info(f"Using cached metadata for download: {url}")
    else:
        # Fetch fresh metadata with retries
        extracted = extract_info_with_retry(url)
        info = extracted["info"]
        title = info.get("title", "video")
        successful_proxy = extracted["proxy"]

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
    if successful_proxy:
        cmd.extend(["--proxy", successful_proxy])
    else:
        proxy = proxy_manager.get_proxy()
        if proxy:
            cmd.extend(["--proxy", proxy])

    cmd.append(url)

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
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
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Robots-Tag": "noindex, nofollow",
        }

        return StreamingResponse(
            iterfile(),
            media_type=media_type,
            headers=headers
        )

    except Exception as e:
        logger.error(f"Streaming failed for {url}: {e}")
        raise HTTPException(status_code=500, detail="Download streaming failed. Please try again later.")
