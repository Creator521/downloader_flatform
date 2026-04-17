# app/multilingual_data.py
import copy
try:
    from app.seo_data import SEO_PAGES          # type: ignore
    from app.programmatic_seo_data import PROGRAMMATIC_PAGES  # type: ignore
except ImportError:
    from seo_data import SEO_PAGES              # type: ignore
    from programmatic_seo_data import PROGRAMMATIC_PAGES      # type: ignore

SUPPORTED_LANGUAGES = [
    "en", "hi", "es", "fr", "de", "pt", "ar", "id",
    "bn", "tr", "th", "ko", "ja", "uk", "pl"
]

# Core translated keywords per language
T = {
    "en": {"dw": "Download", "on": "Online", "fr": "Free", "dl": "Downloader", "vid": "Video", "ph": "Photo", "st": "Story", "rl": "Reels", "step1": "Step 1: Copy Link", "step2": "Step 2: Paste URL", "step3": "Step 3: Download", "title_suffix": "SnapReelDownload"},
    "hi": {"dw": "डाउनलोड", "on": "ऑनलाइन", "fr": "मुफ्त", "dl": "डाउनलोडर", "vid": "वीडियो", "ph": "फोटो", "st": "स्टोरी", "rl": "रील्स", "step1": "स्टेप 1: लिंक कॉपी करें", "step2": "स्टेप 2: URL पेस्ट करें", "step3": "स्टेप 3: डाउनलोड करें", "title_suffix": "SnapReelDownload"},
    "es": {"dw": "Descargar", "on": "en línea", "fr": "Gratis", "dl": "Descargador", "vid": "Video", "ph": "Foto", "st": "Historia", "rl": "Reels", "step1": "Paso 1: Copiar enlace", "step2": "Paso 2: Pegar URL", "step3": "Paso 3: Descargar", "title_suffix": "SnapReelDownload"},
    "fr": {"dw": "Télécharger", "on": "en ligne", "fr": "Gratuit", "dl": "Téléchargeur", "vid": "Vidéo", "ph": "Photo", "st": "Story", "rl": "Reels", "step1": "Étape 1: Copier le lien", "step2": "Étape 2: Coller l'URL", "step3": "Étape 3: Télécharger", "title_suffix": "SnapReelDownload"},
    "de": {"dw": "Herunterladen", "on": "Online", "fr": "Kostenlos", "dl": "Downloader", "vid": "Video", "ph": "Foto", "st": "Story", "rl": "Reels", "step1": "Schritt 1: Link kopieren", "step2": "Schritt 2: URL einfügen", "step3": "Schritt 3: Herunterladen", "title_suffix": "SnapReelDownload"},
    "pt": {"dw": "Baixar", "on": "Online", "fr": "Grátis", "dl": "Baixador", "vid": "Vídeo", "ph": "Foto", "st": "Story", "rl": "Reels", "step1": "Passo 1: Copiar link", "step2": "Passo 2: Colar URL", "step3": "Passo 3: Baixar", "title_suffix": "SnapReelDownload"},
    "ar": {"dw": "تحميل", "on": "عبر الانترنت", "fr": "مجاني", "dl": "محمل", "vid": "فيديو", "ph": "صورة", "st": "قصة", "rl": "ريلز", "step1": "الخطوة 1: انسخ الرابط", "step2": "الخطوة 2: الصق الرابط", "step3": "الخطوة 3: تحميل", "title_suffix": "SnapReelDownload"},
    "id": {"dw": "Unduh", "on": "Online", "fr": "Gratis", "dl": "Pengunduh", "vid": "Video", "ph": "Foto", "st": "Cerita", "rl": "Reels", "step1": "Langkah 1: Salin Tautan", "step2": "Langkah 2: Tempel URL", "step3": "Langkah 3: Unduh", "title_suffix": "SnapReelDownload"},
    "bn": {"dw": "ডাউনলোড", "on": "অনলাইন", "fr": "বিনামূল্যে", "dl": "ডাউনলোডার", "vid": "ভিডিও", "ph": "ছবি", "st": "গল্প", "rl": "রিলস", "step1": "ধাপ ১: লিঙ্ক কপি করুন", "step2": "ধাপ ২: URL পেস্ট করুন", "step3": "ধাপ ৩: ডাউনলোড করুন", "title_suffix": "SnapReelDownload"},
    "tr": {"dw": "İndir", "on": "Çevrimiçi", "fr": "Ücretsiz", "dl": "İndirici", "vid": "Video", "ph": "Fotoğraf", "st": "Hikaye", "rl": "Reels", "step1": "Adım 1: Bağlantıyı Kopyala", "step2": "Adım 2: URL'yi Yapıştır", "step3": "Adım 3: İndir", "title_suffix": "SnapReelDownload"},
    "th": {"dw": "ดาวน์โหลด", "on": "ออนไลน์", "fr": "ฟรี", "dl": "เครื่องมือดาวน์โหลด", "vid": "วิดีโอ", "ph": "รูปภาพ", "st": "สตอรี่", "rl": "Reels", "step1": "ขั้นตอนที่ 1: คัดลอกลิงก์", "step2": "ขั้นตอนที่ 2: วาง URL", "step3": "ขั้นตอนที่ 3: ดาวน์โหลด", "title_suffix": "SnapReelDownload"},
    "ko": {"dw": "다운로드", "on": "온라인", "fr": "무료", "dl": "다운로더", "vid": "비디오", "ph": "사진", "st": "스토리", "rl": "릴스", "step1": "1단계: 링크 복사", "step2": "2단계: URL 붙여넣기", "step3": "3단계: 다운로드", "title_suffix": "SnapReelDownload"},
    "ja": {"dw": "ダウンロード", "on": "オンライン", "fr": "無料", "dl": "ダウンローダー", "vid": "動画", "ph": "写真", "st": "ストーリー", "rl": "リール", "step1": "ステップ1：リンクをコピー", "step2": "ステップ2：URLを貼り付け", "step3": "ステップ3：ダウンロード", "title_suffix": "SnapReelDownload"},
    "uk": {"dw": "Завантажити", "on": "онлайн", "fr": "Безкоштовно", "dl": "Завантажувач", "vid": "Відео", "ph": "Фото", "st": "Історія", "rl": "Reels", "step1": "Крок 1: Копіювати посилання", "step2": "Крок 2: Вставити URL", "step3": "Крок 3: Завантажити", "title_suffix": "SnapReelDownload"},
    "pl": {"dw": "Pobierz", "on": "Online", "fr": "Za darmo", "dl": "Pobieracz", "vid": "Wideo", "ph": "Zdjęcie", "st": "Relacja", "rl": "Reels", "step1": "Krok 1: Kopiuj link", "step2": "Krok 2: Wklej URL", "step3": "Krok 3: Pobierz", "title_suffix": "SnapReelDownload"},
}

