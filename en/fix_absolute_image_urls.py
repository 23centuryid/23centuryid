#!/usr/bin/env python3
"""
Fix absolute URLs in src attributes to local /assets/img/ paths.
"""

import os
import re
from pathlib import Path

ROOT_DIR = Path('/Users/asiboro/Sources/Work/23centuryid')

def fix_html_file(filepath):
    """Convert absolute image URLs to local paths."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return 0
    
    original = content
    fixes = 0
    
    # Fix src="https://23c.jp/wp-content/uploads/YYYY/MM/filename" → src="/assets/img/filename"
    def convert_url(match):
        nonlocal fixes
        url = match.group(1)
        # Extract just filename
        filename = url.split('/')[-1]
        fixes += 1
        return f'src="/assets/img/{filename}"'
    
    content = re.sub(
        r'src="https://23c\.jp/wp-content/uploads/\d{4}/\d{2}/([^"]+)"',
        convert_url,
        content
    )
    
    # Fix src="https://23c.jp/wp-content/themes/_23c/..." → src="/assets/..."
    def convert_theme_url(match):
        nonlocal fixes
        filename = match.group(1)
        fixes += 1
        return f'src="/assets/{filename}"'
    
    content = re.sub(
        r'src="https://23c\.jp/wp-content/themes/_23c/(.+?)"',
        convert_theme_url,
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return fixes

def main():
    print("=" * 80)
    print("FIXING ABSOLUTE IMAGE URLs")
    print("=" * 80)
    
    total_fixes = 0
    files_fixed = 0
    
    for html_file in ROOT_DIR.rglob('*.html'):
        if 'fetched_pages' in str(html_file):
            continue
        
        fixes = fix_html_file(html_file)
        if fixes > 0:
            rel_path = html_file.relative_to(ROOT_DIR)
            print(f"  {rel_path}: {fixes} fixes")
            total_fixes += fixes
            files_fixed += 1
    
    print(f"\n{'-' * 80}")
    print(f"✅ Fixed {total_fixes} absolute URLs in {files_fixed} files")
    print("=" * 80)

if __name__ == '__main__':
    main()
