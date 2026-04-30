# -*- coding: utf-8 -*-
"""Fix: page-square display CSS conflict"""
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

# 1. Fix page-square: remove inline display:flex, add proper CSS for active
# Old inline style
old_inline = b'style="display:flex;gap:0;min-height:500px;height:calc(100vh - 200px);overflow:hidden"'
new_style = b'id="page-square" style="gap:0;min-height:500px;height:calc(100vh - 200px);overflow:hidden"'

# Need to find the exact bytes
ps_idx = r.find(b'class="page" id="page-square"')
if ps_idx > 0:
    # Find the style ending
    style_end = r.find(b'"', ps_idx + 40)
    if style_end > 0 and style_end < ps_idx + 300:
        before = r[ps_idx:style_end+1]
        after = b'class="page" id="page-square" style="gap:0;min-height:500px;height:calc(100vh - 200px);overflow:hidden"'
        r = r[:ps_idx] + after + r[style_end+1:]
        print(f'Replaced page-square style')
        print(f'  Old: {before}')
        print(f'  New: {after}')
else:
    print('WARNING: page-square not found')

# 2. Add .page-square.active CSS rule
# Find .page.active in CSS
css_idx = r.find(b'.page.active')
if css_idx > 0:
    after_page_active = r.find(b'}', css_idx)
    flex_css = b'\n.page.active\\[id\\=page-square\\],.page#page-square.active{display:flex}'
    # Simpler: just add a rule
    flex_css = b'\n.page#page-square.active{display:flex;flex-direction:row}'
    r = r[:after_page_active+1] + flex_css + r[after_page_active+1:]
    print(f'Added flex CSS for #page-square.active')
else:
    print('WARNING: .page.active CSS not found')

with open(filepath, 'wb') as f:
    f.write(r)
print(f'Saved: {len(r)} bytes')

# Verify
if b'flex;flex-direction:row' in r:
    print('CSS OK')
if b'display:flex' not in r[:ps_idx+100]:
    print('Inline display:flex removed from HTML')
