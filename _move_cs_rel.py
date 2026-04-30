# -*- coding: utf-8 -*-
"""
Move ALL CS Widget logic into script 4, then remove script 5 entirely.
Use script index approach - find scripts by their position.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find all script tags
scripts = []
i = 0
while True:
    s = t.find('<script>', i)
    if s < 0:
        s = t.find('<script ', i)
    if s < 0: break
    
    # Find the closing tag
    close = t.find('</script>', s) + 9
    
    src_attr = ''
    src_pos = t.find(' src=', s, s+50)
    if src_pos > 0 and src_pos < close:
        src_end = t.find('>', src_pos)
        src_attr = t[src_pos:src_end+1]
    
    scripts.append((s, close, src_attr))
    i = close

print(f'Total scripts: {len(scripts)}')
for idx, (s, e, src) in enumerate(scripts):
    has_toggle = 'toggleCS' in t[s:e]
    has_cs = '/* 客服 Widget' in t[s:e] or '客服 Widget 逻辑' in t[s:e]
    print(f'  {idx}: {s}-{e} ({e-s} chars) src={src[:30] if src else "inline"}, toggle={has_toggle}, CS={has_cs}')

# Script 5 (index 5) is the CS Widget script
s5_start, s5_end, _ = scripts[5]
s5_content = t[s5_start+8:s5_end-9]  # bare JS without <script></script>
print(f'\nScript 5 content: {len(s5_content)} chars')
print(f'First 50: {repr(s5_content[:50])}')

# Script 4 (index 4) is the diagnostic script that IS executed
s4_start, s4_end, _ = scripts[4]
print(f'\nScript 4: {s4_start} to {s4_end} ({s4_end-s4_start} chars)')

# Insert CS Widget JS into script 4 (before its closing </script>)
t = t[:s4_end-9] + '\n' + s5_content + '\n' + t[s4_end-9:]
print('Added CS Widget JS into script 4')

# Remove script 5 (the original)
t = t[:s5_start] + t[s5_end:]
print(f'Removed script 5 ({s5_end-s5_start} chars)')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')

# Recount scripts
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

print(f'\n=== Final Verification ===')
print(f'File: {len(data)/1024:.1f} KB')
print(f'Scripts: {len(scripts2)}')

for idx, (s, e) in enumerate(scripts2):
    has_toggle = 'toggleCS' in text[s:e]
    has_all = all(fn in text[s:e] for fn in ['csGreet', 'csAddMsg', 'csSendQuick'])
    print(f'  {idx}: {s}-{e} ({e-s} chars), toggle={has_toggle}, all={has_all}')

print(f'\nGlobal scope check:')
print(f'  toggleCS in window: {text.count("window.toggleCS")}')
