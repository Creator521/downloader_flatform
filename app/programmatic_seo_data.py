# app/programmatic_seo_data.py
"""Programmatic SEO page generator — creates 350+ pages from templates across 7 languages.
FIXES APPLIED:
 1. Platform-specific unique intro_text — no duplicate content
 2. Canonical + hreflang fields on every translated page
 3. Smart title truncation (no mid-word cuts)
 4. Platform-specific FAQs per page
"""

# ── Translations ─────────────────────────────────────────────────────────────
TRANSLATIONS = {
    "en": {"Download": "Download", "Save": "Save", "Online": "Online", "Free": "Free", "in HD": "in HD", "to MP4": "to MP4"},
    "es": {"Download": "Descargar", "Save": "Guardar", "Online": "En línea", "Free": "Gratis", "in HD": "en HD", "to MP4": "a MP4"},
    "hi": {"Download": "डाउनलोड", "Save": "सेव", "Online": "ऑनलाइन", "Free": "मुफ्त", "in HD": "HD में", "to MP4": "MP4 में"},
    "ar": {"Download": "تحميل", "Save": "حفظ", "Online": "عبر الانترنت", "Free": "مجاني", "in HD": "بجودة HD", "to MP4": "إلى MP4"},
    "id": {"Download": "Unduh", "Save": "Simpan", "Online": "Online", "Free": "Gratis", "in HD": "dalam HD", "to MP4": "ke MP4"},
    "pt": {"Download": "Baixar", "Save": "Salvar", "Online": "Online", "Free": "Grátis", "in HD": "em HD", "to MP4": "para MP4"},
    "fr": {"Download": "Télécharger", "Save": "Sauvegarder", "Online": "En ligne", "Free": "Gratuit", "in HD": "en HD", "to MP4": "vers MP4"}
}

SUPPORTED_LANGUAGES = list(TRANSLATIONS.keys())

def _translate(text, lang):
    if lang == "en" or not text:
        return text
    trans_dict = TRANSLATIONS.get(lang, {})
    for eng_word, trans_word in trans_dict.items():
        if eng_word in text:
            text = text.replace(eng_word, trans_word)
    return text

def _smart_truncate(text, max_len):
    """✅ FIX 3: Truncate at last complete word boundary, not mid-word."""
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    last_space = truncated.rfind(" ")
    if last_space > max_len - 20:
        return truncated[:last_space].rstrip(" -|")
    return truncated.rstrip(" -|")


