"""Legal page routes — content now lives in template files."""
import logging
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


@router.get("/about-us", response_class=HTMLResponse)
async def about_us(request: Request):
    return templates.TemplateResponse("pages/about_us.html", {"request": request})


@router.get("/contact-us", response_class=HTMLResponse)
async def contact_us(request: Request):
    return templates.TemplateResponse("pages/contact_us.html", {"request": request})


@router.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse("pages/privacy_policy.html", {"request": request})


@router.get("/terms-of-service", response_class=HTMLResponse)
async def terms_of_service(request: Request):
    return templates.TemplateResponse("pages/terms.html", {"request": request})


@router.get("/disclaimer", response_class=HTMLResponse)
async def disclaimer(request: Request):
    return templates.TemplateResponse("pages/disclaimer.html", {"request": request})


@router.get("/dmca", response_class=HTMLResponse)
async def dmca(request: Request):
    return templates.TemplateResponse("pages/dmca.html", {"request": request})


@router.get("/cookie-policy", response_class=HTMLResponse)
async def cookie_policy(request: Request):
    return templates.TemplateResponse("pages/cookie_policy.html", {"request": request})