# ✅ Reverted to original short URLs to prevent keyword stuffing
TOOLS = [
    # (path, platform, subject, target_content)
    ("/",                              "Any",         "Universal",        "vid"),
    ("/reels",                         "Instagram",   "Instagram",        "rl"),
    ("/video",                         "Instagram",   "Instagram",        "vid"),
    ("/photo",                         "Instagram",   "Instagram",        "ph"),
    ("/story",                         "Instagram",   "Instagram",        "st"),
    ("/youtube",                       "YouTube",     "YouTube",          "vid"),
    ("/tiktok",                        "TikTok",      "TikTok",           "vid"),
    ("/facebook",                      "Facebook",    "Facebook",         "vid"),
    ("/twitter",                       "Twitter (X)", "Twitter",          "vid"),
    ("/pinterest",                     "Pinterest",   "Pinterest",        "vid"),
    ("/snapchat",                      "Snapchat",    "Snapchat",         "vid"),
    ("/tiktok-mp3-downloader",         "TikTok",      "TikTok to MP3",    "vid"),
    ("/youtube-shorts-downloader",     "YouTube",     "YouTube Shorts",   "vid"),
    ("/youtube-to-mp3",                "YouTube",     "YouTube to MP3",   "vid"),
]


def make_page_data(path, platform, brand_name, content_key, lang):
    t = T.get(lang, T["en"])
    content_word = t.get(content_key, t.get("vid", "Video"))
    suffix = t["title_suffix"]

    if path == "/youtube-to-mp3":
        if lang == "hi":
            title = f'यूट्यूब से MP3 कनवर्टर ऑनलाइन मुफ्त | उच्च गुणवत्ता | {suffix}'
            desc   = f'यूट्यूब वीडियो को ऑनलाइन मुफ्त में MP3 में बदलें। 320kbps उच्च गुणवत्ता वाली MP3 फाइलें तुरंत डाउनलोड करें।'
        elif lang == "es":
            title = f'Convertidor de YouTube a MP3 gratis | Alta calidad | {suffix}'
            desc   = f'Convierte videos de YouTube a MP3 gratis en línea. Descarga archivos MP3 de alta calidad al instante.'
        else:
            title = f'YouTube to MP3 Converter Online Free | High Quality 320kbps | {suffix}'
            desc   = f'Convert YouTube videos to MP3 audio online for free. Download high-quality 320kbps MP3 files instantly.'
        h1        = f'YouTube to MP3 {t["dl"]}'
        tool_name = "YouTube to MP3"

    elif path == "/":
        if lang == "hi":
            title = f'{suffix} - मुफ्त ऑनलाइन वीडियो डाउनलोडर | Instagram, TikTok, YouTube'
            desc   = f'Instagram, TikTok, YouTube, Facebook और अन्य से वीडियो मुफ्त में डाउनलोड करें। बिना वॉटरमार्क के HD वीडियो सेव करें।'
        elif lang == "es":
            title = f'{suffix} - Descargador de videos en línea gratis | Instagram, TikTok'
            desc   = f'Descarga videos de Instagram, TikTok, YouTube y más gratis. Guarda videos HD sin marca de agua.'
        else:
            title = f'{suffix} - Free Online Video Downloader | Instagram, TikTok, YouTube'
            desc   = f'Download videos from Instagram, TikTok, YouTube, Facebook, Snapchat & more. Save HD quality videos online free.'
        h1        = f'Free Online {content_word} {t["dl"]}'
        tool_name = f'Universal {content_word} {t["dl"]}'

    else:
        if lang == "en":
            if brand_name == "TikTok":
                desc = f'Download TikTok videos without watermark in HD. Free TikTok video downloader online — fast, secure, unlimited.'
            elif brand_name == "Facebook":
                desc = f'Download Facebook videos online in HD. Free Facebook video downloader for Reels and public videos. No login.'
            elif brand_name == "YouTube Shorts":
                desc = f'Download YouTube Shorts free in HD. Save YouTube Shorts to gallery — no watermark, no login. Works on Android & iPhone.'
            else:
                desc = f'{t["dw"]} {brand_name} {content_word} in HD quality for {t["fr"]}. No watermark, no login. Fast & secure.'
        else:
            desc = f'{t["dw"]} {brand_name} {content_word} in HD quality for {t["fr"]}. No watermark, no login. Fast & secure.'

        title     = f'{t["dw"]} {brand_name} {content_word} HD {t["fr"]} {t["on"]} | {suffix}'
        h1        = f'{t["dw"]} {brand_name} {content_word}'
        tool_name = f'{brand_name} {content_word} {t["dl"]}'

    intro = f"<p><strong>{t['dw']} {brand_name} {content_word} {t['on']}</strong> — {t['fr']}, fast, no watermark, no login. Works on Android, iPhone & PC.</p>"

    steps = [
        {"title": t["step1"], "desc": f"Open {platform} and find the content. Tap Share and select Copy Link."},
        {"title": t["step2"], "desc": "Paste the copied link into the input box above."},
        {"title": t["step3"], "desc": f"Click Download and save the {content_word.lower()} to your device in HD."}
    ]

    features = [
        {"title": "HD Quality",          "desc": f"Download {brand_name} {content_word.lower()} in original high-definition quality."},
        {"title": "No Watermark",        "desc": "Get clean files without any platform logos or overlays."},
        {"title": "100% Free",           "desc": "No hidden charges, no subscription, unlimited downloads forever."},
        {"title": "No Login Required",   "desc": f"No {platform} account needed. Your account stays completely safe."},
        {"title": "All Devices",         "desc": "Works on Android, iPhone, iPad, Windows, Mac — any browser."},
    ]

    faqs = [
        {"question": f"Is this {tool_name} completely free to use?", "answer": "Yes, it is 100% free. There are no hidden fees, no subscriptions required, and no premium gates. You can download as many videos as you want at zero cost."},
        {"question": "Do I need to sign up or create an account?", "answer": "No — our platform works instantly. We do not require any signup, email registration, or login to any social media account, ensuring your data remains absolutely private."},
        {"question": "Can creators see that I downloaded their content?", "answer": "No. Your download activity is completely anonymous. The original creator is never notified when you fetch or save their public videos using our application."},
        {"question": "Is it legal to download social media videos?", "answer": "Yes, downloading videos for personal, offline viewing is generally acceptable. However, you should not use downloaded content for commercial purposes or upload it as your own without explicit permission from the creator."},
        {"question": "What video and audio formats can I download?", "answer": "Our tool primarily downloads videos in the universally compatible MP4 format. For audio extraction (like TikTok sounds or YouTube music), we provide secure M4A or MP3 files. These formats play flawlessly on virtually any modern device."},
        {"question": "Does this downloader work on an iPhone or iPad?", "answer": "Yes, absolutely. For Apple devices running iOS, simply use the Safari web browser. Paste your link, tap download, and use the native iOS file manager to save the video directly to your Photos app."},
        {"question": "How do I download videos on my Android phone?", "answer": "On any Android device, open your preferred browser (like Google Chrome, Firefox, or Samsung Internet), enter the video link, and tap download. The video will automatically save to your local 'Downloads' folder or gallery app."},
        {"question": "Is downloading safe for my device? Will I get a virus?", "answer": "Our service is completely safe and SSL encrypted. We provide direct media files (.mp4 or .m4a) without forcing you to download sketchy executable files (.exe) or applications. Your security is our top priority."},
        {"question": "Where are the downloaded videos saved on my PC or Mac?", "answer": "On desktop computers, downloaded files are typically saved to your system's default 'Downloads' folder. You can easily drag and drop these MP4 files into your preferred media player or video editor."},
        {"question": "Do you keep a copy of my downloaded files?", "answer": "No. We process the extraction links on the fly. We do not store, host, or archive the media files you download, nor do we track your download history."},
    ]

    # Shared rich content sections
    shared_extra = [
        {
            "title": "Download Format & Quality Comparison",
            "content": "<table style='width:100%; border-collapse:collapse; margin:20px 0;'><thead style='background:#f0f4ff;'><tr style='border-bottom:2px solid #667eea;'><th style='padding:12px; text-align:left;'>Format</th><th style='padding:12px; text-align:left;'>Type</th><th style='padding:12px; text-align:left;'>Quality</th><th style='padding:12px; text-align:left;'>Best For</th></tr></thead><tbody><tr style='border-bottom:1px solid #e2e8f0;'><td style='padding:12px;'><strong>MP4</strong></td><td style='padding:12px;'>Video</td><td style='padding:12px; color:#48bb78;'>HD / 4K</td><td style='padding:12px;'>Video with audio, editing</td></tr><tr><td style='padding:12px;'><strong>M4A</strong></td><td style='padding:12px;'>Audio Only</td><td style='padding:12px; color:#48bb78;'>320kbps</td><td style='padding:12px;'>Music, podcasts, audio</td></tr></tbody></table>"
        },
        {
            "title": "Device Compatibility Guide",
            "content": "<table style='width:100%; border-collapse:collapse; margin:20px 0;'><thead style='background:#f0f4ff;'><tr style='border-bottom:2px solid #667eea;'><th style='padding:12px;'>Device</th><th style='padding:12px;'>Browser</th><th style='padding:12px;'>Support</th><th style='padding:12px;'>Speed</th></tr></thead><tbody><tr style='border-bottom:1px solid #e2e8f0;'><td style='padding:12px;'><strong>iPhone / iPad</strong></td><td style='padding:12px;'>Safari, Chrome</td><td style='padding:12px; color:#48bb78;'>✅ Full</td><td style='padding:12px;'>⚡ Fast</td></tr><tr style='border-bottom:1px solid #e2e8f0;'><td style='padding:12px;'><strong>Android</strong></td><td style='padding:12px;'>Chrome, Firefox</td><td style='padding:12px; color:#48bb78;'>✅ Full</td><td style='padding:12px;'>⚡ Fast</td></tr><tr style='border-bottom:1px solid #e2e8f0;'><td style='padding:12px;'><strong>Windows PC</strong></td><td style='padding:12px;'>Chrome, Firefox, Edge</td><td style='padding:12px; color:#48bb78;'>✅ Full</td><td style='padding:12px;'>⚡⚡ Fastest</td></tr><tr><td style='padding:12px;'><strong>Mac</strong></td><td style='padding:12px;'>Safari, Chrome</td><td style='padding:12px; color:#48bb78;'>✅ Full</td><td style='padding:12px;'>⚡⚡ Fastest</td></tr></tbody></table>"
        },
        {
            "title": "All Supported Platforms",
            "content": "<table style='width:100%; border-collapse:collapse; margin:20px 0; font-size:13px;'><thead style='background:#667eea; color:white;'><tr><th style='padding:12px;'>Platform</th><th style='padding:12px; text-align:center;'>Video</th><th style='padding:12px; text-align:center;'>Audio</th><th style='padding:12px; text-align:center;'>Max Quality</th></tr></thead><tbody><tr style='background:#f8f9fa; border-bottom:1px solid #e2e8f0;'><td style='padding:12px;'><strong>Instagram</strong></td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>1080p</td></tr><tr style='border-bottom:1px solid #e2e8f0;'><td style='padding:12px;'><strong>TikTok</strong></td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>1080p</td></tr><tr style='background:#f8f9fa; border-bottom:1px solid #e2e8f0;'><td style='padding:12px;'><strong>YouTube</strong></td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>4K</td></tr><tr style='border-bottom:1px solid #e2e8f0;'><td style='padding:12px;'><strong>Facebook</strong></td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>720p</td></tr><tr style='background:#f8f9fa; border-bottom:1px solid #e2e8f0;'><td style='padding:12px;'><strong>Twitter / X</strong></td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>1080p</td></tr><tr style='border-bottom:1px solid #e2e8f0;'><td style='padding:12px;'><strong>Pinterest</strong></td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>—</td><td style='padding:12px; text-align:center;'>720p</td></tr><tr style='background:#f8f9fa;'><td style='padding:12px;'><strong>Snapchat</strong></td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>✅</td><td style='padding:12px; text-align:center;'>480p</td></tr></tbody></table>"
        },
    ]

    # Build extra_sections per page type
    if path != "/":
        extra_sections = [
            {
                "title": f"Why Use SnapReelDownload for {brand_name}?",
                "content": "<p>When you want to save a video, you need a solution that is fast, reliable, and secure. Our downloader operates entirely in the cloud, meaning it won't slow down your device. <strong>Zero watermarks</strong> ensure that the video remains exactly as the creator uploaded it, providing the best possible viewing experience. Furthermore, we support the extraction of high-fidelity audio tracks (MP3/M4A), offering complete versatility for your media library.</p>"
            },
            {
                "title": f"How to Download {brand_name} {content_word} on iPhone / iOS Devices",
                "content": f"<p>Downloading to an Apple device requires no third-party apps from the App Store. Simply open the <strong>Safari browser</strong> on your iPhone or iPad. Paste the {brand_name} link into our input field and tap 'Download.' Safari's native download manager will fetch the file. Once it finishes, tap the downward arrow near the address bar, select the video, and tap <strong>'Save Video'</strong> to move it securely into your Photos app camera roll.</p>"
            },
            {
                "title": f"How to Save {brand_name} {content_word} on Android Phones",
                "content": f"<p>For Android users (Samsung, Google Pixel, Xiaomi, etc.), the process is incredibly straightforward. Launch <strong>Google Chrome</strong> or your default browser. Paste the copied {brand_name} link and press the download button. The original MP4 video or audio file will automatically save to your device's <strong>'Downloads'</strong> folder, meaning it will instantly appear in your system's gallery app, ready to be viewed completely offline or shared on WhatsApp.</p>"
            },
            {
                "title": "Downloading to PC or Mac Desktop",
                "content": f"<p>Whether you're running Windows 11, Windows 10, macOS, or Linux, our web-tool functions perfectly. Open the {brand_name} website in a separate tab, copy the video link from the address bar, and paste it into our {tool_name}. Right-click the generated download button and select <strong>'Save link as...'</strong> (or simply click it). It's the ideal method for collecting high-quality HD media for video editing projects or personal archives.</p>"
            },
            {
                "title": "Other Downloader Tools",
                "content": "<ul style='columns:2; list-style:none; padding:0;'><li style='margin-bottom:8px;'><a href='/video'>📸 Instagram Video</a></li><li style='margin-bottom:8px;'><a href='/reels'>🎬 Instagram Reels</a></li><li style='margin-bottom:8px;'><a href='/tiktok'>🎵 TikTok Downloader</a></li><li style='margin-bottom:8px;'><a href='/youtube'>▶️ YouTube Video</a></li><li style='margin-bottom:8px;'><a href='/facebook'>📘 Facebook Video</a></li><li style='margin-bottom:8px;'><a href='/youtube-to-mp3'>🎧 YouTube to MP3</a></li><li style='margin-bottom:8px;'><a href='/snapchat'>👻 Snapchat Video</a></li><li style='margin-bottom:8px;'><a href='/youtube-shorts-downloader'>▶️ YouTube Shorts</a></li></ul>"
            },
        ]
        extra_sections.extend(shared_extra)
    else:
        # ✅ FIX 3: Removed "instgram" / "yotube" intentional typos — bad for credibility & AdSense
        extra_sections = [
            {
                "title": "All-in-One Free Video Downloader",
                "content": (
                    "<p>SnapReelDownload is a universal free tool to download videos from "
                    "<strong>Instagram</strong>, <strong>YouTube</strong>, <strong>TikTok</strong>, "
                    "<strong>Facebook</strong>, <strong>Twitter/X</strong>, <strong>Snapchat</strong>, "
                    "and <strong>Pinterest</strong>. Save HD quality videos without any watermark — "
                    "no login, no app, works on all devices.</p>"
                )
            },
            {
                "title": "Key Features",
                "content": (
                    "<ul>"
                    "<li>✅ 100% Free and unlimited downloads — no signup required.</li>"
                    "<li>✅ High-quality MP4 video and MP3 audio (up to 320kbps) support.</li>"
                    "<li>✅ No watermark — clean downloads from all platforms.</li>"
                    "<li>✅ Works on iPhone, Android, Windows, and Mac.</li>"
                    "<li>✅ Fast, secure, SSL encrypted — your data is never stored.</li>"
                    "</ul>"
                )
            },
        ]
        extra_sections.extend(shared_extra)

    # ── SEO_PAGES override (Phase 4 merge) ───────────────────────────────────
    page_subtitle = f"{t['dw']} {content_word}s in HD"

    if path in SEO_PAGES:
        override   = SEO_PAGES[path]
        lang_data  = override.get(lang, {})
        # Only fallback to the base English override if the requested language is actually english!
        # Filter to only use top-level string/list fields (skip nested lang dicts like 'es', 'hi')
        if not lang_data and lang == "en":
            LANG_CODES = {"en","hi","es","fr","de","pt","ar","id","bn","tr","th","ko","ja","uk","pl"}
            lang_data = {k: v for k, v in override.items() if k not in LANG_CODES}

        if isinstance(lang_data, dict):
            if "title"       in lang_data: title     = lang_data["title"]
            if "description" in lang_data: desc      = lang_data["description"]
            if "h1"          in lang_data: h1        = lang_data["h1"]
            if "subtitle"    in lang_data:
                page_subtitle = lang_data["subtitle"]
            elif "subtitle" in override and lang == "en":
                page_subtitle = override["subtitle"]

            # Merge — custom content first, generated content appended
            if "intro_text"     in lang_data: intro          = lang_data["intro_text"] + "<hr style='margin:30px 0; border:0; border-top:1px dashed #cbd5e0;'>" + intro
            if "faqs"           in lang_data: faqs           = lang_data["faqs"] + faqs
            if "features"       in lang_data: features       = lang_data["features"] + features
            if "extra_sections" in lang_data: extra_sections = lang_data["extra_sections"] + extra_sections
            if "tool_name"      in lang_data: tool_name      = lang_data["tool_name"]

    # ✅ FIX 5: Prevent "Duplicate, Google chose different canonical" indexing errors
    # Remove bulky English boilerplate on translated pages unless explicitly translated
    if lang != "en":
        _is_translated = False
        if path in SEO_PAGES and lang in SEO_PAGES[path] and "faqs" in SEO_PAGES[path][lang]:
            _is_translated = True
            
        if not _is_translated:
            faqs = []
            extra_sections = []
            intro = f"<p><strong>{t['dw']} {brand_name} {content_word} {t['on']}</strong> — {t['fr']}.</p>"
            steps = [
                {"title": t["step1"], "desc": f"Copy {brand_name} link."},
                {"title": t["step2"], "desc": "Paste the URL."},
                {"title": t["step3"], "desc": "Download file."}
            ]
            features = features[:2]

    return {
        "title":         str(title)[:65],
        "description":   str(desc)[:160],
        "h1":            str(h1),
        "subtitle":      str(page_subtitle),
        "tool_name":     str(tool_name),
        "intro_text":    str(intro),
        "keyword":       f"{brand_name} {content_word}".lower(),
        "platform":      platform,
        "steps":         steps,
        "features":      features,
        "faqs":          faqs,
        "extra_sections": extra_sections,
        "lang":          lang,
    }


