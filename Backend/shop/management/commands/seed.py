from django.core.management.base import BaseCommand
from shop.models import Category, Product, ProductVariant


CATEGORIES = [
    {"name": "Dresses",     "slug": "dresses",     "description": "Effortless silhouettes for every occasion."},
    {"name": "Tops",        "slug": "tops",        "description": "Refined separates crafted from the finest fabrics."},
    {"name": "Shoes",       "slug": "shoes",       "description": "Artisan footwear with timeless appeal."},
    {"name": "Accessories", "slug": "accessories", "description": "Understated pieces that complete the look."},
]

PRODUCTS = [
    # ── DRESSES ────────────────────────────────────────────────────────────────
    {
        "category": "dresses",
        "name": "Silk Midi Dress",
        "slug": "silk-midi-dress",
        "description": "Cut from the finest Italian silk, this midi dress drapes effortlessly for an evening of understated glamour. The fluid silhouette skims the body without clinging, while a subtle V-neckline and delicate self-tie at the waist define the form with quiet precision.",
        "price": "385.00",
        "variants": [
            *[{"size": s, "color": "Ivory",    "stock": 10} for s in ("XS", "S", "M")],
            *[{"size": s, "color": "Ivory",    "stock": 0}  for s in ("L", "XL")],
            *[{"size": s, "color": "Blush",    "stock": 8}  for s in ("XS", "S")],
             {"size": "M", "color": "Blush",   "stock": 0},
            *[{"size": s, "color": "Noir",     "stock": 12} for s in ("XS", "S", "M", "L")],
            *[{"size": s, "color": "Sage",     "stock": 6}  for s in ("S", "M")],
        ],
    },
    {
        "category": "dresses",
        "name": "Linen Wrap Dress",
        "slug": "linen-wrap-dress",
        "description": "Effortless summer dressing in stone-washed Belgian linen. The wrap silhouette is universally flattering — adjust the tie for a relaxed or cinched look. Naturally breathable and beautifully textured.",
        "price": "290.00",
        "variants": [
            *[{"size": s, "color": "Sand",      "stock": 10} for s in ("XS", "S", "M")],
            *[{"size": s, "color": "White",     "stock": 8}  for s in ("S", "M")],
             {"size": "S", "color": "Terracotta","stock": 5},
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
    # ── TOPS ──────────────────────────────────────────────────────────────────
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
    # ── SHOES ──────────────────────────────────────────────────────────────────
    {
        "category": "shoes",
        "name": "Leather Kitten Heels",
        "slug": "leather-kitten-heels",
        "description": "A 4 cm kitten heel in full-grain Nappa leather. Pointed toe, slim heel, and a hidden padded footbed for all-day comfort.",
        "price": "310.00",
        "variants": [
            *[{"size": str(s), "color": "Noir",  "stock": 5} for s in range(36, 42)],
            *[{"size": str(s), "color": "Nude",  "stock": 4} for s in range(36, 41)],
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
    # ── ACCESSORIES ────────────────────────────────────────────────────────────
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
        "description": "Hand-rolled 90 × 90 cm scarf in 12mm twill silk, printed with an original botanical illustration exclusive to Aurelia.",
        "price": "175.00",
        "variants": [
            {"size": "90×90", "color": "Blue",  "stock": 12},
            {"size": "90×90", "color": "Pink",  "stock": 10},
            {"size": "90×90", "color": "Ivory", "stock": 8},
        ],
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample categories, products, and variants"

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

        # Products + Variants
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
