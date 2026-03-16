"""
Snap Reel Download — FastAPI Application Entry Point
Slim entry point: all route logic lives in app/routes/ modules.
"""
import os
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# GZip middleware can be in Starlette (preferred) or FastAPI (older versions).
# Use a safe import so the app won't crash if the environment has a different FastAPI version.
try:
    from starlette.middleware.gzip import GZipMiddleware
except ImportError:
    try:
        from fastapi.middleware.gzip import GZipMiddleware
    except ImportError:
        GZipMiddleware = None

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

# --- GZip Compression Middleware (for faster delivery) ---
# Temporarily disabled - causing slowdown
# if GZipMiddleware is not None:
#     app.add_middleware(GZipMiddleware, minimum_size=1000)

# --- CORS Middleware ---
ALLOWED_ORIGINS = [
    "https://snapreeldownload.com",
    "https://www.snapreeldownload.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# --- Static Files & Caching Middleware ---
app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent / "frontend"), name="static")

@app.middleware("http")
async def add_cache_headers(request, call_next):
    response = await call_next(request)

    # Optimized caching for static files
    if request.url.path.startswith("/static"):
        # JS/CSS files - 6 months cache
        if request.url.path.endswith(('.js', '.css')):
            response.headers["Cache-Control"] = "public, max-age=15552000, immutable"  # 6 months
        # Images - 1 year cache
        elif request.url.path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"  # 1 year
        # Other static assets - 1 month
        else:
            response.headers["Cache-Control"] = "public, max-age=2592000"  # 30 days

    # Dynamic content caching for SEO pages (5 minutes)
    elif request.url.path.startswith(("/en/", "/hi/", "/es/", "/fr/", "/de/", "/pt/", "/ar/", "/id/", "/bn/", "/tr/", "/th/", "/ko/", "/ja/", "/uk/", "/pl/")):
        response.headers["Cache-Control"] = "public, max-age=300"  # 5 minutes for SEO pages

    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response

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

logger.info("Snap Reel Download app initialized with modular routes.")

