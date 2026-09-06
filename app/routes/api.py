"""Preview and Download API routes with Redis caching and proper error handling."""
import json
import subprocess
import sys
import os
import logging
import ipaddress
import socket
import time
import uuid
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import StreamingResponse, RedirectResponse, HTMLResponse
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
    hostname = urlparse(url).hostname
    return hostname is not None and "instagram.com" in hostname.lower()


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
        L.context.max_connection_attempts = 1

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
    hostname = urlparse(url).hostname
    return hostname is not None and "tiktok.com" in hostname.lower()


def is_youtube_url(url: str) -> bool:
    """YouTube, Shorts, Music, and youtu.be links."""
    hostname = (urlparse(url).hostname or "").lower()
    if hostname.startswith("www."):
        hostname = hostname[4:]
    return (
        hostname in {"youtube.com", "youtu.be", "m.youtube.com", "music.youtube.com", "youtube-nocookie.com"}
        or hostname.endswith(".youtube.com")
    )


# YouTube web client now requires a browser PO token. Android clients still
# return real stream URLs without cookies. Node is used for n-sig when needed.
YOUTUBE_PLAYER_CLIENTS = ["android_sdkless", "android", "ios_music"]
YOUTUBE_EXTRACTOR_ARGS = (
    "youtube:player_client=" + ",".join(YOUTUBE_PLAYER_CLIENTS)
    + ";player_skip=webpage,configs"
)
YT_INFO_CACHE = {}
YT_INFO_CACHE_TTL = 900
URL_RESULT_CACHE = {}
MAX_URL_RESULT_CACHE = 500


def get_cached_yt_info(url: str):
    """Avoid repeated yt-dlp extraction on the same URL for a short window."""
    cached = YT_INFO_CACHE.get(url)
    if not cached:
        return None
    if time.time() - cached["ts"] > YT_INFO_CACHE_TTL:
        YT_INFO_CACHE.pop(url, None)
        return None
    return cached["payload"]


def set_cached_yt_info(url: str, payload: dict):
    YT_INFO_CACHE[url] = {"ts": time.time(), "payload": payload}


def get_cached_url_result(key: str):
    cached = URL_RESULT_CACHE.get(key)
    if not cached:
        return None
    if time.time() - cached["ts"] > 600:
        URL_RESULT_CACHE.pop(key, None)
        return None
    return cached["payload"]


def set_cached_url_result(key: str, payload: dict):
    if len(URL_RESULT_CACHE) >= MAX_URL_RESULT_CACHE:
        oldest_key = next(iter(URL_RESULT_CACHE))
        URL_RESULT_CACHE.pop(oldest_key, None)
    URL_RESULT_CACHE[key] = {"ts": time.time(), "payload": payload}


def apply_youtube_ydl_opts(ydl_opts: dict) -> dict:
    """Use clients that bypass YouTube's 'confirm you're not a bot' web check."""
    ydl_opts["extractor_args"] = {
        "youtube": {
            "player_client": list(YOUTUBE_PLAYER_CLIENTS),
            "player_skip": ["webpage", "configs"],
        }
    }
    ydl_opts["js_runtimes"] = {"node": {}}
    # Chrome UA forces the web client and triggers bot-check / empty formats.
    ydl_opts.pop("http_headers", None)
    return ydl_opts


def youtube_format_selector(fmt: str) -> str:
    if fmt == "audio":
        return "bestaudio[ext=m4a]/bestaudio/best"
    if fmt == "high_quality":
        return "bestvideo[vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best"
    # Fastest default for normal YouTube videos: prefer a single progressive MP4
    # instead of a DASH video+audio merge that takes longer to resolve and buffer.
    return "18/22/136/135/134/best[height<=720][ext=mp4]/best[ext=mp4]/best"


