from fastapi import FastAPI, Form, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import yt_dlp
import os
import json
from app.seo_data import SEO_PAGES
from app.blog_data import BLOG_POSTS
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import functools
import time

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Simple In-Memory Cache for Preview
# Dict[URL, (Timestamp, Data)]
PREVIEW_CACHE = {}
CACHE_DURATION = 3600 # 1 Hour

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="e:/downloader_flatform/frontend"), name="static")
templates = Jinja2Templates(directory="e:/downloader_flatform/app/templates")

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# SEO Routes Generator
# We dynamically register GET routes for all pages defined in SEO_PAGES
def create_route(path, data):
    @app.get(path, response_class=HTMLResponse)
    async def page_route(request: Request):
        # Generate Schema
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

        # Inject schema into page data
        page_data = data.copy()
        page_data["faq_schema"] = json.dumps(faq_schema)
        page_data["howto_schema"] = json.dumps(howto_schema)

        # Get latest 6 blog posts for the footer area
        latest_posts = dict(list(BLOG_POSTS.items())[:6])

        return templates.TemplateResponse("landing_page.html", {"request": request, "page": page_data, "latest_posts": latest_posts})

# Register all routes

# Register all routes
for path, data in SEO_PAGES.items():
    create_route(path, data)

# 🔹 BLOG ROUTES
@app.get("/blog", response_class=HTMLResponse)
async def blog_list(request: Request):
    return templates.TemplateResponse("blog_list.html", {"request": request, "posts": BLOG_POSTS})

