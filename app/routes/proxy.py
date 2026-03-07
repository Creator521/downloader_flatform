"""Proxy image route with SSRF protection and size limits."""
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from urllib.parse import urlparse
import requests

logger = logging.getLogger(__name__)

router = APIRouter()

# Maximum allowed image size (10 MB)
MAX_IMAGE_SIZE = 10 * 1024 * 1024


@router.get("/proxy-image")
def proxy_image(url: str):
    if not url:
        raise HTTPException(status_code=404, detail="URL required")

    # Security: SSRF Protection
    parsed_url = urlparse(url)
    allowed_domains = [
        "instagram.com", "cdninstagram.com", "fbcdn.net",
        "twimg.com", "ytimg.com", "tiktok.com", "tiktokcdn.com"
    ]

    is_allowed = False
    for domain in allowed_domains:
        if parsed_url.hostname and (
            parsed_url.hostname == domain or
            parsed_url.hostname.endswith("." + domain)
        ):
            is_allowed = True
            break

    if not is_allowed:
        logger.warning(f"Blocked proxy request for disallowed domain: {parsed_url.hostname}")
        raise HTTPException(status_code=403, detail="Domain not allowed for proxying")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.instagram.com/"
        }
        resp = requests.get(url, headers=headers, stream=True, timeout=10)

        # Check Content-Length before streaming (Point 8: size limit)
        content_length = resp.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_IMAGE_SIZE:
            resp.close()
            raise HTTPException(status_code=413, detail="Image too large")

        # Stream with size tracking to prevent bypass (when Content-Length is missing)
        def size_limited_stream():
            total = 0
            for chunk in resp.iter_content(chunk_size=64 * 1024):
                total += len(chunk)
                if total > MAX_IMAGE_SIZE:
                    resp.close()
                    logger.warning(f"Proxy image exceeded size limit during streaming: {url}")
                    return
                yield chunk

        return StreamingResponse(
            size_limited_stream(),
            media_type=resp.headers.get("Content-Type", "image/jpeg")
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Proxy image failed for URL {url}: {e}")
        raise HTTPException(status_code=404, detail="Image not found")
