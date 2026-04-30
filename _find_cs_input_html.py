"""Find the exact CS input template creation"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# The CS Widget creates the panel HTML in a template literal.
# Search for the innerHTML assignment that creates cs-foot and cs-input
cs_js = t[720887:724962]

# Find where the cs-foot div is created (in template literal)
for kw in ['cs-foot', 'cs-input-wrap', 'cs-input"', 'cs-send"', '<textarea']:
    idx = cs_js.find(kw)
    if idx >= 0:
        print(f'--- {kw} at abs {720887+idx} ---')
        start = max(0, idx-100)
        end = min(len(cs_js), idx+200)
        print(cs_js[start:end])
        print()
