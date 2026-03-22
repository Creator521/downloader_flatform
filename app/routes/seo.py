"""SEO landing page routes."""
import logging
from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.multilingual_data import MULTILINGUAL_PAGES
from app.blog_data import BLOG_POSTS

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


# ── ✅ FIX 1: All redirects in one unified dict — no closure bug ──────────────
# Both old-path redirects and EN redirects merged cleanly
ALL_REDIRECTS = {
    # Old named URLs → short canonical URLs
    "/instagram-video-downloader":   "/en/video",
    "/instagram-reel-downloader":    "/en/reels",
    "/tiktok-video-downloader":      "/en/tiktok",
    "/youtube-video-downloader":     "/en/youtube",
    "/x-video-downloader":           "/en/twitter",
    "/snapchat-video-downloader":    "/en/snapchat",
    "/instagram-photo-downloader":   "/en/photo",
    "/facebook-video-downloader":    "/en/facebook",
    "/instagram-story-downloader":   "/en/story",
    "/story-saver":                  "/en/story",
    "/story-saver/":                 "/en/story",
    "/igtv":                         "/en/video",
    "/igtv/":                        "/en/video",
    "/pinterest-video-downloader":   "/en/pinterest",

    # ✅ FIX 2: /youtubeshort → correct URL /en/youtube-shorts-downloader
    "/youtubeshort":                 "/en/youtube-shorts-downloader",
    "/youtubeshort/":                "/en/youtube-shorts-downloader",
    "/youtube-shorts":               "/en/youtube-shorts-downloader",

    # Root English paths → /en/ prefixed canonical URLs
    "/":                             "/en/",
    "/reels":                        "/en/reels",
    "/video":                        "/en/video",
    "/photo":                        "/en/photo",
    "/story":                        "/en/story",
    "/youtube":                      "/en/youtube",
    "/tiktok":                       "/en/tiktok",
    "/facebook":                     "/en/facebook",
    "/twitter":                      "/en/twitter",
    "/pinterest":                    "/en/pinterest",
    "/snapchat":                     "/en/snapchat",
    "/youtube-shorts-downloader":    "/en/youtube-shorts-downloader",
    "/tiktok-mp3-downloader":        "/en/tiktok-mp3-downloader",
    "/youtube-to-mp3":               "/en/youtube-to-mp3",
}


# ── Register all 301 redirects ────────────────────────────────────────────────
def _make_redirect(target: str):
    """✅ FIX: Factory function prevents closure bug in loops."""
    async def redirect_handler(request: Request):
        return RedirectResponse(url=target, status_code=301)
    return redirect_handler

for old_path, new_path in ALL_REDIRECTS.items():
    router.add_api_route(
        old_path,
        _make_redirect(new_path),
        methods=["GET"],
        include_in_schema=False,
    )


# ── Dynamic SEO page route registration ──────────────────────────────────────
def create_route(path: str, data: dict):
    """Dynamically register GET routes for all SEO pages."""

    async def page_route(request: Request):
        page_data = data.copy()
        latest_posts = dict(list(BLOG_POSTS.items())[:6])
        return templates.TemplateResponse("landing_page.html", {
            "request": request,
            "page": page_data,
            "latest_posts": latest_posts,
        })

    router.add_api_route(
        path,
        page_route,
        methods=["GET"],
        response_class=HTMLResponse,
        include_in_schema=False,
    )


# Register all multilingual SEO pages
for path, data in MULTILINGUAL_PAGES.items():
    create_route(path, data)


# ── Static / utility routes ───────────────────────────────────────────────────

@router.get("/ads.txt")
async def ads_txt():
    content = "google.com, pub-3721817985222293, DIRECT, f08c47fec0942fa0"
    return PlainTextResponse(content=content, media_type="text/plain")


@router.get("/llms.txt")
async def llms_txt():
    file_path = Path(__file__).parent.parent.parent / "frontend" / "llms.txt"
    return FileResponse(file_path)


@router.get("/favicon.ico", include_in_schema=False)
async def favicon_ico():
    file_path = Path(__file__).parent.parent.parent / "frontend" / "favicon.png"
    return FileResponse(file_path)


@router.get("/robots.txt")
async def robots_txt():
    """✅ FIX 4: Corrected robots.txt syntax — /*? not /*?*"""
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
        "# Block internal API and non-indexable paths\n"
        "Disallow: /preview\n"
        "Disallow: /proxy-image\n"
        "Disallow: /api/\n"
        "Disallow: /proxy/\n"
        "Disallow: /temp/\n"
        "Disallow: /*?\n"
        "\n"
        "# Block admin and development files\n"
        "Disallow: /admin\n"
        "Disallow: /_debug\n"
        "Disallow: /*.log$\n"
        "Disallow: /*.tmp$\n"
        "\n"
        "Crawl-delay: 1\n"
        "\n"
        f"Sitemap: {domain}/sitemap.xml\n"
    )
    return PlainTextResponse(content=content, media_type="text/plain")