@app.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post(request: Request, slug: str):
    post = BLOG_POSTS.get(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return templates.TemplateResponse("blog_post.html", {"request": request, "post": post})

# 🔹 LEGAL ROUTES
@app.get("/about-us", response_class=HTMLResponse)
async def about_us(request: Request):
    content = """
    <h2>Our Mission</h2>
    <p>ReelDownloader was built with a simple mission: to help content creators, marketers, and everyday users save their favorite videos for offline viewing. We believe in an open internet where content is accessible to everyone.</p>
    <h2>Who We Are</h2>
    <p>We are a small team of developers and video enthusiasts passionate about building useful web tools. Our infrastructure is designed to be fast, reliable, and secure.</p>
    """
    return templates.TemplateResponse("legal.html", {"request": request, "title": "About Us", "content": content})

@app.get("/contact-us", response_class=HTMLResponse)
async def contact_us(request: Request):
    content = """
    <h2>Get in Touch</h2>
    <p>We love hearing from our users! Whether you have a feature request, a bug report, or just want to say hello, feel free to contact us.</p>
    <p>We typically respond within 24-48 hours.</p>
    """
    return templates.TemplateResponse("legal.html", {"request": request, "title": "Contact Us", "content": content, "email": "support@reeldownloader.com"})

@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    content = """
    <h2>1. Information We Collect</h2>
    <p>We do not require you to create an account to use our service. We may collect non-personal information such as your browser type, language preference, and referring site for analytics purposes.</p>
    <h2>2. Cookies</h2>
    <p>We use cookies to improve your experience and to serve personalized ads via Google AdSense.</p>
    <h2>3. Third-Party Services</h2>
    <p>We use third-party services like Google Analytics and Google AdSense. These services have their own privacy policies.</p>
    """
    return templates.TemplateResponse("legal.html", {"request": request, "title": "Privacy Policy", "content": content})

@app.get("/terms-of-service", response_class=HTMLResponse)
async def terms_of_service(request: Request):
    content = """
    <h2>1. Acceptance of Terms</h2>
    <p>By accessing this website, you agree to be bound by these Terms and Conditions and all applicable laws and regulations.</p>
    <h2>2. Usage License</h2>
    <p>Permission is granted to temporarily download one copy of the materials (videos) for personal, non-commercial transitory viewing only.</p>
    <h2>3. Disclaimer</h2>
    <p>The materials on ReelDownloader are provided on an 'as is' basis. We make no warranties, expressed or implied.</p>
    """
    return templates.TemplateResponse("legal.html", {"request": request, "title": "Terms & Conditions", "content": content})

@app.get("/disclaimer", response_class=HTMLResponse)
async def disclaimer(request: Request):
    content = """
    <h2>Not Affiliated</h2>
    <p>ReelDownloader is an independent tool and is NOT affiliated, endorsed, sponsored, or certified by Instagram, Facebook, TikTok, YouTube, or any other platform.</p>
    <p>All logos and trademarks displayed on this site are the property of their respective owners.</p>
    <h2>User Responsibility</h2>
    <p>You are solely responsible for valid downloads and any copyright infringements that may occur as a result of using this tool.</p>
    """
    return templates.TemplateResponse("legal.html", {"request": request, "title": "Disclaimer", "content": content})

@app.get("/dmca", response_class=HTMLResponse)
async def dmca(request: Request):
    content = """
    <h2>Copyright Infringement</h2>
    <p>We respect the intellectual property of others. If you believe your work has been copied in a way that constitutes copyright infringement, please contact us.</p>
    <h2>Removal Request</h2>
    <p>Since we do not host files, we can only block specific URLs from being processed by our tool. Please send the URL to our email.</p>
    """
    return templates.TemplateResponse("legal.html", {"request": request, "title": "DMCA Policy", "content": content, "email": "dmca@reeldownloader.com"})


# 🔹 API ROUTES (Keep existing logic)
# Note: Root "/" is already handled by SEO_PAGES loop above if present in dictionary
# If "/" is NOT in SEO_PAGES, we should keep the old one, but it IS in SEO_PAGES.
# So we effectively replaced the static file serve with the template serve.

@app.get("/sitemap.xml")
async def sitemap():
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    base = "http://yourdomain.com" # Should be config
    for path in SEO_PAGES:
        xml += f'  <url><loc>{base}{path}</loc><changefreq>daily</changefreq></url>\n'
    xml += '</urlset>'
    return HTMLResponse(content=xml, media_type="application/xml")


# 🔹 PREVIEW API
@app.post("/preview")
@limiter.limit("10/minute")
def preview(request: Request, url: str = Form(...)):
    # Check Cache
    if url in PREVIEW_CACHE:
        timestamp, data = PREVIEW_CACHE[url]
        if time.time() - timestamp < CACHE_DURATION:
            return data
        else:
            del PREVIEW_CACHE[url] # Expired
    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        data = {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "video_url": info.get("url")
        }
        # Save to Cache
        PREVIEW_CACHE[url] = (time.time(), data)
        return data
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail=f"Invalid video URL: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# 🔹 DOWNLOAD API (same as before)
@app.post("/download")
@limiter.limit("5/minute")
def download(request: Request, url: str = Form(...), format: str = Form("video")):
    import subprocess
    import sys
    
    # 1. Get Metadata first (lightweight)
    ydl_opts_meta = {
        "quiet": True,
        "skip_download": True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts_meta) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "video")
            ext = "mp4" # Default container
            
            # Determine format code and extension
            if format == "audio":
                # bestaudio converted to m4a (compatible) or mp3 is tricky in stream
                # standard 'bestaudio' usually returns m4a or webm. 
                # To be safe for streaming without ffmpeg post-processing on server side (which blocks),
                # we should just request the best available audio.
                # However, strict format conversion (mp3) requires processing.
                # For scalability, we stream the raw 'bestaudio' (usually m4a/opus).
                format_code = "bestaudio/best"
                ext = "m4a" # Common audio ext
            else:
                format_code = "best[ext=mp4]/best"
                ext = "mp4"

            # Clean filename
            filename = f"{title}.{ext}"
            # Remove characters that might break headers
            filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).strip()

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch metadata: {str(e)}")

    # 2. Start Streaming Subprocess
    # We use sys.executable to ensure we use the same python environment's yt-dlp
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--no-part",               # Write directly
        "--output", "-",           # Output to stdout
        "--format", format_code,
        "--quiet",                 # No logs in stdout
        url
    ]

    try:
        # bufsize=0 ensures unbuffered output for smoother streaming
        proc = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, # Capture errors just in case
            bufsize=10**7 # 10MB buffer
        )

        # 3. Create Generator
        def iterfile():
            try:
                while True:
                    data = proc.stdout.read(64 * 1024) # Read 64KB chunks
                    if not data:
                        break
                    yield data
            except Exception:
                proc.kill()
            finally:
                proc.wait()

        # 4. Return Streaming Response
        media_type = "audio/mp4" if format == "audio" else "video/mp4"
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
        
        return StreamingResponse(
            iterfile(),
            media_type=media_type,
            headers=headers
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Streaming failed: {str(e)}")
