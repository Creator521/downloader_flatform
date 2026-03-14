# app/multilingual_data.py
import copy

SUPPORTED_LANGUAGES = [
    "en", "hi", "es", "fr", "de", "pt", "ar", "id", 
    "bn", "tr", "th", "ko", "ja", "uk", "pl"
]

# Core translated keywords
T = {
    "en": {"dw": "Download", "on": "Online", "fr": "Free", "dl": "Downloader", "vid": "Video", "ph": "Photo", "st": "Story", "rl": "Reels", "step1": "Step 1: Copy Link", "step2": "Step 2: Paste URL", "step3": "Step 3: Download"},
    "hi": {"dw": "डाउनलोड", "on": "ऑनलाइन", "fr": "मुफ्त", "dl": "डाउनलोडर", "vid": "वीडियो", "ph": "फोटो", "st": "स्टोरी", "rl": "रील्स", "step1": "स्टेप 1: लिंक कॉपी करें", "step2": "स्टेप 2: URL पेस्ट करें", "step3": "स्टेप 3: डाउनलोड करें"},
    "es": {"dw": "Descargar", "on": "en línea", "fr": "Gratis", "dl": "Descargador", "vid": "Video", "ph": "Foto", "st": "Historia", "rl": "Reels", "step1": "Paso 1: Copiar enlace", "step2": "Paso 2: Pegar URL", "step3": "Paso 3: Descargar"},
    "fr": {"dw": "Télécharger", "on": "en ligne", "fr": "Gratuit", "dl": "Téléchargeur", "vid": "Vidéo", "ph": "Photo", "st": "Story", "rl": "Reels", "step1": "Étape 1: Copier le lien", "step2": "Étape 2: Coller l'URL", "step3": "Étape 3: Télécharger"},
    "de": {"dw": "Herunterladen", "on": "Online", "fr": "Kostenlos", "dl": "Downloader", "vid": "Video", "ph": "Foto", "st": "Story", "rl": "Reels", "step1": "Schritt 1: Link kopieren", "step2": "Schritt 2: URL einfügen", "step3": "Schritt 3: Herunterladen"},
    "pt": {"dw": "Baixar", "on": "Online", "fr": "Grátis", "dl": "Baixador", "vid": "Vídeo", "ph": "Foto", "st": "Story", "rl": "Reels", "step1": "Passo 1: Copiar link", "step2": "Passo 2: Colar URL", "step3": "Passo 3: Baixar"},
    "ar": {"dw": "تحميل", "on": "عبر الانترنت", "fr": "مجاني", "dl": "محمل", "vid": "فيديو", "ph": "صورة", "st": "قصة", "rl": "ريلز", "step1": "الخطوة 1: انسخ الرابط", "step2": "الخطوة 2: الصق الرابط", "step3": "الخطوة 3: تحميل"},
    "id": {"dw": "Unduh", "on": "Online", "fr": "Gratis", "dl": "Pengunduh", "vid": "Video", "ph": "Foto", "st": "Cerita", "rl": "Reels", "step1": "Langkah 1: Salin Tautan", "step2": "Langkah 2: Tempel URL", "step3": "Langkah 3: Unduh"},
    "bn": {"dw": "ডাউনলোড", "on": "অনলাইন", "fr": "বিনামূল্যে", "dl": "ডাউনলোডার", "vid": "ভিডিও", "ph": "ছবি", "st": "গল্প", "rl": "রিলস", "step1": "ধাপ ১: লিঙ্ক কপি করুন", "step2": "ধাপ ২: URL পেস্ট করুন", "step3": "ধাপ ৩: ডাউনলোড করুন"},
    "tr": {"dw": "İndir", "on": "Çevrimiçi", "fr": "Ücretsiz", "dl": "İndirici", "vid": "Video", "ph": "Fotoğraf", "st": "Hikaye", "rl": "Reels", "step1": "Adım 1: Bağlantıyı Kopyala", "step2": "Adım 2: URL'yi Yapıştır", "step3": "Adım 3: İndir"},
    "th": {"dw": "ดาวน์โหลด", "on": "ออนไลน์", "fr": "ฟรี", "dl": "เครื่องมือดาวน์โหลด", "vid": "วิดีโอ", "ph": "รูปภาพ", "st": "สตอรี่", "rl": "Reels", "step1": "ขั้นตอนที่ 1: คัดลอกลิงก์", "step2": "ขั้นตอนที่ 2: วาง URL", "step3": "ขั้นตอนที่ 3: ดาวน์โหลด"},
    "ko": {"dw": "다운로드", "on": "온라인", "fr": "무료", "dl": "다운로더", "vid": "비디오", "ph": "사진", "st": "스토리", "rl": "릴스", "step1": "1단계: 링크 복사", "step2": "2단계: URL 붙여넣기", "step3": "3단계: 다운로드"},
    "ja": {"dw": "ダウンロード", "on": "オンライン", "fr": "無料", "dl": "ダウンローダー", "vid": "動画", "ph": "写真", "st": "ストーリー", "rl": "リール", "step1": "ステップ1：リンクをコピー", "step2": "ステップ2：URLを貼り付け", "step3": "ステップ3：ダウンロード"},
    "uk": {"dw": "Завантажити", "on": "онлайн", "fr": "Безкоштовно", "dl": "Завантажувач", "vid": "Відео", "ph": "Фото", "st": "Історія", "rl": "Reels", "step1": "Крок 1: Копіювати посилання", "step2": "Крок 2: Вставити URL", "step3": "Крок 3: Завантажити"},
    "pl": {"dw": "Pobierz", "on": "Online", "fr": "Za darmo", "dl": "Pobieracz", "vid": "Wideo", "ph": "Zdjęcie", "st": "Relacja", "rl": "Reels", "step1": "Krok 1: Kopiuj link", "step2": "Krok 2: Wklej URL", "step3": "Krok 3: Pobierz"},
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
    ("/youtube-to-mp3", "YouTube", "YouTube to MP3", "vid") # The exception path kept exactly as is
]

