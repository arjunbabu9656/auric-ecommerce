from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Populates the database with initial AURIC products and categories'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting Production Database Seed...'))

        # ── Persistent Admin Creation (Render Fix) ──
        import os
        from django.contrib.auth.models import User
        # Get password from environment variable OR use a default if not set
        admin_pass = os.environ.get('ADMIN_PASSWORD', 'Auric@2026')
        
        u = User.objects.filter(username='arjunaju').first()
        if not u:
            User.objects.create_superuser('arjunaju', 'arjunb7025@gmail.com', admin_pass)
            self.stdout.write(self.style.SUCCESS(f'  Admin: Re-created arjunaju superuser.'))
        else:
            # Always ensure the password is what's in the Env Variable
            u.set_password(admin_pass)
            u.is_superuser = True
            u.is_staff = True
            u.save()
            self.stdout.write(self.style.SUCCESS(f'  Admin: Updated arjunaju password.'))

        # ── Categories ──
        cat_data = [
            ('Men',        'men',        'categories/category_men_1773082495281.png'),
            ('Women',      'women',      'categories/category_women_1773082512416.png'),
            ('Outerwear',  'outerwear',  'categories/category_outerwear_1773082545977.png'),
            ('Essentials', 'essentials', 'categories/category_essentials_1773082528120.png'),
        ]

        cats = {}
        for name, slug, img in cat_data:
            cat, created = Category.objects.get_or_create(slug=slug, defaults={'name': name})
            if created or not cat.image:
                cat.image = img
                cat.save()
            cats[slug] = cat
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  Category: {name} ({status})')

        # ── Products ──
        products_data = [
            # --- ESSENTIALS ---
            ('Heavyweight Core Hoodie', 'heavyweight-core-hoodie', 'essentials', 12000, None,  'products/product_hoodie_1773082418751.png', True),
            ('Technical Cargo Trouser', 'technical-cargo-trouser', 'essentials', 14500, 11000, 'products/product_pants_1773082436753.png', True),
            ('Oversized Blank Tee',     'oversized-blank-tee',     'essentials', 5500,  None,  'products/product_tee_1773082453469.png',   True),
            ('Men Technical Jacket', 'men-technical-jacket', 'men', 3500, None , 'products/men_jacket.jpeg', True),
            
            # --- WOMEN LUXURY ---
            ('Technical Minimalist Dress', 'technical-minimalist-dress', 'women', 12500, None,  'products/dress_tech_black.png', True),
            ('Architectural Pleated Dress','architectural-pleated-dress','women', 18900, None,  'products/dress_pleated_white.png', True),
            ('Bonded Midi Dress',        'bonded-midi-dress',          'women', 14200, None,  'products/dress_midi_grey.png', True),
            ('Fluid Evening Gown',       'fluid-evening-gown',         'women', 28500, None,  'products/dress_evening_navy.png', True),
            ('Technical Pleated Maxi',   'technical-pleated-maxi',     'women', 16800, None,  'products/dress_pleated_green.png', True),
            ('Minimalist Utility Dress', 'minimalist-utility-dress',   'women', 11500, None,  'products/dress_utility_sand.png', True),

            # --- MEN LUXURY ---
            ('Technical Overshirt',      'technical-overshirt',        'men',    9800,  None, 'products/men_tech_overshirt_black.png', True),
            ('Structured Technical Blazer','structured-technical-blazer','men', 22500,  None, 'products/men_blazer_charcoal.png', True),
            ('Tapered Technical Trouser','tapered-trouser',            'men',    8900,  None, 'products/men_trouser_sand.png', True),
            ('Minimalist Shell Parka',   'minimalist-shell-parka',     'men',   24900,  None, 'products/men_parka_navy.png', True),
        ]

        for name, slug, cat_slug, price, sale_price, img, featured in products_data:
            p, created = Product.objects.get_or_create(slug=slug, defaults={
                'name': name,
                'category': cats[cat_slug],
                'price': price,
                'sale_price': sale_price,
                'description': f'A premium AURIC archival piece. Engineered with technical-grade fabrics and architectural form. Designed for the modern urban environment.',
                'is_featured': featured,
                'stock': 50,
            })
            if created or not p.image:
                p.image = img
                p.save()
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  Product: {name} ({status})')

        self.stdout.write(self.style.SUCCESS('✅ Database Seeded Successfully.'))
