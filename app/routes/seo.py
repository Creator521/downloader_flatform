"""SEO landing page routes."""
import logging
import os
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
INDEXNOW_KEY = os.getenv("INDEXNOW_KEY", "0b102804d0d44e2993313a2fb9b662cc")


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
    "/hi/igtv":                      "/video",
    "/es/igtv":                      "/video",
    "/fr/igtv":                      "/video",
    "/de/igtv":                      "/video",
    "/pt/igtv":                      "/video",
    "/ar/igtv":                      "/video",
    "/id/igtv":                      "/video",
    "/bn/igtv":                      "/video",
    "/tr/igtv":                      "/video",
    "/th/igtv":                      "/video",
    "/ko/igtv":                      "/video",
    "/ja/igtv":                      "/video",
    "/uk/igtv":                      "/video",
    "/pl/igtv":                      "/video",
    "/en/igtv":                      "/video",

    # ── Cloudflare email protection path (prevents 404 in GSC) ──────────────
    "/cdn-cgi/l/email-protection":   "/",

    # ── Language-prefixed old youtubeshort paths ─────────────────────────────
    "/hi/youtubeshort":              "/youtube-shorts-downloader",
    "/es/youtubeshort":              "/youtube-shorts-downloader",
    "/fr/youtubeshort":              "/youtube-shorts-downloader",
    "/de/youtubeshort":              "/youtube-shorts-downloader",
    "/pt/youtubeshort":              "/youtube-shorts-downloader",
    "/ar/youtubeshort":              "/youtube-shorts-downloader",
    "/id/youtubeshort":              "/youtube-shorts-downloader",
    "/bn/youtubeshort":              "/youtube-shorts-downloader",
    "/tr/youtubeshort":              "/youtube-shorts-downloader",
    "/th/youtubeshort":              "/youtube-shorts-downloader",
    "/ko/youtubeshort":              "/youtube-shorts-downloader",
    "/ja/youtubeshort":              "/youtube-shorts-downloader",
    "/uk/youtubeshort":              "/youtube-shorts-downloader",
    "/pl/youtubeshort":              "/youtube-shorts-downloader",

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

    # ── TOP-LEVEL CLEAN PATHS (Self-referencing or already served via dynamic routes) ──
    # Note: These are no longer redirects; they will be served by create_route()
    # But we keep them here if we want to ensure any legacy links redirect correctly.
    "/reels/":                       "/reels",
    "/video/":                       "/video",

    # ── LANGUAGE ROOT PATHS WITHOUT TRAILING SLASH → canonical with slash ───
    "/hi":  "/",
    "/es":  "/",
    "/fr":  "/",
    "/de":  "/",
    "/pt":  "/",
    "/ar":  "/",
    "/id":  "/",
    "/bn":  "/",
    "/tr":  "/",
    "/th":  "/",
    "/ko":  "/",
    "/ja":  "/",
    "/uk":  "/",
    "/pl":  "/",
    
    # ── LANGUAGE ROOT PATHS WITH TRAILING SLASH → redirect to english root ───
    "/hi/": "/",
    "/es/": "/",
    "/fr/": "/",
    "/de/": "/",
    "/pt/": "/",
    "/ar/": "/",
    "/id/": "/",
    "/bn/": "/",
    "/tr/": "/",
    "/th/": "/",
    "/ko/": "/",
    "/ja/": "/",
    "/uk/": "/",
    "/pl/": "/",

    # ── DUPLICATE BLOG POST REDIRECT ─────────────────────────────────────────
    "/blog/instagram-video-not-downloading-old": "/blog/instagram-video-not-downloading-fixes",

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
        keyword_path = path
        lang = page_data.get("lang")
        if lang and lang != "en":
            prefix = f"/{lang}"
            if keyword_path == f"{prefix}/":
                keyword_path = "/"
            elif keyword_path.startswith(f"{prefix}/"):
                keyword_path = keyword_path[len(prefix):]

        groups = PAGE_KEYWORD_MAP.get(keyword_path, ["core"])
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


@router.get(f"/{INDEXNOW_KEY}.txt", include_in_schema=False)
async def indexnow_key_file():
    """Expose the IndexNow key file required by Bing and IndexNow partners."""
    return PlainTextResponse(content=INDEXNOW_KEY, media_type="text/plain")


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
    """Robots.txt — optimized for search engines and AI crawlers."""
    domain = "https://snapreeldownload.com"
    content = (
        "# robots.txt for snapreeldownload.com\n"
        "# Optimized for search engines and AI search discovery\n"
        "\n"
        "# Allow ChatGPT Search crawler to discover and cite public pages\n"
        "User-agent: OAI-SearchBot\n"
        "Allow: /\n"
        "\n"
        "# Allow user-triggered ChatGPT browsing actions\n"
        "User-agent: ChatGPT-User\n"
        "Allow: /\n"
        "\n"
        "# Allow OpenAI training crawler; disallow here if you want search only\n"
        "User-agent: GPTBot\n"
        "Allow: /\n"
        "\n"
        "User-agent: *\n"
        "\n"
        "# Block internal API and non-indexable paths\n"
        "Disallow: /proxy-image\n"
        "Disallow: /api/\n"
        "Disallow: /proxy/\n"
        "Disallow: /temp/\n"
        "Disallow: /cdn-cgi/\n"
        "Disallow: /api/*?\n"
        "Disallow: /proxy/*?\n"
        "\n"
        "# Block admin and development files\n"
        "Disallow: /admin\n"
        "Disallow: /_debug\n"
        "Disallow: /*.log$\n"
        "Disallow: /*.tmp$\n"
        "\n"
        f"Sitemap: {domain}/sitemap.xml\n"
    )
    return PlainTextResponse(content=content, media_type="text/plain")
