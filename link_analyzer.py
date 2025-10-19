#!/usr/bin/env python3
"""
Analyze broken links in HTML files and generate a report with fixes.
"""
import os
import re
from pathlib import Path
from collections import defaultdict

def find_all_html_files(root_dir):
    """Find all HTML files in the directory tree."""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip node_modules and other irrelevant directories
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '.venv', '__pycache__'}]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def extract_links_from_html(html_content):
    """Extract all links, images, and assets from HTML content."""
    links = {
        'images': [],
        'stylesheets': [],
        'scripts': [],
        'links': [],
        'other': []
    }
    
    # Image src attributes
    for match in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', html_content):
        links['images'].append(match.group(1))
    
    # Stylesheet links
    for match in re.finditer(r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']stylesheet', html_content):
        links['stylesheets'].append(match.group(1))
    
    # Script src
    for match in re.finditer(r'<script[^>]+src=["\']([^"\']+)["\']', html_content):
        links['scripts'].append(match.group(1))
    
    # Anchor links
    for match in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\']', html_content):
        links['links'].append(match.group(1))
    
    # Meta tags with content
    for match in re.finditer(r'<meta[^>]+content=["\']([^"\']+)["\']', html_content):
        content = match.group(1)
        if content.startswith('/wp-') or content.startswith('http'):
            links['other'].append(content)
    
    return links

def categorize_broken_links(links, root_dir):
    """Categorize broken links by type."""
    broken = defaultdict(set)
    
    for category, url_list in links.items():
        for url in url_list:
            # Skip external URLs and JavaScript
            if url.startswith('http') or url.startswith('//') or url.startswith('javascript:'):
                continue
            
            # Check WordPress paths
            if '/wp-content/' in url or '/wp-includes/' in url:
                # Determine subcategory
                if '/wp-content/uploads/' in url:
                    subcategory = 'wp_uploads'
                elif '/wp-content/themes/' in url:
                    subcategory = 'wp_themes'
                elif '/wp-includes/' in url:
                    subcategory = 'wp_includes'
                else:
                    subcategory = 'wp_other'
                
                broken[f'{category}_{subcategory}'].add(url)
            # Check relative paths
            elif url.startswith('/') and not url.startswith('javascript:'):
                full_path = os.path.join(root_dir, url.lstrip('/'))
                if not os.path.exists(full_path):
                    broken[f'{category}_missing'].add(url)
    
    return broken

def main():
    root_dir = '/Users/asiboro/Sources/Work/23centuryid'
    html_files = find_all_html_files(root_dir)
    
    all_broken = defaultdict(lambda: defaultdict(set))
    
    print(f"Found {len(html_files)} HTML files\n")
    
    for html_file in sorted(html_files):
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        links = extract_links_from_html(content)
        broken = categorize_broken_links(links, root_dir)
        
        if broken:
            rel_path = os.path.relpath(html_file, root_dir)
            for category, urls in broken.items():
                for url in urls:
                    all_broken[category][url].add(rel_path)
    
    # Generate report
    print("=" * 80)
    print("BROKEN LINKS ANALYSIS REPORT")
    print("=" * 80)
    
    for category in sorted(all_broken.keys()):
        print(f"\n\n### {category.upper()} ###\n")
        for url in sorted(all_broken[category].keys()):
            files = sorted(all_broken[category][url])
            print(f"  {url}")
            print(f"    Found in: {len(files)} file(s)")
            for f in files[:3]:
                print(f"      - {f}")
            if len(files) > 3:
                print(f"      ... and {len(files) - 3} more")
    
    # Summary
    print("\n\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total_broken = sum(len(urls) for urls in all_broken.values())
    print(f"\nTotal broken link categories: {len(all_broken)}")
    print(f"Total unique broken URLs: {total_broken}")
    
    # Statistics by type
    wp_uploads = len(all_broken.get('images_wp_uploads', {}))
    wp_themes = len(all_broken.get('images_wp_themes', {})) + len(all_broken.get('stylesheets_wp_themes', {})) + len(all_broken.get('scripts_wp_themes', {}))
    wp_includes = len(all_broken.get('scripts_wp_includes', {}))
    
    print(f"\nBy type:")
    print(f"  - WP Uploads (images): {wp_uploads}")
    print(f"  - WP Themes (CSS/JS): {wp_themes}")
    print(f"  - WP Includes (jQuery): {wp_includes}")

if __name__ == '__main__':
    main()
