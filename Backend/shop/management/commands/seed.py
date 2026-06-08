import urllib.request
import urllib.error
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from shop.models import Category, Product, ProductVariant


CATEGORIES = [
    {"name": "Dresses",     "slug": "dresses",     "description": "Effortless silhouettes for every occasion."},
    {"name": "Tops",        "slug": "tops",        "description": "Refined separates crafted from the finest fabrics."},
    {"name": "Shoes",       "slug": "shoes",       "description": "Artisan footwear with timeless appeal."},
    {"name": "Accessories", "slug": "accessories", "description": "Understated pieces that complete the look."},
]

# Unsplash image for each product slug
PRODUCT_IMAGES = {
    "silk-midi-dress":      "https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=800&q=80",
    "linen-wrap-dress":     "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=800&q=80",
    "evening-gown-noir":    "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=800&q=80",
    "floral-summer-dress":  "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&q=80",
    "satin-slip-dress":     "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80",
    "knit-mini-dress":      "https://images.unsplash.com/photo-1612336307429-8a898d10e223?w=800&q=80",
    "cashmere-knit-top":    "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=800&q=80",
    "silk-blouse-ivory":    "https://images.unsplash.com/photo-1485462537746-965f33f7f6a7?w=800&q=80",
    "structured-blazer":    "https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=800&q=80",
    "cotton-poplin-shirt":  "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&q=80",
    "linen-tank-top":       "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&q=80",
    "leather-kitten-heels": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800&q=80",
    "suede-ankle-boots":    "https://images.unsplash.com/photo-1515355337-65edb5e3ac2e?w=800&q=80",
    "strappy-sandals-gold": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=800&q=80",
    "ballet-flats-noir":    "https://images.unsplash.com/photo-1518049362265-d5b2a6467637?w=800&q=80",
    "espadrille-wedges":    "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=800&q=80",
    "pearl-drop-earrings":  "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=800&q=80",
    "leather-clutch-noir":  "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=800&q=80",
    "silk-scarf-floral":    "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=800&q=80",
    "gold-chain-bracelet":  "https://images.unsplash.com/photo-1611652022419-a9419f74343d?w=800&q=80",
    "canvas-tote-bag":      "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800&q=80",
}

