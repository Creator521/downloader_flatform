import os
import importlib.util

SEO_PAGES = {}

current_dir = os.path.dirname(os.path.abspath(__file__))
seo_pages_dir = os.path.join(current_dir, "seo_pages")

if os.path.exists(seo_pages_dir):
    files = os.listdir(seo_pages_dir)
    for filename in files:
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            file_path = os.path.join(seo_pages_dir, filename)
            
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    if hasattr(module, 'page_data'):
                        page_data = module.page_data
                        
                        route = page_data.get('route')
                        if route is not None:
                            # Remove the 'route' key to keep the dictionary exactly as original
                            del page_data['route']
                        else:
                            if module_name == "home":
                                route = "/"
                            else:
                                route = "/" + module_name.replace('_', '-')
                        
                        SEO_PAGES[route] = page_data
                except Exception as e:
                    pass

SEO_KEYWORDS = {

    # ─── 1. CORE — main money keywords (high volume) ──────────────────────────
    "core": [
        "video download",
        "video downloader",
        "free video downloader",
        "online video downloader",
        "youtube downloader",
        "instagram video downloader",
        "tiktok downloader",
        "facebook video downloader",
        "twitter video downloader",
        "reels downloader",
        "youtube to mp3",
    ],

    # ─── 2. HIGH INTENT — users ready to download right now ──────────────────
    "high_intent": [
        "download youtube video",
        "download instagram video",
        "download tiktok video",
        "download facebook video",
        "save video online",
        "download reels video",
        "download video without watermark",
        "download video free online",
        "mp4 video downloader",
        "hd video downloader",
    ],

    # ─── 3. LONG-TAIL GOLD — easy rank + ChatGPT picks ────────────────────────
    "long_tail": [
        "download youtube video without login",
        "download instagram video without watermark",
        "download tiktok video without watermark",
        "how to download instagram reels",
        "how to download youtube video in hd",
        "save reels to gallery",
        "download facebook reels without watermark",
        "youtube video downloader 4k free",
        "download video from link",
        "online video downloader free no login",
    ],

    # ─── 4. DEVICE BASED — mobile traffic ─────────────────────────────────────
    "device_based": [
        "download youtube video on android",
        "download youtube video on iphone",
        "instagram video download ios",
        "tiktok video download android",
        "save reels on iphone",
        "video downloader for pc",
        "video downloader for mobile",
        "download video on windows",
        "mac video downloader",
        "chrome video downloader",
    ],

    # ─── 5. QUESTION BASED — ChatGPT / AI favourite format ───────────────────
    "question_based": [
        "how to download youtube videos",
        "how to download instagram videos",
        "how to save reels without watermark",
        "how to download tiktok videos",
        "how to download facebook videos",
        "is it legal to download youtube videos",
        "best video downloader online",
        "fastest video downloader",
        "how to convert youtube to mp3",
        "how to save video from link",
    ],

    # ─── 6. PLATFORM-SPECIFIC: YouTube ───────────────────────────────────────
    "youtube": [
        "youtube video download free",
        "youtube downloader online",
        "youtube video saver",
        "youtube video download 1080p",
        "youtube shorts downloader",
        "save youtube video offline",
        "youtube to mp3 converter free",
        "youtube audio downloader",
        "download youtube shorts",
        "youtube video downloader no watermark",
    ],

    # ─── 7. PLATFORM-SPECIFIC: Instagram ─────────────────────────────────────
    "instagram": [
        "instagram reels downloader",
        "instagram video saver",
        "download instagram reels hd",
        "save instagram video",
        "instagram downloader online",
        "reels video download",
        "instagram photo downloader",
        "instagram story downloader",
        "download instagram reels without watermark",
        "instagram video download free",
    ],

    "instagram_reels": [
        "instagram reels downloader",
        "download instagram reels",
        "reels downloader",
        "instagram reel downloader",
        "download instagram reels without watermark",
        "save instagram reels to gallery",
        "instagram reels download hd",
        "instagram reels mp4 download",
        "download reels from instagram",
        "instagram reels downloader no login",
        "instagram reels downloader for iphone",
        "instagram reels downloader for android",
    ],

    "instagram_video": [
        "instagram video downloader",
        "download instagram video",
        "instagram video download",
        "instagram video saver",
        "download instagram videos hd",
        "instagram video download without watermark",
        "instagram video download mp4",
        "save instagram video to gallery",
        "instagram video downloader no login",
        "download videos from instagram",
        "instagram carousel video downloader",
        "instagram video downloader for pc",
    ],

    "instagram_story": [
        "instagram story downloader",
        "download instagram story",
        "instagram story saver",
        "save instagram story",
        "download instagram stories anonymously",
        "instagram story download by link",
        "anonymous instagram story downloader",
        "instagram story downloader no login",
        "download instagram story video",
        "download instagram story photo",
        "instagram highlights downloader",
        "save instagram stories to gallery",
    ],

    "instagram_photo": [
        "instagram photo downloader",
        "download instagram photos",
        "instagram image downloader",
        "save instagram photo",
        "instagram photo download hd",
        "instagram photo downloader full size",
        "instagram carousel downloader",
        "download instagram carousel photos",
        "instagram profile picture downloader",
        "instagram image download by link",
        "instagram photo downloader no login",
        "save instagram pictures online",
    ],

    # ─── 8. PLATFORM-SPECIFIC: TikTok ────────────────────────────────────────
    "tiktok": [
        "tiktok video downloader no watermark",
        "save tiktok video",
        "tiktok video saver",
        "tiktok downloader online",
        "download tiktok audio",
        "tiktok to mp3 converter",
        "save tiktok video hd",
        "download tiktok without watermark",
        "tiktok video download free",
        "remove tiktok watermark",
    ],

    "tiktok_mp3": [
        "tiktok to mp3",
        "tiktok mp3 downloader",
        "download tiktok audio",
        "tiktok audio downloader",
        "save tiktok sound",
        "download tiktok sound mp3",
        "tiktok sound downloader",
        "tiktok video to mp3",
        "extract audio from tiktok",
        "tiktok mp3 converter online",
    ],

    # ─── 9. PLATFORM-SPECIFIC: Facebook ──────────────────────────────────────
    "facebook": [
        "facebook video download",
        "facebook reels downloader",
        "save facebook video",
        "fb video downloader",
        "download facebook reels",
        "facebook video saver online",
        "download fb video hd",
        "facebook video download free",
        "fb reels download without watermark",
        "facebook video to mp4",
    ],

    "youtube_shorts": [
        "youtube shorts downloader",
        "download youtube shorts",
        "youtube shorts download",
        "save youtube shorts",
        "youtube shorts downloader hd",
        "download youtube shorts to mp4",
        "youtube shorts video downloader",
        "youtube shorts downloader no watermark",
        "download youtube shorts on iphone",
        "download youtube shorts on android",
    ],

    "youtube_mp3": [
        "youtube to mp3",
        "youtube to mp3 converter",
        "youtube mp3 downloader",
        "convert youtube to mp3",
        "youtube audio downloader",
        "youtube to mp3 320kbps",
        "youtube video to mp3",
        "download youtube audio",
        "free youtube to mp3 converter",
        "youtube mp3 converter online",
    ],

    "twitter": [
        "twitter video downloader",
        "x video downloader",
        "download twitter video",
        "download x video",
        "twitter video download hd",
        "x video download hd",
        "save twitter video",
        "save x video",
        "twitter to mp4",
        "download twitter gif",
        "twitter video downloader no login",
        "x video downloader online",
    ],

    "snapchat": [
        "snapchat video downloader",
        "download snapchat video",
        "snapchat story downloader",
        "snapchat spotlight downloader",
        "save snapchat video",
        "download snapchat spotlight",
        "snapchat video download hd",
        "snapchat downloader online",
        "snapchat video saver",
        "download snapchat story online",
    ],

    "pinterest": [
        "pinterest video downloader",
        "download pinterest video",
        "pinterest video download",
        "save pinterest video",
        "pinterest to mp4",
        "pinterest video downloader hd",
        "download pinterest video online",
        "pinterest downloader no login",
        "pinterest pin downloader",
        "save pinterest videos to gallery",
    ],

    # ─── 10. PLATFORM-SPECIFIC: Reddit ───────────────────────────────────────
    "alternatives": [
        "savefrom alternative",
        "snaptik alternative",
        "ssstiktok alternative",
        "best video downloader alternative",
        "best instagram reels downloader alternatives",
        "best tiktok downloader without watermark",
        "online video downloader alternative",
        "free video downloader alternative",
        "no app video downloader",
        "browser based video downloader",
        "video downloader no login",
        "safe video downloader online",
    ],

    "reddit": [
        "reddit video download",
        "reddit video downloader with audio",
        "download reddit video",
        "reddit video saver",
        "save video from reddit",
        "reddit to mp4",
        "reddit audio downloader",
        "reddit video download iphone",
    ],
}

