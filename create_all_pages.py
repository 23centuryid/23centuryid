#!/usr/bin/env python3
"""
Generate all remaining missing treatment and content pages for 23Century.id
"""
import os
from pathlib import Path

def create_treatment_page(path, title, h1, description=""):
    """Create a treatment information page"""
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    
    if os.path.exists(path):
        return False
    
    if not description:
        description = f"<p>Informasi tentang {h1} sedang dalam pengembangan.</p><p>Silakan hubungi kami untuk konsultasi lebih lanjut.</p>"
    
    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
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
                <li><span>{h1}</span></li>
            </ul>
        </div>
    </div>

    <div class="entry-content">
        <h1>{h1}</h1>
        {description}
        <div class="btn01"><a href="/treatable/">Kembali ke Kondisi yang Dapat Ditangani</a></div>
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
                </ul>
            </nav>
        </div>
    </footer>
</div>

<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="/assets/js/main.js"></script>
</body>
</html>"""
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return True

def create_all_missing_pages():
    """Create all remaining missing content pages"""
    root_dir = '/Users/asiboro/Sources/Work/23centuryid'
    
    # Treatment pages for various MSC therapies
    treatment_pages = {
        # Treatment menu sub-pages
        'treatment-menu/msc/index.html': ('Terapi Sel Punca (MSC) - 23Century.id', 'Terapi Sel Punca'),
        'treatment-menu/nk-cell/index.html': ('Terapi Sel NK - 23Century.id', 'Terapi Sel NK'),
        'treatment-menu/secretome/index.html': ('Terapi Secretome - 23Century.id', 'Terapi Secretome'),
        
        # Treatable conditions
        'treatable/msc-therapy-alzheimers/index.html': ('Terapi MSC untuk Alzheimer - 23Century.id', 'Terapi MSC untuk Alzheimer'),
        'treatable/msc-therapy-amd/index.html': ('Terapi MSC untuk AMD (Age-related Macular Degeneration) - 23Century.id', 'Terapi MSC untuk AMD'),
        'treatable/msc-therapy-asd/index.html': ('Terapi MSC untuk ASD (Autism Spectrum Disorder) - 23Century.id', 'Terapi MSC untuk ASD'),
        'treatable/msc-therapy-blindness/index.html': ('Terapi MSC untuk Kebutaan - 23Century.id', 'Terapi MSC untuk Kebutaan'),
        'treatable/msc-therapy-chronic-pain/index.html': ('Terapi MSC untuk Nyeri Kronis - 23Century.id', 'Terapi MSC untuk Nyeri Kronis'),
        'treatable/msc-therapy-ckd/index.html': ('Terapi MSC untuk CKD (Chronic Kidney Disease) - 23Century.id', 'Terapi MSC untuk Penyakit Ginjal Kronis'),
        'treatable/msc-therapy-crohns-disease/index.html': ('Terapi MSC untuk Penyakit Crohn - 23Century.id', 'Terapi MSC untuk Penyakit Crohn'),
        'treatable/msc-therapy-diabetes/index.html': ('Terapi MSC untuk Diabetes - 23Century.id', 'Terapi MSC untuk Diabetes'),
        'treatable/msc-therapy-diabetic-retinopathy/index.html': ('Terapi MSC untuk Diabetic Retinopathy - 23Century.id', 'Terapi MSC untuk Retinopati Diabetik'),
        'treatable/msc-therapy-glaucoma/index.html': ('Terapi MSC untuk Glaukoma - 23Century.id', 'Terapi MSC untuk Glaukoma'),
        'treatable/msc-therapy-liver-cirrhosis/index.html': ('Terapi MSC untuk Sirosis Hati - 23Century.id', 'Terapi MSC untuk Sirosis Hati'),
        'treatable/msc-therapy-osteoarthritis/index.html': ('Terapi MSC untuk Osteoarthritis - 23Century.id', 'Terapi MSC untuk Osteoarthritis'),
        'treatable/msc-therapy-pad/index.html': ('Terapi MSC untuk PAD (Peripheral Artery Disease) - 23Century.id', 'Terapi MSC untuk Penyakit Arteri Perifer'),
        'treatable/msc-therapy-parkinsons-disease/index.html': ('Terapi MSC untuk Penyakit Parkinson - 23Century.id', 'Terapi MSC untuk Penyakit Parkinson'),
        'treatable/msc-therapy-post-mi-heart-failure/index.html': ('Terapi MSC untuk Gagal Jantung Pasca-MI - 23Century.id', 'Terapi MSC untuk Gagal Jantung'),
        'treatable/msc-therapy-post-stroke-sequelae/index.html': ('Terapi MSC untuk Sekuele Pasca-Stroke - 23Century.id', 'Terapi MSC untuk Akibat Stroke'),
        'treatable/msc-therapy-raumatic-brain-injury/index.html': ('Terapi MSC untuk Traumatic Brain Injury - 23Century.id', 'Terapi MSC untuk Cedera Otak Traumatis'),
        'treatable/msc-therapy-renal-failure/index.html': ('Terapi MSC untuk Gagal Ginjal - 23Century.id', 'Terapi MSC untuk Gagal Ginjal'),
        'treatable/msc-therapy-rp/index.html': ('Terapi MSC untuk RP (Retinitis Pigmentosa) - 23Century.id', 'Terapi MSC untuk Retinitis Pigmentosa'),
        'treatable/msc-therapy-sjogrens-syndrome/index.html': ('Terapi MSC untuk Sindrom Sjögren - 23Century.id', 'Terapi MSC untuk Sindrom Sjögren'),
        'treatable/msc-therapy-sle/index.html': ('Terapi MSC untuk SLE (Systemic Lupus Erythematosus) - 23Century.id', 'Terapi MSC untuk Lupus'),
        'treatable/msc-therapy-snhl/index.html': ('Terapi MSC untuk SNHL (Sudden Sensorineural Hearing Loss) - 23Century.id', 'Terapi MSC untuk Gangguan Pendengaran'),
        'treatable/msc-therapy-spinal-cord-injury/index.html': ('Terapi MSC untuk Cedera Sumsum Tulang Belakang - 23Century.id', 'Terapi MSC untuk Cedera Sumsum Tulang Belakang'),
        'treatable/msc-treatment-rheumatoid-arthritis/index.html': ('Terapi MSC untuk Rheumatoid Arthritis - 23Century.id', 'Terapi MSC untuk Rheumatoid Arthritis'),
        'treatable/nk-cell-therapy-cancer/index.html': ('Terapi Sel NK untuk Kanker - 23Century.id', 'Terapi Sel NK untuk Kanker'),
        
        # MSC educational content
        'msc/index.html': ('Terapi Sel Punca (MSC) - 23Century.id', 'Terapi Sel Punca'),
        'msc/conversation-2025-04-03/index.html': ('Percakapan - 2025-04-03 - 23Century.id', 'Percakapan tentang Terapi Sel Punca'),
        'msc/difference-secretome-exosome/index.html': ('Perbedaan Secretome dan Exosome - 23Century.id', 'Perbedaan Secretome dan Exosome'),
        'msc/misunderstandings-about-stem-cells/index.html': ('Kesalahpahaman tentang Sel Punca - 23Century.id', 'Kesalahpahaman tentang Sel Punca'),
        'msc/stem-cell-treatment-risk-countries/index.html': ('Risiko Perawatan Sel Punca di Berbagai Negara - 23Century.id', 'Risiko Perawatan Sel Punca di Berbagai Negara'),
        'msc/stem-cell-types-regenerative-medicine/index.html': ('Jenis-jenis Sel Punca dalam Pengobatan Regeneratif - 23Century.id', 'Jenis-jenis Sel Punca'),
        
        # News articles
        'news/globalhealth-award-2025/index.html': ('Global Health Award 2025 - 23Century.id', 'Global Health Award 2025'),
        'news/site-renewal/index.html': ('Pembaruan Situs - 23Century.id', 'Pembaruan Situs'),
        'news/unauthorized-cgtp-warning/index.html': ('Peringatan CGTP Tidak Sah - 23Century.id', 'Peringatan CGTP Tidak Sah'),
        'news/whartons-jelly-secretome-seminar-2025/index.html': ('Seminar Wharton\'s Jelly Secretome 2025 - 23Century.id', 'Seminar Wharton\'s Jelly Secretome 2025'),
        
        # Other sections
        'voice/index.html': ('Suara Pasien - 23Century.id', 'Suara Pasien'),
        'case-studies/index.html': ('Studi Kasus - 23Century.id', 'Studi Kasus'),
        'column/index.html': ('Kolom - 23Century.id', 'Kolom'),
        
        # Certification info
        'certifications/iso9001/index.html': ('Sertifikasi ISO 9001 - 23Century.id', 'Sertifikasi ISO 9001'),
        'certifications/pics/index.html': ('Sertifikasi PICS - 23Century.id', 'Sertifikasi PICS'),
    }
    
    print("=" * 70)
    print("Creating all remaining missing content pages...")
    print("=" * 70)
    
    created = 0
    for path, (title, h1) in treatment_pages.items():
        full_path = os.path.join(root_dir, path)
        if create_treatment_page(full_path, title, h1):
            created += 1
            print(f"  ✓ Created {path}")
        else:
            print(f"  - {path} already exists")
    
    print(f"\n✅ Created {created} new pages")
    print("=" * 70)

if __name__ == '__main__':
    create_all_missing_pages()
