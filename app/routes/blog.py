"""Blog routes."""
import os
import logging
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.blog_data import BLOG_POSTS

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


@router.get("/blog", response_class=HTMLResponse)
async def blog_list(request: Request):
    return templates.TemplateResponse("blog_list.html", {
        "request": request,
        "posts": BLOG_POSTS
    })


@router.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post(request: Request, slug: str):
    post = BLOG_POSTS.get(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")

    domain_name = os.getenv("DOMAIN_NAME", "https://snapreeldownload.com")
    # Ensure always https://
    if domain_name.startswith("http://"):
        domain_name = domain_name.replace("http://", "https://", 1)
    elif not domain_name.startswith("https://"):
        domain_name = f"https://{domain_name}"

    # Related posts: same tags, excluding current post (up to 3)
    post_tags = set(post.get("tags", []))
    related = []
    for s, p in BLOG_POSTS.items():
        if s == slug:
            continue
        if post_tags and set(p.get("tags", [])) & post_tags:
            related.append((s, p))
        if len(related) >= 3:
            break
    # Fallback: if not enough tag-matched posts, take latest 3 excluding current
    if len(related) < 3:
        for s, p in BLOG_POSTS.items():
            if s == slug or (s, p) in related:
                continue
            related.append((s, p))
            if len(related) >= 3:
                break

    return templates.TemplateResponse("blog_post.html", {
        "request": request,
        "post": post,
        "slug": slug,
        "domain_name": domain_name,
        "related_posts": related,
    })
