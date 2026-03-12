"""
Seed script: populate AURIC with initial categories and products.
Run with: python manage.py shell < seed_data.py
"""

import os
import shutil
from pathlib import Path

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auric.settings')
django.setup()

from store.models import Category, Product

BASE = Path(__file__).parent
ASSETS = BASE / 'assets'
MEDIA_PRODUCTS = BASE / 'media' / 'products'
MEDIA_CATEGORIES = BASE / 'media' / 'categories'
MEDIA_PRODUCTS.mkdir(parents=True, exist_ok=True)
MEDIA_CATEGORIES.mkdir(parents=True, exist_ok=True)

def copy_asset(src_name, dest_dir):
    src = ASSETS / src_name
    dest = dest_dir / src_name
    if src.exists() and not dest.exists():
        shutil.copy2(src, dest)
    return src_name if src.exists() else ''


# ── Categories ──
cat_data = [
    ('Outerwear',  'outerwear',  'category_outerwear_1773082545977.png'),
    ('Men',        'men',        'category_men_1773082495281.png'),
    ('Women',      'women',      'category_women_1773082512416.png'),
    ('Essentials', 'essentials', 'category_essentials_1773082528120.png'),
]

cats = {}
for name, slug, img in cat_data:
    cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
    fname = copy_asset(img, MEDIA_CATEGORIES)
    if fname:
        cat.image = f'categories/{fname}'
        cat.save()
    cats[slug] = cat
    print(f'  Category: {name}')

# ── Products ──
products_data = [
    ('Heavyweight Core Hoodie', 'heavyweight-core-hoodie', 'essentials', 120.00, None,  'product_hoodie_1773082418751.png', True),
    ('Technical Cargo Trouser', 'technical-cargo-trouser', 'essentials', 145.00, 110.00,'product_pants_1773082436753.png', True),
    ('Oversized Blank Tee',     'oversized-blank-tee',     'essentials',  55.00, None,  'product_tee_1773082453469.png',   True),
    ('Apex Shell Jacket',       'apex-shell-jacket',       'outerwear',   280.00, 230.00,'product_jacket_1773082468782.png',True),
    ('Archive Longline Coat',   'archive-longline-coat',   'outerwear',   350.00, None,  'category_outerwear_1773082545977.png', False),
    ('Core Crew Essential',     'core-crew-essential',     'men',          85.00, None,  'category_men_1773082495281.png', False),
    ('Minimal Slip Dress',      'minimal-slip-dress',      'women',        95.00, 70.00, 'category_women_1773082512416.png', False),
    ('Daily Foundation Set',    'daily-foundation-set',    'essentials',  165.00, None,  'category_essentials_1773082528120.png', False),
]

for name, slug, cat_slug, price, sale_price, img, featured in products_data:
    p, created = Product.objects.get_or_create(slug=slug, defaults={
        'name': name,
        'category': cats[cat_slug],
        'price': price,
        'sale_price': sale_price,
        'description': f'A premium AURIC piece from the {cats[cat_slug].name} collection. Crafted from technical-grade fabric with precision finishing.',
        'is_featured': featured,
        'stock': 25,
    })
    fname = copy_asset(img, MEDIA_PRODUCTS)
    if fname and created:
        p.image = f'products/{fname}'
        p.save()
    action = 'Created' if created else 'Exists'
    print(f'  {action}: {name}')

print('\n✅ Seed complete. Open /admin to manage products.')
