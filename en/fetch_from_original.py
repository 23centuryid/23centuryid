#!/usr/bin/env python3
"""
Fetch missing images and pages from https://23c.jp/ (original Japanese site)
"""
import os
import re
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import urljoin, urlparse
import time

def fetch_image(image_url, save_path):
    """Download an image from a URL and save it locally"""
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Set a user agent to avoid being blocked
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        req = urllib.request.Request(image_url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(save_path, 'wb') as out_file:
                out_file.write(response.read())
        return True
    except Exception as e:
        print(f"    Failed to download {image_url}: {e}")
        return False

def fetch_page(page_url, save_path):
    """Download a page from the original Japanese site"""
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        req = urllib.request.Request(page_url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
        
        # Fix image paths and links for local use
        content = fix_html_for_local_use(content)
        
        with open(save_path, 'w', encoding='utf-8') as out_file:
            out_file.write(content)
        return True
    except Exception as e:
        print(f"    Failed to download {page_url}: {e}")
        return False

def fix_html_for_local_use(html_content):
    """Fix HTML content to work with local file paths"""
    # This would need more sophisticated handling
    # For now, just ensure it has proper structure
    return html_content

def fetch_missing_images():
    """Fetch missing images from the original site"""
    base_url = 'https://23c.jp'
    img_dir = '/Users/asiboro/Sources/Work/23centuryid/assets/img'
    
    # Images that need to be fetched from the original site
    missing_images = {
        # About section
        'about.webp': '/wp-content/uploads/2025/03/about.webp',
        'about_img_001.png': '/wp-content/themes/_23c/img/about/about_img_001.png',
        'about_img_002.png': '/wp-content/themes/_23c/img/about/about_img_002.png',
        'about_img_003.png': '/wp-content/themes/_23c/img/about/about_img_003.png',
        'about_img_004.png': '/wp-content/themes/_23c/img/about/about_img_004.png',
        'about_img_005.png': '/wp-content/themes/_23c/img/about/about_img_005.png',
        'about_img_006.png': '/wp-content/themes/_23c/img/about/about_img_006.png',
        
        # Gallery
        'gallery_img_001.webp': '/wp-content/themes/_23c/img/garally/gallery_img_001.webp',
        'gallery_img_002.webp': '/wp-content/themes/_23c/img/garally/gallery_img_002.webp',
        'gallery_img_003.webp': '/wp-content/themes/_23c/img/garally/gallery_img_003.webp',
        'gallery_img_004.webp': '/wp-content/themes/_23c/img/garally/gallery_img_004.webp',
        'gallery_img_005.webp': '/wp-content/themes/_23c/img/garally/gallery_img_005.webp',
        'gallery_img_006.webp': '/wp-content/themes/_23c/img/garally/gallery_img_006.webp',
        'gallery_img_007.webp': '/wp-content/themes/_23c/img/garally/gallery_img_007.webp',
        'gallery_img_008.webp': '/wp-content/themes/_23c/img/garally/gallery_img_008.webp',
        'gallery_img_009.webp': '/wp-content/themes/_23c/img/garally/gallery_img_009.webp',
        
        # Flow and process
        'flow_img_001.webp': '/wp-content/themes/_23c/img/flow/flow_img_001.webp',
        'flow_img_002.webp': '/wp-content/themes/_23c/img/flow/flow_img_002.webp',
        'first_img_004.webp': '/wp-content/themes/_23c/img/top/first_img_004.webp',
        'first_img_005.webp': '/wp-content/themes/_23c/img/top/first_img_005.webp',
        
        # Cell laboratory
        'cell-laboratory.webp': '/wp-content/uploads/2025/03/cell-laboratory.webp',
    }
    
    print("=" * 70)
    print("Fetching missing images from https://23c.jp/")
    print("=" * 70)
    
    downloaded = 0
    failed = 0
    
    for filename, image_path in missing_images.items():
        save_path = os.path.join(img_dir, filename)
        
        if os.path.exists(save_path):
            print(f"  - {filename} already exists")
            continue
        
        image_url = urljoin(base_url, image_path)
        print(f"  Fetching {filename}...")
        
        if fetch_image(image_url, save_path):
            downloaded += 1
            print(f"    ✓ Downloaded {filename}")
        else:
            failed += 1
            print(f"    ✗ Failed to download {filename}")
        
        time.sleep(0.5)  # Be polite to the server
    
    print(f"\n  Downloaded: {downloaded}, Failed: {failed}")
    return downloaded, failed

def fetch_missing_pages():
    """Fetch missing content pages from the original site"""
    base_url = 'https://23c.jp'
    root_dir = '/Users/asiboro/Sources/Work/23centuryid'
    
    # Pages to fetch from the original Japanese site
    missing_pages = {
        'contact': '/contact/',
        'price': '/price/',
        'disclaimer': '/disclaimer/',
        'privacy-policy': '/privacy-policy/',
        'terms-of-service': '/terms-of-service/',
        'operation-company': '/operation-company/',
        'entry-list': '/entry-list/',
        'malaysia-stemcell': '/malaysia-stemcell/',
        'whartons-jelly-msc': '/whartons-jelly-msc/',
        'voice': '/voice/',
        'case-studies': '/case-studies/',
        'column': '/column/',
    }
    
    print("\n" + "=" * 70)
    print("Fetching missing pages from https://23c.jp/")
    print("=" * 70)
    
    downloaded = 0
    failed = 0
    
    for page_name, page_path in missing_pages.items():
        local_path = os.path.join(root_dir, page_name, 'index.html')
        
        if os.path.exists(local_path):
            print(f"  - {page_name}/index.html already exists")
            continue
        
        page_url = urljoin(base_url, page_path)
        print(f"  Fetching {page_name}...")
        
        if fetch_page(page_url, local_path):
            downloaded += 1
            print(f"    ✓ Downloaded {page_name}")
        else:
            failed += 1
            print(f"    ✗ Failed to download {page_name}")
        
        time.sleep(1)  # Be polite to the server
    
    print(f"\n  Downloaded: {downloaded}, Failed: {failed}")
    return downloaded, failed

def fetch_treatment_pages():
    """Fetch treatment information pages from the original site"""
    base_url = 'https://23c.jp'
    root_dir = '/Users/asiboro/Sources/Work/23centuryid'
    
    # Treatment and condition pages
    treatment_pages = {
        'treatable/msc-therapy-alzheimers': '/treatable/msc-therapy-alzheimers/',
        'treatable/msc-therapy-amd': '/treatable/msc-therapy-amd/',
        'treatable/msc-therapy-asd': '/treatable/msc-therapy-asd/',
        'treatable/msc-therapy-blindness': '/treatable/msc-therapy-blindness/',
        'treatable/msc-therapy-chronic-pain': '/treatable/msc-therapy-chronic-pain/',
        'treatable/msc-therapy-diabetes': '/treatable/msc-therapy-diabetes/',
        'treatable/msc-therapy-liver-cirrhosis': '/treatable/msc-therapy-liver-cirrhosis/',
        'treatable/msc-therapy-osteoarthritis': '/treatable/msc-therapy-osteoarthritis/',
        'treatable/msc-therapy-parkinsons-disease': '/treatable/msc-therapy-parkinsons-disease/',
        'treatable/msc-therapy-post-mi-heart-failure': '/treatable/msc-therapy-post-mi-heart-failure/',
        'treatable/msc-therapy-post-stroke-sequelae': '/treatable/msc-therapy-post-stroke-sequelae/',
        'treatable/msc-therapy-renal-failure': '/treatable/msc-therapy-renal-failure/',
        'treatable/msc-therapy-snhl': '/treatable/msc-therapy-snhl/',
        'treatable/msc-therapy-spinal-cord-injury': '/treatable/msc-therapy-spinal-cord-injury/',
        'treatable/msc-treatment-rheumatoid-arthritis': '/treatable/msc-treatment-rheumatoid-arthritis/',
        'msc': '/msc/',
        'news/globalhealth-award-2025': '/news/globalhealth-award-2025/',
        'news/unauthorized-cgtp-warning': '/news/unauthorized-cgtp-warning/',
    }
    
    print("\n" + "=" * 70)
    print("Fetching treatment and condition pages from https://23c.jp/")
    print("=" * 70)
    
    downloaded = 0
    failed = 0
    
    for page_name, page_path in treatment_pages.items():
        local_path = os.path.join(root_dir, page_name, 'index.html')
        
        if os.path.exists(local_path):
            print(f"  - {page_name}/index.html already exists")
            continue
        
        page_url = urljoin(base_url, page_path)
        print(f"  Fetching {page_name}...")
        
        if fetch_page(page_url, local_path):
            downloaded += 1
            print(f"    ✓ Downloaded {page_name}")
        else:
            failed += 1
            print(f"    ✗ Failed to download {page_name}")
        
        time.sleep(1)  # Be polite to the server
    
    print(f"\n  Downloaded: {downloaded}, Failed: {failed}")
    return downloaded, failed

def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  23Century.id - Fetch Missing Assets from https://23c.jp/".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    img_downloaded, img_failed = fetch_missing_images()
    page_downloaded, page_failed = fetch_missing_pages()
    treat_downloaded, treat_failed = fetch_treatment_pages()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Images downloaded: {img_downloaded}, Failed: {img_failed}")
    print(f"Pages downloaded: {page_downloaded}, Failed: {page_failed}")
    print(f"Treatment pages downloaded: {treat_downloaded}, Failed: {treat_failed}")
    print(f"\nTotal downloaded: {img_downloaded + page_downloaded + treat_downloaded}")
    print(f"Total failed: {img_failed + page_failed + treat_failed}")
    print("=" * 70)

if __name__ == '__main__':
    main()
