"""Preview and Download API routes with Redis caching and proper error handling."""
import json
import subprocess
import sys
import os
import logging
import ipaddress
import time
import uuid
import random
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import StreamingResponse, RedirectResponse
from urllib.parse import quote, urlparse
import yt_dlp

from app.proxy_utils import proxy_manager
from app.dependencies import limiter

logger = logging.getLogger(__name__)

router = APIRouter()


# ─────────────────────────────────────────────
# INSTALOADER HELPER  (Primary for Instagram)
# ─────────────────────────────────────────────
def is_instagram_url(url: str) -> bool:
    """Check karo ke URL Instagram ka hai ya nahi."""
    return "instagram.com" in urlparse(url).hostname.lower()


def extract_info_with_instaloader(url: str) -> dict | None:
    """
    Instaloader se Instagram Reel/Post ka info extract karo.
    Success pe dict return karta hai, failure pe None.
    Koi login, proxy, ya cookies ki zaroorat nahi!
    """
    try:
        import instaloader
    except ImportError:
        logger.warning("Instaloader not installed. Run: pip install instaloader")
        return None

    try:
        # Shortcode URL se nikalo
        # Supported formats:
        #   https://www.instagram.com/reel/ABC123/
        #   https://www.instagram.com/p/ABC123/
        path_parts = [p for p in urlparse(url).path.split("/") if p]
        shortcode = None
        for i, part in enumerate(path_parts):
            if part in ("reel", "reels", "p", "tv") and i + 1 < len(path_parts):
                shortcode = path_parts[i + 1]
                break

        if not shortcode:
            logger.warning(f"Instaloader: Could not parse shortcode from URL: {url}")
            return None

        L = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,      # Hum sirf info chahte hain
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            quiet=True,
        )

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Video URL — public reels ke liye bina login ke milti hai
        video_url = post.video_url if post.is_video else None
        if not video_url:
            logger.info("Instaloader: Post is not a video/reel.")
            return None

        thumbnail = post.url  # Cover image
        title = post.caption[:100] if post.caption else f"Instagram Reel {shortcode}"
        uploader = post.owner_username
        duration = int(post.video_duration) if post.video_duration else None

        logger.info(f"Instaloader: Successfully extracted info for {shortcode}")

        return {
            "title": title,
            "thumbnail": thumbnail,
            "video_url": video_url,
            "uploader": uploader,
            "view_count": post.video_view_count,
            "duration": duration,
            "_shortcode": shortcode,      # Download ke liye
        }

    except Exception as e:
        logger.warning(f"Instaloader extraction failed for {url}: {e}")
        return None


def stream_with_instaloader(url: str, fmt: str):
    """
    Instaloader se video URL nikalo, phir usse stream karo.
    Returns: (generator, filename) ya (None, None) on failure.
    """
    info = extract_info_with_instaloader(url)
    if not info or not info.get("video_url"):
        return None, None

    video_url = info["video_url"]
    title = info.get("title", "instagram_video")

    # Clean filename
    ext = "mp4" if fmt != "audio" else "m4a"
    filename = f"{title}.{ext}"
    filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).strip()

    # Direct URL se stream karo using requests
    try:
        import requests

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": "https://www.instagram.com/",
        }

        resp = requests.get(video_url, headers=headers, stream=True, timeout=30)
        resp.raise_for_status()

        def iterfile():
            try:
                for chunk in resp.iter_content(chunk_size=64 * 1024):
                    if chunk:
                        yield chunk
            except Exception as ex:
                logger.error(f"Instaloader stream error: {ex}")

        logger.info(f"Instaloader: Streaming video for {url}")
        return iterfile(), filename

    except Exception as e:
        logger.warning(f"Instaloader stream request failed: {e}")
        return None, None



# ─────────────────────────────────────────────
# TIKTOK HELPER (Primary for TikTok)
# ─────────────────────────────────────────────
def is_tiktok_url(url: str) -> bool:
    """Check karo ke URL TikTok ka hai ya nahi."""
    return "tiktok.com" in urlparse(url).hostname.lower()