# ── ✅ FIX 1: Platform-specific unique intro templates ────────────────────────
PLATFORM_INTROS = {
    "Instagram": """
    <p>Instagram is packed with creative videos, stunning Reels, inspiring stories, and beautiful photos — but the app doesn't offer a built-in way to save most of this content to your device. Whether you want to watch your favorite creator's Reel offline, save a recipe before it disappears, or keep a funny clip to share on WhatsApp, you need a reliable <strong>{tool_name}</strong>.</p>
    <p>Our free online tool lets you <strong>{action_lower} {keyword_lower}</strong> directly to your phone or computer in HD quality. No app installation, no login to Instagram required, no watermark on the downloaded file. {extra_desc}</p>
    <p>Works on Android, iPhone, iPad, Windows PC, and Mac — any browser, any device.</p>
    """,
    "TikTok": """
    <p>TikTok videos are some of the most creative, entertaining, and shareable content on the internet — but the platform's built-in download option adds an unavoidable watermark with the creator's username. For personal archives, video editing projects, or simply a clean viewing experience, that watermark is a problem.</p>
    <p>Our <strong>{tool_name}</strong> removes the TikTok watermark automatically and lets you <strong>{action_lower} {keyword_lower}</strong> in original HD quality. Completely free, no login, works in any browser. {extra_desc}</p>
    <p>Compatible with all Android phones, iPhones, iPads, Windows, and Mac — no app needed.</p>
    """,
    "YouTube": """
    <p>YouTube has over 800 million videos — tutorials, music, documentaries, courses, and more. But streaming requires an internet connection and burns through mobile data. Saving YouTube videos for offline use makes perfect sense for travelers, students, and anyone on a limited data plan.</p>
    <p>Our free <strong>{tool_name}</strong> lets you <strong>{action_lower} {keyword_lower}</strong> in HD, 1080p, or even 4K quality where available. No software to install, no Google account needed, no daily limits. {extra_desc}</p>
    <p>Works on Android, iPhone, Windows, Mac, and any modern browser.</p>
    """,
    "Facebook": """
    <p>Facebook hosts billions of videos — news clips, cooking tutorials, funny moments, sports highlights, and Facebook Reels. But unlike YouTube, Facebook provides almost no native download option for most content types, leaving users unable to save videos they want to keep.</p>
    <p>Our <strong>{tool_name}</strong> solves this — <strong>{action_lower} {keyword_lower}</strong> in HD quality, completely free. No Facebook login required, no software to install, works instantly in your browser. {extra_desc}</p>
    <p>Supports Android, iPhone, iPad, Windows PC, and Mac.</p>
    """,
    "Twitter (X)": """
    <p>X (formerly Twitter) is the home of breaking news, viral sports moments, trending memes, and real-time event coverage — all in short video clips. But X provides no built-in download button for videos, and links shared outside the platform often lose context or stop working.</p>
    <p>Our <strong>{tool_name}</strong> lets you <strong>{action_lower} {keyword_lower}</strong> directly to your device in HD quality. No X account needed, no login, completely free and anonymous. {extra_desc}</p>
    <p>Works on all devices: Android, iPhone, PC, and Mac.</p>
    """,
    "Multiple": """
    <p>In today's social media landscape, great video content is spread across dozens of platforms — Instagram, TikTok, YouTube, Facebook, Twitter, Pinterest, and more. Switching between multiple apps and tools to download from each platform is slow and frustrating.</p>
    <p>Our <strong>{tool_name}</strong> is a universal solution — <strong>{action_lower} {keyword_lower}</strong> from multiple platforms with one simple tool. Free, no login, works in any browser. {extra_desc}</p>
    <p>Compatible with all devices and operating systems.</p>
    """,
}

