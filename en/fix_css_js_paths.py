#!/usr/bin/env python3
"""
Fix all remaining WordPress theme paths to point to local assets
Convert /wp-content/themes/_23c/ to /assets/
"""

import os
import re
from pathlib import Path

def fix_theme_paths():
    """Fix all WordPress theme paths in HTML files"""
    
    # Mapping of old WordPress paths to new local paths
    path_mappings = [
        ("/wp-content/themes/_23c/style.css", "/assets/css/style.css"),
        ("/wp-content/themes/_23c/css/main.css", "/assets/css/main.css"),
        ("/wp-content/themes/_23c/js/main.js", "/assets/js/main.js"),
        # Also handle https:// versions
        ("https://23c.jp/wp-content/themes/_23c/style.css", "/assets/css/style.css"),
        ("https://23c.jp/wp-content/themes/_23c/css/main.css", "/assets/css/main.css"),
        ("https://23c.jp/wp-content/themes/_23c/js/main.js", "/assets/js/main.js"),
    ]
    
    print("\n" + "="*80)
    print("Fixing All WordPress Theme Paths")
    print("="*80 + "\n")
    
    files_updated = 0
    total_replacements = 0
    
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
                
                # Apply all path mappings
                for old_path, new_path in path_mappings:
                    if old_path in updated_content:
                        updated_content = updated_content.replace(old_path, new_path)
                        made_change = True
                        total_replacements += 1
                
                if made_change:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"  ✓ {filepath}")
                    files_updated += 1
                    
            except Exception as e:
                print(f"  ✗ Error processing {filepath}: {e}")
    
    print(f"\n{files_updated} files updated")
    print(f"{total_replacements} path replacements made")
    print("\n" + "="*80 + "\n")
    
    return files_updated


def verify_all_paths_fixed():
    """Verify no more WordPress theme paths remain"""
    
    print("Verifying all paths are fixed...\n")
    
    found_issues = False
    
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in [".git", "node_modules", "__pycache__"]]
        
        for file in files:
            if not file.endswith(".html"):
                continue
            
            filepath = os.path.join(root, file)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "/wp-content/themes/_23c/" in content or "https://23c.jp/wp-content/themes/_23c/" in content:
                    print(f"  ⚠️  Still contains WordPress paths: {filepath}")
                    found_issues = True
                    
            except Exception as e:
                pass
    
    if not found_issues:
        print("  ✅ All WordPress theme paths have been fixed!\n")
    else:
        print("\n  ⚠️  Some files still contain WordPress paths\n")
    
    return not found_issues


if __name__ == "__main__":
    # Fix paths
    fix_theme_paths()
    
    # Verify
    verify_all_paths_fixed()