def generate_multilingual_pages():
    pages = {}
    base_domain = "https://snapreeldownload.com"

    # 1. Core multilingual pages (TOOLS × SUPPORTED_LANGUAGES)
    for path, platform, brand_name, content_key in TOOLS:
        for lang in SUPPORTED_LANGUAGES:
            prefix    = f"/{lang}" if lang != "en" else ""
            full_path = f"{prefix}{path}"
            
            # Handle trailing slash for roots (e.g., /, /de/)
            if path == "/":
                if lang == "en":
                    full_path = "/"
                else:
                    full_path = f"/{lang}/"
            elif full_path.endswith("/") and full_path != "/":
                full_path = full_path.rstrip("/")

            page_data = make_page_data(path, platform, brand_name, content_key, lang)

            # ✅ FIX 4: Self-referencing canonical for all pages
            page_data["canonical"] = f"{base_domain}{full_path}"

            # Build complete hreflang map
            hreflangs_map = {}
            for l in SUPPORTED_LANGUAGES:
                if l == "en":
                    l_full = path if path != "/" else "/"
                else:
                    l_full = f"/{l}{path}" if path != "/" else f"/{l}/"
                
                if l_full.endswith("/") and len(l_full) > 1 and l != "en" and path != "/":
                    pass  # Handled below by l_final logic

                # Hreflang path logic: matches full_path generation
                if path == "/":
                    if l == "en":
                        l_final = "/"
                    else:
                        l_final = f"/{l}/"
                else:
                    if l == "en":
                        l_final = path
                    else:
                        l_final = f"/{l}{path}"
                    if l_final.endswith("/"):
                        l_final = l_final.rstrip("/")

                hreflangs_map[l] = f"{base_domain}{l_final}"
            page_data["hreflangs"] = hreflangs_map

            pages[full_path] = page_data

    # 2. Programmatic SEO pages (already have canonical + hreflang from their generator)
    for path, page_data in PROGRAMMATIC_PAGES.items():
        clean_path = path.lower()
        if clean_path.endswith("/") and len(clean_path) > 4:
            clean_path = clean_path.rstrip("/")

        parts = clean_path.strip("/").split("/")
        if parts[0] in SUPPORTED_LANGUAGES:
            base_tool_path = "/" + "/".join(parts[1:])
            page_lang      = parts[0]
        else:
            base_tool_path = clean_path
            page_lang      = "en"

        # ✅ FIX 4: Self-referencing canonical for programmatic pages
        page_data["canonical"] = f"{base_domain}{clean_path}"

        hreflangs_map = {}
        for l in SUPPORTED_LANGUAGES:
            if l == "en":
                l_full = base_tool_path if base_tool_path != "" else "/"
            else:
                l_full = f"/{l}{base_tool_path}"
                
            if l_full.endswith("/") and len(l_full) > 1:
                l_full = l_full.rstrip("/")
            hreflangs_map[l] = f"{base_domain}{l_full}"
        page_data["hreflangs"] = hreflangs_map

        if not page_data.get("tool_name"):
            page_data["tool_name"] = "Video Downloader"

        actual_path = hreflangs_map[page_data.get("lang", "en")].replace(base_domain, "")
        pages[actual_path] = page_data

    return pages


MULTILINGUAL_PAGES = generate_multilingual_pages()
