#!/usr/bin/env python3
"""
Create pages for the remaining missing links and fix WordPress image paths
"""

import os
from pathlib import Path

def create_missing_pages():
    """Create placeholder pages for missing links"""
    
    pages_to_create = [
        # Certification pages
        {
            "path": "certifications/iso9001/index.html",
            "title": "ISO 9001 Certification",
            "breadcrumb": "Certifications > ISO 9001"
        },
        {
            "path": "certifications/pics/index.html",
            "title": "PICS Certification",
            "breadcrumb": "Certifications > PICS"
        },
        # MSC educational pages
        {
            "path": "msc/conversation-2025-04-03/index.html",
            "title": "MSC Conversation - April 3, 2025",
            "breadcrumb": "MSC > Conversations > April 3, 2025"
        },
        {
            "path": "msc/difference-secretome-exosome/index.html",
            "title": "Difference between Secretome and Exosome",
            "breadcrumb": "MSC > Education > Secretome vs Exosome"
        },
        {
            "path": "msc/misunderstandings-about-stem-cells/index.html",
            "title": "Misunderstandings About Stem Cells",
            "breadcrumb": "MSC > Education > Misunderstandings"
        },
        {
            "path": "msc/stem-cell-treatment-risk-countries/index.html",
            "title": "Stem Cell Treatment Risk by Country",
            "breadcrumb": "MSC > Education > Treatment Risk"
        },
        {
            "path": "msc/stem-cell-types-regenerative-medicine/index.html",
            "title": "Stem Cell Types in Regenerative Medicine",
            "breadcrumb": "MSC > Education > Cell Types"
        },
        # News pages
        {
            "path": "news/site-renewal/index.html",
            "title": "Site Renewal News",
            "breadcrumb": "News > Site Renewal"
        },
        {
            "path": "news/whartons-jelly-secretome-seminar-2025/index.html",
            "title": "Wharton's Jelly Secretome Seminar 2025",
            "breadcrumb": "News > Seminars > Wharton's Jelly Secretome"
        },
        # Treatable conditions (only those referenced in main pages)
        {
            "path": "treatable/msc-therapy-ckd/index.html",
            "title": "MSC Therapy for Chronic Kidney Disease",
            "breadcrumb": "Treatable > CKD"
        },
        {
            "path": "treatable/msc-therapy-crohns-disease/index.html",
            "title": "MSC Therapy for Crohn's Disease",
            "breadcrumb": "Treatable > Crohn's Disease"
        },
        {
            "path": "treatable/msc-therapy-diabetic-retinopathy/index.html",
            "title": "MSC Therapy for Diabetic Retinopathy",
            "breadcrumb": "Treatable > Diabetic Retinopathy"
        },
        {
            "path": "treatable/msc-therapy-glaucoma/index.html",
            "title": "MSC Therapy for Glaucoma",
            "breadcrumb": "Treatable > Glaucoma"
        },
        {
            "path": "treatable/msc-therapy-pad/index.html",
            "title": "MSC Therapy for Peripheral Arterial Disease",
            "breadcrumb": "Treatable > PAD"
        },
        {
            "path": "treatable/msc-therapy-raumatic-brain-injury/index.html",
            "title": "MSC Therapy for Traumatic Brain Injury",
            "breadcrumb": "Treatable > TBI"
        },
        {
            "path": "treatable/msc-therapy-rp/index.html",
            "title": "MSC Therapy for Retinitis Pigmentosa",
            "breadcrumb": "Treatable > RP"
        },
        {
            "path": "treatable/msc-therapy-sjogrens-syndrome/index.html",
            "title": "MSC Therapy for Sjögren's Syndrome",
            "breadcrumb": "Treatable > Sjögren's"
        },
        {
            "path": "treatable/msc-therapy-sle/index.html",
            "title": "MSC Therapy for Systemic Lupus Erythematosus",
            "breadcrumb": "Treatable > SLE"
        },
        {
            "path": "treatable/nk-cell-therapy-cancer/index.html",
            "title": "NK Cell Therapy for Cancer",
            "breadcrumb": "Treatable > NK Cell > Cancer"
        },
    ]
    
    template = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 23Century.id</title>
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="/assets/css/main.css">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .breadcrumb {{ color: #666; font-size: 14px; margin-bottom: 20px; }}
        h1 {{ color: #333; margin-bottom: 30px; }}
        .content {{ color: #555; line-height: 1.6; }}
        .placeholder {{ background: #f5f5f5; padding: 40px; text-align: center; color: #999; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="breadcrumb">{breadcrumb}</div>
        <h1>{title}</h1>
        <div class="content">
            <div class="placeholder">
                <p>Halaman ini sedang dalam proses pengembangan.</p>
                <p>Content akan ditambahkan segera.</p>
                <p><a href="/">Kembali ke Beranda</a></p>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    created = 0
    for page_info in pages_to_create:
        page_path = Path(page_info["path"])
        page_path.parent.mkdir(parents=True, exist_ok=True)
        
        if page_path.exists():
            print(f"  ⊘ {page_info['path']} already exists")
            continue
        
        html_content = template.format(
            title=page_info["title"],
            breadcrumb=page_info["breadcrumb"]
        )
        
        page_path.write_text(html_content)
        print(f"  ✓ Created {page_info['path']}")
        created += 1
    
    print(f"\nTotal pages created: {created}\n")
    return created


def fix_wordpress_image_paths():
    """Fix remaining WordPress image paths in HTML files"""
    
    image_mappings = {
        "/wp-content/uploads/2025/04/msc-treatment-rheumatoid-arthritis-1.webp": "/assets/img/msc-treatment-rheumatoid-arthritis-1.webp",
        "/wp-content/uploads/2025/04/msc-treatment-rheumatoid-arthritis-2.webp": "/assets/img/msc-treatment-rheumatoid-arthritis-2.webp",
    }
    
    print("Fixing remaining WordPress image paths...\n")
    
    files_updated = 0
    replacements = 0
    
    for root, dirs, files in os.walk("."):
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
                
                for old_path, new_path in image_mappings.items():
                    if old_path in updated_content:
                        updated_content = updated_content.replace(old_path, new_path)
                        made_change = True
                        replacements += 1
                
                if made_change:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"  ✓ Updated {filepath}")
                    files_updated += 1
                    
            except Exception as e:
                print(f"  ✗ Error processing {filepath}: {e}")
    
    print(f"\nTotal files updated: {files_updated}")
    print(f"Total replacements: {replacements}\n")
    return files_updated


def main():
    print("\n" + "="*80)
    print("Creating Missing Pages and Fixing Remaining Links")
    print("="*80 + "\n")
    
    # Create missing pages
    print("Creating missing pages...")
    create_missing_pages()
    
    # Fix WordPress paths
    print("Fixing remaining WordPress paths...")
    fix_wordpress_image_paths()
    
    print("="*80)
    print("COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