# ── ✅ FIX 4: Platform-specific FAQs ─────────────────────────────────────────
PLATFORM_FAQS = {
    "Instagram": [
        {"question": "Can I download Instagram videos without logging in?", "answer": "Yes — our tool works without any Instagram login. We never ask for your username or password, keeping your account completely safe."},
        {"question": "Will Instagram notify the creator when I download their video?", "answer": "No. Instagram does not send notifications to creators when their content is downloaded via third-party tools. Your download is completely anonymous."},
        {"question": "Can I download from private Instagram accounts?", "answer": "No — our tool only supports content from public Instagram accounts. Private content is protected and inaccessible to any third-party tool."},
        {"question": "Do downloaded Instagram videos have a watermark?", "answer": "No — our tool downloads the original clean video file directly from Instagram's servers, without adding any watermarks or logos."},
        {"question": "What Instagram content types can I download?", "answer": "You can download Instagram Reels, feed videos, Stories, IGTV videos, and photos from any public account."},
        {"question": "Is there a limit on how many Instagram videos I can download?", "answer": "No — you can download as many videos as you want. Our service is completely free with no daily limits."},
        {"question": "What format are downloaded Instagram videos in?", "answer": "Videos download as MP4 files. Photos download as JPG files. Both formats are compatible with all devices and players."},
    ],
    "TikTok": [
        {"question": "Does the downloaded TikTok video have a watermark?", "answer": "No — our tool automatically removes the TikTok watermark and username overlay. You get a clean, professional-looking HD video file."},
        {"question": "Can I download TikTok videos if the creator disabled downloads?", "answer": "Yes — our tool works for all public TikTok videos regardless of whether the creator has disabled TikTok's built-in download feature."},
        {"question": "Can I download TikTok audio only as MP3?", "answer": "Yes! Use our TikTok to MP3 converter to extract just the audio track from any public TikTok video."},
        {"question": "Can I download from private TikTok accounts?", "answer": "No — we only support content from public TikTok accounts. Private account videos cannot be accessed by any third-party tool."},
        {"question": "Does TikTok notify the creator when I download their video?", "answer": "No — downloading via our tool is completely anonymous. The creator will not receive any notification."},
        {"question": "What quality are downloaded TikTok videos?", "answer": "Videos are downloaded in the original HD quality from TikTok's servers — typically 720p or 1080p depending on the original upload."},
        {"question": "Is there a daily limit on TikTok downloads?", "answer": "No — completely free and unlimited. Download as many TikTok videos as you want."},
    ],
    "YouTube": [
        {"question": "Can I download YouTube videos in 4K quality?", "answer": "Yes — when the creator uploads in 4K, our tool will offer 4K download options. Most videos are available in HD (720p/1080p)."},
        {"question": "Can I download YouTube Shorts with this tool?", "answer": "Yes — paste a Shorts URL (youtube.com/shorts/...) and it works exactly like regular YouTube videos."},
        {"question": "Can I extract audio from YouTube videos as MP3?", "answer": "Yes! Use our YouTube to MP3 converter to extract and download just the audio track."},
        {"question": "Is it legal to download YouTube videos?", "answer": "YouTube's Terms of Service restrict downloading without permission. Download only for personal offline viewing. Never redistribute or monetize downloaded content."},
        {"question": "Do I need a Google or YouTube account?", "answer": "No — our tool works completely without any account or login on YouTube or our site."},
        {"question": "What format are YouTube downloads?", "answer": "Videos download as MP4 files compatible with all devices. Audio extracts as M4A/AAC format."},
        {"question": "Is there a video length limit?", "answer": "We support videos up to 2 hours in length for most content types."},
    ],
    "Facebook": [
        {"question": "Do I need to log in to Facebook to download videos?", "answer": "No — our tool downloads public Facebook videos without requiring any Facebook account or login."},
        {"question": "Can I download Facebook Reels?", "answer": "Yes — Facebook Reels are fully supported. Paste the Reel link and download in HD quality without watermark."},
        {"question": "Can I download Facebook Live recordings?", "answer": "Yes — if a Facebook Live stream has been saved as a public post after ending, it can be downloaded like any other Facebook video."},
        {"question": "Why did my Facebook video download fail?", "answer": "The most common reason is that the video is from a private profile or private group. Our tool only supports publicly accessible content."},
        {"question": "What quality are Facebook video downloads?", "answer": "Facebook videos typically download in HD (720p) or SD (480p) depending on the original upload quality. We always offer the highest available quality."},
        {"question": "Does Facebook notify when I download a video?", "answer": "No — Facebook does not notify content owners when their public videos are downloaded via third-party tools."},
        {"question": "Are Facebook video downloads free?", "answer": "Yes — completely free with no daily limits, no signup, and no hidden charges."},
    ],
    "Twitter (X)": [
        {"question": "Does this work for X.com links as well as Twitter links?", "answer": "Yes — both twitter.com and x.com links work identically with our downloader."},
        {"question": "Can I download GIFs from X (Twitter)?", "answer": "Yes — animated GIFs from X posts download as MP4 video files, compatible with all devices."},
        {"question": "Can I download from private X accounts?", "answer": "No — only content from public X accounts is supported."},
        {"question": "What quality are X (Twitter) video downloads?", "answer": "We download in the highest available quality from the original tweet — typically 720p or 1080p where available."},
        {"question": "Is it free to download X (Twitter) videos?", "answer": "Yes — completely free with no limits and no login required."},
        {"question": "Does the creator know I downloaded their X video?", "answer": "No — X does not notify creators when their public videos are downloaded via third-party tools."},
        {"question": "Can I download Twitter Spaces recordings?", "answer": "We support video tweets and GIFs. Twitter Spaces audio recordings are a different format and may not be supported."},
    ],
    "Multiple": [
        {"question": "Which platforms does this multi-platform downloader support?", "answer": "It supports Instagram, TikTok, YouTube, Facebook, Twitter/X, Pinterest, Snapchat, and more."},
        {"question": "Do I need different tools for different platforms?", "answer": "No — our universal downloader handles all major platforms in one tool. Paste any supported link and it works automatically."},
        {"question": "Is it free for all platforms?", "answer": "Yes — completely free for all supported platforms with no daily limits and no account required."},
        {"question": "Does it work without logging in to any platform?", "answer": "Yes — no login to any social media platform is needed. Just paste the public link and download."},
        {"question": "Do downloaded videos have watermarks?", "answer": "No — our tool delivers clean watermark-free video files from all supported platforms."},
        {"question": "What video quality can I expect?", "answer": "We always fetch the highest available quality from the platform — typically HD (720p or 1080p). YouTube supports up to 4K."},
        {"question": "Can I download from private accounts on any platform?", "answer": "No — only publicly accessible content is supported across all platforms. Private content is protected."},
    ],
}