def youtube_can_direct_stream(format_code: str) -> bool:
    """Only return True for formats that are a single progressive stream."""
    if not format_code:
        return False
    lowered = format_code.lower()
    if "bestaudio" in lowered and "+bestaudio" in lowered:
        return False
    if "+bestaudio" in lowered or "bestvideo" in lowered and "bestaudio" in lowered:
        return False
    if "bestaudio" in lowered:
        return False
    return True


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

    hostname = parsed.hostname.lower()

    # Block known dangerous hostnames (cloud metadata, localhost, etc.)
    blocked_hosts = {
        "localhost", "0.0.0.0", "metadata.google.internal",
        "169.254.169.254", "metadata.google", "metadata.azure.com",
        "metadata.internal", "instance-data",
    }
    if hostname in blocked_hosts:
        raise HTTPException(status_code=400, detail="This URL is not allowed.")

    # Resolve hostname to IP(s) and validate each — catches both IP literals
    # AND domains that DNS-resolve to private/reserved addresses (DNS rebinding).
    CGNAT = ipaddress.ip_network("100.64.0.0/10")
    try:
        addrinfos = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror:
        raise HTTPException(status_code=400, detail="Could not resolve the hostname.")

    for _family, _type, _proto, _canon, sockaddr in addrinfos:
        try:
            ip = ipaddress.ip_address(sockaddr[0])
        except ValueError:
            continue
        if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local or ip.is_unspecified:
            raise HTTPException(status_code=400, detail="URL resolves to an internal or reserved address.")
        if ip in CGNAT:
            raise HTTPException(status_code=400, detail="URL resolves to a blocked address range.")

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
    cached = get_cached_yt_info(url)
    if cached:
        logger.info(f"Using cached yt-dlp metadata for {url}")
        return cached

    last_error = None
    for attempt in range(max_retries):
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "socket_timeout": 30,
            "retries": 3,
            "extractor_retries": 3,
            "nocheckcertificate": True,
            "noplaylist": True,
            "js_runtimes": {"node": {}},
        }
        if not is_youtube_url(url):
            ydl_opts["http_headers"] = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            }
        else:
            apply_youtube_ydl_opts(ydl_opts)

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
                if proxy:
                    proxy_manager.clear_proxy_failure(proxy)
                payload = {"info": info, "proxy": proxy}
                set_cached_yt_info(url, payload)
                return payload
        except Exception as e:
            last_error = e
            if proxy:
                proxy_manager.mark_proxy_failed(proxy)
            logger.warning(f"yt-dlp extract error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(1.0, 3.0))

    error_msg = str(last_error).lower()
    logger.error(f"yt-dlp failed after {max_retries} attempts for {url}. Error: {last_error}")

    if "sign in" in error_msg or "login" in error_msg or "requested format is not available" in error_msg:
        if is_youtube_url(url):
            raise HTTPException(
                status_code=400,
                detail="YouTube is blocking this request right now. Please wait a few seconds and try again."
            )
        raise HTTPException(
            status_code=400,
            detail="This platform requires login. We are experiencing high traffic. Please try again in a few moments."
        )
    if "no supported javascript runtime" in error_msg or "js runtime" in error_msg:
        raise HTTPException(
            status_code=500,
            detail="Server configuration issue. Please try again later."
        )
    if "video unavailable" in error_msg or "private video" in error_msg:
        raise HTTPException(
            status_code=400,
            detail="This video is private or unavailable. Please check the URL."
        )
    if "members" in error_msg or "member" in error_msg or "join this channel" in error_msg:
        raise HTTPException(
            status_code=400,
            detail="This video is for channel members only. Only public videos can be downloaded."
        )
    if "age" in error_msg and ("restricted" in error_msg or "verify" in error_msg or "gate" in error_msg):
        raise HTTPException(
            status_code=400,
            detail="This video is age-restricted. Please try a different video."
        )
    if "geo" in error_msg or "not available in your country" in error_msg:
        raise HTTPException(
            status_code=400,
            detail="This video is not available in our server region. Please try another video."
        )
    raise HTTPException(status_code=400, detail="Failed to process the video URL. Please check and try again.")


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@router.get("/preview")
def redirect_api_gets(request: Request):
    """
    SEO FIX: Prevent 405 Method Not Allowed errors when Googlebot
    crawls these POST-only API endpoints via GET requests.
    Returns a 301 Permanent Redirect to the home page instead.
    """
    return RedirectResponse(url="/", status_code=301)

@router.get("/download")
@limiter.limit("5/minute")
def download_get(request: Request, url: str, format: str = "video"):
    return download(request, url=url, format=format)
@router.post("/preview")
@limiter.limit("10/minute")
def preview(request: Request, url: str = Form(...)):
    url = validate_url(url)

    # Redis cache check
    cached_data = cache_get(url)
    if cached_data:
        return cached_data

    key_result = get_cached_url_result(f"preview:{url}")
    if key_result:
        return key_result

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
                set_cached_url_result(f"preview:{url}", data)
                return data

            # Instaloader fail hua → yt-dlp fallback
            logger.info(f"Instaloader failed, falling back to yt-dlp for: {url}")

        # ── PRIMARY: TikWM API (TikTok URLs ke liye) ──
        if is_tiktok_url(url):
            logger.info(f"Using TikWM (primary) for TikTok: {url}")
            tiktok_info = extract_info_with_tikwm(url)
            
            if tiktok_info:
                cache_set(url, tiktok_info)
                set_cached_url_result(f"preview:{url}", tiktok_info)
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
        set_cached_url_result(f"preview:{url}", data)
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

        is_yt = is_youtube_url(url)

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
            format_code = youtube_format_selector("audio") if is_yt else "bestaudio[ext=m4a]/bestaudio/best"
            ext = "m4a"
        elif format == "high_quality":
            format_code = youtube_format_selector("high_quality") if is_yt else "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best"
            ext = "mp4"
        else:
            format_code = youtube_format_selector("video") if is_yt else "best[ext=mp4]/best"
            ext = "mp4"
    
        filename = f"{title}.{ext}"
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).strip()
        if not filename:
            filename = f"video.{ext}"

        cmd = [sys.executable, "-m", "yt_dlp", "--no-part", "--format", format_code, "--quiet", "--no-playlist", "--js-runtimes", "node"]
        if is_yt:
            cmd.extend(["--extractor-args", YOUTUBE_EXTRACTOR_ARGS])

        # Prefer direct streaming for standard progressive YouTube formats so the
        # browser starts receiving data immediately instead of waiting for the full
        # file to land in /temp. Merge formats must still use temp files.
        use_temp_file = format == "high_quality" or (is_yt and not youtube_can_direct_stream(format_code))

        if use_temp_file:
            temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "temp")
            os.makedirs(temp_dir, exist_ok=True)
            temp_id = uuid.uuid4().hex
            temp_path = os.path.join(temp_dir, f"{temp_id}.{ext}")
            cmd.extend(["--output", os.path.join(temp_dir, f"{temp_id}.%(ext)s")])
            if ext == "mp4":
                cmd.extend(["--merge-output-format", "mp4"])
        else:
            cmd.extend(["-o", "-"])  # Stream directly to stdout

        cookie_file = proxy_manager.get_cookie_file()
        if cookie_file:
            cmd.extend(["--cookies", cookie_file])

        proxy_value = None
        if "pinterest.com" in url.lower() or "pinimg.com" in url.lower():
            pass  # Bypass proxy for Pinterest to prevent 0 KB download issues
        elif successful_proxy:
            proxy_value = successful_proxy
        else:
            proxy_value = proxy_manager.get_proxy()
        if proxy_value:
            cmd.extend(["--proxy", proxy_value])

        cmd.append(url)

        if use_temp_file:
            logger.info(f"Starting high-quality download (temp file) with format: {format_code} for {url}")
            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, bufsize=10**7)
            try:
                _, stderr_output = proc.communicate(timeout=900)  # 15 min timeout
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
                for leftover in os.listdir(temp_dir):
                    if leftover.startswith(temp_id):
                        try:
                            os.remove(os.path.join(temp_dir, leftover))
                        except OSError:
                            pass
                logger.error(f"yt-dlp download timed out after 900s for {url}")
                raise HTTPException(status_code=504, detail="Download timed out. The video may be too large. Please try again.")

            produced = None
            for leftover in os.listdir(temp_dir):
                if leftover.startswith(temp_id) and os.path.isfile(os.path.join(temp_dir, leftover)):
                    candidate = os.path.join(temp_dir, leftover)
                    if os.path.getsize(candidate) > 0:
                        produced = candidate
                        break
            if produced:
                temp_path = produced

            if proc.returncode != 0 or not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
                for leftover in os.listdir(temp_dir):
                    if leftover.startswith(temp_id):
                        try:
                            os.remove(os.path.join(temp_dir, leftover))
                        except OSError:
                            pass
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
                    try:
                        os.remove(temp_path)
                    except Exception as cleanup_err:
                        logger.warning(f"Failed to cleanup temp file {temp_path}: {cleanup_err}")

            headers = {
                "Content-Disposition": f'attachment; filename="video.mp4"; filename*=UTF-8\'\'{quote(filename)}',
                "Content-Length": str(file_size),
                "X-Robots-Tag": "noindex, nofollow",
            }
        else:
            logger.info(f"Starting direct stream download with format: {format_code} for {url}")
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10**7)

            try:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(proc.stdout.read, 1024)
                    first_chunk = future.result(timeout=20)
            except Exception:
                first_chunk = b""
                try:
                    proc.kill()
                    proc.wait(timeout=10)
                except Exception:
                    pass

            if not first_chunk:
                stderr = proc.stderr.read().decode('utf-8', errors='ignore') if proc.stderr else ''
                logger.warning(f"Direct stream failed to start for {url}. Falling back to temp-file mode. Stderr: {stderr[:500]}")
                if proc.poll() is None:
                    proc.kill()
                    proc.wait(timeout=10)

                use_temp_file = True
                temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "temp")
                os.makedirs(temp_dir, exist_ok=True)
                temp_id = uuid.uuid4().hex
                temp_path = os.path.join(temp_dir, f"{temp_id}.{ext}")
                fallback_cmd = [
                    sys.executable, "-m", "yt_dlp", "--no-part", "--format", format_code,
                    "--quiet", "--no-playlist", "--js-runtimes", "node",
                    "--output", os.path.join(temp_dir, f"{temp_id}.%(ext)s"),
                    "--merge-output-format", "mp4" if ext == "mp4" else None,
                ]
                if is_yt:
                    fallback_cmd.extend(["--extractor-args", YOUTUBE_EXTRACTOR_ARGS])
                if cookie_file:
                    fallback_cmd.extend(["--cookies", cookie_file])
                if "pinterest.com" in url.lower() or "pinimg.com" in url.lower():
                    pass
                elif successful_proxy:
                    fallback_cmd.extend(["--proxy", successful_proxy])
                else:
                    proxy = proxy_manager.get_proxy()
                    if proxy:
                        fallback_cmd.extend(["--proxy", proxy])
                fallback_cmd.append(url)
                fallback_cmd = [part for part in fallback_cmd if part is not None]
                proc = subprocess.Popen(fallback_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, bufsize=10**7)
                try:
                    _, stderr_output = proc.communicate(timeout=900)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                    for leftover in os.listdir(temp_dir):
                        if leftover.startswith(temp_id):
                            try:
                                os.remove(os.path.join(temp_dir, leftover))
                            except OSError:
                                pass
                    logger.error(f"yt-dlp fallback download timed out after 900s for {url}")
                    raise HTTPException(status_code=504, detail="Download timed out. Please try again.")

                produced = None
                for leftover in os.listdir(temp_dir):
                    if leftover.startswith(temp_id) and os.path.isfile(os.path.join(temp_dir, leftover)):
                        candidate = os.path.join(temp_dir, leftover)
                        if os.path.getsize(candidate) > 0:
                            produced = candidate
                            break
                if produced:
                    temp_path = produced
                if proc.returncode != 0 or not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
                    for leftover in os.listdir(temp_dir):
                        if leftover.startswith(temp_id):
                            try:
                                os.remove(os.path.join(temp_dir, leftover))
                            except OSError:
                                pass
                    stderr_text = stderr_output.decode(errors='ignore') if stderr_output else 'Unknown error'
                    logger.error(f"yt-dlp fallback failed (rc={proc.returncode}): {stderr_text[:500]}")
                    raise HTTPException(status_code=500, detail="Download failed. Please try again later.")

                file_size = os.path.getsize(temp_path)

                def iterfile():
                    try:
                        with open(temp_path, "rb") as f:
                            while True:
                                data = f.read(64 * 1024)
                                if not data:
                                    break
                                yield data
                    finally:
                        try:
                            os.remove(temp_path)
                        except Exception as cleanup_err:
                            logger.warning(f"Failed to cleanup temp file {temp_path}: {cleanup_err}")

                headers = {
                    "Content-Disposition": f'attachment; filename="video.mp4"; filename*=UTF-8\'\'{quote(filename)}',
                    "Content-Length": str(file_size),
                    "X-Robots-Tag": "noindex, nofollow",
                }
                media_type = "audio/mp4" if format == "audio" else "video/mp4"
                response = StreamingResponse(iterfile(), media_type=media_type, headers=headers)
                response.set_cookie(key="download_ready", value="1", max_age=60, path="/")
                return response

            def iterfile():
                yield first_chunk
                try:
                    while True:
                        data = proc.stdout.read(64 * 1024)
                        if not data:
                            break
                        yield data
                except Exception as e:
                    logger.error(f"Stream interrupted: {e}")
                finally:
                    proc.stdout.close()
                    proc.kill()
                    proc.wait()

            headers = {
                "Content-Disposition": f'attachment; filename="video.mp4"; filename*=UTF-8\'\'{quote(filename)}',
                "X-Robots-Tag": "noindex, nofollow",
            }

        media_type = "audio/mp4" if format == "audio" else "video/mp4"
        response = StreamingResponse(iterfile(), media_type=media_type, headers=headers)
        response.set_cookie(key="download_ready", value="1", max_age=60, path="/")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Streaming failed for {url}: {e}")
        raise HTTPException(status_code=500, detail="Download streaming failed. Please try again later.")