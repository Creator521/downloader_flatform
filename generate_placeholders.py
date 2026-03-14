#!/usr/bin/env python3
"""
Generate minimal placeholder PNG images using base64 encoded data.
These are simple 1x1 pixel placeholders that can be replaced with actual screenshots.
"""

import base64
import os

# Directory to save images
IMAGE_DIR = "frontend/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Minimal 1x1 gray PNG (can be replaced with actual images later)
# This is a valid PNG that displays as a gray placeholder
MINIMAL_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mN8/8DwHwAFBQIB"
    "lJDIkQAAAABJRU5ErkJggg=="
)

PLACEHOLDER_IMAGES = [
    "guide-step-1-copy-link.png",
    "guide-step-2-paste.png",
    "guide-step-3-download.png",
    "guide-step-4-format.png",
    "guide-step-5-save.png"
]

def create_placeholder_images():
    """Create minimal placeholder PNG images."""
    png_data = base64.b64decode(MINIMAL_PNG_BASE64)
    
    for filename in PLACEHOLDER_IMAGES:
        filepath = os.path.join(IMAGE_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(png_data)
        print(f"✅ Created: {filepath}")

if __name__ == "__main__":
    print("📸 Generating placeholder images...\n")
    create_placeholder_images()
    print(f"\n✅ All {len(PLACEHOLDER_IMAGES)} placeholder images created!")
    print("📝 Note: These are minimal placeholders. Replace with actual screenshots:")
    for img in PLACEHOLDER_IMAGES:
        print(f"   - {IMAGE_DIR}/{img}")