def _make_page(path, platform, keyword, action, modifier, tool_name, extra_desc="", lang="en"):
    """Generate a complete SEO page dict with unique content and canonical tags."""

    t_action = _translate(action, lang)
    t_modifier = _translate(modifier, lang)

    # ✅ FIX 3: Smart title truncation — no mid-word cuts
    raw_title = f"{t_action} {keyword} {t_modifier} — Free {tool_name}".strip().replace("  ", " ")
    title = _smart_truncate(raw_title, 60)

    desc_raw = f"{t_action} {keyword} {t_modifier} for free. {extra_desc} No login, no watermark, works on Android, iPhone & PC."
    description = _smart_truncate(desc_raw.strip().replace("  ", " "), 160)

    h1 = f"{t_action} {keyword} {t_modifier}".strip().replace("  ", " ")
    subtitle = f"Free Online {tool_name} — Fast, HD Quality, No Login Required"

    # ✅ FIX 1: Platform-specific unique intro
    intro_template = PLATFORM_INTROS.get(platform, PLATFORM_INTROS["Multiple"])
    intro_text = intro_template.format(
        tool_name=tool_name,
        action_lower=action.lower(),
        keyword_lower=keyword.lower(),
        extra_desc=extra_desc
    )

    steps = [
        {"title": f"Copy the {platform} Link", "desc": f"Open the {platform} app or website. Find the content you want to save. Tap Share and select 'Copy Link'."},
        {"title": "Paste the URL", "desc": "Visit SnapReelDownload and paste the copied link into the input box above."},
        {"title": f"Download in HD", "desc": f"Click Download. Select your preferred quality and save the {keyword.lower()} to your device instantly."}
    ]

    features = [
        {"title": "100% Free & Unlimited", "desc": "No hidden charges, no subscription, no daily limits on downloads."},
        {"title": "HD Quality", "desc": f"Download {keyword.lower()} in original high-definition quality — no compression added."},
        {"title": "No Watermark", "desc": "Get clean video files without any platform logos or overlays."},
        {"title": "No Login Required", "desc": f"No {platform} account needed. Your account stays completely safe."},
        {"title": "All Devices Supported", "desc": "Works on Android, iPhone, iPad, Windows, Mac — any modern browser."},
        {"title": "Secure & Private", "desc": "SSL encrypted. We never store your data, downloads, or history."}
    ]

    # ✅ FIX 4: Platform-specific FAQs
    faqs = PLATFORM_FAQS.get(platform, PLATFORM_FAQS["Multiple"])

    # ✅ FIX 2: Canonical + hreflang fields
    base_domain = "https://snapreeldownload.com"
    # English version is canonical for all language variants
    english_path = path.replace(f"/{lang}/", "/") if lang != "en" else path
    canonical = f"{base_domain}{english_path}"

    # Build hreflang map
    hreflang_map = {}
    for supported_lang in SUPPORTED_LANGUAGES:
        if supported_lang == "en":
            hreflang_map[supported_lang] = f"{base_domain}{english_path}"
        else:
            hreflang_map[supported_lang] = f"{base_domain}/{supported_lang}{english_path}"

    return {
        "title": title,
        "description": description,
        "h1": h1,
        "subtitle": subtitle,
        "tool_name": tool_name,
        "intro_text": intro_text,
        "keyword": keyword.lower(),
        "platform": platform,
        "steps": steps,
        "features": features,
        "faqs": faqs,
        "lang": lang,
        # ✅ FIX 2: Canonical and hreflang
        "canonical": canonical,
        "hreflang": hreflang_map,
    }


