#!/usr/bin/env python3
"""
Audit all image references in HTML files and verify they exist.
For missing images, prepare fetch commands from the original site.
"""

import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse, urljoin
import json

# Configuration
ROOT_DIR = Path('/Users/asiboro/Sources/Work/23centuryid')
ASSETS_IMG_DIR = ROOT_DIR / 'assets' / 'img'
ORIGIN_URL = 'https://23c.jp'

# Patterns to find image references
IMAGE_PATTERNS = [
    r'src=["\']([^"\']*\.(?:svg|png|jpg|jpeg|webp|gif))["\']',
    r'href=["\']([^"\']*\.(?:svg|png|jpg|jpeg|webp|gif))["\']',
    r'data-[^=]*=["\']([^"\']*\.(?:svg|png|jpg|jpeg|webp|gif))["\']',
]

def get_all_html_files():
    """Get all HTML files in the workspace."""
    html_files = []
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip fetched_pages, as those are archived
        if 'fetched_pages' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    return sorted(html_files)

def extract_image_references(html_file):
    """Extract all image references from an HTML file."""
    references = set()
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            for pattern in IMAGE_PATTERNS:
                matches = re.findall(pattern, content, re.IGNORECASE)
                references.update(matches)
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
    return references

def normalize_path(path):
    """Normalize image path to local path."""
    if path.startswith('/'):
        return path
    if path.startswith('http'):
        # Extract just the path component
        parsed = urlparse(path)
        return parsed.path
    return '/' + path

def check_image_exists(img_path):
    """Check if image file exists locally."""
    normalized = normalize_path(img_path)
    
    # For root-based paths
    if normalized.startswith('/assets/img/'):
        local_path = ROOT_DIR / normalized[1:]  # Remove leading slash
    else:
        return None  # Can't determine local path
    
    return local_path if local_path.exists() else None

def get_fetch_command(img_path, filename):
    """Generate fetch command for missing image."""
    # Map local paths to origin paths
    if img_path.startswith('/assets/img/'):
        # Figure out the original path
        filename_only = img_path.split('/')[-1]
        
        # Common patterns for original paths
        origin_paths = [
            f'/wp-content/themes/_23c/img/common/{filename_only}',
            f'/wp-content/uploads/{filename_only}',
            f'/wp-content/themes/_23c/{filename_only}',
        ]
        
        for origin_path in origin_paths:
            return f"curl -s \"{ORIGIN_URL}{origin_path}\" -o \"{ROOT_DIR / img_path[1:]}\""
    
    return None

def main():
    print("=" * 80)
    print("IMAGE REFERENCE AUDIT")
    print("=" * 80)
    
    html_files = get_all_html_files()
    print(f"\nScanning {len(html_files)} HTML files...")
    
    all_references = {}
    missing_images = {}
    existing_images = {}
    
    # Collect all image references
    for html_file in html_files:
        references = extract_image_references(html_file)
        for ref in references:
            if ref not in all_references:
                all_references[ref] = []
            all_references[ref].append(str(html_file.relative_to(ROOT_DIR)))
    
    print(f"\nFound {len(all_references)} unique image references\n")
    
    # Check which exist and which don't
    for img_ref in sorted(all_references.keys()):
        normalized = normalize_path(img_ref)
        
        # Only check /assets/img references (ignore CDN, external URLs)
        if not normalized.startswith('/assets/'):
            continue
            
        local_file = check_image_exists(normalized)
        
        if local_file:
            existing_images[img_ref] = {
                'path': normalized,
                'files': len(all_references[img_ref]),
                'local_path': str(local_file),
                'size': local_file.stat().st_size
            }
        else:
            missing_images[img_ref] = {
                'path': normalized,
                'files_count': len(all_references[img_ref]),
                'found_in': all_references[img_ref][:3],  # First 3 files
                'origin_url': f"{ORIGIN_URL}/wp-content/uploads/{img_ref.split('/')[-1]}"
            }
    
    # Report
    print(f"\n✅ EXISTING IMAGES: {len(existing_images)}")
    for img_ref in sorted(existing_images.keys()):
        info = existing_images[img_ref]
        print(f"  {img_ref} ({info['size']} bytes, used in {info['files']} files)")
    
    print(f"\n❌ MISSING IMAGES: {len(missing_images)}")
    if missing_images:
        for img_ref in sorted(missing_images.keys()):
            info = missing_images[img_ref]
            print(f"\n  {img_ref}")
            print(f"    Used in {info['files_count']} files")
            print(f"    Example files: {', '.join(info['found_in'][:2])}")
            print(f"    Origin: {info['origin_url']}")
    else:
        print("  ✅ No missing images!")
    
    print("\n" + "=" * 80)
    print(f"SUMMARY: {len(existing_images)} existing, {len(missing_images)} missing")
    print("=" * 80)
    
    return missing_images

if __name__ == '__main__':
    missing = main()
    if missing:
        print("\n⚠️  Found missing images. Run fetch_missing_images.py to download them.")
