# app/programmatic_seo_data.py
"""Programmatic SEO page generator — creates 50+ pages from templates."""


def _make_page(path, platform, keyword, action, modifier, tool_name, extra_desc=""):
    """Generate a complete SEO page dict from minimal inputs."""
    title = f"{action} {keyword} {modifier} - Free Online {tool_name}".strip()
    desc = f"{action} {keyword} {modifier} for free. {extra_desc} Fast, safe, no login required. Works on Android, iPhone & PC."
    h1 = f"{action} {keyword} {modifier}".strip()
    subtitle = f"Free Online {tool_name} – {modifier if modifier else 'Fast & Easy'}".strip()

    intro = f"""
    <p>Looking for a fast and reliable way to <strong>{action.lower()} {keyword.lower()}</strong>? You've come to the right place.
    Our free online <strong>{tool_name}</strong> lets you save {keyword.lower()} directly to your device in HD quality — no app installation, no login, no watermark.</p>
    <p>Whether you're on a smartphone, tablet, or computer, simply paste the link and download instantly.
    {extra_desc}</p>
    """

    steps = [
        {"title": "Step 1: Copy the Link", "desc": f"Open the {platform} app or website, find the content, and copy the share link."},
        {"title": "Step 2: Paste the URL", "desc": "Come back here and paste the link into the input box above."},
        {"title": "Step 3: Download", "desc": f"Click Download and save the {keyword.lower()} to your device in HD."}
    ]

    features = [
        {"title": "🆓 100% Free", "desc": "No hidden charges, no subscription, unlimited downloads."},
        {"title": "✨ HD Quality", "desc": f"Download {keyword.lower()} in original high-definition quality."},
        {"title": "⚡ Fast Processing", "desc": "Our servers process your request in seconds."},
        {"title": "📱 All Devices", "desc": "Works on Android, iPhone, iPad, Windows, Mac, and Linux."},
        {"title": "🔒 Safe & Private", "desc": "SSL encrypted. We don't store your data or downloads."}
    ]

    faqs = [
        {"question": f"Is this {tool_name.lower()} free?", "answer": "Yes, completely free with no limits."},
        {"question": "Do I need to install an app?", "answer": "No, our tool works directly in your web browser."},
        {"question": "Is login required?", "answer": "No, you can download without any account or login."},
        {"question": f"Can I {action.lower()} in HD?", "answer": "Yes, we always fetch the highest available quality."},
        {"question": "Is it safe to use?", "answer": "Absolutely. Our site uses SSL encryption and we don't store any data."}
    ]

    return {
        "title": title[:60],
        "description": desc[:160],
        "h1": h1,
        "subtitle": subtitle,
        "tool_name": tool_name,
        "intro_text": intro,
        "keyword": keyword.lower(),
        "platform": platform,
        "steps": steps,
        "features": features,
        "faqs": faqs
    }


# ── Keyword Variation Pages ──────────────────────────────────────────────────