def extract_info_with_tikwm(url: str) -> dict | None:
    """
    TikWM API se TikTok video ka info extract karo.
    """
    try:
        import requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }
        res = requests.get("https://www.tikwm.com/api/", params={"url": url}, headers=headers, timeout=15)
        res.raise_for_status()
        data_json = res.json()
        
        if data_json.get("code") == 0 and "data" in data_json:
            data = data_json["data"]
            title = data.get("title", "TikTok Video")
            if not title:
                title = "TikTok Video"
            return {
                "title": title[:100],
                "thumbnail": data.get("cover"),
                "video_url": data.get("play"),      # No watermark
                "audio_url": data.get("music"),
                "uploader": data.get("author", {}).get("nickname"),
                "view_count": data.get("play_count"),
                "duration": data.get("duration"),
            }
        else:
            logger.warning(f"TikWM returned error: {data_json.get('msg')}")
    except Exception as e:
        logger.warning(f"TikWM extraction failed for {url}: {e}")
    return None

def stream_with_tikwm(url: str, fmt: str):
    """
    TikWM API se video ya audio URL nikal kar stream karo.
    """
    info = extract_info_with_tikwm(url)
    if not info:
        return None, None

    media_url = info.get("audio_url") if fmt == "audio" else info.get("video_url")
    if not media_url:
        return None, None

    title = info.get("title", "tiktok_video")
    ext = "mp3" if fmt == "audio" else "mp4"
    filename = f"{title}.{ext}"
    filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).strip()
    if not filename:
        filename = f"tiktok.{ext}"

    try:
        import requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        resp = requests.get(media_url, headers=headers, stream=True, timeout=30)
        resp.raise_for_status()

        def iterfile():
            try:
                for chunk in resp.iter_content(chunk_size=64 * 1024):
                    if chunk:
                        yield chunk
            except Exception as ex:
                logger.error(f"TikWM stream error: {ex}")

        logger.info(f"TikWM: Streaming media for {url}")
        return iterfile(), filename
    except Exception as e:
        logger.warning(f"TikWM stream request failed: {e}")
        return None, None

# ─────────────────────────────────────────────
# URL VALIDATION
# ─────────────────────────────────────────────
def validate_url(url: str) -> str:
    """Validate and sanitize URL to prevent SSRF attacks."""
    if not url or not url.strip():
        raise HTTPException(status_code=400, detail="URL is required.")

    url = url.strip()
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="Only HTTP and HTTPS URLs are allowed.")

    if not parsed.hostname:
        raise HTTPException(status_code=400, detail="Invalid URL: no hostname found.")

    try:
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private or ip.is_loopback or ip.is_reserved:
            raise HTTPException(status_code=400, detail="Internal URLs are not allowed.")
    except ValueError:
        pass

    blocked_hosts = ["localhost", "0.0.0.0", "metadata.google.internal"]
    if parsed.hostname.lower() in blocked_hosts:
        raise HTTPException(status_code=400, detail="This URL is not allowed.")

    return url


# ─────────────────────────────────────────────
# REDIS HELPERS
# ─────────────────────────────────────────────
def get_redis_client():
    try:
        import redis
        REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        client = redis.from_url(REDIS_URL, decode_responses=True)
        client.ping()
        return client
    except Exception as e:
        logger.warning(f"Redis unavailable, running without cache: {e}")
        return None


redis_client = get_redis_client()
CACHE_DURATION = 3600  # 1 hour


def cache_get(key: str):
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
    if redis_client is None:
        return
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception as e:
        logger.warning(f"Redis write error: {e}")


