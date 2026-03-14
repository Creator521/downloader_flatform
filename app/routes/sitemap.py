"""Sitemap route with full coverage including programmatic pages."""
import os
import logging
from datetime import date
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.multilingual_data import MULTILINGUAL_PAGES
from app.blog_data import BLOG_POSTS

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


@router.get("/sitemap.xml")
async def sitemap():
    today = date.today().isoformat()
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    base = os.getenv("DOMAIN_NAME", "yourdomain.com")
    if not base.startswith("http"):
        base = f"https://{base}"

    # Homepage (highest priority)
    xml += f'  <url><loc>{base}/</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>\n'

    # Multilingual SEO landing pages
    for path in MULTILINGUAL_PAGES:
        if path == "/":
            continue
        xml += f'  <url><loc>{base}{path}</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>\n'

    # Blog list page
    xml += f'  <url><loc>{base}/blog</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>0.7</priority></url>\n'

    # Individual blog posts
    for slug, post in BLOG_POSTS.items():
        post_date = post.get("date", today)
        xml += f'  <url><loc>{base}/blog/{slug}</loc><lastmod>{post_date}</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>\n'

    # Legal pages (low priority)
    for path in LEGAL_PAGES:
        xml += f'  <url><loc>{base}{path}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.3</priority></url>\n'

    xml += '</urlset>'
    return HTMLResponse(content=xml, media_type="application/xml")
