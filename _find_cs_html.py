"""Find CS Widget panel HTML construction"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# The CS Widget panel HTML is created via JS innerHTML
# Look for the template literal that creates the panel
# search in the CS Widget script section (>720000)
idx = t.find('cs-panel')
if idx < 0: idx = t.find('CS Widget')

# Search in the CS Widget JS script
cs_script = t.find('<script>', 720000)
cs_end = t.find('</script>', cs_script + 8)
cs_js = t[cs_script+8:cs_end]
print(f'CS script: {cs_script} -> {cs_end} ({cs_end-cs_script} bytes)')

# Find cs-foot in JS (template literal)
for kw in ['cs-foot', 'cs-input', 'cs-msgs']:
    idx = cs_js.find(kw)
    if idx >= 0:
        start = max(0, idx-200)
        end = min(len(cs_js), idx+200)
        print(f'\n--- {kw} at relative {idx} ---')
        print(cs_js[start:end])
