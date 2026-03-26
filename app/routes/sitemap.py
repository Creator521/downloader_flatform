"""Sitemap route with full coverage including programmatic pages."""
import os
import logging
from datetime import date
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.multilingual_data import MULTILINGUAL_PAGES
from app.blog_data import BLOG_POSTS
from app.routes.seo import ALL_REDIRECTS

logger = logging.getLogger(__name__)

router = APIRouter()

# Legal pages
LEGAL_PAGES = [
    "/about-us",
    "/contact-us",
    "/privacy-policy",
    "/terms-of-service",
    "/disclaimer",
    "/dmca",
]

# Build a set of all redirect source paths for fast lookup
REDIRECT_PATHS = set(ALL_REDIRECTS.keys())


@router.get("/sitemap.xml")
async def sitemap():
    today = date.today().isoformat()
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    
    # We use MULTILINGUAL_PAGES which now includes 350+ programmatic pages 
    # and already has 'canonical' and 'hreflangs' pre-computed.
    
    # 1. Homepage (Manual override for top priority)
    base = "https://snapreeldownload.com"
    xml += f'  <url>\n    <loc>{base}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n'
    # Add hreflangs for homepage
    for lang in ["en", "hi", "es", "fr", "de", "pt", "ar", "id", "bn", "tr", "th", "ko", "ja", "uk", "pl"]:
        prefix = f"/{lang}/" if lang != "en" else "/"
        xml += f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{base}{prefix}"/>\n'
    xml += '  </url>\n'

    # 2. Multilingual & Programmatic Pages
    for path, page in MULTILINGUAL_PAGES.items():
        # ✅ Skip any path that is a redirect source — these cause "Page with redirect" in GSC
        if path in REDIRECT_PATHS:
            continue

        # Set priority based on tool type
        priority = "0.7"
        if any(keyword in path for keyword in ["reels", "video", "tiktok", "youtube", "mp3"]):
            priority = "0.8"
        
        xml += f'  <url>\n    <loc>{base}{path}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>{priority}</priority>\n'
        
        # Add xhtml:link hreflang entries
        if "hreflangs" in page:
            for lang, href in page["hreflangs"].items():
                xml += f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{href}"/>\n'
        
        xml += '  </url>\n'

    # 3. Blog Posts
    for slug, post in BLOG_POSTS.items():
        post_date = post.get("date", today)
        xml += f'  <url>\n    <loc>{base}/blog/{slug}</loc>\n    <lastmod>{post_date}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.6</priority>\n  </url>\n'

    # 4. Legal Pages
    for path in LEGAL_PAGES:
        xml += f'  <url>\n    <loc>{base}{path}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.3</priority>\n  </url>\n'

    xml += '</urlset>'
    return HTMLResponse(content=xml, media_type="application/xml")
