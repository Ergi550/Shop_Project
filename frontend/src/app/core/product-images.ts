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
  if (raw.startsWith('#')) return raw;
  return COLOR_HEX[raw] ?? COLOR_HEX[toTitleCase(raw)] ?? '#888888';
}

export const COLOR_HEX: Record<string, string> = {
  // Whites & Lights
  'White':          '#FFFFFF',
  'Ghost White':    '#F8F8FF',
  'Snow':           '#FFFAFA',
  'Ivory':          '#F5F0E8',
  'Cream':          '#FAF8F5',
  'Pearl White':    '#F8F5F0',
  'Off White':      '#FAF9F6',
  'Antique White':  '#FAEBD7',
  'Linen':          '#FAF0E6',
  // Neutrals & Beiges
  'Nude':           '#E3C9A8',
  'Beige':          '#F5F5DC',
  'Sand':           '#C8B89A',
  'Taupe':          '#B5A898',
  'Tan':            '#D2B48C',
  'Camel':          '#C19A6B',
  'Khaki':          '#C3B091',
  // Grays
  'Pearl':          '#F8F5F0',
  'Platinum':       '#E5E4E2',
  'Silver':         '#C0C0C0',
  'Light Gray':     '#D3D3D3',
  'Ash':            '#B2BEB5',
  'Gray':           '#808080',
  'Stone':          '#928E85',
  'Slate':          '#708090',
  'Charcoal':       '#36454F',
  'Graphite':       '#374649',
  // Blacks
  'Dark Charcoal':  '#333333',
  'Dark Gray':      '#2F2F2F',
  'Black':          '#1A1A1A',
  'Noir':           '#1A1A1A',
  'Jet Black':      '#000000',
  // Pinks & Blushes
  'Baby Pink':      '#FFD1DC',
  'Misty Rose':     '#FFE4E1',
  'Pearl Pink':     '#F4C2C2',
  'Blush':          '#E8C4B8',
  'Blush Pearl':    '#E8C4B8',
  'Cotton Candy':   '#FFBCD9',
  'Pink':           '#E8A0B4',
  'Flamingo':       '#FC8EAC',
  'Hot Pink':       '#FF69B4',
  'Rose':           '#E8718A',
  'Deep Pink':      '#FF1493',
  'Fuchsia':        '#FF00FF',
  'Magenta':        '#CC00CC',
  // Reds & Corals
  'Coral':          '#FF7F7F',
  'Salmon':         '#FA8072',
  'Tomato':         '#FF6347',
  'Terracotta':     '#C1694F',
  'Red':            '#C0392B',
  'Crimson':        '#DC143C',
  'Scarlet':        '#FF2400',
  'Cherry':         '#DE3163',
  'Raspberry':      '#872657',
  'Wine':           '#722F37',
  'Burgundy':       '#800020',
  'Maroon':         '#800000',
  'Oxblood':        '#4A0000',
  // Oranges
  'Peach':          '#FFCBA4',
  'Apricot':        '#FBCEB1',
  'Light Orange':   '#FFD580',
  'Orange':         '#FF8C00',
  'Tangerine':      '#F28500',
  'Pumpkin':        '#FF7518',
  'Burnt Orange':   '#CC5500',
  'Rust':           '#B7410E',
  'Sienna':         '#A0522D',
  // Yellows & Golds
  'Butter':         '#FFFACD',
  'Lemon':          '#FFF44F',
  'Pale Yellow':    '#FFFF99',
  'Canary':         '#FFEF00',
  'Yellow':         '#FFD700',
  'Gold':           '#C9A962',
  'Amber':          '#FFBF00',
  'Mustard':        '#FFDB58',
  'Saffron':        '#F4C430',
  'Ochre':          '#CC7722',
  // Metallics
  'Bronze':         '#CD7F32',
  // Blues
  'Baby Blue':      '#89CFF0',
  'Powder Blue':    '#B0E0E6',
  'Light Blue':     '#ADD8E6',
  'Sky Blue':       '#87CEEB',
  'Cornflower':     '#6495ED',
  'Cornflower Blue':'#6495ED',
  'Periwinkle':     '#CCCCFF',
  'Steel Blue':     '#4682B4',
  'Blue':           '#4A7FA5',
  'Cerulean':       '#007BA7',
  'Denim':          '#1560BD',
  'Royal Blue':     '#4169E1',
  'Cobalt':         '#0047AB',
  'Sapphire':       '#0F52BA',
  'Navy':           '#1B2A4A',
  'Midnight Blue':  '#191970',
  // Greens
  'Mint':           '#98FF98',
  'Honeydew':       '#F0FFF0',
  'Pale Green':     '#90EE90',
  'Sage':           '#9CAF88',
  'Lime':           '#32CD32',
  'Lime Green':     '#32CD32',
  'Olive':          '#8A9A5B',
  'Moss':           '#6B7C4D',
  'Green':          '#5A8C6E',
  'Teal':           '#008080',
  'Forest':         '#228B22',
  'Hunter':         '#355E3B',
  'Hunter Green':   '#355E3B',
  'Emerald':        '#50C878',
  'Bottle Green':   '#006A4E',
  'Dark Green':     '#013220',
  // Purples
  'Lavender':       '#E6E6FA',
  'Thistle':        '#D8BFD8',
  'Lilac':          '#C8A2C8',
  'Mauve':          '#E0B0FF',
  'Orchid':         '#DA70D6',
  'Violet':         '#EE82EE',
  'Amethyst':       '#9966CC',
  'Purple':         '#9B59B6',
  'Heather':        '#B57EDC',
  'Plum':           '#8E4585',
  'Indigo':         '#4B0082',
  'Eggplant':       '#614051',
  'Dark Purple':    '#301934',
  // Browns
  'Mocha':          '#967969',
  'Brown':          '#8B6914',
  'Chocolate':      '#7B3F00',
  'Mahogany':       '#C04000',
  'Chestnut':       '#954535',
};