KEYWORD_PAGES_CONFIG = [
    # Instagram Reels variations
    ("/download-instagram-reels", "Instagram", "Instagram Reels", "Download", "", "Instagram Reels Downloader", "Save your favorite Reels without watermark."),
    ("/download-instagram-reels-online", "Instagram", "Instagram Reels", "Download", "Online", "Instagram Reels Downloader", "No software needed — works in your browser."),
    ("/download-instagram-reels-hd", "Instagram", "Instagram Reels HD", "Download", "in HD", "Instagram Reels HD Downloader", "Get crystal clear 1080p quality."),
    ("/instagram-reel-downloader-free", "Instagram", "Instagram Reels", "Download", "Free", "Free Instagram Reel Downloader", "Zero cost, unlimited downloads."),
    ("/save-instagram-video-online", "Instagram", "Instagram Videos", "Save", "Online", "Instagram Video Saver", "Archive your favorite posts offline."),
    ("/best-instagram-reel-downloader", "Instagram", "Instagram Reels", "Download", "", "Best Instagram Reel Downloader", "Rated #1 by users for speed and quality."),
    ("/instagram-video-download-tool", "Instagram", "Instagram Videos", "Download", "", "Instagram Video Download Tool", "A powerful tool for all Instagram content."),
    ("/instagram-reel-saver", "Instagram", "Instagram Reels", "Save", "", "Instagram Reel Saver", "Save Reels to your gallery instantly."),
    ("/instagram-reel-to-mp4", "Instagram", "Instagram Reels", "Convert", "to MP4", "Instagram Reel to MP4 Converter", "Get universal MP4 format files."),
    ("/instagram-video-saver-online", "Instagram", "Instagram Videos", "Save", "Online", "Online Instagram Video Saver", "Works on any device, any browser."),
    ("/free-instagram-video-downloader", "Instagram", "Instagram Videos", "Download", "Free", "Free Instagram Video Downloader", "No registration, no payments, ever."),
    ("/download-instagram-reels-without-watermark", "Instagram", "Instagram Reels Without Watermark", "Download", "", "Instagram Reels Downloader", "Get clean videos without any logos."),
    # YouTube variations
    ("/download-youtube-video-online", "YouTube", "YouTube Videos", "Download", "Online", "Online YouTube Video Downloader", "Save any public YouTube video."),
    ("/youtube-video-downloader-free", "YouTube", "YouTube Videos", "Download", "Free", "Free YouTube Video Downloader", "No cost, no limits, no ads."),
    ("/youtube-to-mp4-converter", "YouTube", "YouTube Videos", "Convert", "to MP4", "YouTube to MP4 Converter", "Get MP4 files for any device."),
    ("/save-youtube-videos-online", "YouTube", "YouTube Videos", "Save", "Online", "Online YouTube Video Saver", "Build your offline video library."),
    ("/best-youtube-downloader", "YouTube", "YouTube Videos", "Download", "", "Best YouTube Downloader", "Fast, reliable, supports 4K quality."),
    # TikTok variations
    ("/download-tiktok-video-online", "TikTok", "TikTok Videos", "Download", "Online", "Online TikTok Video Downloader", "Remove watermark automatically."),
    ("/tiktok-downloader-without-watermark", "TikTok", "TikTok Videos Without Watermark", "Download", "", "TikTok Downloader No Watermark", "Clean videos without the bouncing logo."),
    ("/save-tiktok-videos-free", "TikTok", "TikTok Videos", "Save", "Free", "Free TikTok Video Saver", "Unlimited free downloads."),
    ("/tiktok-video-saver", "TikTok", "TikTok Videos", "Save", "", "TikTok Video Saver", "Archive your favorite TikToks."),
    # Facebook variations
    ("/download-facebook-video-online", "Facebook", "Facebook Videos", "Download", "Online", "Online Facebook Video Downloader", "Save FB videos and Reels."),
    ("/facebook-video-downloader-free", "Facebook", "Facebook Videos", "Download", "Free", "Free Facebook Video Downloader", "No login to Facebook required."),
    ("/save-facebook-videos", "Facebook", "Facebook Videos", "Save", "Online", "Facebook Video Saver", "Keep videos from your feed."),
    # Twitter/X variations
    ("/download-twitter-video-online", "Twitter (X)", "Twitter Videos", "Download", "Online", "Online Twitter Video Downloader", "Works with twitter.com and x.com links."),
    ("/save-twitter-videos-free", "Twitter (X)", "Twitter Videos", "Save", "Free", "Free Twitter Video Saver", "Save tweets with video instantly."),
    ("/x-video-saver", "Twitter (X)", "X (Twitter) Videos", "Save", "", "X Video Saver", "Download from X.com in HD."),
    # General / multi-platform
    ("/social-media-video-downloader", "Multiple", "Social Media Videos", "Download", "", "Social Media Video Downloader", "One tool for Instagram, TikTok, YouTube, Facebook & Twitter."),
    ("/online-video-downloader-free", "Multiple", "Online Videos", "Download", "Free", "Free Online Video Downloader", "Universal downloader for all platforms."),
    ("/video-downloader-no-watermark", "Multiple", "Videos Without Watermark", "Download", "", "Video Downloader No Watermark", "Clean downloads from any platform."),
    ("/hd-video-downloader-online", "Multiple", "HD Videos", "Download", "Online", "HD Video Downloader", "Always get the highest available quality."),
    ("/reels-downloader", "Instagram", "Reels", "Download", "", "Reels Downloader", "The fastest way to save Reels."),
]

# ── Device-Specific Pages ────────────────────────────────────────────────────

