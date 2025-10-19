#!/usr/bin/env python3
"""
Fetch missing image files from https://23c.jp/wp-content/uploads/
This script downloads the actual image files referenced in the HTML files.
"""

import os
import urllib.request
import urllib.error
from pathlib import Path

# Missing images found by link_analyzer.py
MISSING_IMAGES = [
    # News/content images
    {
        "local": "cambodian-boy-nk-cell-therapy-23c-1024x379.png",
        "remote": "https://23c.jp/wp-content/uploads/2024/11/cambodian-boy-nk-cell-therapy-23c-1024x379.png"
    },
    {
        "local": "globalhealth-award-2025-1-1024x691.jpg",
        "remote": "https://23c.jp/wp-content/uploads/2025/04/globalhealth-award-2025-1-1024x691.jpg"
    },
    {
        "local": "logo_white_001.svg",
        "remote": "https://23c.jp/wp-content/themes/_23c/img/common/logo_white_001.svg"
    },
    {
        "local": "menu_img_001.webp",
        "remote": "https://23c.jp/wp-content/themes/_23c/img/common/menu/menu_img_001.webp"
    },
    {
        "local": "menu_img_002.webp",
        "remote": "https://23c.jp/wp-content/themes/_23c/img/common/menu/menu_img_002.webp"
    },
    {
        "local": "menu_img_003.webp",
        "remote": "https://23c.jp/wp-content/themes/_23c/img/common/menu/menu_img_003.webp"
    },
    {
        "local": "menu_img_004.webp",
        "remote": "https://23c.jp/wp-content/themes/_23c/img/common/menu/menu_img_004.webp"
    },
    {
        "local": "misunderstandings-about-stem-cells-1024x512.webp",
        "remote": "https://23c.jp/wp-content/uploads/2024/12/misunderstandings-about-stem-cells-1024x512.webp"
    },
    {
        "local": "movie_img_001.webp",
        "remote": "https://23c.jp/wp-content/themes/_23c/img/common/movie_img_001.webp"
    },
    {
        "local": "movie_img_002.webp",
        "remote": "https://23c.jp/wp-content/themes/_23c/img/common/movie_img_002.webp"
    },
    {
        "local": "mv_txt_001_sp.svg",
        "remote": "https://23c.jp/wp-content/themes/_23c/img/common/mv_txt_001_sp.svg"
    },
    {
        "local": "no_img_001-1024x538.png",
        "remote": "https://23c.jp/wp-content/uploads/2024/11/no_img_001-1024x538.png"
    },
    {
        "local": "process_img_001.webp",
        "remote": "https://23c.jp/wp-content/themes/_23c/img/common/process_img_001.webp"
    },
    {
        "local": "process_img_002.webp",
        "remote": "https://23c.jp/wp-content/themes/_23c/img/common/process_img_002.webp"
    },
    {
        "local": "stem-cell-treatment-risk-countries-1024x439.webp",
        "remote": "https://23c.jp/wp-content/uploads/2024/12/stem-cell-treatment-risk-countries-1024x439.webp"
    },
    {
        "local": "stem-cell-vision-recovery-1024x640.jpg",
        "remote": "https://23c.jp/wp-content/uploads/2024/11/stem-cell-vision-recovery-1024x640.jpg"
    },
    {
        "local": "unauthorized-cgtp-warning-1024x554.webp",
        "remote": "https://23c.jp/wp-content/uploads/2025/01/unauthorized-cgtp-warning-1024x554.webp"
    },
    {
        "local": "whartons-jelly-msc-1024x618.webp",
        "remote": "https://23c.jp/wp-content/uploads/2024/11/whartons-jelly-msc-1024x618.webp"
    },
    {
        "local": "whartons-jelly-secretome-seminar-2025-1024x538.webp",
        "remote": "https://23c.jp/wp-content/uploads/2025/04/whartons-jelly-secretome-seminar-2025-1024x538.webp"
    },
    # Medical treatment images
    {
        "local": "msc-treatment-rheumatoid-arthritis-1.webp",
        "remote": "https://23c.jp/wp-content/uploads/2025/04/msc-treatment-rheumatoid-arthritis-1.webp"
    },
    {
        "local": "msc-treatment-rheumatoid-arthritis-2.webp",
        "remote": "https://23c.jp/wp-content/uploads/2025/04/msc-treatment-rheumatoid-arthritis-2.webp"
    },
]

def fetch_image(remote_url, local_path):
    """Download an image from remote URL to local path"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        print(f"    Fetching: {remote_url}")
        req = urllib.request.Request(remote_url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(local_path, 'wb') as out_file:
                out_file.write(response.read())
        
        file_size = os.path.getsize(local_path)
        print(f"    ✓ Downloaded {local_path} ({file_size:,} bytes)")
        return True
        
    except urllib.error.HTTPError as e:
        print(f"    ✗ HTTP Error {e.code}: {remote_url}")
        return False
    except urllib.error.URLError as e:
        print(f"    ✗ URL Error: {e.reason}")
        return False
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False


def main():
    print("\n" + "="*80)
    print("Fetching Missing Images from https://23c.jp/")
    print("="*80 + "\n")
    
    img_dir = Path("assets/img")
    img_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded = 0
    failed = 0
    skipped = 0
    
    for img_info in MISSING_IMAGES:
        local_path = img_dir / img_info["local"]
        
        # Skip if already exists
        if local_path.exists():
            print(f"  ⊘ {img_info['local']} already exists")
            skipped += 1
            continue
        
        # Fetch the image
        if fetch_image(img_info["remote"], str(local_path)):
            downloaded += 1
        else:
            failed += 1
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Downloaded: {downloaded}")
    print(f"Failed: {failed}")
    print(f"Skipped (already exist): {skipped}")
    print(f"Total: {len(MISSING_IMAGES)}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
