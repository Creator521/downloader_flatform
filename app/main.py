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
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

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

CORE_SEO_PATHS = {
    "/",
    "/reels",
    "/video",
    "/photo",
    "/story",
    "/youtube",
    "/tiktok",
    "/facebook",
    "/twitter",
    "/pinterest",
    "/snapchat",
    "/tiktok-mp3-downloader",
    "/youtube-shorts-downloader",
    "/youtube-to-mp3",
    "/reddit",
    "/savefrom-alternative",
    "/snaptik-alternative",
    "/ssstiktok-alternative",
    "/best-instagram-reels-downloader-alternatives",
    "/best-tiktok-downloader-without-watermark",
}

LANGUAGE_PREFIXES = ()
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
    1. Force HTTP → HTTPS.
    2. Force www → non-www.
    3. Force lowercase URLs.
    4. Handle trailing slashes consistently.
       - Language roots (e.g., /hi/) KEEP the trailing slash.
       - Specific tool paths (e.g., /hi/video) REMOVE the trailing slash.
    """
    from fastapi.responses import RedirectResponse

    path   = request.url.path

    # Skip normalization for static files — preserve original case for filesystem lookups
    if path.startswith("/static/"):
        return await call_next(request)

    scheme = request.headers.get("x-forwarded-proto", request.url.scheme)
    host   = request.headers.get("x-forwarded-host", request.url.hostname) or request.url.hostname
    query  = request.url.query

    # 1. Force HTTPS (Skip for local development)
    is_localhost = host in ("localhost", "127.0.0.1", "0.0.0.0")
    if scheme == "http" and not is_localhost:
        url = f"https://{host}{path}"
        if query:
            url += f"?{query}"
        return RedirectResponse(url=url, status_code=301)

    # 2. Force non-www
    if host and host.startswith("www."):
        non_www_host = host[4:]
        url = f"https://{non_www_host}{path}"
        if query:
            url += f"?{query}"
        return RedirectResponse(url=url, status_code=301)

    # 3. Lowercase check
    normalized_path = path.lower()

    # 404 Fixes for legacy paths and Cloudflare routes reported by GSC
    if normalized_path == "/twitter-video-downloader":
        url = "/twitter" + (f"?{query}" if query else "")
        return RedirectResponse(url=url, status_code=301)
        
    if normalized_path == "/api" or normalized_path.startswith("/cdn-cgi/"):
        return RedirectResponse(url="/", status_code=301)

    # 4. Trailing slash check
    # Language roots should keep trailing slash: /, /hi/, /es/, etc.
    # Other paths should not have it: /story, /hi/story
    is_lang_root = (path == "/")

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
    elif request.url.path in CORE_SEO_PATHS or request.url.path.startswith(LANGUAGE_PREFIXES):
        response.headers["Cache-Control"] = "public, max-age=300"  # 5 minutes for SEO pages

    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
            "https://www.googletagmanager.com https://pagead2.googlesyndication.com "
            "https://quge5.com https://5gvci.com https://*.googlesyndication.com "
            "https://adservice.google.com https://www.google-analytics.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https: blob:; "
        "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://www.google-analytics.com https://analytics.google.com https://region1.google-analytics.com https://stats.g.doubleclick.net https://*.googlesyndication.com "
            "https://pagead2.googlesyndication.com https://5gvci.com https://quge5.com; "
        "frame-src 'self' https://googleads.g.doubleclick.net https://*.googlesyndication.com; "
        "frame-ancestors 'self'; "
        "media-src 'self' https: blob:;"
    )

    return response

# --- Temp Directory ---
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# --- Register All Route Modules (Point 11: APIRouter split) ---
from fastapi.responses import PlainTextResponse

# Note: /ads.txt is handled by seo_router (app/routes/seo.py)

@app.get("/49ee0a05f62d4645bd7fd30f5840e72e.txt", include_in_schema=False)
async def indexnow_key():
    return PlainTextResponse("49ee0a05f62d4645bd7fd30f5840e72e")

@app.get("/sw.js", include_in_schema=False)
async def monetag_service_worker():
    """Monetag push notification service worker — must be served at root scope."""
    from fastapi.responses import Response
    content = (
        'self.options = {\n'
        '    "domain": "5gvci.com",\n'
        '    "zoneId": 11184914\n'
        '}\n'
        'self.lary = ""\n'
        'importScripts(\'https://5gvci.com/act/files/service-worker.min.js?r=sw\')\n'
    )
    return Response(
        content=content,
        media_type="application/javascript",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Service-Worker-Allowed": "/",
        },
    )

@app.get("/tag.min.js", include_in_schema=False)
async def monetag_tag_js():
    """Monetag Luminous tag JS file — must be served at root for installation check."""
    import httpx  # type: ignore
    from fastapi.responses import Response
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://quge5.com/88/tag.min.js",
            headers={"User-Agent": "Mozilla/5.0"},
            follow_redirects=True,
            timeout=10.0,
        )
    return Response(
        content=r.content,
        media_type="application/javascript",
        headers={"Cache-Control": "public, max-age=3600"},
    )

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

# --- Custom 404 Handler (Screaming Frog: Internal Client Error 4xx) ---
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import HTMLResponse

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 404:
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Not Found - SnapReelDownload</title>
    <meta name="robots" content="noindex, nofollow">
    <style>
        body{font-family:'Inter',-apple-system,sans-serif;background:#f8fafc;color:#0f172a;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}
        .c{text-align:center;max-width:500px;padding:40px}
        h1{font-size:72px;color:#4f46e5;margin:0}
        h2{font-size:24px;margin:16px 0 8px}
        p{color:#64748b;line-height:1.6}
        a{display:inline-block;margin-top:24px;padding:12px 32px;background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;border-radius:10px;text-decoration:none;font-weight:600;transition:transform .2s}
        a:hover{transform:translateY(-2px)}
    </style>
</head>
<body>
    <div class="c">
        <h1>404</h1>
        <h2>Page Not Found</h2>
        <p>The page you're looking for doesn't exist or has been moved. Try one of our video downloader tools instead.</p>
        <a href="/">Go to Homepage</a>
    </div>
</body>
</html>"""
        return HTMLResponse(content=html, status_code=404)
    # For other HTTP errors, return JSON
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

logger.info("Snap Reel Download app initialized with modular routes.")

