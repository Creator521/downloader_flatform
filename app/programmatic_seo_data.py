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
    <p>Instagram is packed with creative videos, stunning Reels, inspiring stories, and beautiful photos — but the app doesn't offer a built-in way to save most of this content directly to your device. Whether you want to watch your favorite creator's Reel offline, save a recipe before it disappears, or keep a funny clip to share on WhatsApp without sending a link, you need a reliable <strong>{tool_name}</strong>.</p>
    
    <h3>What are Instagram Reels and Why Download Them?</h3>
    <p>Instagram Reels are short, entertaining videos that have become the core of Instagram's platform. They feature everything from educational tutorials to trending dances and comedy sketches. Since the Instagram algorithm keeps refreshing your feed, finding a specific video later can be very difficult. That's why users prefer to <strong>{action_lower} {keyword_lower}</strong> straight to their phone memory.</p>

    <h3>How Our Tool Helps You</h3>
    <p>Our free online tool lets you <strong>{action_lower} {keyword_lower}</strong> directly to your phone or computer in HD quality. Unlike screen recording, which lowers quality and captures UI elements, our service fetches the original MP4 file. No app installation, no login to Instagram required, and absolutely no watermark on the downloaded file. {extra_desc}</p>
    
    <p>Compatible with all operating systems: Android, iPhone (iOS), iPad, Windows PC, and Mac — any browser, any device. Just copy, paste, and save.</p>
    """,
    "TikTok": """
    <p>TikTok videos are some of the most creative, entertaining, and shareable content on the internet — but the platform's built-in download option adds an unavoidable, bouncing watermark with the creator's username. For personal archives, video editing projects, or simply a clean viewing experience, that watermark is a significant problem.</p>
    
    <h3>Why Use a TikTok Downloader Without Watermark?</h3>
    <p>When you download directly from the app, the quality is often compressed, and the logo covers important parts of the video. Our <strong>{tool_name}</strong> removes the TikTok watermark automatically and fetches the highest available resolution from the TikTok servers. Whether it's a makeup tutorial, a dance trend, or a cooking lifehack, you'll get it in pristine condition.</p>

    <h3>Fast, Free, and Secure</h3>
    <p>With our service, you can <strong>{action_lower} {keyword_lower}</strong> in original HD quality instantly. It is completely free, does not require you to log into your TikTok account, and works natively in any web browser. {extra_desc} We prioritize your privacy and do not keep logs of your downloads.</p>
    
    <p>Compatible with all Android phones, iPhones, iPads, Windows, and Mac — no extra apps or software needed. Experience the fastest download speeds today.</p>
    """,
    "YouTube": """
    <p>YouTube hosts over billions of videos covering every topic imaginable — detailed tutorials, music videos, documentaries, educational courses, and podcasts. But streaming these videos requires a constant, fast internet connection and burns through your mobile data plan. Saving YouTube videos for offline viewing makes perfect sense for daily commuters, travelers, students, and anyone on a limited data plan.</p>
    
    <h3>The Ultimate Solution for Offline Viewing</h3>
    <p>Our free <strong>{tool_name}</strong> lets you safely and quickly <strong>{action_lower} {keyword_lower}</strong> in HD 720p, 1080p, or even 4K quality where available. You can also extract audio-only formats if you just want to listen to music or a podcast. There is no software to install on your computer, no Google account signup needed, and absolutely no daily limitations.</p>
    
    <h3>Why We Stand Out</h3>
    <p>We provide original, uncompressed files at blazing fast speeds. {extra_desc} Whether you want to back up a fragile video that might get deleted or prepare a playlist for a flight, we have you covered.</p>
    
    <p>Works seamlessly on Android smartphones, iPhone (via Safari), Windows laptops, Mac computers, and any modern internet browser.</p>
    """,
    "Facebook": """
    <p>Facebook hosts billions of videos on its platform — from breaking news clips and cooking tutorials to funny moments, sports highlights, and the newly popular Facebook Reels. But unlike some platforms, Facebook provides almost no native download option for most video types, leaving users frustrated when they want to save a memory or an interesting post.</p>
    
    <h3>Download Facebook Videos and Reels Instantly</h3>
    <p>Our <strong>{tool_name}</strong> is built to solve this exact problem. With just a copied link, you can <strong>{action_lower} {keyword_lower}</strong> in the highest available HD quality, completely free of charge. Whether it's from an open page, a public group, or a trending Reel, our extractor gets the direct video file for you.</p>

    <p>No Facebook login is required, ensuring your account remains 100% secure. There's no shady software to install — everything works instantly inside your web browser. {extra_desc} It's fast, anonymous, and incredibly easy to use.</p>
    
    <p>Fully supports Android, iPhone, iPad, Windows PC, and Mac operating systems.</p>
    """,
    "Twitter (X)": """
    <p>X (formerly known as Twitter) is the global hub for breaking news, viral sports moments, trending memes, and real-time event coverage — all usually shared in short, impactful video clips. But X provides no built-in download button for its media. Furthermore, links shared outside the platform often lose context, require logins to view, or simply stop working over time.</p>
    
    <h3>How to Save Videos from X (Twitter)?</h3>
    <p>Our <strong>{tool_name}</strong> lets you effortlessly <strong>{action_lower} {keyword_lower}</strong> directly to your device's local storage in crisp HD quality. You don't need an X account, you don't have to log in, and the entire process is completely free and anonymous. We fetch the pure MP4 file so you can share it natively on WhatsApp, Telegram, or keep it in your gallery.</p>
    
    <p>Our tool parses the tweet URL instantly and extracts the highest resolution available. {extra_desc}</p>
    
    <p>Works powerfully on all devices: Android phones, iPhones, tablets, desktop PCs, and Mac systems.</p>
    """,
    "Multiple": """
    <p>In today's fast-paced social media landscape, great video content is spread across dozens of different platforms — Instagram, TikTok, YouTube, Facebook, Twitter (X), Pinterest, and Snapchat. Switching between multiple downloading apps or visiting five different websites to save videos from each platform is slow, clunky, and frustrating.</p>
    
    <h3>Your All-In-One Universal Video Saver</h3>
    <p>Our <strong>{tool_name}</strong> is a universal, all-in-one solution. You can seamlessly <strong>{action_lower} {keyword_lower}</strong> from virtually any major platform using one single, simple website. We provide clean, watermark-free files in the highest HD quality available.</p>
    
    <p>It is 100% free, requires no user registration, and works flawlessly in any web browser. We respect your privacy by processing links instantaneously without storing your download history. {extra_desc}</p>
    
    <p>Compatible with all mobile devices (Android/iOS) and desktop operating systems.</p>
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
        {"question": "Can I save Instagram Stories before they disappear?", "answer": "Absolutely. Just copy the link of the active story while it is still visible, paste it here, and you can download it as an MP4 directly to your device."},
        {"question": "What should I do if the video link doesn't work?", "answer": "First, ensure the profile is public. If it is, double-check that you copied the complete URL. Sometimes, Instagram temporarily blocks our servers; if so, try again in a few minutes."},
        {"question": "Is the downloaded video quality the same as the original?", "answer": "Yes. We do not compress or alter the video. You will receive the exact HD or original quality file that the creator uploaded to Instagram."},
        {"question": "Can I save videos directly to my iPhone camera roll?", "answer": "Yes. If you use Safari on iOS, tap 'Download', and it will go to your Safari Downloads manager. From there, you can click 'Save Video' to push it to your Camera Roll."},
        {"question": "Do you store any of my downloaded videos?", "answer": "No. We process the files strictly on the fly. We do not store, host, or keep a history of the videos you download, ensuring your absolute privacy."},
    ],
    "TikTok": [
        {"question": "Does the downloaded TikTok video have a watermark?", "answer": "No — our tool automatically removes the TikTok watermark and username overlay. You get a clean, professional-looking HD video file."},
        {"question": "Can I download TikTok videos if the creator disabled downloads?", "answer": "Yes — our tool works for all public TikTok videos regardless of whether the creator has disabled TikTok's built-in download feature."},
        {"question": "Can I download TikTok audio only as MP3?", "answer": "Yes! Use our TikTok to MP3 converter to extract just the audio track from any public TikTok video."},
        {"question": "Can I download from private TikTok accounts?", "answer": "No — we only support content from public TikTok accounts. Private account videos cannot be accessed by any third-party tool."},
        {"question": "Does TikTok notify the creator when I download their video?", "answer": "No — downloading via our tool is completely anonymous. The creator will not receive any notification."},
        {"question": "What quality are downloaded TikTok videos?", "answer": "Videos are downloaded in the original HD quality from TikTok's servers — typically 720p or 1080p depending on the original upload."},
        {"question": "Is there a daily limit on TikTok downloads?", "answer": "No — completely free and unlimited. Download as many TikTok videos as you want."},
        {"question": "Why does TikTok put watermarks on videos natively?", "answer": "TikTok adds watermarks to promote its platform and identify the original creator when videos are shared elsewhere. However, for personal editing, this can be intrusive."},
        {"question": "How do I find the TikTok link to copy?", "answer": "On the TikTok app, tap the 'Share' arrow icon on the right side of the video, then tap 'Copy Link'. Paste that link into our input box above."},
        {"question": "Can I save videos straight to my iPhone Photos app?", "answer": "Yes. Use Safari on your iPhone, hit download, and then use the Safari download manager to 'Save Video' directly to your Photos app."},
        {"question": "Do I need to install a standalone app?", "answer": "No app installation is required. SnapReelDownload runs entirely in your web browser, making it safer and saving your device's storage space."},
        {"question": "Does downloading work on my Windows PC or Mac?", "answer": "Yes, it works perfectly on desktop. Just open TikTok in your web browser, copy the URL from the address bar, and paste it here."},
    ],
    "YouTube": [
        {"question": "Can I download YouTube videos in 4K quality?", "answer": "Yes — when the creator uploads in 4K, our tool will offer 4K download options. Most videos are available in HD (720p/1080p)."},
        {"question": "Can I download YouTube Shorts with this tool?", "answer": "Yes — paste a Shorts URL (youtube.com/shorts/...) and it works exactly like regular YouTube videos."},
        {"question": "Can I extract audio from YouTube videos as MP3?", "answer": "Yes! Use our YouTube to MP3 converter to extract and download just the audio track."},
        {"question": "Is it legal to download YouTube videos?", "answer": "YouTube's Terms of Service restrict downloading without permission. Download only for personal offline viewing. Never redistribute or monetize downloaded content."},
        {"question": "Do I need a Google or YouTube account?", "answer": "No — our tool works completely without any account or login on YouTube or our site."},
        {"question": "What format are YouTube downloads?", "answer": "Videos download as MP4 files compatible with all devices. Audio extracts as M4A/AAC format."},
        {"question": "Is there a video length limit?", "answer": "We support videos up to 2 hours in length for most content types."},
        {"question": "Can I download entire YouTube playlists at once?", "answer": "Currently, we process one video at a time to ensure the highest quality and fastest speed. You'll need to insert individual video links."},
        {"question": "Are YouTube Live streams supported?", "answer": "You can download live streams only after they have securely ended and YouTube has processed them into regular VOD (Video on Demand) posts."},
        {"question": "Why is my 4K video downloading slowly?", "answer": "4K files are massive (often gigabytes in size). While our servers are fast, the download time will largely depend on your own internet connection speed."},
        {"question": "Is it safe to use this downloader on my computer?", "answer": "100% safe. We don't require you to download any sketchy executable software. You just receive a clean `.mp4` media file."},
        {"question": "Does it work on Android phones natively?", "answer": "Yes. Using Chrome on Android, simply tap download, and the MP4 video will be permanently saved to your 'Downloads' folder or gallery."},
    ],
    "Facebook": [
        {"question": "Do I need to log in to Facebook to download videos?", "answer": "No — our tool downloads public Facebook videos without requiring any Facebook account or login."},
        {"question": "Can I download Facebook Reels?", "answer": "Yes — Facebook Reels are fully supported. Paste the Reel link and download in HD quality without watermark."},
        {"question": "Can I download Facebook Live recordings?", "answer": "Yes — if a Facebook Live stream has been saved as a public post after ending, it can be downloaded like any other Facebook video."},
        {"question": "Why did my Facebook video download fail?", "answer": "The most common reason is that the video is from a private profile or private group. Our tool only supports publicly accessible content."},
        {"question": "What quality are Facebook video downloads?", "answer": "Facebook videos typically download in HD (720p) or SD (480p) depending on the original upload quality. We always offer the highest available quality."},
        {"question": "Does Facebook notify when I download a video?", "answer": "No — Facebook does not notify content owners when their public videos are downloaded via third-party tools."},
        {"question": "Are Facebook video downloads free?", "answer": "Yes — completely free with no daily limits, no signup, and no hidden charges."},
        {"question": "How do I get the correct link for a Facebook video?", "answer": "On a computer, click the video's timestamp or right-click to 'Copy link address'. On mobile, tap the 'Share' button and select 'Copy Link'."},
        {"question": "Can I download Facebook Stories?", "answer": "Yes, as long as the story is from a public profile or page, you can copy its link and download the short video or image."},
        {"question": "Why am I getting a 'Private Video' error?", "answer": "Unlike other tools, we do not bypass Facebook's privacy settings. If a user sets their video to 'Friends Only', our servers cannot access it."},
        {"question": "Will the downloaded MP4 video play on my phone?", "answer": "Absolutely. MP4 is the universal standard for digital video and will play natively on Android, iOS, Windows, and Mac players."},
        {"question": "Do you keep a copy of the downloaded Facebook videos?", "answer": "Never. Files are passed directly from Facebook's servers to your device. We do not store any media files on our infrastructure."},
    ],
    "Twitter (X)": [
        {"question": "Does this work for X.com links as well as Twitter links?", "answer": "Yes — both twitter.com and x.com links work identically with our downloader."},
        {"question": "Can I download GIFs from X (Twitter)?", "answer": "Yes — animated GIFs from X posts download as MP4 video files, compatible with all devices."},
        {"question": "Can I download from private X accounts?", "answer": "No — only content from public X accounts is supported."},
        {"question": "What quality are X (Twitter) video downloads?", "answer": "We download in the highest available quality from the original tweet — typically 720p or 1080p where available."},
        {"question": "Is it free to download X (Twitter) videos?", "answer": "Yes — completely free with no limits and no login required."},
        {"question": "Does the creator know I downloaded their X video?", "answer": "No — X does not notify creators when their public videos are downloaded via third-party tools."},
        {"question": "Can I download Twitter Spaces recordings?", "answer": "We support video tweets and GIFs. Twitter Spaces audio recordings are a different format and may not be supported."},
        {"question": "How do I copy a X/Twitter URL effectively?", "answer": "Tap the 'Share' icon (arrow or nodes) right below the tweet and select 'Copy Link'. If on desktop, you can also copy the URL directly from the address browser bar."},
        {"question": "What happens to the video quality when I download?", "answer": "We grab the exact master file that X hosts on its CDN. It won't lose quality during the download process."},
        {"question": "Can I download videos from a protected tweet?", "answer": "No. If a user's account has a padlock icon (protected tweets), their content is hidden from our servers."},
        {"question": "Do I need to pay for multiple downloads?", "answer": "No, whether you download 1 video or 100 videos, our service remains entirely free indefinitely."},
        {"question": "Does downloading X videos require a browser extension?", "answer": "Not at all. The entire system works purely on the web. Paste the link and click download."},
    ],
    "Multiple": [
        {"question": "Which platforms does this multi-platform downloader support?", "answer": "It supports Instagram, TikTok, YouTube, Facebook, Twitter/X, Pinterest, Snapchat, and more."},
        {"question": "Do I need different tools for different platforms?", "answer": "No — our universal downloader handles all major platforms in one tool. Paste any supported link and it works automatically."},
        {"question": "Is it free for all platforms?", "answer": "Yes — completely free for all supported platforms with no daily limits and no account required."},
        {"question": "Does it work without logging in to any platform?", "answer": "Yes — no login to any social media platform is needed. Just paste the public link and download."},
        {"question": "Do downloaded videos have watermarks?", "answer": "No — our tool delivers clean watermark-free video files from all supported platforms."},
        {"question": "What video quality can I expect?", "answer": "We always fetch the highest available quality from the platform — typically HD (720p or 1080p). YouTube supports up to 4K."},
        {"question": "Can I download from private accounts on any platform?", "answer": "No — only publicly accessible content is supported across all platforms. Private content is protected."},
        {"question": "What is the difference between MP4 and MP3 options?", "answer": "MP4 files include both the video visuals and the audio, making it perfect for watching. MP3 files strip away the video, giving you an audio-only file, which is great for music or podcast listening."},
        {"question": "Why choose SnapReelDownload over other tools?", "answer": "SnapReelDownload combines speed, privacy, and an ad-light experience. While other sites force pop-ups or require sign-ups, we offer a fast, clean, and universally compatible tool for free."},
        {"question": "Is downloading videos safe for my device?", "answer": "Yes! Because you only download a `.mp4` or `.m4a` media file (and no `.exe` or `.apk` apps), your device remains safe from viruses and malware."},
        {"question": "Can I use this downloader on an iPad?", "answer": "Absolutely. Just open Safari on your iPad, paste the link, and save it directly to your iPad's file manager or Photos app."},
        {"question": "Do I need to clear cookies or cache to fix download errors?", "answer": "Usually, no. If a download fails, it's typically because the source video was deleted or set to private. Simply hard refreshing the page is often enough."},
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

    # ✅ FIX 5: Prevent Duplicate Content mapping by Google
    if lang != "en":
        faqs = []
        intro_text = f"<p><strong>{t_action} {keyword} {t_modifier}</strong> — {t_action} {keyword.lower()} {t_modifier}.</p>"
        steps = [
            {"title": "1", "desc": f"Copy {platform} URL."},
            {"title": "2", "desc": "Paste URL."},
            {"title": "3", "desc": "Download."}
        ]
        features = features[:2]

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
