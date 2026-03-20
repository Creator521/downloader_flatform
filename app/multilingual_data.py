# app/multilingual_data.py
import copy
try:
    from app.seo_data import SEO_PAGES # type: ignore
except ImportError:
    from seo_data import SEO_PAGES # type: ignore

SUPPORTED_LANGUAGES = [
    "en", "hi", "es", "fr", "de", "pt", "ar", "id", 
    "bn", "tr", "th", "ko", "ja", "uk", "pl"
]

# Core translated keywords
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

TOOLS = [
    # (path, platform, subject, target_content)
    ("/", "Any", "Universal", "vid"),
    ("/reels", "Instagram", "Instagram", "rl"),
    ("/video", "Instagram", "Instagram", "vid"),
    ("/photo", "Instagram", "Instagram", "ph"),
    ("/story", "Instagram", "Instagram", "st"),
    ("/youtube", "YouTube", "YouTube", "vid"),
    ("/tiktok", "TikTok", "TikTok", "vid"),
    ("/facebook", "Facebook", "Facebook", "vid"),
    ("/twitter", "Twitter (X)", "Twitter", "vid"),
    ("/pinterest", "Pinterest", "Pinterest", "vid"),
    ("/snapchat", "Snapchat", "Snapchat", "vid"),
    ("/tiktok-mp3-downloader", "TikTok", "TikTok to MP3", "vid"),
    ("/youtubeshort", "YouTube", "YouTube Shorts", "vid"),
    ("/youtube-to-mp3", "YouTube", "YouTube to MP3", "vid")
]

