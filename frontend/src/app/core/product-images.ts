export const PRODUCT_IMAGES: Record<string, string[]> = {
  'silk-midi-dress': [
    'https://images.unsplash.com/photo-1539008835657-9e8e9680c956?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
    'https://images.unsplash.com/photo-1566174053879-31528523f8ae?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
    'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
    'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
  ],
  'linen-wrap-dress': [
    'https://images.unsplash.com/photo-1566174053879-31528523f8ae?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
    'https://images.unsplash.com/photo-1568251188392-ae32f898cb3b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
  ],
  'evening-gown-noir': [
    'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
    'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
  ],
  'cashmere-knit-top': [
    'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
  ],
  'silk-blouse-ivory': [
    'https://images.unsplash.com/photo-1485462537746-965f33f7f6a7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
  ],
  'structured-blazer': [
    'https://images.unsplash.com/photo-1591369822096-ffd140ec948f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
  ],
  'leather-kitten-heels': [
    'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
  ],
  'suede-ankle-boots': [
    'https://images.unsplash.com/photo-1515355337-65edb5e3ac2e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
  ],
  'strappy-sandals-gold': [
    'https://images.unsplash.com/photo-1603487742131-4160ec999306?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
  ],
  'pearl-drop-earrings': [
    'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
  ],
  'leather-clutch-noir': [
    'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
  ],
  'silk-scarf-floral': [
    'https://images.unsplash.com/photo-1601924994987-69e26d50dc26?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200',
  ],
};

export const PLACEHOLDER_IMAGE =
  'https://images.unsplash.com/photo-1539008835657-9e8e9680c956?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200';

export function productImage(slug: string, apiImage: string | null): string {
  if (apiImage) return apiImage;
  return PRODUCT_IMAGES[slug]?.[0] ?? PLACEHOLDER_IMAGE;
}

export function productImages(slug: string, apiImage: string | null): string[] {
  if (apiImage) return [apiImage];
  return PRODUCT_IMAGES[slug] ?? [PLACEHOLDER_IMAGE];
}

function toTitleCase(s: string): string {
  return s.trim().split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ');
}

export function getColorHex(colorName: string): string {
  const raw = colorName.trim();
  return COLOR_HEX[raw] ?? COLOR_HEX[toTitleCase(raw)] ?? '#888888';
}

export const COLOR_HEX: Record<string, string> = {
  'Ivory':       '#F5F0E8',
  'Blush':       '#E8C4B8',
  'Noir':        '#1A1A1A',
  'Black':       '#1A1A1A',
  'Sage':        '#9CAF88',
  'Sand':        '#C8B89A',
  'White':       '#FFFFFF',
  'Terracotta':  '#C1694F',
  'Cream':       '#FAF8F5',
  'Navy':        '#1B2A4A',
  'Camel':       '#C19A6B',
  'Nude':        '#E3C9A8',
  'Taupe':       '#B5A898',
  'Gold':        '#C9A962',
  'Silver':      '#C0C0C0',
  'Pearl White': '#F8F5F0',
  'Blush Pearl': '#E8C4B8',
  'Blue':        '#4A7FA5',
  'Pink':        '#E8A0B4',
};
