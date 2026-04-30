# -*- coding: utf-8 -*-
"""SIMPLE: Append CS Widget JS to Script 0 (SW registration script that definitely executes)."""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find Script 0 (starts with "SW 仅在生产部署时启用")
s0 = t.find('// SW 仅在生产部署时启用')
s0_tag_open = t.find('<script>', s0-200)
s0_tag_close = t.find('</script>', s0_tag_open)

print(f'Script 0: {s0_tag_open} to {s0_tag_close} ({s0_tag_close-s0_tag_open} chars)')

# Find Script 4 (CS Widget, starts with "客服 Widget 逻辑")
s4 = t.find('// ===== 客服 Widget 逻辑 =====')
s4_tag_open = t.find('<script>', s4-200)
s4_tag_close = t.find('</script>', s4_tag_open) + 9

s4_content = t[s4_tag_open:s4_tag_close]

print(f'Script 4 (CS Widget): {s4_tag_open} to {s4_tag_close} ({s4_tag_close-s4_tag_open} chars)')

# Insert CS Widget content BEFORE the closing </script> of Script 0
t = t[:s0_tag_close-9] + '\n' + s4_content + '\n' + t[s0_tag_close-9:]
print('Merged CS Widget into Script 0')

# Remove original Script 4
# After insertion, s4 offsets shifted. Find by marker again.
s4_new = t.find('// ===== 客服 Widget 逻辑 =====', s0_tag_close+1)
s4_new_tag_open = t.find('<script>', s4_new-200)
s4_new_tag_close = t.find('</script>', s4_new_tag_open) + 9
print(f'Remove original Script 4 at: {s4_new_tag_open} to {s4_new_tag_close}')

t = t[:s4_new_tag_open] + t[s4_new_tag_close:]
print(f'Removed original Script 4 ({s4_new_tag_close-s4_new_tag_open} chars)')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')

# Count scripts
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
    cs = 'toggleCS' in c or 'csGreet' in c or 'csAddMsg' in c
    print(f'  {idx}: {e-s} chars, CS={cs}')