DEVICE_PAGES_CONFIG = [
    # Instagram + device
    ("/download-instagram-reels-iphone", "Instagram", "Instagram Reels on iPhone", "Download", "", "Use Safari to paste the link and save Reels directly to your Photos app."),
    ("/download-instagram-reels-android", "Instagram", "Instagram Reels on Android", "Download", "", "Use Chrome and the video saves straight to your Downloads folder."),
    ("/download-instagram-reels-pc", "Instagram", "Instagram Reels on PC", "Download", "", "Copy the URL from your desktop browser and download the MP4 file."),
    ("/instagram-video-downloader-chrome", "Instagram", "Instagram Videos via Chrome", "Download", "", "Works perfectly with Google Chrome on any OS."),
    ("/instagram-video-downloader-mobile", "Instagram", "Instagram Videos on Mobile", "Download", "", "Optimized for mobile browsers — fast and responsive."),
    ("/instagram-reel-downloader-iphone", "Instagram", "Instagram Reels on iPhone", "Download", "", "Save Reels to your iPhone camera roll in seconds."),
    ("/instagram-reel-downloader-android", "Instagram", "Instagram Reels on Android", "Download", "", "Download Reels to your Android gallery instantly."),
    ("/instagram-downloader-safari", "Instagram", "Instagram Videos via Safari", "Download", "", "Fully compatible with Safari on iPhone, iPad, and Mac."),
    ("/instagram-downloader-firefox", "Instagram", "Instagram Videos via Firefox", "Download", "", "Works seamlessly with Firefox on all platforms."),
    # TikTok + device
    ("/download-tiktok-videos-iphone", "TikTok", "TikTok Videos on iPhone", "Download", "", "Save TikToks directly to your iPhone Photos app."),
    ("/download-tiktok-videos-android", "TikTok", "TikTok Videos on Android", "Download", "", "Download TikToks to your Android phone in HD."),
    ("/download-tiktok-videos-pc", "TikTok", "TikTok Videos on PC", "Download", "", "Save TikTok content directly to your computer."),
    # YouTube + device
    ("/youtube-video-downloader-mobile", "YouTube", "YouTube Videos on Mobile", "Download", "", "Save YouTube videos on your phone for offline viewing."),
    ("/youtube-video-downloader-pc", "YouTube", "YouTube Videos on PC", "Download", "", "Download YouTube videos to your desktop in 4K quality."),
    ("/youtube-downloader-for-mac", "YouTube", "YouTube Videos on Mac", "Download", "", "Compatible with Safari and Chrome on macOS."),
    # Facebook + device
    ("/download-facebook-videos-iphone", "Facebook", "Facebook Videos on iPhone", "Download", "", "Copy the FB link and save to your iPhone camera roll."),
    ("/download-facebook-videos-android", "Facebook", "Facebook Videos on Android", "Download", "", "Works with Chrome, Firefox, and Samsung Internet."),
    # Twitter + device
    ("/download-twitter-videos-iphone", "Twitter (X)", "Twitter Videos on iPhone", "Download", "", "Save tweet videos to your iPhone Photos app."),
    ("/download-twitter-videos-android", "Twitter (X)", "Twitter Videos on Android", "Download", "", "Download X/Twitter videos to your Android gallery."),
    # General device
    ("/video-downloader-for-windows", "Multiple", "Videos on Windows PC", "Download", "", "Download social media videos on Windows 10/11."),
]


def _make_device_page(path, platform, keyword, action, modifier, device_tip):
    """Generate device-specific page with tailored instructions."""
    page = _make_page(path, platform, keyword, action, modifier,
                      f"{keyword.split(' on ')[0] if ' on ' in keyword else keyword} Downloader",
                      device_tip)
    # Override intro with device-specific content
    page["intro_text"] = f"""
    <p>Want to <strong>{action.lower()} {keyword.lower()}</strong>? Our free online tool makes it easy.
    {device_tip} No app installation needed — everything works right in your browser.</p>
    <p>Our tool is optimized for all devices and browsers, ensuring a smooth experience whether you're on
    a smartphone, tablet, or desktop computer. Just paste the link and download in HD quality.</p>
    """
    return page


def generate_all_programmatic_pages():
    """Generate all programmatic SEO pages and return as a single dict."""
    pages = {}

    # Keyword variation pages
    for config in KEYWORD_PAGES_CONFIG:
        path, platform, keyword, action, modifier, tool_name, extra = config
        pages[path] = _make_page(path, platform, keyword, action, modifier, tool_name, extra)

    # Device-specific pages
    for config in DEVICE_PAGES_CONFIG:
        path, platform, keyword, action, modifier, device_tip = config
        pages[path] = _make_device_page(path, platform, keyword, action, modifier, device_tip)

    return pages


# Export the generated pages
PROGRAMMATIC_PAGES = generate_all_programmatic_pages()