def _make_device_page(path, platform, keyword, action, modifier, device_tip, lang="en"):
    """Generate device-specific page with canonical + unique device intro."""
    tool_name_base = keyword.split(" on ")[0] if " on " in keyword else keyword
    page = _make_page(path, platform, keyword, action, modifier,
                      f"{tool_name_base} Downloader",
                      device_tip, lang=lang)

    # Override intro with device-specific content (still platform-aware)
    device_name = keyword.split(" on ")[-1] if " on " in keyword else "your device"
    page["intro_text"] = f"""
    <p>Want to <strong>{action.lower()} {keyword.lower()}</strong>? You are in the right place.
    {device_tip} No app installation needed — everything runs directly in your browser.</p>
    <p>Our tool is specifically optimized for {device_name} users — fast loading, smooth downloads,
    and HD quality files saved directly to your device storage. Just copy the {platform} link,
    paste it above, and tap Download.</p>
    <p><strong>Why use a web tool instead of an app?</strong> Web tools require zero installation,
    request no device permissions, and always stay up to date automatically. Your device and
    your data stay completely safe.</p>
    """
    return page


# ── Keyword Variation Pages ──────────────────────────────────────────────────
KEYWORD_PAGES_CONFIG = [
    # Instagram Reels variations
    ("/download-instagram-reels",                  "Instagram", "Instagram Reels",                    "Download", "",        "Instagram Reels Downloader",     "Save your favorite Reels without watermark."),
    ("/download-instagram-reels-online",           "Instagram", "Instagram Reels",                    "Download", "Online",  "Instagram Reels Downloader",     "No software needed — works in your browser."),
    ("/download-instagram-reels-hd",               "Instagram", "Instagram Reels HD",                 "Download", "in HD",   "Instagram Reels HD Downloader",  "Get crystal clear 1080p quality."),
    ("/instagram-reel-downloader-free",            "Instagram", "Instagram Reels",                    "Download", "Free",    "Free Instagram Reel Downloader", "Zero cost, unlimited downloads."),
    ("/save-instagram-video-online",               "Instagram", "Instagram Videos",                   "Save",     "Online",  "Instagram Video Saver",          "Archive your favorite posts offline."),
    ("/best-instagram-reel-downloader",            "Instagram", "Instagram Reels",                    "Download", "",        "Best Instagram Reel Downloader", "Rated #1 by users for speed and quality."),
    ("/instagram-video-download-tool",             "Instagram", "Instagram Videos",                   "Download", "",        "Instagram Video Download Tool",  "A powerful tool for all Instagram content."),
    ("/instagram-reel-saver",                      "Instagram", "Instagram Reels",                    "Save",     "",        "Instagram Reel Saver",           "Save Reels to your gallery instantly."),
    ("/instagram-reel-to-mp4",                     "Instagram", "Instagram Reels",                    "Convert",  "to MP4",  "Instagram Reel to MP4",          "Get universal MP4 format files."),
    ("/instagram-video-saver-online",              "Instagram", "Instagram Videos",                   "Save",     "Online",  "Online Instagram Video Saver",   "Works on any device, any browser."),
    ("/free-instagram-video-downloader",           "Instagram", "Instagram Videos",                   "Download", "Free",    "Free Instagram Video Downloader","No registration, no payments ever."),
    ("/download-instagram-reels-without-watermark","Instagram", "Instagram Reels Without Watermark",  "Download", "",        "Instagram Reels Downloader",     "Get clean videos without any logos."),
    ("/story-saver",                               "Instagram", "Instagram Stories",                  "Download", "",        "Instagram Story Saver",          "Save stories before they disappear in 24 hours."),
    ("/igtv",                                      "Instagram", "Instagram IGTV",                     "Download", "",        "IGTV Downloader",                "Download long-form IGTV videos offline."),
    ("/carousel",                                  "Instagram", "Instagram Carousel",                 "Download", "",        "Carousel Downloader",            "Download multiple photos/videos from one post."),
    ("/instagram-photo-downloader",                "Instagram", "Instagram Photos",                   "Download", "in HD",   "Instagram Photo Downloader",     "Save high-quality images from any public post."),
    ("/instagram-anonymously-viewer",              "Instagram", "Instagram Stories",                  "View",     "Anonymously", "Anonymous Story Viewer",     "Watch and download stories without them knowing."),
    ("/instagram-highlights-downloader",           "Instagram", "Instagram Highlights",               "Download", "",        "Highlights Downloader",          "Save full profile highlights covers and videos."),
    # YouTube variations
    ("/download-youtube-video-online",             "YouTube",   "YouTube Videos",                     "Download", "Online",  "Online YouTube Video Downloader","Save any public YouTube video."),
    ("/youtube-video-downloader-free",             "YouTube",   "YouTube Videos",                     "Download", "Free",    "Free YouTube Video Downloader",  "No cost, no limits, no ads."),
    ("/youtube-to-mp4-converter",                  "YouTube",   "YouTube Videos",                     "Convert",  "to MP4",  "YouTube to MP4 Converter",       "Get MP4 files for any device."),
    ("/save-youtube-videos-online",                "YouTube",   "YouTube Videos",                     "Save",     "Online",  "Online YouTube Video Saver",     "Build your offline video library."),
    ("/best-youtube-downloader",                   "YouTube",   "YouTube Videos",                     "Download", "",        "Best YouTube Downloader",        "Fast, reliable, supports 4K quality."),
    # TikTok variations
    ("/download-tiktok-video-online",              "TikTok",    "TikTok Videos",                      "Download", "Online",  "Online TikTok Video Downloader", "Remove watermark automatically."),
    ("/tiktok-downloader-without-watermark",       "TikTok",    "TikTok Videos Without Watermark",    "Download", "",        "TikTok Downloader No Watermark", "Clean videos without the bouncing logo."),
    ("/save-tiktok-videos-free",                   "TikTok",    "TikTok Videos",                      "Save",     "Free",    "Free TikTok Video Saver",        "Unlimited free downloads."),
    ("/tiktok-video-saver",                        "TikTok",    "TikTok Videos",                      "Save",     "",        "TikTok Video Saver",             "Archive your favorite TikToks."),
    # Facebook variations
    ("/download-facebook-video-online",            "Facebook",  "Facebook Videos",                    "Download", "Online",  "Online Facebook Video Downloader","Save FB videos and Reels."),
    ("/facebook-video-downloader-free",            "Facebook",  "Facebook Videos",                    "Download", "Free",    "Free Facebook Video Downloader", "No login to Facebook required."),
    ("/save-facebook-videos",                      "Facebook",  "Facebook Videos",                    "Save",     "Online",  "Facebook Video Saver",           "Keep videos from your feed."),
    # Twitter/X variations
    ("/download-twitter-video-online",             "Twitter (X)","Twitter Videos",                    "Download", "Online",  "Online Twitter Video Downloader","Works with twitter.com and x.com links."),
    ("/save-twitter-videos-free",                  "Twitter (X)","Twitter Videos",                    "Save",     "Free",    "Free Twitter Video Saver",       "Save tweets with video instantly."),
    ("/x-video-saver",                             "Twitter (X)","X (Twitter) Videos",                "Save",     "",        "X Video Saver",                  "Download from X.com in HD."),
    # General / multi-platform
    ("/social-media-video-downloader",             "Multiple",  "Social Media Videos",                "Download", "",        "Social Media Video Downloader",  "One tool for Instagram, TikTok, YouTube, Facebook & Twitter."),
    ("/online-video-downloader-free",              "Multiple",  "Online Videos",                      "Download", "Free",    "Free Online Video Downloader",   "Universal downloader for all platforms."),
    ("/video-downloader-no-watermark",             "Multiple",  "Videos Without Watermark",           "Download", "",        "Video Downloader No Watermark",  "Clean downloads from any platform."),
    ("/hd-video-downloader-online",                "Multiple",  "HD Videos",                          "Download", "Online",  "HD Video Downloader",            "Always get the highest available quality."),
    ("/reels-downloader",                          "Instagram", "Reels",                              "Download", "",        "Reels Downloader",               "The fastest way to save Reels."),
]

