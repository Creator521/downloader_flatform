"""SEO landing page routes."""
import json
import logging
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.seo_data import SEO_PAGES
from app.blog_data import BLOG_POSTS
from app.programmatic_seo_data import PROGRAMMATIC_PAGES

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


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

        # Deduce hreflangs for programmatic pages
        hreflangs_map = {}
        target_lang = data.get("lang")
        if target_lang: # It means this is a programmatic page
            from app.programmatic_seo_data import SUPPORTED_LANGUAGES
            base_url = str(request.base_url).rstrip('/')
            
            # The current path could be '/hi/instagram-reel' or '/instagram-reel'
            # Let's derive the english root path first
            path_parts = path.strip('/').split('/')
            if path_parts[0] in SUPPORTED_LANGUAGES:
                en_root = '/' + '/'.join(path_parts[1:])
            else:
                en_root = path
                
            for lang in SUPPORTED_LANGUAGES:
                prefix = f"/{lang}" if lang != "en" else ""
                hreflangs_map[lang] = f"{base_url}{prefix}{en_root}"

        # Inject schema into page data
        page_data = data.copy()
        page_data["faq_schema"] = json.dumps(faq_schema)
        page_data["howto_schema"] = json.dumps(howto_schema)
        if hreflangs_map:
            page_data["hreflangs"] = hreflangs_map

        # Get latest 6 blog posts for the footer area
        latest_posts = dict(list(BLOG_POSTS.items())[:6])

        return templates.TemplateResponse("landing_page.html", {
            "request": request,
            "page": page_data,
            "latest_posts": latest_posts
        })


# Register all SEO routes
for path, data in SEO_PAGES.items():
    create_route(path, data)

# Register all programmatic SEO routes
for path, data in PROGRAMMATIC_PAGES.items():
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