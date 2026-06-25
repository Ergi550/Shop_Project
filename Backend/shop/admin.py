import json
from django import forms  # needed for forms.TextInput base class
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


_SWATCHES = _swatches_html()
_PAL_JSON = json.dumps(PALETTE)

_JS = """
<script>
(function(){
  if(window.__geriCP) return;
  window.__geriCP = true;

  function initOne(inp){
    if(inp.__gcp) return;
    inp.__gcp = true;

    var wrap = inp.closest('.gcp-wrap');
    if(!wrap) return;
    var prev     = wrap.querySelector('.gcp-prev');
    var dropdown = wrap.querySelector('.gcp-dd');
    var palette  = JSON.parse(wrap.getAttribute('data-palette'));

    function getHex(name){
      var n = (name||'').trim();
      if(palette[n]) return palette[n];
      var t = n.charAt(0).toUpperCase() + n.slice(1).toLowerCase();
      return palette[t] || null;
    }

    function updatePreview(val){
      var h = getHex(val);
      prev.style.background  = h || '#eee';
      prev.style.borderColor = h ? '#999' : '#ddd';
    }

    function filterSwatches(query){
      dropdown.querySelectorAll('.gcp-sw').forEach(function(sw){
        var show = !query || sw.getAttribute('data-name').toLowerCase().indexOf(query.toLowerCase()) !== -1;
        sw.style.display = show ? 'inline-block' : 'none';
      });
    }

    function markSelected(name){
      dropdown.querySelectorAll('.gcp-sw').forEach(function(sw){
        var selected = sw.getAttribute('data-name').toLowerCase() === (name||'').toLowerCase();
        sw.style.borderColor = selected ? '#333' : '#ddd';
        sw.style.transform   = selected ? 'scale(1.15)' : 'scale(1)';
      });
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
            "<p style='font-size:11px;color:#999;margin:0 0 8px;"
            "font-family:sans-serif;'>Click a colour to select</p>"
            "<div>" + _SWATCHES + "</div>"
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
