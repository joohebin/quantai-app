# -*- coding: utf-8 -*-
"""
Simple approach: Merge CS Widget (Script 4) into Script 1 (84 chars).
Script 0=SW, Script 1=tiny, Script 2=main 489KB, Script 3=diagnostic, Script 4=CS Widget.
Script 4 is never executed. Move its content into Script 1.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find scripts by positions
scripts = []
i = 0
while True:
    s = t.find('<script>', i)
    if s < 0:
        s = t.find('<script ', i)
    if s < 0: break
    close = t.find('</script>', s) + 9
    scripts.append((s, close))
    i = close

print(f'Scripts: {len(scripts)}')
for idx, (s, e) in enumerate(scripts):
    content = t[s+8:e-9]  # bare JS
    print(f'  {idx}: {s}-{e} ({e-s} chars), has toggleCS={"toggleCS" in content}')

# Script 1 content
s1_start, s1_end = scripts[1]
s1_bare = t[s1_start+8:s1_end-9]
print(f'\nScript 1 current: {repr(s1_bare)}')

# Script 4 (CS Widget)
s4_start, s4_end = scripts[4]
s4_bare = t[s4_start+8:s4_end-9]
print(f'Script 4 (CS Widget): {len(s4_bare)} chars')

# Replace script 1 content with CS Widget JS
# Keep script 1's original content
t = t[:s1_start+8] + '\n// CS Widget (moved for execution)\n' + s4_bare + '\n' + t[s1_end-9:]
print('Replaced script 1 with CS Widget content')

# Remove script 4 (original CS Widget)
# Recalculate positions after insertion
new_s1_end = s1_start + 8 + len(s4_bare) + 30  # approximate
# Actually find it properly
s4_new_start = t.find('// ===== 客服 Widget 逻辑 =====')
script_tag_start = t.rfind('<script>', s4_new_start-200, s4_new_start)
script_tag_end = t.find('</script>', s4_new_start) + 9

if script_tag_start > 0:
    t = t[:script_tag_start] + t[script_tag_end:]
    print(f'Removed original script 4 ({script_tag_end - script_tag_start} chars)')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')

scripts2 = []
i = 0
while True:
    s = text.find('<script>', i)
    if s < 0:
        s = text.find('<script ', i)
    if s < 0: break
    close = text.find('</script>', s) + 9
    scripts2.append((s, close))
    i = close

print(f'\n=== Final ===')
print(f'File: {len(data)/1024:.1f} KB')
print(f'Scripts: {len(scripts2)}')
for idx, (s, e) in enumerate(scripts2):
    content = text[s+8:e-9]
    cs = 'toggleCS' in content or 'csGreet' in content
    print(f'  {idx}: {e-s} chars, CS={cs}')

print(f'\nCS functions in window:')
print(f'  window.toggleCS: {text.count("window.toggleCS")}')