def make_page_data(path, platform, brand_name, content_key, lang):
    t = T.get(lang, T["en"])
    
    content_word = t[content_key]
    
    if path == "/youtube-to-mp3":
        title = f'YouTube to MP3 {t["dl"]} {t["on"]} {t["fr"]}'
        desc = f'{t["dw"]} YouTube to MP3 {t["on"]} {t["fr"]}. High quality 320kbps.'
        h1 = f'YouTube to MP3 {t["dl"]}'
        tool_name = "YouTube to MP3"
    elif path == "/":
        title = f'Universal {content_word} {t["dl"]} {t["on"]} {t["fr"]}'
        desc = f'{t["dw"]} {content_word}s {t["on"]} {t["fr"]}. Fast, free {content_word} {t["dl"]}.'
        h1 = f'Universal {content_word} {t["dl"]}'
        tool_name = f'Universal {content_word} {t["dl"]}'
    else:
        title = f'{t["dw"]} {brand_name} {content_word} {t["on"]} {t["fr"]}'
        desc = f'{t["dw"]} {brand_name} {content_word} {t["on"]} {t["fr"]} without watermark. Fast {brand_name} {t["dl"]}.'
        h1 = f'{t["dw"]} {brand_name} {content_word}'
        tool_name = f'{brand_name} {content_word} {t["dl"]}'
        
    intro = f"<p>{t['dw']} {brand_name} {content_word} {t['on']}. fast, secure and free.</p>"
    
    steps = [
        {"title": t["step1"], "desc": f"Copy the link of the {content_word}."},
        {"title": t["step2"], "desc": f"Paste the link into the input box."},
        {"title": t["step3"], "desc": f"Click the download button."}
    ]
    
    features = [
        {"title": "HD Quality", "desc": f"Save {content_word} in best quality."},
        {"title": "Free", "desc": "100% Free forever."},
        {"title": "Fast", "desc": "Lightning fast download speeds."}
    ]
    
    faqs = [
        {"question": f"Is this {brand_name} {t['dl']} completely free?", "answer": "Yes, absolutely free! No hidden charges, no premium features, no watermarks added. Download unlimited videos forever at no cost."},
        {"question": f"Do I need to create an account or sign up?", "answer": "No! Our tool works instantly without signup, registration, or login. Just paste the link and download."},
        {"question": f"Can {brand_name} creators see that I downloaded their {content_word}?", "answer": "No, your download is completely anonymous. The creator is never notified, and your activity is completely private."},
        {"question": f"Is it legal to download {brand_name} {content_word}s?", "answer": "Yes, for personal use like offline viewing, archiving, or educational reference. However, do not repost content as your own or use for commercial purposes without permission."},
        {"question": f"What formats can I download {content_word}s in?", "answer": "We support MP4 for videos and M4A for audio. MP4 works on all devices and players. Audio extraction is available for compatible content."},
        {"question": f"Can I use this on my iPhone/iPad?", "answer": "Yes! Works perfectly on iOS through Safari or Chrome. Downloaded videos appear in your Photos app or Files app."},
        {"question": f"Does this work on Android phones?", "answer": "Absolutely. Android users can use Chrome, Firefox, or any browser. Videos download to your Downloads folder or Gallery."},
        {"question": f"Can I download {content_word}s on my computer?", "answer": "Yes, works great on Windows, Mac, and Linux. Use any modern browser (Chrome, Firefox, Safari, Edge)."},
        {"question": f"Why is {brand_name} not letting me download with my app?", "answer": f"{brand_name} doesn't allow native downloads to encourage app engagement. Our tool bypasses this limitation legally for personal use."},
        {"question": f"What if the download fails or the link doesn't work?", "answer": "Make sure the link is correct and the content is still public. If still failing, try a different video. We support only public, accessible content."},
        {"question": f"Can I download private {content_word}s or accounts?", "answer": "No, we only support publicly accessible content. Private profiles, age-restricted content, and deleted posts cannot be downloaded."},
        {"question": f"Is my data safe with your tool?", "answer": "Yes! We use SSL encryption, never store your personal data, never log your activity, and never sell information. Complete privacy guaranteed."},
        {"question": f"How long does a download take?", "answer": "Most downloads complete in seconds, depending on video length and file size. Longer videos may take 20-30 seconds."},
        {"question": f"Can I download story content that will disappear?", "answer": "For Stories and Highlights - yes, if the creator has made them public. Private stories cannot be accessed per privacy policy."},
    ]
    
    # Add extra SEO content sections - device guides for tool pages
    extra_sections = []
    
    if path != "/":
        # For tool pages: Add device-specific download guides
        extra_sections = [
            {
                "title": f"How to Download {brand_name} {content_word} on iPhone/iOS",
                "content": f"<p><strong>iOS Download Steps:</strong></p><ol><li>Open {brand_name} app and find your {content_word}</li><li>Tap Share button → Copy Link</li><li>Open Safari or Chrome browser</li><li>Visit snapreeldownload.com</li><li>Paste the link and tap Download</li><li>Video appears in Photos app or Downloads folder</li></ol><p><strong>Tip:</strong> Safari usually provides the smoothest download experience on iOS.</p>"
            },
            {
                "title": f"Download {brand_name} {content_word} on Android Devices",
                "content": f"<p><strong>Android Download Steps:</strong></p><ol><li>Open the {brand_name} app and locate your {content_word}</li><li>Tap the three-dot menu (⋮)</li><li>Select Copy Link</li><li>Open Chrome, Firefox, or your browser</li><li>Go to snapreeldownload.com</li><li>Paste the link and tap Download</li><li>Check your Downloads folder or Gallery app</li></ol><p><strong>Tip:</strong> Files usually save automatically to your Downloads folder or Gallery.</p>"
            },
            {
                "title": f"Save {brand_name} {content_word} on Windows & Mac PC",
                "content": f"<p><strong>Desktop Download Steps:</strong></p><ol><li>Open {brand_name} in Chrome, Firefox, Safari, or Edge</li><li>Find your {content_word} and copy its link</li><li>Visit snapreeldownload.com in your browser</li><li>Paste the link into the download box</li><li>Click the Download button</li><li>Select your format (MP4 video or MP3 audio)</li><li>The file saves to your Downloads folder</li></ol><p><strong>Windows Tip:</strong> Check C:\Users\[YourName]\Downloads | <strong>Mac Tip:</strong> Downloads are in ~/Downloads</p>"
            },
            {
                "title": "Is It Legal to Download Videos?",
                "content": "<p>Yes! Downloading public videos for <strong>personal use is completely legal</strong> under Fair Use copyright laws in most countries.</p><ul><li><strong>✅ Legal:</strong> Personal offline viewing, archiving for yourself, educational reference, time-shifting</li><li><strong>❌ Not Legal:</strong> Reposting as your own, commercial use, redistribution without permission, claiming authorship</li></ul><p><strong>Best Practice:</strong> Always credit the original creator if you share downloaded content anywhere.</p>"
            }
        ]
    else:
        # Homepage only
        extra_sections = [
        extra_sections = [
            {
                "title": "Download Videos from Instagram, TikTok, YouTube & More",
                "content": (
                    "<p>Snap Reel Download is a free online tool to download videos from popular platforms like "
                    "Instagram, TikTok, YouTube, Facebook, and more. Paste any public video link into the box above "
                    "and click Download to save it instantly.</p>"
                    "<p>We never require login, and your privacy is protected — it’s 100% free and anonymous.</p>"
                )
            },
            {
                "title": "How to Use the Universal Video Downloader",
                "content": (
                    "<ol>"
                    "<li>Copy the video link from your browser.</li>"
                    "<li>Paste it into the box above.</li>"
                    "<li>Click Download and choose the format you want.</li>"
                    "</ol>"
                    "<p>It works on any device (mobile, tablet, desktop), and you don’t need to install any app.</p>"
                )
            },
            {
                "title": "Key Features of Snap Reel Download",
                "content": (
                    "<ul>"
                    "<li>✅ Free & unlimited downloads (no signup required).</li>"
                    "<li>✅ Works on Android, iPhone, and desktop.</li>"
                    "<li>✅ Fast downloads in original quality.</li>"
                    "<li>✅ Supports Instagram, TikTok, YouTube, Facebook, Twitter, Pinterest, and more.</li>"
                    "<li>✅ No tracking or personal data stored.</li>"
                    "</ul>"
                )
            },
            {
                "title": "Why Use Our Video Downloader",
                "content": (
                    "<p>Many social platforms don’t let you save videos directly. Our tool makes it easy to keep any public video for offline viewing, sharing with friends, or saving for later.</p>"
                    "<p>We built the tool to be simple, safe, and reliable: just paste a link and download — no ads in the download process, no popups, and no surprising redirects.</p>"
                )
            }
        ]

    return {
        "title": title[:60],
        "description": desc[:160],
        "h1": h1,
        "subtitle": f"{t['dw']} {content_word}s in HD",
        "tool_name": tool_name,
        "intro_text": intro,
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
            # Generate the URL structure
            # e.g., /hi/reels, or /reels for en. /youtube-to-mp3 is kept same as per exception.
            prefix = "" if lang == "en" else f"/{lang}"
            full_path = f"{prefix}{path}"
            
            # Root path handling
            if full_path == "":
                full_path = "/"
            elif full_path.endswith("/") and full_path != "/":
                full_path = full_path.rstrip("/")
            
            # Create page data
            page_data = make_page_data(path, platform, brand_name, content_key, lang)
            
            # Setup hreflangs
            hreflangs_map = {}
            for l in SUPPORTED_LANGUAGES:
                l_prefix = "" if l == "en" else f"/{l}"
                l_full = f"{l_prefix}{path}"
                if l_full == "": 
                    l_full = "/"
                elif l_full.endswith("/") and l_full != "/":
                    l_full = l_full.rstrip("/")
                hreflangs_map[l] = f"{base_domain}{l_full}"
                
            page_data["hreflangs"] = hreflangs_map
            page_data["canonical"] = f"{base_domain}{full_path}"
            
            pages[full_path] = page_data
            
    return pages

MULTILINGUAL_PAGES = generate_multilingual_pages()
