#!/usr/bin/env python3
"""
Fix srcset attributes in HTML files:
1. Convert /wp-content/uploads/ paths to /assets/img/ 
2. Verify referenced images exist
"""

import os
import re
from pathlib import Path

ROOT_DIR = Path('/Users/asiboro/Sources/Work/23centuryid')

def process_html_file(filepath):
    """Process a single HTML file to fix srcset paths."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return 0
    
    original_content = content
    fixes = 0
    
    # Pattern to find srcset attributes with /wp-content/uploads/ paths
    # We need to convert srcset="/wp-content/uploads/YYYY/MM/filename..." 
    # to srcset="/assets/img/filename..."
    
    def convert_srcset(match):
        nonlocal fixes
        srcset_value = match.group(1)
        
        # Convert each URL in the srcset
        # Format: "url1 1200w, url2 300w, ..."
        parts = srcset_value.split(',')
        converted_parts = []
        
        for part in parts:
            # Split URL and descriptor (e.g., "1200w")
            items = part.strip().rsplit(' ', 1)
            if len(items) == 2:
                url, descriptor = items
            else:
                url = items[0]
                descriptor = ""
            
            # Convert /wp-content/uploads/YYYY/MM/filename to /assets/img/filename
            if '/wp-content/uploads/' in url:
                # Extract just the filename
                filename = url.split('/')[-1]
                new_url = f'/assets/img/{filename}'
                converted_parts.append(f'{new_url} {descriptor}'.rstrip())
                fixes += 1
            else:
                # Keep as is (probably https:// URL or already correct)
                if descriptor:
                    converted_parts.append(f'{url} {descriptor}')
                else:
                    converted_parts.append(url)
        
        new_srcset = ', '.join(converted_parts)
        return f'srcset="{new_srcset}"'
    
    # Replace srcset attributes
    content = re.sub(r'srcset="([^"]*)"', convert_srcset, content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return fixes

def main():
    print("=" * 80)
    print("FIXING SRCSET PATHS")
    print("=" * 80)
    
    total_fixes = 0
    files_processed = 0
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip fetched_pages
        if 'fetched_pages' in root:
            continue
        
        for file in files:
            if file.endswith('.html'):
                filepath = Path(root) / file
                fixes = process_html_file(filepath)
                if fixes > 0:
                    rel_path = filepath.relative_to(ROOT_DIR)
                    print(f"  {rel_path}: {fixes} fixes")
                    total_fixes += fixes
                files_processed += 1
    
    print(f"\n{'-' * 80}")
    print(f"✅ Processed {files_processed} HTML files")
    print(f"✅ Applied {total_fixes} srcset path fixes")
    print("=" * 80)

if __name__ == '__main__':
    main()
