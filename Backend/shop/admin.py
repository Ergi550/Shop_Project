import json
from django import forms
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Category, Product, ProductVariant, Order, OrderItem


PALETTE = {
    'White':       '#FFFFFF',
    'Ivory':       '#F5F0E8',
    'Cream':       '#FAF8F5',
    'Pearl White': '#F8F5F0',
    'Nude':        '#E3C9A8',
    'Sand':        '#C8B89A',
    'Taupe':       '#B5A898',
    'Camel':       '#C19A6B',
    'Black':       '#1A1A1A',
    'Noir':        '#1A1A1A',
    'Blush':       '#E8C4B8',
    'Blush Pearl': '#E8C4B8',
    'Pink':        '#E8A0B4',
    'Rose':        '#E8718A',
    'Coral':       '#FF7F7F',
    'Red':         '#C0392B',
    'Burgundy':    '#800020',
    'Wine':        '#722F37',
    'Terracotta':  '#C1694F',
    'Blue':        '#4A7FA5',
    'Sky Blue':    '#87CEEB',
    'Navy':        '#1B2A4A',
    'Royal Blue':  '#4169E1',
    'Cobalt':      '#0047AB',
    'Sage':        '#9CAF88',
    'Olive':       '#8A9A5B',
    'Green':       '#5A8C6E',
    'Forest':      '#228B22',
    'Purple':      '#9B59B6',
    'Lavender':    '#E6E6FA',
    'Mauve':       '#E0B0FF',
    'Gold':        '#C9A962',
    'Silver':      '#C0C0C0',
    'Bronze':      '#CD7F32',
    'Brown':       '#8B6914',
    'Chocolate':   '#7B3F00',
}

LIGHT = {'#FFFFFF', '#F8F5F0', '#FAF8F5', '#F5F0E8', '#E6E6FA', '#E0B0FF', '#87CEEB', '#E3C9A8'}