# ── Device-Specific Pages ────────────────────────────────────────────────────
DEVICE_PAGES_CONFIG = [
    ("/download-instagram-reels-iphone",    "Instagram",   "Instagram Reels on iPhone",        "Download", "", "Use Safari to paste the link and save Reels directly to your Photos app."),
    ("/download-instagram-reels-android",   "Instagram",   "Instagram Reels on Android",       "Download", "", "Use Chrome — the video saves straight to your Downloads folder."),
    ("/download-instagram-reels-pc",        "Instagram",   "Instagram Reels on PC",            "Download", "", "Copy the URL from your desktop browser and download the MP4 file."),
    ("/instagram-video-downloader-chrome",  "Instagram",   "Instagram Videos via Chrome",      "Download", "", "Works perfectly with Google Chrome on any OS."),
    ("/instagram-video-downloader-mobile",  "Instagram",   "Instagram Videos on Mobile",       "Download", "", "Optimized for mobile browsers — fast and responsive."),
    ("/instagram-reel-downloader-iphone",   "Instagram",   "Instagram Reels on iPhone",        "Download", "", "Save Reels to your iPhone camera roll in seconds."),
    ("/instagram-reel-downloader-android",  "Instagram",   "Instagram Reels on Android",       "Download", "", "Download Reels to your Android gallery instantly."),
    ("/instagram-downloader-safari",        "Instagram",   "Instagram Videos via Safari",      "Download", "", "Fully compatible with Safari on iPhone, iPad, and Mac."),
    ("/instagram-downloader-firefox",       "Instagram",   "Instagram Videos via Firefox",     "Download", "", "Works seamlessly with Firefox on all platforms."),
    ("/download-tiktok-videos-iphone",      "TikTok",      "TikTok Videos on iPhone",          "Download", "", "Save TikToks directly to your iPhone Photos app via Safari."),
    ("/download-tiktok-videos-android",     "TikTok",      "TikTok Videos on Android",         "Download", "", "Download TikToks to your Android phone in HD via Chrome."),
    ("/download-tiktok-videos-pc",          "TikTok",      "TikTok Videos on PC",              "Download", "", "Save TikTok content directly to your computer."),
    ("/youtube-video-downloader-mobile",    "YouTube",     "YouTube Videos on Mobile",         "Download", "", "Save YouTube videos on your phone for offline viewing."),
    ("/youtube-video-downloader-pc",        "YouTube",     "YouTube Videos on PC",             "Download", "", "Download YouTube videos to your desktop in 4K quality."),
    ("/youtube-downloader-for-mac",         "YouTube",     "YouTube Videos on Mac",            "Download", "", "Compatible with Safari and Chrome on macOS."),
    ("/download-facebook-videos-iphone",    "Facebook",    "Facebook Videos on iPhone",        "Download", "", "Copy the FB link and save to your iPhone camera roll."),
    ("/download-facebook-videos-android",   "Facebook",    "Facebook Videos on Android",       "Download", "", "Works with Chrome, Firefox, and Samsung Internet on Android."),
    ("/download-twitter-videos-iphone",     "Twitter (X)", "Twitter Videos on iPhone",         "Download", "", "Save tweet videos to your iPhone Photos app via Safari."),
    ("/download-twitter-videos-android",    "Twitter (X)", "Twitter Videos on Android",        "Download", "", "Download X/Twitter videos to your Android gallery via Chrome."),
    ("/video-downloader-for-windows",       "Multiple",    "Videos on Windows PC",             "Download", "", "Download social media videos on Windows 10 and 11 — any browser."),
]


def generate_all_programmatic_pages():
    """Generate all 350+ programmatic SEO pages across 7 languages."""
    pages = {}

    for lang in SUPPORTED_LANGUAGES:
        lang_prefix = f"/{lang}" if lang != "en" else ""

        for config in KEYWORD_PAGES_CONFIG:
            path, platform, keyword, action, modifier, tool_name, extra = config
            full_path = f"{lang_prefix}{path}"
            pages[full_path] = _make_page(full_path, platform, keyword, action, modifier, tool_name, extra, lang=lang)

        for config in DEVICE_PAGES_CONFIG:
            path, platform, keyword, action, modifier, device_tip = config
            full_path = f"{lang_prefix}{path}"
            pages[full_path] = _make_device_page(full_path, platform, keyword, action, modifier, device_tip, lang=lang)

    return pages


PROGRAMMATIC_PAGES = generate_all_programmatic_pages()
