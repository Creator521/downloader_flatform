"""
ReelDownloader — FastAPI Application Entry Point
Slim entry point: all route logic lives in app/routes/ modules.
"""
import os
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.dependencies import limiter

# --- Logging Setup (Point 6: proper logging instead of print) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# --- FastAPI App ---
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static Files ---
app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent / "frontend"), name="static")

# --- Temp Directory ---
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# --- Register All Route Modules (Point 11: APIRouter split) ---
from app.routes.seo import router as seo_router
from app.routes.blog import router as blog_router
from app.routes.legal import router as legal_router
from app.routes.api import router as api_router
from app.routes.proxy import router as proxy_router
from app.routes.sitemap import router as sitemap_router

app.include_router(seo_router)
app.include_router(blog_router)
app.include_router(legal_router)
app.include_router(api_router)
app.include_router(proxy_router)
app.include_router(sitemap_router)

logger.info("ReelDownloader app initialized with modular routes.")