# Color families shown when admin types a colour keyword
FAMILIES = [
    {
        'keywords': ['blue'],
        'label': 'Blue Shades',
        'colors': [
            {'name': 'Baby Blue',    'hex': '#89CFF0'},
            {'name': 'Powder Blue',  'hex': '#B0E0E6'},
            {'name': 'Light Blue',   'hex': '#ADD8E6'},
            {'name': 'Sky Blue',     'hex': '#87CEEB'},
            {'name': 'Cornflower',   'hex': '#6495ED'},
            {'name': 'Periwinkle',   'hex': '#CCCCFF'},
            {'name': 'Steel Blue',   'hex': '#4682B4'},
            {'name': 'Blue',         'hex': '#4A7FA5'},
            {'name': 'Cerulean',     'hex': '#007BA7'},
            {'name': 'Royal Blue',   'hex': '#4169E1'},
            {'name': 'Cobalt',       'hex': '#0047AB'},
            {'name': 'Denim',        'hex': '#1560BD'},
            {'name': 'Sapphire',     'hex': '#0F52BA'},
            {'name': 'Navy',         'hex': '#1B2A4A'},
            {'name': 'Midnight Blue','hex': '#191970'},
        ]
    },
    {
        'keywords': ['red'],
        'label': 'Red Shades',
        'colors': [
            {'name': 'Salmon',       'hex': '#FA8072'},
            {'name': 'Coral',        'hex': '#FF7F7F'},
            {'name': 'Rose',         'hex': '#E8718A'},
            {'name': 'Tomato',       'hex': '#FF6347'},
            {'name': 'Terracotta',   'hex': '#C1694F'},
            {'name': 'Red',          'hex': '#C0392B'},
            {'name': 'Crimson',      'hex': '#DC143C'},
            {'name': 'Scarlet',      'hex': '#FF2400'},
            {'name': 'Cherry',       'hex': '#DE3163'},
            {'name': 'Raspberry',    'hex': '#872657'},
            {'name': 'Wine',         'hex': '#722F37'},
            {'name': 'Burgundy',     'hex': '#800020'},
            {'name': 'Maroon',       'hex': '#800000'},
            {'name': 'Oxblood',      'hex': '#4A0000'},
        ]
    },
    {
        'keywords': ['green'],
        'label': 'Green Shades',
        'colors': [
            {'name': 'Mint',         'hex': '#98FF98'},
            {'name': 'Honeydew',     'hex': '#F0FFF0'},
            {'name': 'Pale Green',   'hex': '#90EE90'},
            {'name': 'Sage',         'hex': '#9CAF88'},
            {'name': 'Lime',         'hex': '#32CD32'},
            {'name': 'Olive',        'hex': '#8A9A5B'},
            {'name': 'Moss',         'hex': '#6B7C4D'},
            {'name': 'Green',        'hex': '#5A8C6E'},
            {'name': 'Teal',         'hex': '#008080'},
            {'name': 'Forest',       'hex': '#228B22'},
            {'name': 'Hunter',       'hex': '#355E3B'},
            {'name': 'Emerald',      'hex': '#50C878'},
            {'name': 'Bottle Green', 'hex': '#006A4E'},
            {'name': 'Dark Green',   'hex': '#013220'},
        ]
    },
    {
        'keywords': ['pink'],
        'label': 'Pink Shades',
        'colors': [
            {'name': 'Baby Pink',    'hex': '#FFD1DC'},
            {'name': 'Misty Rose',   'hex': '#FFE4E1'},
            {'name': 'Pearl Pink',   'hex': '#F4C2C2'},
            {'name': 'Blush',        'hex': '#E8C4B8'},
            {'name': 'Cotton Candy', 'hex': '#FFBCD9'},
            {'name': 'Pink',         'hex': '#E8A0B4'},
            {'name': 'Flamingo',     'hex': '#FC8EAC'},
            {'name': 'Hot Pink',     'hex': '#FF69B4'},
            {'name': 'Rose',         'hex': '#E8718A'},
            {'name': 'Deep Pink',    'hex': '#FF1493'},
            {'name': 'Fuchsia',      'hex': '#FF00FF'},
            {'name': 'Magenta',      'hex': '#CC00CC'},
        ]
    },
    {
        'keywords': ['purple'],
        'label': 'Purple Shades',
        'colors': [
            {'name': 'Lavender',     'hex': '#E6E6FA'},
            {'name': 'Thistle',      'hex': '#D8BFD8'},
            {'name': 'Lilac',        'hex': '#C8A2C8'},
            {'name': 'Mauve',        'hex': '#E0B0FF'},
            {'name': 'Orchid',       'hex': '#DA70D6'},
            {'name': 'Violet',       'hex': '#EE82EE'},
            {'name': 'Amethyst',     'hex': '#9966CC'},
            {'name': 'Purple',       'hex': '#9B59B6'},
            {'name': 'Heather',      'hex': '#B57EDC'},
            {'name': 'Plum',         'hex': '#8E4585'},
            {'name': 'Indigo',       'hex': '#4B0082'},
            {'name': 'Eggplant',     'hex': '#614051'},
            {'name': 'Dark Purple',  'hex': '#301934'},
        ]
    },
    {
        'keywords': ['yellow'],
        'label': 'Yellow Shades',
        'colors': [
            {'name': 'Butter',       'hex': '#FFFACD'},
            {'name': 'Lemon',        'hex': '#FFF44F'},
            {'name': 'Pale Yellow',  'hex': '#FFFF99'},
            {'name': 'Canary',       'hex': '#FFEF00'},
            {'name': 'Yellow',       'hex': '#FFD700'},
            {'name': 'Gold',         'hex': '#C9A962'},
            {'name': 'Amber',        'hex': '#FFBF00'},
            {'name': 'Mustard',      'hex': '#FFDB58'},
            {'name': 'Saffron',      'hex': '#F4C430'},
            {'name': 'Ochre',        'hex': '#CC7722'},
        ]
    },
    {
        'keywords': ['orange'],
        'label': 'Orange Shades',
        'colors': [
            {'name': 'Peach',        'hex': '#FFCBA4'},
            {'name': 'Apricot',      'hex': '#FBCEB1'},
            {'name': 'Light Orange', 'hex': '#FFD580'},
            {'name': 'Orange',       'hex': '#FF8C00'},
            {'name': 'Tangerine',    'hex': '#F28500'},
            {'name': 'Pumpkin',      'hex': '#FF7518'},
            {'name': 'Terracotta',   'hex': '#C1694F'},
            {'name': 'Burnt Orange', 'hex': '#CC5500'},
            {'name': 'Rust',         'hex': '#B7410E'},
            {'name': 'Sienna',       'hex': '#A0522D'},
        ]
    },
    {
        'keywords': ['brown'],
        'label': 'Brown Shades',
        'colors': [
            {'name': 'Nude',         'hex': '#E3C9A8'},
            {'name': 'Linen',        'hex': '#FAF0E6'},
            {'name': 'Beige',        'hex': '#F5F5DC'},
            {'name': 'Sand',         'hex': '#C8B89A'},
            {'name': 'Taupe',        'hex': '#B5A898'},
            {'name': 'Tan',          'hex': '#D2B48C'},
            {'name': 'Camel',        'hex': '#C19A6B'},
            {'name': 'Khaki',        'hex': '#C3B091'},
            {'name': 'Mocha',        'hex': '#967969'},
            {'name': 'Brown',        'hex': '#8B6914'},
            {'name': 'Chocolate',    'hex': '#7B3F00'},
            {'name': 'Mahogany',     'hex': '#C04000'},
            {'name': 'Chestnut',     'hex': '#954535'},
        ]
    },
    {
        'keywords': ['gray', 'grey'],
        'label': 'Gray Shades',
        'colors': [
            {'name': 'Platinum',     'hex': '#E5E4E2'},
            {'name': 'Silver',       'hex': '#C0C0C0'},
            {'name': 'Light Gray',   'hex': '#D3D3D3'},
            {'name': 'Ash',          'hex': '#B2BEB5'},
            {'name': 'Gray',         'hex': '#808080'},
            {'name': 'Stone',        'hex': '#928E85'},
            {'name': 'Slate',        'hex': '#708090'},
            {'name': 'Charcoal',     'hex': '#36454F'},
            {'name': 'Graphite',     'hex': '#374649'},
        ]
    },
    {
        'keywords': ['black'],
        'label': 'Dark & Black Shades',
        'colors': [
            {'name': 'Charcoal',      'hex': '#36454F'},
            {'name': 'Dark Charcoal', 'hex': '#333333'},
            {'name': 'Graphite',      'hex': '#374649'},
            {'name': 'Dark Gray',     'hex': '#2F2F2F'},
            {'name': 'Noir',          'hex': '#1A1A1A'},
            {'name': 'Black',         'hex': '#0A0A0A'},
            {'name': 'Jet Black',     'hex': '#000000'},
        ]
    },
    {
        'keywords': ['white'],
        'label': 'White & Light Shades',
        'colors': [
            {'name': 'White',         'hex': '#FFFFFF'},
            {'name': 'Ghost White',   'hex': '#F8F8FF'},
            {'name': 'Snow',          'hex': '#FFFAFA'},
            {'name': 'Ivory',         'hex': '#F5F0E8'},
            {'name': 'Cream',         'hex': '#FAF8F5'},
            {'name': 'Pearl White',   'hex': '#F8F5F0'},
            {'name': 'Off White',     'hex': '#FAF9F6'},
            {'name': 'Antique White', 'hex': '#FAEBD7'},
            {'name': 'Linen',         'hex': '#FAF0E6'},
        ]
    },
]


