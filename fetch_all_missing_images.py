#!/usr/bin/env python3
"""
Fetch all missing responsive image variants from origin site.
"""

import subprocess
from pathlib import Path

ROOT_DIR = Path('/Users/asiboro/Sources/Work/23centuryid')
ORIGIN = 'https://23c.jp'

# List of images needing all variants (1200w, 1024w, 768w, 300w versions)
base_images = [
    ('about', '2025/03'),
    ('cell-laboratory', '2025/03'),
    ('msc-therapy-alzheimers', '2025/04'),
    ('msc-therapy-amd', '2025/04'),
    ('msc-therapy-asd', '2025/04'),
    ('msc-therapy-blindness', '2025/04'),
    ('msc-therapy-chronic-pain', '2025/04'),
    ('msc-therapy-diabetes', '2025/04'),
    ('msc-therapy-liver-cirrhosis', '2025/04'),
    ('msc-therapy-osteoarthritis', '2025/04'),
    ('msc-therapy-parkinsons-disease', '2025/04'),
    ('msc-therapy-post-mi-heart-failure', '2025/04'),
    ('msc-therapy-post-stroke-sequelae', '2025/04'),
    ('msc-therapy-renal-failure', '2025/04'),
    ('msc-therapy-snhl', '2025/04'),
    ('msc-therapy-spinal-cord-injury', '2025/04'),
    ('msc-treatment-rheumatoid-arthritis-2_01', '2025/04'),
    ('globalhealth-award-2025-1', '2025/06'),
    ('globalhealth-award-2025-2', '2025/10'),
]

def fetch_image_variants(base_name, date_path):
    """Fetch all responsive variants of an image."""
    # Determine extension based on name
    if 'globalhealth' in base_name or 'award' in base_name:
        ext = 'jpg'
    else:
        ext = 'webp'
    
    variants = [
        (f'{base_name}.{ext}', ''),  # Full size (1200w)
        (f'{base_name}-300x200.{ext}', '300x200'),
        (f'{base_name}-1024x683.{ext}', '1024x683'),
        (f'{base_name}-768x512.{ext}', '768x512'),
    ]
    
    # Special handling for specific images
    if 'rheumatoid' in base_name:
        variants = [
            (f'{base_name}.{ext}', ''),
            (f'{base_name}-300x134.{ext}', '300x134'),
            (f'{base_name}-1024x459.{ext}', '1024x459'),
            (f'{base_name}-768x344.{ext}', '768x344'),
        ]
    elif 'globalhealth-award-2025-1' in base_name:
        variants = [
            (f'{base_name}.{ext}', ''),
            (f'{base_name}-300x203.{ext}', '300x203'),
            (f'{base_name}-768x518.{ext}', '768x518'),
            (f'{base_name}-1536x1037.{ext}', '1536x1037'),
        ]
    elif 'globalhealth-award-2025-2' in base_name:
        variants = [
            (f'{base_name}.{ext}', ''),
            (f'{base_name}-225x300.{ext}', '225x300'),
            (f'{base_name}-768x1024.{ext}', '768x1024'),
        ]
    elif 'rheumatoid' in base_name:
        pass
    elif any(x in base_name for x in ['renal', 'snhl', 'spinal']):
        variants = [
            (f'{base_name}.{ext}', ''),
            (f'{base_name}-300x152.{ext}', '300x152'),
            (f'{base_name}-1024x520.{ext}', '1024x520'),
            (f'{base_name}-768x390.{ext}', '768x390'),
        ]
    
    success = 0
    for filename, desc in variants:
        origin_url = f'{ORIGIN}/wp-content/uploads/{date_path}/{filename}'
        local_path = ROOT_DIR / 'assets' / 'img' / filename
        
        if local_path.exists():
            continue  # Skip if already exists
        
        cmd = ['curl', '-s', origin_url, '-o', str(local_path)]
        subprocess.run(cmd, capture_output=True)
        
        if local_path.exists() and local_path.stat().st_size > 0:
            size = local_path.stat().st_size
            print(f'✅ {filename} ({size:,} bytes)')
            success += 1
        else:
            if local_path.exists():
                local_path.unlink()
            print(f'⚠️  {filename} - not found')
    
    return success

def main():
    print("=" * 80)
    print("FETCHING ALL MISSING RESPONSIVE IMAGE VARIANTS")
    print("=" * 80)
    print()
    
    total_success = 0
    for base_name, date_path in base_images:
        print(f"📦 Fetching: {base_name}")
        success = fetch_image_variants(base_name, date_path)
        total_success += success
        print()
    
    print("=" * 80)
    print(f"✅ Successfully fetched {total_success} images")
    print("=" * 80)

if __name__ == '__main__':
    main()
