"""Find ALL CS Widget template HTML"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# Search the entire file for template strings that create CS panel
# Look for patterns like: '<div id="cs-foot'
idx = t.find('cs-foot', 720000)
if idx >= 0:
    start = max(0, idx-1000)
    end = min(len(t), idx+300)
    print(f'cs-foot in HTML/template at {idx}:')
    print(t[start:end])
else:
    print('cs-foot not found in HTML')

# Search for where the panel div is built
idx = t.find('<div id="cs-panel"')
if idx >= 0:
    print(f'\n--- cs-panel HTML at {idx} ---')
    print(t[idx:idx+800])
else:
    # Check if cs-panel is created via JS
    print('\ncs-panel not in HTML, checking JS...')

# Search raw binary for '<textarea' + 'cs-input' near each other
import re
for m in re.finditer(r'<textarea[^>]*cs-input', t):
    print(f'\n<textarea cs-input at {m.start()}:')
    print(t[m.start():m.start()+300])
