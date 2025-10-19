#!/usr/bin/env python3
"""
Fix all broken links in HTML files by replacing WordPress paths with local assets.
"""
import os
import re
from pathlib import Path

def find_all_html_files(root_dir):
    """Find all HTML files in the directory tree."""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '.venv', '__pycache__'}]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def create_mapping():
    """Create mapping from WordPress paths to local asset paths."""
    mapping = {}
    
    # Map wp-content/uploads images to /assets/img/
    wp_upload_mappings = {
        # Logo
        '/wp-content/uploads/2025/03/logo_black_001.svg': '/assets/img/logo_black_001.svg',
        
        # Site icons
        '/wp-content/uploads/2025/03/cropped-site-icon-32x32.png': '/assets/img/cropped-site-icon-32x32.png',
        '/wp-content/uploads/2025/03/cropped-site-icon-192x192.png': '/assets/img/cropped-site-icon-192x192.png',
        '/wp-content/uploads/2025/03/cropped-site-icon-180x180.png': '/assets/img/cropped-site-icon-180x180.png',
        '/wp-content/uploads/2025/03/cropped-site-icon-270x270.png': '/assets/img/cropped-site-icon-270x270.png',
        
        # OGP images
        '/wp-content/uploads/2025/03/ogp.png': '/assets/img/ogp.png',
        
        # Main content images
        '/wp-content/uploads/2025/03/about.webp': '/assets/img/about.webp',
        '/wp-content/uploads/2025/03/cell-laboratory.webp': '/assets/img/cell-laboratory.webp',
        '/wp-content/uploads/2025/02/difference-secretome-exosome-1024x675.webp': '/assets/img/difference-secretome-exosome-1024x675.webp',
        '/wp-content/uploads/2025/03/misunderstandings-about-stem-cells-1024x512.webp': '/assets/img/misunderstandings-about-stem-cells-1024x512.webp',
        '/wp-content/uploads/2025/03/stem-cell-treatment-risk-countries-1024x439.webp': '/assets/img/stem-cell-treatment-risk-countries-1024x439.webp',
        '/wp-content/uploads/2025/03/whartons-jelly-msc-1024x618.webp': '/assets/img/whartons-jelly-msc-1024x618.webp',
        '/wp-content/uploads/2025/03/no_img_001-1024x538.png': '/assets/img/no_img_001-1024x538.png',
        '/wp-content/uploads/2025/03/whartons-jelly-secretome-seminar-2025-1024x538.webp': '/assets/img/whartons-jelly-secretome-seminar-2025-1024x538.webp',
        '/wp-content/uploads/2025/04/conversation-2025-04-03.jpg': '/assets/img/conversation-2025-04-03.jpg',
        '/wp-content/uploads/2025/04/unauthorized-cgtp-warning-1024x554.webp': '/assets/img/unauthorized-cgtp-warning-1024x554.webp',
        '/wp-content/uploads/2025/06/globalhealth-award-2025-1-1024x691.jpg': '/assets/img/globalhealth-award-2025-1-1024x691.jpg',
        '/wp-content/uploads/2025/08/stem-cell-vision-recovery-1024x640.jpg': '/assets/img/stem-cell-vision-recovery-1024x640.jpg',
        '/wp-content/uploads/2025/10/cambodian-boy-nk-cell-therapy-23c-1024x379.png': '/assets/img/cambodian-boy-nk-cell-therapy-23c-1024x379.png',
    }
    mapping.update(wp_upload_mappings)
    
    # Map wp-content/themes images to /assets/img/
    wp_theme_img_mappings = {
        # Common images
        '/wp-content/themes/_23c/img/common/logo_white_001.svg': '/assets/img/logo_white_001.svg',
        
        # Top section images
        '/wp-content/themes/_23c/img/top/mv_img_001.webp': '/assets/img/mv_img_001.webp',
        '/wp-content/themes/_23c/img/top/mv_txt_001_pc.svg': '/assets/img/mv_txt_001_pc.svg',
        '/wp-content/themes/_23c/img/top/mv_txt_001_sp.svg': '/assets/img/mv_txt_001_sp.svg',
        '/wp-content/themes/_23c/img/top/reason_img_001.webp': '/assets/img/reason_img_001.webp',
        '/wp-content/themes/_23c/img/top/reason_img_002.webp': '/assets/img/reason_img_002.webp',
        '/wp-content/themes/_23c/img/top/reason_img_003.webp': '/assets/img/reason_img_003.webp',
        '/wp-content/themes/_23c/img/top/reason_img_004.webp': '/assets/img/reason_img_004.webp',
        '/wp-content/themes/_23c/img/top/reason_img_005.webp': '/assets/img/reason_img_005.webp',
        '/wp-content/themes/_23c/img/top/reason_img_006.webp': '/assets/img/reason_img_006.webp',
        '/wp-content/themes/_23c/img/top/process_img_001.webp': '/assets/img/process_img_001.webp',
        '/wp-content/themes/_23c/img/top/process_img_002.webp': '/assets/img/process_img_002.webp',
        '/wp-content/themes/_23c/img/top/first_img_004.webp': '/assets/img/first_img_004.webp',
        '/wp-content/themes/_23c/img/top/first_img_005.webp': '/assets/img/first_img_005.webp',
        '/wp-content/themes/_23c/img/top/menu_img_001.webp': '/assets/img/menu_img_001.webp',
        '/wp-content/themes/_23c/img/top/menu_img_003.webp': '/assets/img/menu_img_003.webp',
        '/wp-content/themes/_23c/img/top/menu_img_004.webp': '/assets/img/menu_img_004.webp',
        '/wp-content/themes/_23c/img/top/movie_img_001.webp': '/assets/img/movie_img_001.webp',
        '/wp-content/themes/_23c/img/top/movie_img_002.webp': '/assets/img/movie_img_002.webp',
        
        # About section images
        '/wp-content/themes/_23c/img/about/about_img_001.png': '/assets/img/about_img_001.png',
        '/wp-content/themes/_23c/img/about/about_img_002.png': '/assets/img/about_img_002.png',
        '/wp-content/themes/_23c/img/about/about_img_003.png': '/assets/img/about_img_003.png',
        '/wp-content/themes/_23c/img/about/about_img_004.png': '/assets/img/about_img_004.png',
        '/wp-content/themes/_23c/img/about/about_img_005.png': '/assets/img/about_img_005.png',
        '/wp-content/themes/_23c/img/about/about_img_006.png': '/assets/img/about_img_006.png',
        
        # Gallery images
        '/wp-content/themes/_23c/img/garally/gallery_img_001.webp': '/assets/img/gallery_img_001.webp',
        '/wp-content/themes/_23c/img/garally/gallery_img_002.webp': '/assets/img/gallery_img_002.webp',
        '/wp-content/themes/_23c/img/garally/gallery_img_003.webp': '/assets/img/gallery_img_003.webp',
        '/wp-content/themes/_23c/img/garally/gallery_img_004.webp': '/assets/img/gallery_img_004.webp',
        '/wp-content/themes/_23c/img/garally/gallery_img_005.webp': '/assets/img/gallery_img_005.webp',
        '/wp-content/themes/_23c/img/garally/gallery_img_006.webp': '/assets/img/gallery_img_006.webp',
        '/wp-content/themes/_23c/img/garally/gallery_img_007.webp': '/assets/img/gallery_img_007.webp',
        '/wp-content/themes/_23c/img/garally/gallery_img_008.webp': '/assets/img/gallery_img_008.webp',
        '/wp-content/themes/_23c/img/garally/gallery_img_009.webp': '/assets/img/gallery_img_009.webp',
        
        # Menu images
        '/wp-content/themes/_23c/img/menu/menu_img_001.webp': '/assets/img/menu_img_001.webp',
        '/wp-content/themes/_23c/img/menu/menu_img_002.webp': '/assets/img/menu_img_002.webp',
        '/wp-content/themes/_23c/img/menu/menu_img_003.webp': '/assets/img/menu_img_003.webp',
        
        # Flow images
        '/wp-content/themes/_23c/img/flow/flow_img_001.webp': '/assets/img/flow_img_001.webp',
        '/wp-content/themes/_23c/img/flow/flow_img_002.webp': '/assets/img/flow_img_002.webp',
    }
    mapping.update(wp_theme_img_mappings)
    
    # Handle query string versions
    for url, local_path in list(mapping.items()):
        if url.endswith('.svg'):
            mapping[url + '?001'] = local_path
    
    # CSS and JS - these will be removed/handled differently
    # For now, just comment them out or use CDN
    css_mappings = {
        '/wp-content/themes/_23c/style.css': '/assets/css/style.css',
        '/wp-content/themes/_23c/css/main.css': '/assets/css/main.css',
        '/wp-content/themes/_23c/js/main.js': '/assets/js/main.js',
    }
    mapping.update(css_mappings)
    
    # Add query string version for main.js
    mapping['/wp-content/themes/_23c/js/main.js?ver=2025.04.05-001'] = '/assets/js/main.js'
    
    # jQuery - we'll use CDN
    jquery_mappings = {
        '/wp-includes/js/jquery/jquery.min.js': 'https://code.jquery.com/jquery-3.7.1.min.js',
        '/wp-includes/js/jquery/jquery-migrate.min.js': 'https://code.jquery.com/jquery-migrate-3.4.1.min.js',
    }
    mapping.update(jquery_mappings)
    
    return mapping

