"""SEO landing page routes."""
import json
import logging
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.multilingual_data import MULTILINGUAL_PAGES
from app.blog_data import BLOG_POSTS
from fastapi.responses import HTMLResponse, RedirectResponse

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

# 301 Redirects from old english paths to new short paths
OLD_REDIRECTS = {
    "/instagram-video-downloader": "/video",
    "/instagram-reel-downloader": "/reels",
    "/tiktok-video-downloader": "/tiktok",
    "/youtube-video-downloader": "/youtube",
    "/x-video-downloader": "/twitter",
    "/snapchat-video-downloader": "/snapchat",
    "/instagram-photo-downloader": "/photo",
    "/facebook-video-downloader": "/facebook",
    "/instagram-story-downloader": "/story",
    "/story-saver": "/story",
    "/story-saver/": "/story",
    "/igtv": "/video",
    "/igtv/": "/video",
    "/pinterest-video-downloader": "/pinterest"
}

# 301 Redirects from old English URLs (without lang prefix) to new /en/ URLs
EN_REDIRECTS = {
    "/": "/en/",
    "/reels": "/en/reels",
    "/video": "/en/video", 
    "/photo": "/en/photo",
    "/story": "/en/story",
    "/youtube": "/en/youtube",
    "/tiktok": "/en/tiktok",
    "/facebook": "/en/facebook",
    "/twitter": "/en/twitter",
    "/pinterest": "/en/pinterest",
    "/snapchat": "/en/snapchat",
    "/youtubeshort": "/en/youtubeshort",
    "/tiktok-mp3-downloader": "/en/tiktok-mp3-downloader",
    "/youtube-to-mp3": "/en/youtube-to-mp3"
}

for old_path, new_path in EN_REDIRECTS.items():
    @router.get(old_path, include_in_schema=False)
    async def redirect_en(request: Request, _old=old_path, _new=new_path):
        return RedirectResponse(url=_new, status_code=301)

for old_path, new_path in OLD_REDIRECTS.items():
    @router.get(old_path, include_in_schema=False)
    async def redirect_old_route(request: Request, _old=old_path, _new=new_path):
        return RedirectResponse(url=_new, status_code=301)


def create_route(path: str, data: dict):
    """Dynamically register GET routes for all SEO pages."""
    @router.get(path, response_class=HTMLResponse)
    async def page_route(request: Request):
        # Inject schema into page data (Schema now mostly handled via Jinja2 in templates)
        page_data = data.copy()
        
        # Get latest 6 blog posts for the footer area
        latest_posts = dict(list(BLOG_POSTS.items())[:6])

        return templates.TemplateResponse("landing_page.html", {
            "request": request,
            "page": page_data,
            "latest_posts": latest_posts
        })


# Register all explicitly generated multilingual SEO routes
for path, data in MULTILINGUAL_PAGES.items():
    create_route(path, data)


@router.get("/ads.txt")
async def ads_txt():
    """Serve ads.txt for ad network verification."""
    content = "google.com, pub-3721817985222293, DIRECT, f08c47fec0942fa0"
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(content=content, media_type="text/plain")


@router.get("/llms.txt")
async def llms_txt():
    """Serve llms.txt for AI search engine discovery."""
    from fastapi.responses import FileResponse
    file_path = Path(__file__).parent.parent.parent / "frontend" / "llms.txt"
    return FileResponse(file_path)


@router.get("/favicon.ico", include_in_schema=False)
async def favicon_ico():
    """Serve favicon.ico by redirecting to the PNG version or serving it directly."""
    from fastapi.responses import FileResponse
    file_path = Path(__file__).parent.parent.parent / "frontend" / "favicon.png"
    return FileResponse(file_path)


@router.get("/robots.txt")
async def robots_txt():
    """Serve a production-ready robots.txt for search engine crawlers."""
    domain = "https://snapreeldownload.com"
    content = (
        "# robots.txt for snapreeldownload.com\n"
        "# Optimized for Google Indexing & Crawl Budget\n"
        "\n"
        "User-agent: *\n"
        "Allow: /\n"
        "Allow: /blog\n"
        "Allow: /sitemap.xml\n"
        "Allow: /ads.txt\n"
        "Allow: /robots.txt\n"
        "\n"
        "# Block: Internal API & non-indexable paths\n"
        "Disallow: /preview\n"
        "Disallow: /proxy-image\n"
        "Disallow: /api/\n"
        "Disallow: /proxy/\n"
        "Disallow: /temp/\n"
        "Disallow: /*?*  # Block parameters to prevent duplicate indexing\n"
        "\n"
        "# Block: Admin and development files\n"
        "Disallow: /admin\n"
        "Disallow: /_debug\n"
        "Disallow: /*.log$\n"
        "Disallow: /*.tmp$\n"
        "\n"
        "Crawl-delay: 1\n"
        "\n"
        f"Sitemap: {domain}/sitemap.xml\n"
    )
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(content=content, media_type="text/plain")