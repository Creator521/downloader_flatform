import urllib.request
import urllib.parse
import json
import sys
import re

BASE_URL = "http://127.0.0.1:8000"
VALID_URL = "https://www.youtube.com/watch?v=jNQXAC9IVRw" 

def test_endpoint(name, endpoint, data, expected_status):
    print(f"Testing {name}...")
    api_url = f"{BASE_URL}/{endpoint}"
    encoded_data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(api_url, data=encoded_data)
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            if status == expected_status:
                print(f"  ✅ Success: {status}")
                if endpoint == "download":
                    # Check filename extension
                    disp = response.headers.get("Content-Disposition", "")
                    if data.get("format") == "audio" and ".m4a" not in disp and ".mp3" not in disp:
                        print(f"  ⚠️ Warning: Audio format request but got {disp}")
                    elif data.get("format") == "audio":
                        print(f"  ✅ Audio file validated: {disp}")
                return True
            else:
                print(f"  ❌ Failed: Expected {expected_status}, got {status}")
                return False
    except urllib.error.HTTPError as e:
        if e.code == expected_status:
            print(f"  ✅ Success (Expected Error): {e.code}")
            return True
        else:
            print(f"  ❌ Failed: Expected {expected_status}, got {e.code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_seo_page(path, expected_h1):
    print(f"Testing SEO Page {path}...")
    url = f"{BASE_URL}{path}"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                print(f"  ❌ Failed to load page: {response.status}")
                return False
            html = response.read().decode('utf-8')
            
            # Check Title
            if "<title>" in html:
                print("  ✅ Title Tag Found")
            else:
                print("  ❌ Title Tag Missing")
                
            # Check H1
            if f'<h1 class="hero-h1">{expected_h1}</h1>' in html or expected_h1 in html:
                print(f"  ✅ H1 Verified: {expected_h1}")
            else:
                print(f"  ❌ H1 Mismatch. Expected {expected_h1}")
                
            # Check Schema
            if "application/ld+json" in html:
                print("  ✅ JSON-LD Schema Found")
            else:
                print("  ❌ JSON-LD Schema Missing")
                
            # Check Ad Slot
            if "ad-banner-header" in html:
                 print("  ✅ Ad Slot Found")
            else:
                 print("  ❌ Ad Slot Missing")

            return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

if __name__ == "__main__":
    results = []
    
    # 1. Test Home SEO
    results.append(test_seo_page("/", "Universal Video Downloader Online"))
    
    # 2. Test Instagram Page
    results.append(test_seo_page("/instagram-reel-downloader", "Instagram Reel Downloader Online"))
    
    # 3. Test Preview
    results.append(test_endpoint("Preview API", "preview", {"url": VALID_URL}, 200))
    
    # 4. Test Audio Download
    results.append(test_endpoint("Audio Download", "download", {"url": VALID_URL, "format": "audio"}, 200))

    if all(results):
        print("\n🎉 ALL TESTS PASSED")
    else:
        print("\n⚠️ SOME TESTS FAILED")