def _swatches_html():
    parts = []
    for name, hex_val in PALETTE.items():
        shadow = 'box-shadow:inset 0 0 0 1px #bbb;' if hex_val in LIGHT else ''
        parts.append(
            '<span'
            ' class="gcp-sw"'
            ' data-name="' + name + '"'
            ' title="' + name + '"'
            ' style="'
            'display:inline-block;'
            'width:28px;height:28px;'
            'border-radius:50%;'
            'cursor:pointer;'
            'border:2px solid #ddd;'
            'background:' + hex_val + ';'
            'margin:3px;'
            'vertical-align:middle;'
            'transition:transform .12s;' + shadow +
            '"></span>'
        )
    return ''.join(parts)


_SWATCHES  = _swatches_html()
_PAL_JSON  = json.dumps(PALETTE)
_FAM_JSON  = json.dumps(FAMILIES)

_JS_TEMPLATE = """
<script>
(function(){
  if(window.__geriCP) return;
  window.__geriCP = true;

  var FAMILIES = __FAM_JSON__;

  function isLight(hex){
    if(!hex || hex.charAt(0) !== '#' || hex.length < 7) return false;
    var r=parseInt(hex.slice(1,3),16), g=parseInt(hex.slice(3,5),16), b=parseInt(hex.slice(5,7),16);
    return (0.299*r + 0.587*g + 0.114*b)/255 > 0.82;
  }

  function detectFamily(query){
    if(!query || query.length < 2) return null;
    var q = query.toLowerCase().trim();
    for(var i=0; i<FAMILIES.length; i++){
      var f = FAMILIES[i];
      for(var k=0; k<f.keywords.length; k++){
        var kw = f.keywords[k];
        if(kw.indexOf(q) === 0 || q.indexOf(kw) === 0) return f;
      }
      for(var j=0; j<f.colors.length; j++){
        if(f.colors[j].name.toLowerCase().indexOf(q) !== -1) return f;
      }
    }
    return null;
  }

  function initOne(inp){
    if(inp.__gcp) return;
    inp.__gcp = true;

    var wrap       = inp.closest('.gcp-wrap');
    if(!wrap) return;
    var prev       = wrap.querySelector('.gcp-prev');
    var dropdown   = wrap.querySelector('.gcp-dd');
    var noMatch    = wrap.querySelector('.gcp-no-match');
    var famSection = wrap.querySelector('.gcp-fam-section');
    var famContent = wrap.querySelector('.gcp-fam-content');
    var palette    = JSON.parse(wrap.getAttribute('data-palette'));

    function getHex(val){
      var v = (val||'').trim();
      if(v.charAt(0) === '#') return v;
      if(palette[v]) return palette[v];
      var t = v.charAt(0).toUpperCase() + v.slice(1).toLowerCase();
      return palette[t] || null;
    }

    function updatePreview(val){
      var h = getHex(val);
      prev.style.background  = h || '#eee';
      prev.style.borderColor = h ? '#999' : '#ddd';
    }

    function markSelected(name){
      dropdown.querySelectorAll('.gcp-sw').forEach(function(sw){
        var sel = name && sw.getAttribute('data-name').toLowerCase() === name.toLowerCase();
        sw.style.borderColor = sel ? '#333' : '#ddd';
        sw.style.transform   = sel ? 'scale(1.15)' : 'scale(1)';
        sw.__sel = sel;
      });
    }

    function filterSwatches(query){
      var hasVisible = false;
      dropdown.querySelectorAll('.gcp-sw').forEach(function(sw){
        var show = !query || sw.getAttribute('data-name').toLowerCase().indexOf(query.toLowerCase()) !== -1;
        sw.style.display = show ? 'inline-block' : 'none';
        if(show) hasVisible = true;
      });
      if(noMatch) noMatch.style.display = (!hasVisible && query) ? 'block' : 'none';

      var fam = detectFamily(query);
      if(fam){
        var html = '<p style="font-size:10px;color:#aaa;font-family:sans-serif;'
                 + 'margin:0 0 7px;letter-spacing:.07em;text-transform:uppercase;">'
                 + fam.label + '</p>'
                 + '<div style="display:flex;flex-wrap:wrap;gap:5px;">';
        for(var i=0; i<fam.colors.length; i++){
          var c = fam.colors[i];
          var border = isLight(c.hex) ? '2px solid #ccc' : '2px solid transparent';
          html += '<div class="gcp-fam-sw"'
               +  ' data-hex="' + c.hex + '"'
               +  ' data-label="' + c.name + '"'
               +  ' title="' + c.name + '"'
               +  ' style="width:28px;height:28px;border-radius:50%;cursor:pointer;'
               +  'background:' + c.hex + ';border:' + border + ';'
               +  'transition:transform .12s;flex-shrink:0;"></div>';
        }
        html += '</div>';
        famContent.innerHTML = html;
        famSection.style.display = 'block';

        famContent.querySelectorAll('.gcp-fam-sw').forEach(function(sw){
          sw.addEventListener('mouseenter', function(){ this.style.transform='scale(1.2)'; });
          sw.addEventListener('mouseleave', function(){ this.style.transform='scale(1)'; });
          sw.addEventListener('mousedown', function(e){
            e.preventDefault();
            var lbl = this.getAttribute('data-label');
            var hex = this.getAttribute('data-hex');
            inp.value = lbl;
            prev.style.background  = hex;
            prev.style.borderColor = '#999';
            markSelected(null);
            dropdown.style.display = 'none';
          });
        });
      } else {
        famSection.style.display = 'none';
        famContent.innerHTML = '';
      }
    }

    dropdown.querySelectorAll('.gcp-sw').forEach(function(sw){
      sw.addEventListener('mouseenter', function(){ if(!this.__sel) this.style.transform='scale(1.2)'; });
      sw.addEventListener('mouseleave', function(){ if(!this.__sel) this.style.transform='scale(1)'; });
      sw.addEventListener('mousedown', function(e){
        e.preventDefault();
        var chosen = this.getAttribute('data-name');
        inp.value = chosen;
        updatePreview(chosen);
        markSelected(chosen);
        dropdown.style.display = 'none';
      });
    });

    inp.addEventListener('input', function(){
      filterSwatches(this.value);
      updatePreview(this.value);
      markSelected(this.value);
      dropdown.style.display = 'block';
    });

    inp.addEventListener('focus', function(){
      filterSwatches(this.value);
      markSelected(this.value);
      dropdown.style.display = 'block';
    });

    document.addEventListener('mousedown', function(e){
      if(!wrap.contains(e.target)) dropdown.style.display = 'none';
    });

    updatePreview(inp.value);
    markSelected(inp.value);
  }

  function initAll(){
    document.querySelectorAll('.gcp-input').forEach(initOne);
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  var jq = window.django && window.django.jQuery;
  if(jq) jq(document).on('formset:added', function(){ setTimeout(initAll, 100); });
  document.addEventListener('formset:added', function(){ setTimeout(initAll, 100); });
}());
</script>
"""