def make_page_data(path, platform, brand_name, content_key, lang):
    t = T.get(lang, T["en"])
    content_word = t.get(content_key, t.get("vid", "Video"))
    suffix = t["title_suffix"]
    
    # Keyword Injection Logic (Phase 3)
    misspellings = ""
    if lang == "en":
        if brand_name == "Instagram":
            misspellings = "Instgram video download, download instgram video, instgram download video"
        elif brand_name == "YouTube":
            misspellings = "Yotube video download, download yotube videos, yotube download video"
        elif brand_name == "TikTok":
            misspellings = "Download tiktok video without watermark, tiktok video download without watermark"
        elif brand_name == "Facebook":
            misspellings = "Download facebook video online, facebook video download online"

    if path == "/youtube-to-mp3":
        if lang == "hi":
            title = f'यूट्यूब से MP3 कनवर्टर ऑनलाइन मुफ्त | उच्च गुणवत्ता | {suffix}'
            desc = f'यूट्यूब वीडियो को ऑनलाइन मुफ्त में MP3 में बदलें। 320kbps उच्च गुणवत्ता वाली MP3 फाइलें तुरंत डाउनलोड करें।'
        elif lang == "es":
            title = f'Convertidor de YouTube a MP3 gratis | Alta calidad | {suffix}'
            desc = f'Convierte videos de YouTube a MP3 gratis en línea. Descarga archivos MP3 de alta calidad al instante.'
        else:
            title = f'YouTube to MP3 Converter Online Free | High Quality 320kbps | {suffix}'
            desc = f'Convert YouTube videos to MP3 audio online for free. Download high-quality 320kbps MP3 files instantly.'
        
        h1 = f'YouTube to MP3 {t["dl"]}'
        tool_name = "YouTube to MP3"
    elif path == "/":
        if lang == "hi":
            title = f'{suffix} - मुफ्त ऑनलाइन वीडियो डाउनलोडर | इंस्टाग्राम, टिकटोकर, यूट्यूब'
            desc = f'इंस्टाग्राम, टिकटॉक, यूट्यूब, फेसबुक और अन्य से वीडियो मुफ्त में डाउनलोड करें। बिना वॉटरमार्क के एचडी वीडियो सेव करें।'
        elif lang == "es":
            title = f'{suffix} - Descargador de videos en línea gratis | Instagram, TikTok'
            desc = f'Descarga videos de Instagram, TikTok, YouTube y más gratis. Guarda videos HD sin marca de agua.'
        else:
            title = f'{suffix} - Free Online Video Downloader | Instagram, TikTok, YouTube'
            desc = f'Download videos and reels from Instagram, TikTok, YouTube, Facebook & more. Save HD quality contents online.'
        
        h1 = f'Universal {content_word} {t["dl"]}'
        tool_name = f'Universal {content_word} {t["dl"]}'
    else:
        if lang == "en":
            if brand_name == "TikTok":
                desc = f'Download TikTok videos without watermark in HD. Best free tiktok video downloader online. Fast, secure and unlimited.'
            elif brand_name == "Facebook":
                desc = f'Download Facebook videos online in HD. Best tool for FB video download and reels saving. Free & Anonymous.'
            else:
                desc = f'{t["dw"]} {brand_name} {content_word} in HD quality for {t["fr"]}. Save {content_word}s without watermark. Fast & secure.'
        else:
            desc = f'{t["dw"]} {brand_name} {content_word} in HD quality for {t["fr"]}. Save {content_word}s without watermark. Fast & secure.'
            
        title = f'{t["dw"]} {brand_name} {content_word} HD {t["fr"]} {t["on"]} | {suffix}'
        h1 = f'{t["dw"]} {brand_name} {content_word}'
        tool_name = f'{brand_name} {content_word} {t["dl"]}'
        
    intro = f"<p>{t['dw']} {brand_name} {content_word} {t['on']}. {t['fr']}, fast and secure.</p>"
    
    steps = [
        {"title": t["step1"], "desc": f"Copy the link from the app or website."},
        {"title": t["step2"], "desc": f"Paste it into the input box above."},
        {"title": t["step3"], "desc": f"Click the download button to start."}
    ]
    
    features = [
        {"title": "HD Quality", "desc": f"Save {content_word} in best quality."},
        {"title": "Free", "desc": "100% Free forever."},
        {"title": "Fast", "desc": "Lightning fast download speeds."}
    ]
    
    faqs = [
        {"question": "Is this tool completely free?", "answer": "Yes, absolutely free! No hidden charges, no premium features, no watermarks added. Download unlimited videos forever at no cost."},
        {"question": "Do I need to create an account or sign up?", "answer": "No! Our tool works instantly without signup, registration, or login. Just paste the link and download."},
        {"question": "Can creators see that I downloaded their content?", "answer": "No, your download is completely anonymous. The creator is never notified."},
        {"question": "Is it legal to download videos?", "answer": "Yes, for personal use like offline viewing or archiving. Do not used for commercial purposes without permission."},
        {"question": "What formats can I download in?", "answer": "We support MP4 for videos and M4A for audio. MP4 works on all devices and players."},
        {"question": "Can I use this on my iPhone/iPad?", "answer": "Yes! Works perfectly on iOS through Safari or Chrome browser."},
        {"question": "Does this work on Android phones?", "answer": "Absolutely. Works on all Android browsers (Chrome, Firefox, etc.)."},
        {"question": "Is my data safe with your tool?", "answer": "Yes! We use SSL encryption and never store your personal data or search history."},
    ]

    # Shared sections for BOTH homepage and tool pages
    shared_extra = [
        {
            "title": "Download Format & Quality Comparison",
            "content": "<table style='width:100%; border-collapse: collapse; margin: 20px 0;'><thead style='background: #f0f4ff;'><tr style='border-bottom: 2px solid #667eea;'><th style='padding: 12px; text-align: left; font-weight: 600;'>Format</th><th style='padding: 12px; text-align: left; font-weight: 600;'>File Type</th><th style='padding: 12px; text-align: left; font-weight: 600;'>Quality</th><th style='padding: 12px; text-align: left; font-weight: 600;'>Best For</th></tr></thead><tbody><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>MP4</strong></td><td style='padding: 12px;'>Video</td><td style='padding: 12px;'><span style='color: #48bb78;'>⭐⭐⭐⭐⭐ HD/4K</span></td><td style='padding: 12px;'>Video with audio, editing</td></tr><tr><td style='padding: 12px;'><strong>M4A</strong></td><td style='padding: 12px;'>Audio Only</td><td style='padding: 12px;'><span style='color: #48bb78;'>⭐⭐⭐⭐⭐ 320kbps</span></td><td style='padding: 12px;'>Music, podcasts, audio</td></tr></tbody></table>"
        },
        {
            "title": "Device Compatibility Guide",
            "content": "<table style='width:100%; border-collapse: collapse; margin: 20px 0;'><thead style='background: #f0f4ff;'><tr style='border-bottom: 2px solid #667eea;'><th style='padding: 12px; text-align: left; font-weight: 600;'>Device</th><th style='padding: 12px; text-align: left; font-weight: 600;'>Browsers Supported</th><th style='padding: 12px; text-align: left; font-weight: 600;'>Download Support</th><th style='padding: 12px; text-align: left; font-weight: 600;'>Speed</th></tr></thead><tbody><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>iPhone/iPad</strong></td><td style='padding: 12px;'>Safari, Chrome</td><td style='padding: 12px;'><span style='color: #48bb78;'>✅ Full</span></td><td style='padding: 12px;'>⚡ Fast</td></tr><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>Android</strong></td><td style='padding: 12px;'>Chrome, Firefox, Any</td><td style='padding: 12px;'><span style='color: #48bb78;'>✅ Full</span></td><td style='padding: 12px;'>⚡ Fast</td></tr><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>Windows PC</strong></td><td style='padding: 12px;'>Chrome, Firefox, Edge</td><td style='padding: 12px;'><span style='color: #48bb78;'>✅ Full</span></td><td style='padding: 12px;'>⚡⚡ Fastest</td></tr><tr><td style='padding: 12px;'><strong>Mac</strong></td><td style='padding: 12px;'>Safari, Chrome, Firefox</td><td style='padding: 12px;'><span style='color: #48bb78;'>✅ Full</span></td><td style='padding: 12px;'>⚡⚡ Fastest</td></tr></tbody></table>"
        },
        {
            "title": "Platform Feature Comparison Matrix",
            "content": "<p><strong>Which platforms does our downloader support?</strong></p><table style='width:100%; border-collapse: collapse; margin: 20px 0; font-size: 13px;'><thead style='background: #667eea; color: white;'><tr><th style='padding: 12px; text-align: left; font-weight: 600;'>Platform</th><th style='padding: 12px; text-align: center; font-weight: 600;'>Video</th><th style='padding: 12px; text-align: center; font-weight: 600;'>Audio</th><th style='padding: 12px; text-align: center; font-weight: 600;'>HD Quality</th><th style='padding: 12px; text-align: center; font-weight: 600;'>Speed</th></tr></thead><tbody><tr style='background: #f8f9fa; border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>Instagram</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>⭐ 1080p</td><td style='padding: 12px; text-align: center;'>⚡</td></tr><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>TikTok</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>⭐ 720p</td><td style='padding: 12px; text-align: center;'>⚡⚡</td></tr><tr style='background: #f8f9fa; border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>YouTube</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>⭐⭐ 4K</td><td style='padding: 12px; text-align: center;'>⚡</td></tr><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>Facebook</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>⭐ 720p</td><td style='padding: 12px; text-align: center;'>⚡</td></tr><tr style='background: #f8f9fa; border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>Twitter (X)</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>⭐ 1080p</td><td style='padding: 12px; text-align: center;'>⚡⚡</td></tr><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>Pinterest</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>—</td><td style='padding: 12px; text-align: center;'>⭐ 720p</td><td style='padding: 12px; text-align: center;'>⚡</td></tr><tr style='background: #f8f9fa;'><td style='padding: 12px;'><strong>Snapchat</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>⭐ 480p</td><td style='padding: 12px; text-align: center;'>⚡⚡</td></tr></tbody></table>"
        },
        {
            "title": "Visual Download Guide",
            "content": "<p><strong>Follow this simple step-by-step guide to download any online video:</strong></p><figure style='margin: 20px 0; text-align: center;'><img src='/static/images/guide-step-1-copy-link.png' alt='Step 1: Copy the video link from app or website' style='max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0;' /><figcaption style='font-size: 14px; color: #666; margin-top: 10px;'>Step 1: Copy the link from the source platform</figcaption></figure><figure style='margin: 20px 0; text-align: center;'><img src='/static/images/guide-step-2-paste.png' alt='Step 2: Paste the link into the download box' style='max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0;' /><figcaption style='font-size: 14px; color: #666; margin-top: 10px;'>Step 2: Paste the link in the input field above</figcaption></figure><figure style='margin: 20px 0; text-align: center;'><img src='/static/images/guide-step-3-download.png' alt='Step 3: Click Download to process' style='max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0;' /><figcaption style='font-size: 14px; color: #666; margin-top: 10px;'>Step 3: Click the Download button</figcaption></figure><figure style='margin: 20px 0; text-align: center;'><img src='/static/images/guide-step-4-format.png' alt='Step 4: Choose your preferred format' style='max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0;' /><figcaption style='font-size: 14px; color: #666; margin-top: 10px;'>Step 4: Select MP4 or MP3 format</figcaption></figure><figure style='margin: 20px 0; text-align: center;'><img src='/static/images/guide-step-5-save.png' alt='Step 5: File saves to your device' style='max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0;' /><figcaption style='font-size: 14px; color: #666; margin-top: 10px;'>Step 5: File is saved to your gallery or downloads</figcaption></figure>"
        }
    ]

    extra_sections = []
    
    if path != "/":
        # Tool specific sections
        extra_sections = [
            {
                "title": f"How to Download {brand_name} {content_word} on iPhone & Android",
                "content": f"<p>Whether you're using an iPhone (Safari) or Android (Chrome), our tool works seamlessly. Just copy the {brand_name} link and visit <strong>SnapReelDownload</strong>. Our platform handles the rest, delivering the best HD content directly to your device.</p>"
            },
            {
                "title": "Other Download Tools We Offer",
                "content": "<p>Try our other specialized downloaders: </p><ul style='columns: 2;'><li><a href='/video'>📸 Instagram Video</a></li><li><a href='/reels'>🎬 Instagram Reels</a></li><li><a href='/tiktok'>🎵 TikTok Downloader</a></li><li><a href='/youtube'>▶️ YouTube Video</a></li><li><a href='/facebook'>📘 Facebook Video</a></li><li><a href='/youtube-to-mp3'>🎵 MP3 Converter</a></li></ul>"
            }
        ]
        
        if misspellings:
            extra_sections.append({
                "title": "People also search for",
                "content": f"<p style='opacity: 0.8; font-size: 14px;'>Users looking for specialized tools often search for: <strong>{misspellings}</strong>. Our tool supports all these variations.</p>"
            })
            
        extra_sections.extend(shared_extra)
    else:
        # Homepage specific sections
        extra_sections = [
            {
                "title": "All-in-One Online Video Downloader",
                "content": (
                    "<p>SnapReelDownload is a free tool to download videos from <strong>Instagram (instgram)</strong>, "
                    "<strong>YouTube (yotube)</strong>, TikTok, and Facebook. It’s the easiest way to save your favorite "
                    "online content safely in HD quality without any watermark.</p>"
                )
            },
            {
                "title": "Key Features of Universal Downloader",
                "content": (
                    "<ul>"
                    "<li>✅ 100% Free & Unlimited downloads (No signup).</li>"
                    "<li>✅ High-Quality MP4 & MP3 (320kbps) Support.</li>"
                    "<li>✅ Fast and secure - no tracking or login required.</li>"
                    "<li>✅ Works on iPhone, Android, Windows, and Mac.</li>"
                    "</ul>"
                )
            }
        ]
        # ADD Rich UI sections to homepage as well
        extra_sections.extend(shared_extra)

    # --- SEO DATA OVERRIDES (Phase 4) ---
    # We check if there's custom content in seo_data.py for this path
    if path in SEO_PAGES:
        override = SEO_PAGES[path]
        
        # We look for language-specific data. 
        # If it's English, it can be at the top level or inside an "en" key.
        # For other languages, it must be inside a key like "hi", "es", etc.
        lang_data = override.get(lang, {})
        if not lang_data:
            # Fallback to top-level if specific lang key is missing
            lang_data = override

        if isinstance(lang_data, dict):
            if "title" in lang_data: title = lang_data["title"]
            if "description" in lang_data: desc = lang_data["description"]
            if "h1" in lang_data: h1 = lang_data["h1"]
            
            # Subtitle handling
            if "subtitle" in lang_data: 
                page_subtitle = lang_data["subtitle"]
            elif isinstance(override, dict) and "subtitle" in override and lang == "en": 
                page_subtitle = override["subtitle"] # fallback for en
            else: 
                page_subtitle = f"{t['dw']} {content_word}s in HD"
            
            # --- MERGE LOGIC (Phase 5) ---
            # Instead of just replacing, we ADD the custom content to the default
            # but keep the custom content at the top.
            if "intro_text" in lang_data: 
                intro = lang_data["intro_text"] + "<hr style='margin: 30px 0; border: 0; border-top: 1px dashed #cbd5e0;'> " + intro
            
            if "faqs" in lang_data: 
                faqs = lang_data["faqs"] + faqs # Custom FAQs first
            
            if "features" in lang_data: 
                features = lang_data["features"] + features
            
            if "extra_sections" in lang_data: 
                extra_sections = lang_data["extra_sections"] + extra_sections
            
            if "tool_name" in lang_data: tool_name = lang_data["tool_name"]
    else:
        page_subtitle = f"{t['dw']} {content_word}s in HD"

    final_title = str(title) if title else ""
    final_desc = str(desc) if desc else ""
    
    return {
        "title": final_title[:65], # type: ignore
        "description": final_desc[:160], # type: ignore
        "h1": str(h1),
        "subtitle": str(page_subtitle),
        "tool_name": str(tool_name),
        "intro_text": str(intro),
        "keyword": f"{brand_name} {content_word}".lower(),
        "platform": platform,
        "steps": steps,
        "features": features,
        "faqs": faqs,
        "extra_sections": extra_sections,
        "lang": lang
    }

def generate_multilingual_pages():
    pages = {}
    base_domain = "https://snapreeldownload.com"
    
    for path, platform, brand_name, content_key in TOOLS:
        for lang in SUPPORTED_LANGUAGES:
            prefix = f"/{lang}"
            full_path = f"{prefix}{path}"
            
            if full_path == f"/{lang}":
                full_path = f"/{lang}/"
            elif full_path.endswith("/") and full_path != f"/{lang}/":
                full_path = full_path.rstrip("/")
            
            page_data = make_page_data(path, platform, brand_name, content_key, lang)
            
            hreflangs_map = {}
            for l in SUPPORTED_LANGUAGES:
                l_prefix = f"/{l}"
                l_full = f"{l_prefix}{path}"
                if l_full == f"/{l}": 
                    l_full = f"/{l}/"
                elif l_full.endswith("/") and l_full != f"/{l}/":
                    l_full = l_full.rstrip("/")
                hreflangs_map[l] = f"{base_domain}{l_full}"
                
            page_data["hreflangs"] = hreflangs_map
            page_data["canonical"] = f"{base_domain}{full_path}"
            
            pages[full_path] = page_data
            
    return pages

MULTILINGUAL_PAGES = generate_multilingual_pages()
