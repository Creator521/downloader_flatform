"""SEO landing page routes."""
import logging
from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.multilingual_data import MULTILINGUAL_PAGES
from app.blog_data import BLOG_POSTS
from app.seo_data import SEO_KEYWORDS, PAGE_KEYWORD_MAP

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


# Both old-path redirects and EN redirects merged cleanly
ALL_REDIRECTS = {
    # ── OLD PATHS → NEW CANONICAL PATHS ────────────────────────────────────
    "/instagram-video-downloader":   "/video",
    "/instagram-reel-downloader":    "/reels",
    "/tiktok-video-downloader":      "/tiktok",
    "/youtube-video-downloader":     "/youtube",
    "/x-video-downloader":           "/twitter",
    "/snapchat-video-downloader":    "/snapchat",
    "/instagram-photo-downloader":   "/photo",
    "/facebook-video-downloader":    "/facebook",
    "/instagram-story-downloader":   "/story",
    "/story-saver":                  "/story",
    "/story-saver/":                 "/story",
    "/igtv":                         "/video",
    "/igtv/":                        "/video",
    "/pinterest-video-downloader":   "/pinterest",
    "/youtubeshort":                 "/youtube-shorts-downloader",
    "/youtubeshort/":                "/youtube-shorts-downloader",
    "/youtube-shorts":               "/youtube-shorts-downloader",

    # ── Language-prefixed /igtv paths ───────────────────────────────────────
    "/hi/igtv":                      "/hi/video",
    "/es/igtv":                      "/es/video",
    "/fr/igtv":                      "/fr/video",
    "/de/igtv":                      "/de/video",
    "/pt/igtv":                      "/pt/video",
    "/ar/igtv":                      "/ar/video",
    "/id/igtv":                      "/id/video",
    "/bn/igtv":                      "/bn/video",
    "/tr/igtv":                      "/tr/video",
    "/th/igtv":                      "/th/video",
    "/ko/igtv":                      "/ko/video",
    "/ja/igtv":                      "/ja/video",
    "/uk/igtv":                      "/uk/video",
    "/pl/igtv":                      "/pl/video",
    "/en/igtv":                      "/video",

    # ── Cloudflare email protection path (prevents 404 in GSC) ──────────────
    "/cdn-cgi/l/email-protection":   "/",

    # ── Language-prefixed old youtubeshort paths ─────────────────────────────
    "/hi/youtubeshort":              "/hi/youtube-shorts-downloader",
    "/es/youtubeshort":              "/es/youtube-shorts-downloader",
    "/fr/youtubeshort":              "/fr/youtube-shorts-downloader",
    "/de/youtubeshort":              "/de/youtube-shorts-downloader",
    "/pt/youtubeshort":              "/pt/youtube-shorts-downloader",
    "/ar/youtubeshort":              "/ar/youtube-shorts-downloader",
    "/id/youtubeshort":              "/id/youtube-shorts-downloader",
    "/bn/youtubeshort":              "/bn/youtube-shorts-downloader",
    "/tr/youtubeshort":              "/tr/youtube-shorts-downloader",
    "/th/youtubeshort":              "/th/youtube-shorts-downloader",
    "/ko/youtubeshort":              "/ko/youtube-shorts-downloader",
    "/ja/youtubeshort":              "/ja/youtube-shorts-downloader",
    "/uk/youtubeshort":              "/uk/youtube-shorts-downloader",
    "/pl/youtubeshort":              "/pl/youtube-shorts-downloader",

    # ── REDIRECTS FROM OLD /en/ PREFIXED PATHS ──────────────────────────────
    "/en/":                          "/",
    "/en":                           "/",   # middleware strips trailing slash → /en has no route without this
    "/en/reels":                     "/reels",
    "/en/video":                     "/video",
    "/en/photo":                     "/photo",
    "/en/story":                     "/story",
    "/en/youtube":                   "/youtube",
    "/en/tiktok":                    "/tiktok",
    "/en/facebook":                  "/facebook",
    "/en/twitter":                   "/twitter",
    "/en/pinterest":                 "/pinterest",
    "/en/snapchat":                  "/snapchat",
    "/en/youtube-shorts-downloader": "/youtube-shorts-downloader",
    "/en/tiktok-mp3-downloader":     "/tiktok-mp3-downloader",
    "/en/youtube-to-mp3":            "/youtube-to-mp3",
    "/en/youtubeshort":              "/youtube-shorts-downloader",

    # ── LANGUAGE ROOT PATHS WITHOUT TRAILING SLASH → canonical with slash ───
    "/hi":  "/hi/",
    "/es":  "/es/",
    "/fr":  "/fr/",
    "/de":  "/de/",
    "/pt":  "/pt/",
    "/ar":  "/ar/",
    "/id":  "/id/",
    "/bn":  "/bn/",
    "/tr":  "/tr/",
    "/th":  "/th/",
    "/ko":  "/ko/",
    "/ja":  "/ja/",
    "/uk":  "/uk/",
    "/pl":  "/pl/",

    # ── TOP-LEVEL CLEAN PATHS (Self-referencing or already served via dynamic routes) ──
    # Note: These are no longer redirects; they will be served by create_route()
    # But we keep them here if we want to ensure any legacy links redirect correctly.
    "/reels/":                       "/reels",
    "/video/":                       "/video",
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

        # ── Inject page-specific keywords where Google reads them ──────────
        groups = PAGE_KEYWORD_MAP.get(path, ["core"])
        page_keywords: list[str] = []
        for g in groups:
            page_keywords.extend(SEO_KEYWORDS.get(g, []))
        # Deduplicate while preserving order
        seen: set[str] = set()
        unique_keywords: list[str] = []
        for kw in page_keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)
        page_data["keywords"] = unique_keywords          # list  → for loops
        page_data["keywords_str"] = ", ".join(unique_keywords)  # string → meta tag

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

@router.get("/apple-touch-icon.png", include_in_schema=False)
@router.get("/apple-touch-icon-precomposed.png", include_in_schema=False)
async def apple_touch_icon():
    """✅ FIX 5: Prevent automatic 404s from iOS devices searching for default icons."""
    file_path = Path(__file__).parent.parent.parent / "frontend" / "favicon.png"
    return FileResponse(file_path)


@router.get("/bingsiteauth.xml", include_in_schema=False)
async def bing_site_auth():
    """Verify Bing Webmaster Tools."""
    file_path = Path(__file__).parent.parent.parent / "BingSiteAuth.xml"
    if file_path.exists():
        return FileResponse(file_path, media_type="application/xml")
    
    # Fallback to direct content if file doesn't exist
    content = '<?xml version="1.0"?>\n<users>\n\t<user>FF6947C28B7E462D892C2816116DDC46</user>\n</users>'
    from fastapi.responses import Response
    return Response(content=content, media_type="application/xml")


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
        "Disallow: /proxy-image\n"
        "Disallow: /api/\n"
        "Disallow: /proxy/\n"
        "Disallow: /temp/\n"
        "Disallow: /download\n"
        "Disallow: /preview\n"
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