# ─────────────────────────────────────────────
# YT-DLP FALLBACK  (Non-Instagram + fallback)
# ─────────────────────────────────────────────
def extract_info_with_retry(url: str, max_retries: int = 3) -> dict:
    """yt-dlp se info extract karo with proxy retry logic."""
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
        if proxy and "pinterest.com" not in url.lower() and "pinimg.com" not in url.lower():
            ydl_opts["proxy"] = proxy

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if attempt > 0:
                    logger.info(f"yt-dlp succeeded on attempt {attempt + 1} for {url}")
                return {"info": info, "proxy": proxy}
        except Exception as e:
            last_error = e
            logger.warning(f"yt-dlp extract error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(1.0, 3.0))

    error_msg = str(last_error).lower()
    logger.error(f"yt-dlp failed after {max_retries} attempts for {url}. Error: {last_error}")

    if "sign in" in error_msg or "login" in error_msg or "requested format is not available" in error_msg:
        raise HTTPException(
            status_code=400,
            detail="Instagram/Platform requires login. We are experiencing high traffic from this platform. Please try again in a few moments."
        )
    raise HTTPException(status_code=400, detail="Failed to process the video URL. Please check and try again.")


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@router.get("/preview")
@router.get("/download")
def redirect_api_gets(request: Request):
    """
    SEO FIX: Prevent 405 Method Not Allowed errors when Googlebot
    crawls these POST-only API endpoints via GET requests.
    Returns a 301 Permanent Redirect to the home page instead.
    """
    return RedirectResponse(url="/", status_code=301)
@router.post("/preview")
@limiter.limit("10/minute")
def preview(request: Request, url: str = Form(...)):
    url = validate_url(url)

    # Redis cache check
    cached_data = cache_get(url)
    if cached_data:
        return cached_data

    try:
        # ── PRIMARY: Instaloader (Instagram URLs ke liye) ──
        if is_instagram_url(url):
            logger.info(f"Using Instaloader (primary) for: {url}")
            insta_info = extract_info_with_instaloader(url)

            if insta_info:
                # Thumbnail proxy (agar Instagram CDN link hai)
                thumb = insta_info.get("thumbnail")
                if thumb and ("instagram.com" in thumb or "fbcdn" in thumb):
                    thumb = f"/proxy-image?url={quote(thumb)}"

                data = {
                    "title": insta_info["title"],
                    "thumbnail": thumb,
                    "video_url": insta_info["video_url"],
                    "uploader": insta_info.get("uploader"),
                    "view_count": insta_info.get("view_count"),
                    "duration": insta_info.get("duration"),
                }
                cache_set(url, data)
                return data

            # Instaloader fail hua → yt-dlp fallback
            logger.info(f"Instaloader failed, falling back to yt-dlp for: {url}")

        # ── PRIMARY: TikWM API (TikTok URLs ke liye) ──
        if is_tiktok_url(url):
            logger.info(f"Using TikWM (primary) for TikTok: {url}")
            tiktok_info = extract_info_with_tikwm(url)
            
            if tiktok_info:
                cache_set(url, tiktok_info)
                return tiktok_info
            
            logger.info(f"TikWM failed, falling back to yt-dlp for: {url}")

        # ── FALLBACK / NON-INSTAGRAM: yt-dlp ──
        extracted = extract_info_with_retry(url)
        info = extracted["info"]

        thumb = info.get("thumbnail")
        if thumb and ("instagram.com" in thumb or "fbcdn" in thumb):
            thumb = f"/proxy-image?url={quote(thumb)}"

        data = {
            "title": info.get("title"),
            "thumbnail": thumb,
            "video_url": info.get("url"),
            "uploader": info.get("uploader"),
            "view_count": info.get("view_count"),
            "duration": info.get("duration"),
        }
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

    try:
        # ── PRIMARY: Instaloader stream (Instagram URLs ke liye) ──
        if is_instagram_url(url):
            logger.info(f"Trying Instaloader stream for: {url}")
            stream_gen, filename = stream_with_instaloader(url, format)
    
            if stream_gen:
                encoded_filename = quote(filename)
                media_type = "audio/mp4" if format == "audio" else "video/mp4"
                headers = {
                    "Content-Disposition": f'attachment; filename="video.mp4"; filename*=UTF-8\'\'{encoded_filename}',
                    "X-Robots-Tag": "noindex, nofollow",
                }
                return StreamingResponse(stream_gen, media_type=media_type, headers=headers)
    
            logger.info(f"Instaloader stream failed, falling back to yt-dlp for: {url}")
    
        # ── PRIMARY: TikWM stream (TikTok URLs ke liye) ──
        if is_tiktok_url(url):
            logger.info(f"Trying TikWM stream for: {url}")
            stream_gen, filename = stream_with_tikwm(url, format)
            
            if stream_gen:
                encoded_filename = quote(filename)
                media_type = "audio/mpeg" if format == "audio" else "video/mp4"
                headers = {
                    "Content-Disposition": f'attachment; filename="video.mp4"; filename*=UTF-8\'\'{encoded_filename}',
                    "X-Robots-Tag": "noindex, nofollow",
                }
                return StreamingResponse(stream_gen, media_type=media_type, headers=headers)
            
            logger.info(f"TikWM stream failed, falling back to yt-dlp for: {url}")

        # ── Check if YouTube URL ──
        parsed_host = urlparse(url).hostname or ""
        is_yt = any(h in parsed_host.lower() for h in ("youtube.com", "youtu.be"))

        # ── Get title from cache or extract ──
        cached_data = cache_get(url)
        successful_proxy = None
    
        if cached_data and cached_data.get("title"):
            title = cached_data["title"]
        else:
            extracted = extract_info_with_retry(url)
            info = extracted.get("info") if extracted else None
            title = info.get("title", "video") if info else "video"
            successful_proxy = extracted.get("proxy") if extracted else None

        if format == "audio":
            format_code = "bestaudio[ext=m4a]/bestaudio/best"
            ext = "m4a"
        else:
            # HIGH QUALITY: best video + best audio merged via ffmpeg
            # Falls back gracefully if separate streams aren't available
            format_code = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best"
            ext = "mp4"
    
        filename = f"{title}.{ext}"
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).strip()
        if not filename:
            filename = f"video.{ext}"

        # ── TEMP FILE DOWNLOAD (supports merging for high quality) ──
        temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_filename = f"{uuid.uuid4().hex}.{ext}"
        temp_path = os.path.join(temp_dir, temp_filename)

        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--no-part",
            "--output", temp_path,
            "--format", format_code,
            "--merge-output-format", "mp4" if format != "audio" else "m4a",
            "--quiet",
        ]
    
        cookie_file = proxy_manager.get_cookie_file()
        if cookie_file:
            cmd.extend(["--cookies", cookie_file])
    
        if "pinterest.com" in url.lower() or "pinimg.com" in url.lower():
            pass  # Bypass proxy for Pinterest to prevent 0 KB download issues
        elif successful_proxy:
            cmd.extend(["--proxy", successful_proxy])
        else:
            proxy = proxy_manager.get_proxy()
            if proxy:
                cmd.extend(["--proxy", proxy])
    
        cmd.append(url)

        logger.info(f"Starting high-quality download with format: {format_code} for {url}")

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            bufsize=10**7,
        )
        try:
            _, stderr_output = proc.communicate(timeout=300)  # 5 min timeout
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            if os.path.exists(temp_path):
                os.remove(temp_path)
            logger.error(f"yt-dlp download timed out after 300s for {url}")
            raise HTTPException(status_code=504, detail="Download timed out. The video may be too large. Please try again.")

        if proc.returncode != 0 or not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
            # Cleanup failed temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            stderr_text = stderr_output.decode(errors='ignore') if stderr_output else 'Unknown error'
            logger.error(f"yt-dlp download failed (rc={proc.returncode}): {stderr_text[:500]}")
            raise HTTPException(status_code=500, detail="Download failed. Please try again later.")

        file_size = os.path.getsize(temp_path)
        logger.info(f"High-quality download complete: {temp_path} ({file_size} bytes)")

        def iterfile():
            try:
                with open(temp_path, "rb") as f:
                    while True:
                        data = f.read(64 * 1024)
                        if not data:
                            break
                        yield data
            finally:
                # Cleanup temp file after streaming
                try:
                    os.remove(temp_path)
                    logger.info(f"Cleaned up temp file: {temp_path}")
                except Exception as cleanup_err:
                    logger.warning(f"Failed to cleanup temp file {temp_path}: {cleanup_err}")

        encoded_filename = quote(filename)
        media_type = "audio/mp4" if format == "audio" else "video/mp4"
        headers = {
            "Content-Disposition": f'attachment; filename="video.mp4"; filename*=UTF-8\'\'{encoded_filename}',
            "Content-Length": str(file_size),
            "X-Robots-Tag": "noindex, nofollow",
        }
        return StreamingResponse(iterfile(), media_type=media_type, headers=headers)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Streaming failed for {url}: {e}")
        raise HTTPException(status_code=500, detail="Download streaming failed. Please try again later.")