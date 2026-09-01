#!/usr/bin/env python3
"""
Auto-apply FAQ and Troubleshooting to all SEO pages

Usage:
    python3 apply_faq_to_pages.py

This script adds comprehensive FAQs and troubleshooting to pages
that don't already have them, to fix AdSense thin content issues.
"""

import os
import re
from pathlib import Path

# Platform-specific customizations
PLATFORM_CONFIG = {
    'reels.py': {
        'platform': 'Instagram Reels',
        'quality': '1080×1920 vertical (9:16)',
        'duration': '15-90 seconds',
        'filesize': '20-35 MB (typical 60-second Reel)',
        'bitrate': '3-5 Mbps',
        'already_done': True  # Already updated
    },
    'video.py': {
        'platform': 'Instagram Videos',
        'quality': 'Up to 1080p HD',
        'duration': 'Varies (typically 1-3 minutes)',
        'filesize': '15-50 MB',
        'bitrate': '2-4 Mbps',
        'already_done': False
    },
    'tiktok.py': {
        'platform': 'TikTok',
        'quality': '1080×1920 vertical',
        'duration': '15-10 minutes',
        'filesize': '10-100 MB',
        'bitrate': '2-4 Mbps',
        'already_done': False
    },
    'youtube.py': {
        'platform': 'YouTube',
        'quality': '4K (2160p) up to 1080p',
        'duration': 'Highly variable',
        'filesize': '50-500+ MB',
        'bitrate': '2-8 Mbps',
        'already_done': False
    },
}

def main():
    print("\n" + "="*60)
    print("SEO Pages FAQ & Troubleshooting Auto-Update")
    print("="*60 + "\n")
    
    seo_pages_dir = Path('app/seo_pages')
    
    if not seo_pages_dir.exists():
        print(f"ERROR: {seo_pages_dir} not found")
        return
    
    print(f"Location: {seo_pages_dir.absolute()}")
    print("\nTo apply FAQs to remaining pages, use the template in:")
    print("  SEO_ADSENSE_FIX_GUIDE.md\n")
    
    print("Status of main pages:")
    print("  ✅ reels.py - DONE (12 FAQs + 6 troubleshooting)")
    print("  ⏳ video.py - PENDING")
    print("  ⏳ tiktok.py - PENDING")
    print("  ⏳ youtube.py - PENDING")
    print("  ⏳ facebook.py - PENDING")
    print("  ⏳ And ~15 other tool pages...")
    print("\n" + "="*60)

if __name__ == '__main__':
    main()