_JS = _JS_TEMPLATE.replace('__FAM_JSON__', _FAM_JSON)


class ColorPickerWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs['autocomplete'] = 'off'
        attrs['class']        = (attrs.get('class') or '') + ' gcp-input'
        attrs['style']        = 'flex:1;min-width:0;'

        input_html = str(super().render(name, value, attrs, renderer))

        html = (
            "<div class='gcp-wrap'"
            " data-palette='" + _PAL_JSON.replace("'", '&#39;') + "'"
            " style='position:relative;display:inline-flex;"
            "align-items:center;gap:6px;width:100%;'>"

            "<div class='gcp-prev'"
            " style='width:22px;height:22px;border-radius:50%;"
            "flex-shrink:0;background:#eee;border:2px solid #ddd;'>"
            "</div>"

            + input_html +

            "<div class='gcp-dd'"
            " style='display:none;position:absolute;z-index:9999;"
            "background:#fff;border:1px solid #ccc;border-radius:6px;"
            "padding:12px;top:calc(100% + 4px);left:0;min-width:320px;"
            "box-shadow:0 6px 20px rgba(0,0,0,0.15);'>"

            "<p style='font-size:10px;color:#aaa;margin:0 0 6px;"
            "font-family:sans-serif;letter-spacing:.06em;text-transform:uppercase;'>"
            "Your colours</p>"
            "<div>" + _SWATCHES + "</div>"
            "<p class='gcp-no-match'"
            " style='display:none;font-size:11px;color:#ccc;"
            "font-style:italic;font-family:sans-serif;margin:4px 0 0;'>"
            "No palette match — see shades below</p>"

            "<div class='gcp-fam-section' style='display:none;'>"
            "<div style='margin:10px 0 8px;border-top:1px solid #eee;'></div>"
            "<div class='gcp-fam-content'></div>"
            "</div>"

            "</div>"
            "</div>"
            + _JS
        )

        return mark_safe(html)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display        = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'color':
            kwargs['widget'] = ColorPickerWidget
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display        = ('name', 'category', 'price', 'available', 'created_at')
    list_filter         = ('available', 'category')
    search_fields       = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines             = [ProductVariantInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    list_filter  = ('status', 'created_at')
    inlines      = [OrderItemInline]