PRODUCTS = [
    # ── DRESSES (6) ────────────────────────────────────────────────────────────
    {
        "category": "dresses",
        "name": "Silk Midi Dress",
        "slug": "silk-midi-dress",
        "description": "Cut from the finest Italian silk, this midi dress drapes effortlessly for an evening of understated glamour. The fluid silhouette skims the body without clinging, while a subtle V-neckline and delicate self-tie at the waist define the form with quiet precision.",
        "price": "385.00",
        "variants": [
            *[{"size": s, "color": "Ivory",  "stock": 10} for s in ("XS", "S", "M")],
            *[{"size": s, "color": "Ivory",  "stock": 0}  for s in ("L", "XL")],
            *[{"size": s, "color": "Blush",  "stock": 8}  for s in ("XS", "S")],
             {"size": "M",  "color": "Blush",  "stock": 0},
            *[{"size": s, "color": "Noir",   "stock": 12} for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "Sage",   "stock": 6}  for s in ("S", "M")],
        ],
    },
    {
        "category": "dresses",
        "name": "Linen Wrap Dress",
        "slug": "linen-wrap-dress",
        "description": "Effortless summer dressing in stone-washed Belgian linen. The wrap silhouette is universally flattering — adjust the tie for a relaxed or cinched look. Naturally breathable and beautifully textured.",
        "price": "290.00",
        "variants": [
            *[{"size": s, "color": "Sand",       "stock": 10} for s in ("XS", "S", "M")],
            *[{"size": s, "color": "White",      "stock": 8}  for s in ("S", "M")],
             {"size": "S",  "color": "Terracotta", "stock": 5},
        ],
    },
    {
        "category": "dresses",
        "name": "Evening Gown Noir",
        "slug": "evening-gown-noir",
        "description": "A column gown in matte crépe that moves with quiet authority. Floor-length with a subtle high slit, fastened by a single covered button at the nape.",
        "price": "620.00",
        "variants": [
            *[{"size": s, "color": "Noir",  "stock": 5} for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "Ivory", "stock": 3} for s in ("XS", "S", "M")],
        ],
    },
    {
        "category": "dresses",
        "name": "Floral Summer Dress",
        "slug": "floral-summer-dress",
        "description": "A lightweight chiffon dress adorned with an exclusive botanical print. Smocked bodice, adjustable straps, and a flared skirt that catches the breeze. The ideal companion for garden parties and warm evenings.",
        "price": "215.00",
        "variants": [
            *[{"size": s, "color": "Blush", "stock": 8}  for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "Ivory", "stock": 6}  for s in ("XS", "S", "M")],
        ],
    },
    {
        "category": "dresses",
        "name": "Satin Slip Dress",
        "slug": "satin-slip-dress",
        "description": "A bias-cut slip dress in liquid charmeuse satin. Minimal seaming, thin adjustable straps, and a delicate lace trim at the hem. Wear alone or layer under a blazer.",
        "price": "340.00",
        "variants": [
            *[{"size": s, "color": "Ivory", "stock": 9}  for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "Noir",  "stock": 7}  for s in ("XS", "S", "M")],
            *[{"size": s, "color": "Blush", "stock": 5}  for s in ("S", "M")],
        ],
    },
    {
        "category": "dresses",
        "name": "Knit Mini Dress",
        "slug": "knit-mini-dress",
        "description": "A sculpted ribbed-knit mini in a premium viscose-blend. A square neckline, long sleeves, and a fitted silhouette make this a versatile piece that transitions effortlessly from day to night.",
        "price": "265.00",
        "variants": [
            *[{"size": s, "color": "Cream", "stock": 10} for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "Black", "stock": 8}  for s in ("XS", "S", "M")],
            *[{"size": s, "color": "Sage",  "stock": 5}  for s in ("S", "M")],
        ],
    },

    # ── TOPS (5) ──────────────────────────────────────────────────────────────
    {
        "category": "tops",
        "name": "Cashmere Knit Top",
        "slug": "cashmere-knit-top",
        "description": "Grade-A Mongolian cashmere in a relaxed ribbed knit. Cropped to sit at the high hip — pairs effortlessly with tailored trousers or a midi skirt.",
        "price": "245.00",
        "variants": [
            *[{"size": s, "color": "Cream", "stock": 8} for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "Black", "stock": 8} for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "Navy",  "stock": 5} for s in ("S", "M")],
        ],
    },
    {
        "category": "tops",
        "name": "Silk Blouse Ivory",
        "slug": "silk-blouse-ivory",
        "description": "A classic silk charmeuse blouse with a relaxed collar and mother-of-pearl buttons. Tuck it in for polish or let it float for ease.",
        "price": "195.00",
        "variants": [
            *[{"size": s, "color": "Ivory", "stock": 10} for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "Blush", "stock": 7}  for s in ("XS", "S", "M")],
        ],
    },
    {
        "category": "tops",
        "name": "Structured Blazer",
        "slug": "structured-blazer",
        "description": "Tailored in Italian virgin wool with a half-canvas construction. Clean lapels, three-button cuffs, and a single back vent — the definitive blazer.",
        "price": "475.00",
        "variants": [
            *[{"size": s, "color": "Black", "stock": 6} for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "Camel", "stock": 4} for s in ("S", "M", "L")],
        ],
    },
    {
        "category": "tops",
        "name": "Cotton Poplin Shirt",
        "slug": "cotton-poplin-shirt",
        "description": "A relaxed-fit shirt in 100% Egyptian cotton poplin. Slightly oversized with a dropped shoulder, a curved hem, and subtle tonal stitching throughout.",
        "price": "155.00",
        "variants": [
            *[{"size": s, "color": "White", "stock": 12} for s in ("XS", "S", "M", "L", "XL")],
            *[{"size": s, "color": "Ivory", "stock": 8}  for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "Black", "stock": 6}  for s in ("S", "M", "L")],
        ],
    },
    {
        "category": "tops",
        "name": "Linen Tank Top",
        "slug": "linen-tank-top",
        "description": "A minimal tank in garment-dyed linen. Wide straps, a relaxed body, and a straight hem — effortless layering or wear alone on warm days.",
        "price": "95.00",
        "variants": [
            *[{"size": s, "color": "Sand",  "stock": 15} for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "White", "stock": 12} for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "Black", "stock": 10} for s in ("XS", "S", "M", "L")],
        ],
    },

    # ── SHOES (5) ──────────────────────────────────────────────────────────────
    {
        "category": "shoes",
        "name": "Leather Kitten Heels",
        "slug": "leather-kitten-heels",
        "description": "A 4 cm kitten heel in full-grain Nappa leather. Pointed toe, slim heel, and a hidden padded footbed for all-day comfort.",
        "price": "310.00",
        "variants": [
            *[{"size": str(s), "color": "Noir", "stock": 5} for s in range(36, 42)],
            *[{"size": str(s), "color": "Nude", "stock": 4} for s in range(36, 41)],
        ],
    },
    {
        "category": "shoes",
        "name": "Suede Ankle Boots",
        "slug": "suede-ankle-boots",
        "description": "Supple Italian suede ankle boots with a stacked 6 cm heel and inside zip closure. Structured enough for the boardroom, relaxed enough for the weekend.",
        "price": "420.00",
        "variants": [
            *[{"size": str(s), "color": "Taupe", "stock": 4} for s in range(36, 42)],
            *[{"size": str(s), "color": "Black", "stock": 6} for s in range(36, 42)],
        ],
    },
    {
        "category": "shoes",
        "name": "Strappy Sandals Gold",
        "slug": "strappy-sandals-gold",
        "description": "Barely-there sandals in gold metallic leather. Adjustable ankle strap, thin crossed vamps, and a 7 cm stiletto heel.",
        "price": "265.00",
        "variants": [
            *[{"size": str(s), "color": "Gold",   "stock": 5} for s in range(36, 42)],
            *[{"size": str(s), "color": "Silver", "stock": 3} for s in range(36, 41)],
        ],
    },
    {
        "category": "shoes",
        "name": "Ballet Flats Noir",
        "slug": "ballet-flats-noir",
        "description": "Classic ballet flats in buttery soft calfskin. A rounded toe, delicate bow at the vamp, and a flexible sole make these the most comfortable flat in your wardrobe.",
        "price": "245.00",
        "variants": [
            *[{"size": str(s), "color": "Noir",  "stock": 8} for s in range(36, 42)],
            *[{"size": str(s), "color": "Nude",  "stock": 6} for s in range(36, 41)],
            *[{"size": str(s), "color": "Ivory", "stock": 4} for s in range(36, 40)],
        ],
    },
    {
        "category": "shoes",
        "name": "Espadrille Wedges",
        "slug": "espadrille-wedges",
        "description": "Hand-crafted espadrille wedges with a natural jute sole and a 7 cm heel. Canvas upper with an ankle tie — the quintessential summer shoe.",
        "price": "185.00",
        "variants": [
            *[{"size": str(s), "color": "Sand",  "stock": 7} for s in range(36, 42)],
            *[{"size": str(s), "color": "White", "stock": 5} for s in range(36, 41)],
        ],
    },

    # ── ACCESSORIES (5) ────────────────────────────────────────────────────────
    {
        "category": "accessories",
        "name": "Pearl Drop Earrings",
        "slug": "pearl-drop-earrings",
        "description": "South Sea Baroque pearls suspended from 18k gold vermeil settings. Each pair is unique — expect slight variations in shape and lustre.",
        "price": "145.00",
        "variants": [
            {"size": "One Size", "color": "Pearl White", "stock": 15},
            {"size": "One Size", "color": "Blush Pearl", "stock": 8},
        ],
    },
    {
        "category": "accessories",
        "name": "Leather Clutch Noir",
        "slug": "leather-clutch-noir",
        "description": "A minimal envelope clutch in smooth full-grain leather. Magnetic closure, card slots, and a detachable wrist strap in 18k gold hardware.",
        "price": "285.00",
        "variants": [
            {"size": "One Size", "color": "Noir",  "stock": 10},
            {"size": "One Size", "color": "Ivory", "stock": 6},
        ],
    },
    {
        "category": "accessories",
        "name": "Silk Scarf Floral",
        "slug": "silk-scarf-floral",
        "description": "Hand-rolled 90×90 cm scarf in 12 mm twill silk, printed with an original botanical illustration exclusive to the collection.",
        "price": "175.00",
        "variants": [
            {"size": "90×90", "color": "Blue",  "stock": 12},
            {"size": "90×90", "color": "Pink",  "stock": 10},
            {"size": "90×90", "color": "Ivory", "stock": 8},
        ],
    },
    {
        "category": "accessories",
        "name": "Gold Chain Bracelet",
        "slug": "gold-chain-bracelet",
        "description": "A delicate curb-chain bracelet in 18k gold vermeil over sterling silver. Lobster-claw clasp with a 3 cm extender for a perfect fit.",
        "price": "110.00",
        "variants": [
            {"size": "One Size", "color": "Gold",   "stock": 20},
            {"size": "One Size", "color": "Silver", "stock": 15},
        ],
    },
    {
        "category": "accessories",
        "name": "Canvas Tote Bag",
        "slug": "canvas-tote-bag",
        "description": "A structured tote in heavyweight organic canvas with full-grain leather handles and base corners. Interior zip pocket, two open slip pockets, and a magnetic snap closure.",
        "price": "195.00",
        "variants": [
            {"size": "One Size", "color": "Ivory", "stock": 12},
            {"size": "One Size", "color": "Black", "stock": 10},
            {"size": "One Size", "color": "Sand",  "stock": 8},
        ],
    },
]


