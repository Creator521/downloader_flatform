"""Sitemap route."""
import os
import logging
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.seo_data import SEO_PAGES

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/sitemap.xml")
async def sitemap():
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    base = os.getenv("DOMAIN_NAME", "yourdomain.com")
    if not base.startswith("http"):
        base = f"http://{base}"

    for path in SEO_PAGES:
        xml += f'  <url><loc>{base}{path}</loc><changefreq>daily</changefreq></url>\n'
    xml += '</urlset>'
    return HTMLResponse(content=xml, media_type="application/xml")
