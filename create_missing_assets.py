#!/usr/bin/env python3
"""
Fetch missing images and create missing content pages for 23Century.id
"""
import os
import struct
import zlib
from pathlib import Path

def create_png_placeholder(filepath, width=800, height=600):
    """Create a simple PNG placeholder image without PIL"""
    # Create a minimal valid PNG file (1x1 gray pixel, scaled up)
    # This creates a very basic gray PNG
    
    # PNG header
    png_header = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk (image header)
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    ihdr_chunk = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
    
    # IDAT chunk (image data - a simple gray image)
    raw_data = b''
    gray = bytes([200, 200, 200])  # Gray color (RGB)
    for y in range(height):
        raw_data += b'\x00'  # Filter type for this line
        for x in range(width):
            raw_data += gray
    
    compressed_data = zlib.compress(raw_data, 9)
    idat_crc = zlib.crc32(b'IDAT' + compressed_data) & 0xffffffff
    idat_chunk = struct.pack('>I', len(compressed_data)) + b'IDAT' + compressed_data + struct.pack('>I', idat_crc)
    
    # IEND chunk (end marker)
    iend_crc = zlib.crc32(b'IEND') & 0xffffffff
    iend_chunk = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
    
    # Write PNG file
    with open(filepath, 'wb') as f:
        f.write(png_header + ihdr_chunk + idat_chunk + iend_chunk)

def create_webp_placeholder(filepath, width=800, height=600):
    """Create a minimal WebP placeholder image"""
    # For now, create as PNG and rename - WebP is more complex
    # In production, you'd want to convert or fetch real images
    create_png_placeholder(filepath, width, height)

def create_missing_images():
    """Create placeholder images for missing theme assets"""
    img_dir = '/Users/asiboro/Sources/Work/23centuryid/assets/img'
    
    # List of missing theme images with typical dimensions
    missing_images = {
        # About section
        'about.webp': (1200, 400),
        'about_img_001.png': (400, 300),
        'about_img_002.png': (400, 300),
        'about_img_003.png': (400, 300),
        'about_img_004.png': (400, 300),
        'about_img_005.png': (400, 300),
        'about_img_006.png': (400, 300),
        
        # Gallery
        'gallery_img_001.webp': (600, 400),
        'gallery_img_002.webp': (600, 400),
        'gallery_img_003.webp': (600, 400),
        'gallery_img_004.webp': (600, 400),
        'gallery_img_005.webp': (600, 400),
        'gallery_img_006.webp': (600, 400),
        'gallery_img_007.webp': (600, 400),
        'gallery_img_008.webp': (600, 400),
        'gallery_img_009.webp': (600, 400),
        
        # Flow and process
        'flow_img_001.webp': (1200, 400),
        'flow_img_002.webp': (1200, 400),
        'first_img_004.webp': (800, 600),
        'first_img_005.webp': (800, 600),
        
        # Cell laboratory
        'cell-laboratory.webp': (1200, 800),
    }
    
    print("Creating placeholder images for missing assets...")
    for filename, (width, height) in missing_images.items():
        filepath = os.path.join(img_dir, filename)
        if not os.path.exists(filepath):
            try:
                if filename.endswith('.webp'):
                    create_webp_placeholder(filepath, width, height)
                elif filename.endswith(('.png', '.jpg')):
                    create_png_placeholder(filepath, width, height)
                print(f"  ✓ Created {filename} ({width}x{height})")
            except Exception as e:
                print(f"  ✗ Failed to create {filename}: {e}")
        else:
            print(f"  - {filename} already exists")
    
    print(f"Placeholder image creation complete!")

