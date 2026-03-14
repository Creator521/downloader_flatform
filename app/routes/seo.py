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
    "/tiktok-mp3-downloader": "/tiktok", 
    "/youtube-shorts-downloader": "/youtube",
    "/x-video-downloader": "/twitter",
    "/snapchat-video-downloader": "/snapchat",
    "/instagram-photo-downloader": "/photo",
    "/facebook-video-downloader": "/facebook",
    "/instagram-story-downloader": "/story",
    "/story-saver": "/story",
    "/igtv": "/video",
    "/pinterest-video-downloader": "/pinterest"
}

for old_path, new_path in OLD_REDIRECTS.items():
    @router.get(old_path, include_in_schema=False)
    async def redirect_old_route(request: Request, _old=old_path, _new=new_path):
        return RedirectResponse(url=_new, status_code=301)


def create_route(path: str, data: dict):
    """Dynamically register GET routes for all SEO pages."""
    @router.get(path, response_class=HTMLResponse)
    async def page_route(request: Request):
        # Generate FAQ Schema
        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": []
        }
        for faq in data.get("faqs", []):
            faq_schema["mainEntity"].append({
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            })

        # Generate HowTo Schema
        howto_schema = {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": f"How to download {data.get('keyword')} videos",
            "step": []
        }
        for i, step in enumerate(data.get("steps", [])):
            howto_schema["step"].append({
                "@type": "HowToStep",
                "position": i + 1,
                "name": step["title"],
                "text": step["desc"]
            })

        # Inject schema into page data
        page_data = data.copy()
        page_data["faq_schema"] = json.dumps(faq_schema)
        page_data["howto_schema"] = json.dumps(howto_schema)
        # Hreflangs array is already populated in data["hreflangs"] from MULTILINGUAL_PAGES
        
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


@router.get("/robots.txt")
async def robots_txt():
    """Serve a production-ready robots.txt for search engine crawlers."""
    import os
    domain = os.getenv("DOMAIN_NAME", "https://snapreeldownload.com")
    if not domain.startswith("http"):
        domain = f"https://{domain}"

    content = (
        "# robots.txt for snapreeldownload.com\n"
        "# Last updated: 2026-03-11\n"
        "\n"
        "# ── Allow all search engines ────────────────────────\n"
        "User-agent: *\n"
        "\n"
        "# Allow: Public pages (homepage, tools, blog, legal)\n"
        "Allow: /\n"
        "Allow: /blog\n"
        "Allow: /sitemap.xml\n"
        "\n"
        "# Block: Internal API & backend endpoints\n"
        "Disallow: /preview\n"
        "Disallow: /proxy-image\n"
        "Disallow: /api/\n"
        "\n"
        "# ── Sitemap location ────────────────────────────────\n"
        f"Sitemap: {domain}/sitemap.xml\n"
    )
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(content=content, media_type="text/plain")