# app/multilingual_data.py
import copy

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
    ("/youtube-to-mp3", "YouTube", "YouTube to MP3", "vid")
]

def make_page_data(path, platform, brand_name, content_key, lang):
    t = T.get(lang, T["en"])
    content_word = t.get(content_key, t.get("vid", "Video"))
    suffix = t["title_suffix"]
    
    # Keyword Injection Logic (Phase 3)
    # Target common variations and misspellings (instgram, yotube)
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
        # Tool pages: Inject targeted keywords into descriptions
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
        {"question": f"What's the maximum {content_word} length I can download?", "answer": f"We support {content_word}s of any length. Download time depends on file size, but our servers handle everything from short clips to long-form content."},
        {"question": f"Do you add watermarks to downloaded {content_word}s?", "answer": "No watermarks ever! We deliver clean, original quality content without any branding or modifications."},
        {"question": f"Can I download multiple {content_word}s at once?", "answer": "Currently, we process one {content_word} at a time for optimal quality and speed. Download sequentially for best results."},
        {"question": f"What quality options are available?", "answer": "We automatically download the highest available quality from the source platform, typically HD (1080p) or better when available."},
        {"question": f"Does this work with {brand_name} Live videos?", "answer": "No, we only support pre-recorded content. Live streams cannot be downloaded as they haven't been processed yet."},
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
                "content": f"<p><strong>Desktop Download Steps:</strong></p><ol><li>Open {brand_name} in Chrome, Firefox, Safari, or Edge</li><li>Find your {content_word} and copy its link</li><li>Visit snapreeldownload.com in your browser</li><li>Paste the link into the download box</li><li>Click the Download button</li><li>Select your format (MP4 video or MP3 audio)</li><li>The file saves to your Downloads folder</li></ol><p><strong>Windows Tip:</strong> Check C:\\\\Users\\\\[YourName]\\\\Downloads | <strong>Mac Tip:</strong> Downloads are in ~/Downloads</p>"
            }
        ]
        
        # Inject misspelling keywords naturally if in English
        if misspellings:
            extra_sections.append({
                "title": "People also search for",
                "content": f"<p style='opacity: 0.8; font-size: 14px;'>Users looking for specialized tools often search for: <strong>{misspellings}</strong>. Our tool supports all these variations and ensures high-quality results every time.</p>"
            })

        extra_sections.extend([
            {
                "title": "Is It Legal to Download Videos?",
                "content": "<p>Yes! Downloading public videos for <strong>personal use is completely legal</strong> under Fair Use copyright laws in most countries.</p><ul><li><strong>✅ Legal:</strong> Personal offline viewing, archiving for yourself, educational reference, time-shifting</li><li><strong>❌ Not Legal:</strong> Reposting as your own, commercial use, redistribution without permission, claiming authorship</li></ul><p><strong>Best Practice:</strong> Always credit the original creator if you share downloaded content anywhere.</p>"
            },
            {
                "title": "Download Format & Quality Comparison",
                "content": "<table style='width:100%; border-collapse: collapse; margin: 20px 0;'><thead style='background: #f0f4ff;'><tr style='border-bottom: 2px solid #667eea;'><th style='padding: 12px; text-align: left; font-weight: 600;'>Format</th><th style='padding: 12px; text-align: left; font-weight: 600;'>File Type</th><th style='padding: 12px; text-align: left; font-weight: 600;'>Quality</th><th style='padding: 12px; text-align: left; font-weight: 600;'>Best For</th></tr></thead><tbody><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>MP4</strong></td><td style='padding: 12px;'>Video</td><td style='padding: 12px;'><span style='color: #48bb78;'>⭐⭐⭐⭐⭐ HD/4K</span></td><td style='padding: 12px;'>Video with audio, editing</td></tr><tr><td style='padding: 12px;'><strong>M4A</strong></td><td style='padding: 12px;'>Audio Only</td><td style='padding: 12px;'><span style='color: #48bb78;'>⭐⭐⭐⭐⭐ 320kbps</span></td><td style='padding: 12px;'>Music, podcasts, audio</td></tr></tbody></table>"
            },
            {
                "title": "Device Compatibility Guide",
                "content": "<table style='width:100%; border-collapse: collapse; margin: 20px 0;'><thead style='background: #f0f4ff;'><tr style='border-bottom: 2px solid #667eea;'><th style='padding: 12px; text-align: left; font-weight: 600;'>Device</th><th style='padding: 12px; text-align: left; font-weight: 600;'>Browsers Supported</th><th style='padding: 12px; text-align: left; font-weight: 600;'>Download Support</th><th style='padding: 12px; text-align: left; font-weight: 600;'>Speed</th></tr></thead><tbody><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>iPhone/iPad</strong></td><td style='padding: 12px;'>Safari, Chrome</td><td style='padding: 12px;'><span style='color: #48bb78;'>✅ Full</span></td><td style='padding: 12px;'>⚡ Fast</td></tr><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>Android</strong></td><td style='padding: 12px;'>Chrome, Firefox, Any</td><td style='padding: 12px;'><span style='color: #48bb78;'>✅ Full</span></td><td style='padding: 12px;'>⚡ Fast</td></tr><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>Windows PC</strong></td><td style='padding: 12px;'>Chrome, Firefox, Edge</td><td style='padding: 12px;'><span style='color: #48bb78;'>✅ Full</span></td><td style='padding: 12px;'>⚡⚡ Fastest</td></tr><tr><td style='padding: 12px;'><strong>Mac</strong></td><td style='padding: 12px;'>Safari, Chrome, Firefox</td><td style='padding: 12px;'><span style='color: #48bb78;'>✅ Full</span></td><td style='padding: 12px;'>⚡⚡ Fastest</td></tr></tbody></table>"
            },
            {
                "title": "Other Download Tools We Offer",
                "content": "<p><strong>Need to download from a different platform?</strong> Check out our complete tool suite:</p><ul style='columns: 2; column-gap: 30px; column-rule: 1px solid #e2e8f0; padding: 20px;'><li><a href='/video' style='color: #667eea; text-decoration: none; font-weight: 500;'>📹 Instagram Video Downloader</a> - Download IGTV and regular videos</li><li><a href='/reels' style='color: #667eea; text-decoration: none; font-weight: 500;'>🎬 Instagram Reels Downloader</a> - Save trending Reels content</li><li><a href='/photo' style='color: #667eea; text-decoration: none; font-weight: 500;'>📸 Instagram Photo Downloader</a> - Download images and carousels</li><li><a href='/story' style='color: #667eea; text-decoration: none; font-weight: 500;'>📖 Instagram Story Downloader</a> - Save disappearing Stories</li><li><a href='/tiktok' style='color: #667eea; text-decoration: none; font-weight: 500;'>🎵 TikTok Video Downloader</a> - Download viral TikTok videos</li><li><a href='/youtube' style='color: #667eea; text-decoration: none; font-weight: 500;'>▶️ YouTube Video Downloader</a> - Save YouTube content offline</li><li><a href='/facebook' style='color: #667eea; text-decoration: none; font-weight: 500;'>👥 Facebook Video Downloader</a> - Download Facebook videos and reels</li><li><a href='/youtube-to-mp3' style='color: #667eea; text-decoration: none; font-weight: 500;'>🎶 YouTube to MP3 Converter</a> - Extract audio from videos</li></ul><p><strong>Popular combinations:</strong> Many users download Instagram Reels and convert them to MP3 using our <a href='/youtube-to-mp3' style='color: #667eea; font-weight: 500;'>YouTube to MP3 tool</a> for background music.</p>"
            },
            {
                "title": "Platform Feature Comparison Matrix",
                "content": "<p><strong>Which platforms does our downloader support?</strong></p><table style='width:100%; border-collapse: collapse; margin: 20px 0; font-size: 13px;'><thead style='background: #667eea; color: white;'><tr><th style='padding: 12px; text-align: left; font-weight: 600;'>Platform</th><th style='padding: 12px; text-align: center; font-weight: 600;'>Video</th><th style='padding: 12px; text-align: center; font-weight: 600;'>Audio</th><th style='padding: 12px; text-align: center; font-weight: 600;'>HD Quality</th><th style='padding: 12px; text-align: center; font-weight: 600;'>Speed</th></tr></thead><tbody><tr style='background: #f8f9fa; border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>Instagram</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>⭐ 1080p</td><td style='padding: 12px; text-align: center;'>⚡</td></tr><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>TikTok</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>⭐ 720p</td><td style='padding: 12px; text-align: center;'>⚡⚡</td></tr><tr style='background: #f8f9fa; border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>YouTube</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>⭐⭐ 4K</td><td style='padding: 12px; text-align: center;'>⚡</td></tr><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>Facebook</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>⭐ 720p</td><td style='padding: 12px; text-align: center;'>⚡</td></tr><tr style='background: #f8f9fa; border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>Twitter (X)</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>⭐ 1080p</td><td style='padding: 12px; text-align: center;'>⚡⚡</td></tr><tr style='border-bottom: 1px solid #e2e8f0;'><td style='padding: 12px;'><strong>Pinterest</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>—</td><td style='padding: 12px; text-align: center;'>⭐ 720p</td><td style='padding: 12px; text-align: center;'>⚡</td></tr><tr style='background: #f8f9fa;'><td style='padding: 12px;'><strong>Snapchat</strong></td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>✅</td><td style='padding: 12px; text-align: center;'>⭐ 480p</td><td style='padding: 12px; text-align: center;'>⚡⚡</td></tr></tbody></table>"
            },
            {
                "title": "Visual Download Guide",
                "content": "<p><strong>Step-by-step visual guide:</strong></p><figure style='margin: 20px 0; text-align: center;'><img src='/static/images/guide-step-1-copy-link.png' alt='Step 1: Copy the video link from Instagram app or website - tap share button and select copy link option' style='max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0;' loading='lazy' /><figcaption style='font-size: 14px; color: #666; margin-top: 10px;'>Step 1: Copy the video link from your browser or app</figcaption></figure><figure style='margin: 20px 0; text-align: center;'><img src='/static/images/guide-step-2-paste.png' alt='Step 2: Paste the copied Instagram video link into the download input field above' style='max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0;' loading='lazy' /><figcaption style='font-size: 14px; color: #666; margin-top: 10px;'>Step 2: Paste the link in the input box</figcaption></figure><figure style='margin: 20px 0; text-align: center;'><img src='/static/images/guide-step-3-download.png' alt='Step 3: Click the Download button to start processing the Instagram video' style='max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0;' loading='lazy' /><figcaption style='font-size: 14px; color: #666; margin-top: 10px;'>Step 3: Click Download to process</figcaption></figure><figure style='margin: 20px 0; text-align: center;'><img src='/static/images/guide-step-4-format.png' alt='Step 4: Choose your preferred download format - MP4 video or MP3 audio from available options' style='max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0;' loading='lazy' /><figcaption style='font-size: 14px; color: #666; margin-top: 10px;'>Step 4: Select format and quality</figcaption></figure><figure style='margin: 20px 0; text-align: center;'><img src='/static/images/guide-step-5-save.png' alt='Step 5: Download completes automatically and video saves to your device downloads folder' style='max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0;' loading='lazy' /><figcaption style='font-size: 14px; color: #666; margin-top: 10px;'>Step 5: File downloads to your device</figcaption></figure>"
            }
        ])
    else:
        # Homepage only optimization
        extra_sections = [
            {
                "title": "Download Videos from Instagram, TikTok, YouTube & More",
                "content": (
                    "<p>Snap Reel Download is the best online tool to <strong>download instgram video</strong>, "
                    "save <strong>yotube video download</strong> content, and get TikTok videos without watermarks. "
                    "Paste any public link into the box above and save instantly in HD.</p>"
                    "<p>We never require login, and your privacy is protected — it’s 100% free and anonymous.</p>"
                )
            },
            {
                "title": "How to Use the Universal Video Downloader",
                "content": (
                    "<ol>"
                    "<li>Copy the video link from your browser or app.</li>"
                    "<li>Paste it into the box above.</li>"
                    "<li>Click Download and choose the format you want (MP4 or MP3).</li>"
                    "</ol>"
                    "<p>It works on any device (mobile, tablet, desktop), supporting <strong>facebook video download online</strong> and many more.</p>"
                )
            },
            {
                "title": "Key Features of Snap Reel Download",
                "content": (
                    "<ul>"
                    "<li>✅ Free & unlimited downloads (no signup required).</li>"
                    "<li>✅ Works on Android, iPhone, and desktop.</li>"
                    "<li>✅ Fast downloads in original quality (HD/4K).</li>"
                    "<li>✅ Supports Instagram (instgram), TikTok, YouTube (yotube), Facebook, and Twitter.</li>"
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
            # Generate the URL structure with language prefix for all languages
            prefix = f"/{lang}"
            full_path = f"{prefix}{path}"
            
            # Root path handling
            if full_path == f"/{lang}":
                full_path = f"/{lang}/"
            elif full_path.endswith("/") and full_path != f"/{lang}/":
                full_path = full_path.rstrip("/")
            
            # Create page data
            page_data = make_page_data(path, platform, brand_name, content_key, lang)
            
            # Setup hreflangs
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
