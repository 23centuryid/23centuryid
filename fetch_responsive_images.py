#!/usr/bin/env python3
"""
Fetch missing responsive image variants from origin site.
"""

import subprocess
from pathlib import Path

ROOT_DIR = Path('/Users/asiboro/Sources/Work/23centuryid')
ORIGIN = 'https://23c.jp'

missing_images = [
    'about-768x512.webp',
    'cell-laboratory-768x512.webp',
    'globalhealth-award-2025-1-1536x1037.jpg',
    'globalhealth-award-2025-2-768x1024.jpg',
    'msc-therapy-alzheimers-768x397.webp',
    'msc-therapy-amd-768x413.webp',
    'msc-therapy-asd-768x335.webp',
    'msc-therapy-blindness-768x358.webp',
    'msc-therapy-chronic-pain-768x431.webp',
    'msc-therapy-diabetes-768x322.webp',
    'msc-therapy-liver-cirrhosis-768x460.webp',
    'msc-therapy-osteoarthritis-768x431.webp',
    'msc-therapy-parkinsons-disease-768x384.webp',
    'msc-therapy-post-mi-heart-failure-768x499.webp',
    'msc-therapy-post-stroke-sequelae-768x414.webp',
    'msc-therapy-renal-failure-768x390.webp',
    'msc-therapy-snhl-768x376.webp',
    'msc-therapy-spinal-cord-injury-768x337.webp',
    'msc-treatment-rheumatoid-arthritis-2_01-768x344.webp',
    'unauthorized-cgtp-warning-768x415.webp',
]

def fetch_image(filename):
    """Fetch a single image from origin."""
    origin_url = f'{ORIGIN}/wp-content/uploads/2025/04/{filename}'
    local_path = ROOT_DIR / 'assets' / 'img' / filename
    
    cmd = ['curl', '-s', origin_url, '-o', str(local_path)]
    result = subprocess.run(cmd, capture_output=True)
    
    if local_path.exists():
        size = local_path.stat().st_size
        print(f'✅ {filename} ({size} bytes)')
        return True
    else:
        # Try alternate paths
        for year_month in ['2025/03', '2025/02', '2025/01']:
            origin_url = f'{ORIGIN}/wp-content/uploads/{year_month}/{filename}'
            cmd = ['curl', '-s', origin_url, '-o', str(local_path)]
            subprocess.run(cmd, capture_output=True)
            
            if local_path.exists():
                size = local_path.stat().st_size
                print(f'✅ {filename} from {year_month} ({size} bytes)')
                return True
        
        print(f'⚠️  Could not fetch {filename}')
        return False

def main():
    print("=" * 80)
    print("FETCHING MISSING RESPONSIVE IMAGE VARIANTS")
    print("=" * 80)
    print()
    
    successful = 0
    for filename in missing_images:
        if fetch_image(filename):
            successful += 1
    
    print()
    print("=" * 80)
    print(f"✅ Successfully fetched {successful}/{len(missing_images)} images")
    print("=" * 80)

if __name__ == '__main__':
    main()
