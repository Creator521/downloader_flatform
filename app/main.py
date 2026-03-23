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
if GZipMiddleware is not None:
    app.add_middleware(GZipMiddleware, minimum_size=1000)

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
async def normalize_url_middleware(request, call_next):
    """
    SEO Middleware:
    1. Force lowercase URLs.
    2. Handle trailing slashes consistently.
       - Language roots (e.g., /en/) KEEP the trailing slash.
       - Specific tool paths (e.g., /en/video) REMOVE the trailing slash.
    """
    from fastapi.responses import RedirectResponse
    
    path = request.url.path
    query = request.url.query
    
    # 1. Lowercase check
    normalized_path = path.lower()
    
    # 2. Trailing slash check
    # Language roots should keep trailing slash: /, /hi/, /es/, etc.
    # Other paths should not have it: /story, /hi/story
    is_lang_root = (path == "/") or any(path == f"/{l}/" for l in ["hi", "es", "fr", "de", "pt", "ar", "id", "bn", "tr", "th", "ko", "ja", "uk", "pl"])
    
    if not is_lang_root and normalized_path.endswith("/") and len(normalized_path) > 1:
        normalized_path = normalized_path.rstrip("/")
    
    # Redirect if normalization changed the path
    if normalized_path != path:
        url = normalized_path
        if query:
            url += f"?{query}"
        return RedirectResponse(url=url, status_code=301)

    return await call_next(request)

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
    # Includes root and all language paths
    elif request.url.path == "/" or request.url.path.startswith(("/hi/", "/es/", "/fr/", "/de/", "/pt/", "/ar/", "/id/", "/bn/", "/tr/", "/th/", "/ko/", "/ja/", "/uk/", "/pl/")):
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

