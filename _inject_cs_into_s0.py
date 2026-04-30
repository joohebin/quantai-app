# -*- coding: utf-8 -*-
"""KISS: Extract CS functions from Script 4, append to Script 0 as plain JS (no script tags)."""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Extract CS Widget JS from Script 4 (bare content, no <script> tags)
s4 = t.find('// ===== 客服 Widget 逻辑 =====')
s4_open = t.find('<script>', s4-200)
s4_close = t.find('</script>', s4_open) + 9

# Get bare JS content
cs_js = t[s4_open+8:s4_close-9]  # strip <script> and </script>

print(f'CS JS: {len(cs_js)} chars')

# Append to Script 0 (SW script)
s0 = t.find('// SW 仅在生产部署时启用')
s0_tag_open = t.find('<script>', s0-200)
s0_tag_close = t.find('</script>', s0_tag_open)

# Insert bare JS before closing </script> of Script 0
# Make sure there's no embedded script tags
cs_js_clean = cs_js.replace('<script>', '').replace('</script>', '')
t = t[:s0_tag_close-9] + '\n// ===== CS Widget (merged into S0 for execution) =====\n' + cs_js_clean + '\n' + t[s0_tag_close-9:]

print(f'Inserted into S0 (at {s0_tag_close-9})')

# Now remove Script 4 
s4_new = t.find('// ===== 客服 Widget 逻辑 =====')
# Check if it's inside our merged S0 or the original
# It should be found twice now - once in S0, once original
s4_positions = []
i = 0
while True:
    i = t.find('// ===== 客服 Widget 逻辑 =====', i)
    if i < 0: break
    s4_positions.append(i)
    i += 1

for p in s4_positions:
    ctx = t[max(0,p-20):p+50]
    print(f'  CS marker at {p}: {repr(ctx[:50])}')

# The SECOND occurrence is the original Script 4
if len(s4_positions) >= 2:
    orig_pos = s4_positions[1]
    orig_open = t.find('<script>', orig_pos-200)
    orig_close = t.find('</script>', orig_open) + 9
    print(f'Removing original CS Widget: {orig_open} to {orig_close}')
    t = t[:orig_open] + t[orig_close:]

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')

scripts = []
i = 0
while True:
    s = text.find('<script>', i)
    if s < 0:
        s = text.find('<script ', i)
    if s < 0: break
    e = text.find('</script>', s) + 9
    scripts.append((s, e))
    i = e

print(f'\n=== Final ===')
print(f'File: {len(data)/1024:.1f} KB')
print(f'Scripts: {len(scripts)}')
for idx, (s, e) in enumerate(scripts):
    c = text[s+8:e-9]
    toggle = 'function toggleCS' in c
    greet = 'function csGreet' in c
    all_cs = '// ===== 客服 Widget 逻辑 =====' in c
    print(f'  {idx}: {e-s} chars, toggle={toggle}, greet={greet}, full={all_cs}')