def fix_html_file(file_path, mapping):
    """Fix a single HTML file by replacing broken links."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_content = content
    fixes_made = []
    
    # Replace each mapping, handling query strings
    for old_url, new_url in mapping.items():
        # For jQuery, handle query string separately
        if 'jquery' in old_url.lower():
            # Match with and without query string
            base_url = old_url.split('?')[0]
            import re
            pattern = re.escape(base_url) + r'(\?[^"\s]*)?'
            if re.search(pattern, content):
                content = re.sub(f'"{pattern}"', f'"{new_url}"', content)
                content = re.sub(f"'{pattern}'", f"'{new_url}'", content)
                fixes_made.append(old_url)
        # Replace exact matches
        elif old_url in content:
            content = content.replace(f'"{old_url}"', f'"{new_url}"')
            content = content.replace(f"'{old_url}'", f"'{new_url}'")
            content = content.replace(f'content="{old_url}"', f'content="{new_url}"')
            content = content.replace(f"content='{old_url}'", f"content='{new_url}'")
            fixes_made.append(old_url)
    
    # Write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return fixes_made
    return []

def main():
    root_dir = '/Users/asiboro/Sources/Work/23centuryid'
    html_files = find_all_html_files(root_dir)
    mapping = create_mapping()
    
    print(f"Processing {len(html_files)} HTML files...\n")
    
    total_fixes = 0
    files_modified = 0
    
    for html_file in sorted(html_files):
        fixes = fix_html_file(html_file, mapping)
        if fixes:
            files_modified += 1
            total_fixes += len(fixes)
            rel_path = os.path.relpath(html_file, root_dir)
            print(f"✓ {rel_path}: {len(fixes)} fixes")
    
    print(f"\n{'=' * 60}")
    print(f"Total files modified: {files_modified}")
    print(f"Total fixes applied: {total_fixes}")
    print(f"{'=' * 60}")
    
    # Print summary of replacement rules
    print("\nReplacement rules applied:")
    print("\nWP Uploads → /assets/img/:")
    for old, new in mapping.items():
        if old.startswith('/wp-content/uploads/'):
            print(f"  {old} → {new}")
    
    print("\nWP Themes → /assets/:")
    for old, new in mapping.items():
        if '/wp-content/themes/' in old:
            print(f"  {old} → {new}")
    
    print("\nWP Includes → CDN/Local:")
    for old, new in mapping.items():
        if '/wp-includes/' in old:
            print(f"  {old} → {new}")

if __name__ == '__main__':
    main()
