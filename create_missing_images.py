#!/usr/bin/env python3
"""
Create placeholder WebP/PNG images for missing assets,
and update HTML files to reference them from /assets/img/
"""

import os
import struct
import zlib
from pathlib import Path
import re

def create_png_placeholder(width=1024, height=512, text="Image"):
    """Create a simple PNG placeholder image"""
    # PNG header
    png_header = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk (image header)
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    ihdr_chunk = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
    
    # Create image data (gray background)
    raw_data = b''
    gray = struct.pack('BBB', 200, 200, 200)
    for y in range(height):
        raw_data += b'\x00'  # Filter type for each scanline
        for x in range(width):
            raw_data += gray
    
    # Compress the data
    compressed = zlib.compress(raw_data)
    
    # IDAT chunk (image data)
    idat_crc = zlib.crc32(b'IDAT' + compressed) & 0xffffffff
    idat_chunk = struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', idat_crc)
    
    # IEND chunk (image end)
    iend_crc = zlib.crc32(b'IEND') & 0xffffffff
    iend_chunk = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
    
    return png_header + ihdr_chunk + idat_chunk + iend_chunk

def create_placeholder_images():
    """Create placeholder images for missing assets"""
    
    missing_images = [
        ("cambodian-boy-nk-cell-therapy-23c-1024x379.png", 1024, 379),
        ("globalhealth-award-2025-1-1024x691.jpg", 1024, 691),
        ("menu_img_001.webp", 800, 600),
        ("menu_img_002.webp", 800, 600),
        ("menu_img_003.webp", 800, 600),
        ("menu_img_004.webp", 800, 600),
        ("misunderstandings-about-stem-cells-1024x512.webp", 1024, 512),
        ("movie_img_001.webp", 800, 600),
        ("movie_img_002.webp", 800, 600),
        ("mv_txt_001_sp.svg", 0, 0),  # Will create as SVG
        ("no_img_001-1024x538.png", 1024, 538),
        ("process_img_001.webp", 800, 600),
        ("process_img_002.webp", 800, 600),
        ("stem-cell-treatment-risk-countries-1024x439.webp", 1024, 439),
        ("stem-cell-vision-recovery-1024x640.jpg", 1024, 640),
        ("unauthorized-cgtp-warning-1024x554.webp", 1024, 554),
        ("whartons-jelly-msc-1024x618.webp", 1024, 618),
        ("whartons-jelly-secretome-seminar-2025-1024x538.webp", 1024, 538),
    ]
    
    img_dir = Path("assets/img")
    img_dir.mkdir(parents=True, exist_ok=True)
    
    created = 0
    for img_name, width, height in missing_images:
        img_path = img_dir / img_name
        
        if img_path.exists():
            print(f"  ⊘ {img_name} already exists")
            continue
        
        if img_name.endswith(".svg"):
            # Create simple SVG placeholder
            svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="100" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="100" fill="#c8c8c8"/>
  <text x="100" y="55" text-anchor="middle" font-size="12" fill="#666">SVG Image</text>
</svg>'''
            img_path.write_text(svg_content)
            print(f"  ✓ Created {img_name} (SVG placeholder)")
            created += 1
        elif img_name.endswith(".png"):
            # Create PNG placeholder
            png_data = create_png_placeholder(width, height, img_name)
            img_path.write_bytes(png_data)
            print(f"  ✓ Created {img_name} ({len(png_data)} bytes)")
            created += 1
        else:
            # For WEBP and JPG, create PNG with appropriate name
            # Note: These should ideally be WEBP/JPG, but PNG is easier to generate
            png_data = create_png_placeholder(width, height, img_name)
            img_path.write_bytes(png_data)
            print(f"  ✓ Created {img_name} ({len(png_data)} bytes)")
            created += 1
    
    print(f"\nTotal placeholder images created: {created}\n")
    return created


def update_html_to_use_local_images():
    """Update HTML files to use local /assets/img/ instead of WordPress paths"""
    
    # Mapping of image names to local paths
    image_mappings = {
        "logo_white_001.svg": ("/assets/img/logo_white_001.svg", "/wp-content/themes/_23c/img/common/logo_white_001.svg"),
        "menu_img_001.webp": ("/assets/img/menu_img_001.webp", "/wp-content/themes/_23c/img/common/menu/menu_img_001.webp"),
        "menu_img_002.webp": ("/assets/img/menu_img_002.webp", "/wp-content/themes/_23c/img/common/menu/menu_img_002.webp"),
        "menu_img_003.webp": ("/assets/img/menu_img_003.webp", "/wp-content/themes/_23c/img/common/menu/menu_img_003.webp"),
        "menu_img_004.webp": ("/assets/img/menu_img_004.webp", "/wp-content/themes/_23c/img/common/menu/menu_img_004.webp"),
        "movie_img_001.webp": ("/assets/img/movie_img_001.webp", "/wp-content/themes/_23c/img/common/movie_img_001.webp"),
        "movie_img_002.webp": ("/assets/img/movie_img_002.webp", "/wp-content/themes/_23c/img/common/movie_img_002.webp"),
        "mv_txt_001_sp.svg": ("/assets/img/mv_txt_001_sp.svg", "/wp-content/themes/_23c/img/common/mv_txt_001_sp.svg"),
        "process_img_001.webp": ("/assets/img/process_img_001.webp", "/wp-content/themes/_23c/img/common/process_img_001.webp"),
        "process_img_002.webp": ("/assets/img/process_img_002.webp", "/wp-content/themes/_23c/img/common/process_img_002.webp"),
    }
    
    print("Updating HTML files to reference local images...\n")
    
    files_updated = 0
    replacements_made = 0
    
    for root, dirs, files in os.walk("."):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in [".git", "node_modules", "__pycache__"]]
        
        for file in files:
            if not file.endswith(".html"):
                continue
            
            filepath = os.path.join(root, file)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                updated_content = content
                made_change = False
                
                # Replace WordPress image paths with local paths
                for img_name, (local_path, wp_path) in image_mappings.items():
                    if wp_path in updated_content:
                        updated_content = updated_content.replace(wp_path, local_path)
                        made_change = True
                        replacements_made += 1
                
                if made_change:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"  ✓ Updated {filepath}")
                    files_updated += 1
                    
            except Exception as e:
                print(f"  ✗ Error processing {filepath}: {e}")
    
    print(f"\nTotal files updated: {files_updated}")
    print(f"Total replacements made: {replacements_made}\n")
    return files_updated


def main():
    print("\n" + "="*80)
    print("Creating Missing Image Assets")
    print("="*80 + "\n")
    
    # Create placeholder images
    created = create_placeholder_images()
    
    # Update HTML files
    updated = update_html_to_use_local_images()
    
    print("="*80)
    print("COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
