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
        {"question": f"Is this {brand_name} {t['dl']} free?", "answer": "Yes, absolutely free!"},
        {"question": f"Can I use this on mobile?", "answer": "Yes, works on Android and iOS."}
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