def create_missing_pages():
    """Create placeholder pages for missing content"""
    root_dir = '/Users/asiboro/Sources/Work/23centuryid'
    
    # Define missing pages with their structure
    missing_pages = {
        'contact': {
            'path': 'contact/index.html',
            'title': 'Hubungi Kami - 23Century.id',
            'h1': 'Hubungi Kami',
            'content': '<p>Halaman kontak sedang dalam pengembangan.</p><p>Silakan hubungi kami melalui: info@23century.id</p>'
        },
        'price': {
            'path': 'price/index.html',
            'title': 'Harga Perawatan - 23Century.id',
            'h1': 'Harga Perawatan',
            'content': '<p>Informasi harga perawatan sedang dalam pengembangan.</p><p>Silakan hubungi kami untuk penawaran khusus.</p>'
        },
        'disclaimer': {
            'path': 'disclaimer/index.html',
            'title': 'Disclaimer - 23Century.id',
            'h1': 'Disclaimer',
            'content': '<p>Halaman disclaimer sedang dalam pengembangan.</p><p>Informasi penting tentang layanan kami akan ditampilkan di sini.</p>'
        },
        'privacy-policy': {
            'path': 'privacy-policy/index.html',
            'title': 'Kebijakan Privasi - 23Century.id',
            'h1': 'Kebijakan Privasi',
            'content': '<p>Kebijakan privasi sedang dalam pengembangan.</p><p>Kami berkomitmen melindungi data pribadi Anda.</p>'
        },
        'terms-of-service': {
            'path': 'terms-of-service/index.html',
            'title': 'Syarat dan Ketentuan - 23Century.id',
            'h1': 'Syarat dan Ketentuan',
            'content': '<p>Syarat dan ketentuan sedang dalam pengembangan.</p><p>Mohon baca dengan seksama sebelum menggunakan layanan kami.</p>'
        },
        'operation-company': {
            'path': 'operation-company/index.html',
            'title': 'Perusahaan Pengelola - 23Century.id',
            'h1': 'Perusahaan Pengelola',
            'content': '<p>Informasi perusahaan pengelola sedang dalam pengembangan.</p>'
        },
        'entry-list': {
            'path': 'entry-list/index.html',
            'title': 'Daftar Artikel - 23Century.id',
            'h1': 'Daftar Artikel',
            'content': '<p>Daftar artikel sedang dalam pengembangan.</p>'
        },
        'malaysia-stemcell': {
            'path': 'malaysia-stemcell/index.html',
            'title': 'Tentang Perawatan Sel Punca di Malaysia - 23Century.id',
            'h1': 'Tentang Perawatan Sel Punca di Malaysia',
            'content': '<p>Informasi tentang perawatan sel punca di Malaysia sedang dalam pengembangan.</p>'
        },
        'whartons-jelly-msc': {
            'path': 'whartons-jelly-msc/index.html',
            'title': 'Wharton\'s Jelly MSC - 23Century.id',
            'h1': 'Wharton\'s Jelly MSC',
            'content': '<p>Informasi tentang Wharton\'s Jelly MSC sedang dalam pengembangan.</p>'
        },
    }
    
    print("\nCreating missing content pages...")
    for page_key, page_info in missing_pages.items():
        page_path = os.path.join(root_dir, page_info['path'])
        os.makedirs(os.path.dirname(page_path), exist_ok=True)
        
        if not os.path.exists(page_path):
            html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{page_info['title']}</title>
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>
<div class="wrapper" id="pagetop">
    <header class="l-header">
        <div class="l-header__inner">
            <div class="l-header__logo">
                <h1 class="logo">
                    <a href="/" class="custom-logo-link" rel="home">
                        <img src="/assets/img/logo_black_001.svg" alt="23Century.id" style="max-width: 200px; height: auto;">
                    </a>
                </h1>
            </div>
        </div>
    </header>

    <div class="l-breadcrumbs">
        <div class="l-breadcrumbs__inner">
            <ul class="l-breadcrumbsList">
                <li><a href="/"><span>HOME</span></a></li>
                <li><span>{page_info['h1']}</span></li>
            </ul>
        </div>
    </div>

    <div class="entry-content">
        <h1>{page_info['h1']}</h1>
        {page_info['content']}
        <div class="btn01"><a href="/">Kembali ke Beranda</a></div>
    </div>

    <footer class="l-footer">
        <div class="l-footer__inner">
            <div class="l-footer__infoImage">
                <a href="/"><img src="/assets/img/logo_white_001.svg" alt="23Century.id"></a>
            </div>
            <nav>
                <ul>
                    <li><a href="/contact/">Kontak</a></li>
                    <li><a href="/disclaimer/">Disclaimer</a></li>
                    <li><a href="/privacy-policy/">Kebijakan Privasi</a></li>
                    <li><a href="/terms-of-service/">Syarat & Ketentuan</a></li>
                </ul>
            </nav>
        </div>
    </footer>
</div>

<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="/assets/js/main.js"></script>
</body>
</html>"""
            
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"  ✓ Created {page_info['path']}")
        else:
            print(f"  - {page_info['path']} already exists")

def main():
    print("=" * 70)
    print("23Century.id - Fetch Missing Images & Create Missing Pages")
    print("=" * 70)
    
    # Create placeholder images
    create_missing_images()
    
    # Create missing pages
    create_missing_pages()
    
    print("\n" + "=" * 70)
    print("✅ Process complete!")
    print("=" * 70)

if __name__ == '__main__':
    main()