# Convenience helper — flat list of ALL keywords (useful for meta tags etc.)
ALL_SEO_KEYWORDS: list[str] = [
    kw for group in SEO_KEYWORDS.values() for kw in group
]

# Per-page keyword mapping — maps route → most relevant keyword groups
PAGE_KEYWORD_MAP: dict[str, list[str]] = {
    "/":                        ["core", "high_intent", "question_based"],
    "/youtube":                 ["youtube", "high_intent", "device_based"],
    "/youtube-to-mp3":          ["youtube_mp3", "youtube", "question_based"],
    "/youtube-shorts-downloader": ["youtube_shorts", "youtube", "device_based"],
    "/reels":                   ["instagram_reels", "instagram", "high_intent", "long_tail"],
    "/video":                   ["instagram_video", "instagram", "device_based"],
    "/tiktok":                  ["tiktok", "high_intent", "long_tail"],
    "/tiktok-mp3-downloader":   ["tiktok_mp3", "tiktok"],
    "/facebook":                ["facebook", "high_intent"],
    "/twitter":                 ["twitter", "high_intent"],
    "/reddit":                  ["reddit", "high_intent"],
    "/snapchat":                ["snapchat", "high_intent"],
    "/photo":                   ["instagram_photo", "instagram"],
    "/story":                   ["instagram_story", "instagram"],
    "/pinterest":               ["pinterest", "high_intent"],
    "/savefrom-alternative":    ["alternatives", "core", "high_intent"],
    "/snaptik-alternative":     ["alternatives", "tiktok", "high_intent"],
    "/ssstiktok-alternative":   ["alternatives", "tiktok", "high_intent"],
    "/best-instagram-reels-downloader-alternatives": ["alternatives", "instagram_reels"],
    "/best-tiktok-downloader-without-watermark": ["alternatives", "tiktok", "long_tail"],
}