def _download_image(slug, stdout):
    url = PRODUCT_IMAGES.get(slug)
    if not url:
        return None
    products_dir = Path(settings.MEDIA_ROOT) / "products"
    products_dir.mkdir(parents=True, exist_ok=True)
    filepath = products_dir / f"{slug}.jpg"
    if filepath.exists():
        return f"products/{slug}.jpg"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            filepath.write_bytes(resp.read())
        stdout.write(f"    Image downloaded: {slug}.jpg")
        return f"products/{slug}.jpg"
    except Exception as exc:
        stdout.write(f"    Warning: could not download image for {slug}: {exc}")
        return None


class Command(BaseCommand):
    help = "Seed the database with sample categories, products, variants, and images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing products and categories before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            ProductVariant.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write("Cleared existing data.")

        # Categories
        cat_map = {}
        for c in CATEGORIES:
            obj, created = Category.objects.get_or_create(slug=c["slug"], defaults=c)
            cat_map[c["slug"]] = obj
            self.stdout.write(f"  {'Created' if created else 'Exists '} category: {obj.name}")

        # Products + variants + images
        for p in PRODUCTS:
            cat = cat_map[p["category"]]
            product, created = Product.objects.get_or_create(
                slug=p["slug"],
                defaults={
                    "category": cat,
                    "name": p["name"],
                    "description": p["description"],
                    "price": p["price"],
                    "available": True,
                },
            )
            self.stdout.write(f"  {'Created' if created else 'Exists '} product: {product.name}")

            if created or not product.image:
                image_path = _download_image(p["slug"], self.stdout)
                if image_path:
                    product.image = image_path
                    product.save(update_fields=["image"])

            for v in p["variants"]:
                ProductVariant.objects.get_or_create(
                    product=product,
                    size=v["size"],
                    color=v["color"],
                    defaults={"stock": v["stock"]},
                )

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {len(PRODUCTS)} products across {len(CATEGORIES)} categories."
        ))
