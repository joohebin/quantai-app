# -*- coding: utf-8 -*-
"""Check showPage function and whether flow+log are inside page-arbitrage"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

arb_start = t.find('id="page-arbitrage"')
next_page = t.find('id="page-', arb_start + 50)

flow_pos = t.find('arb-flow-container', arb_start, next_page)
log_pos = t.find('arb-trade-log', arb_start, next_page)
print(f'arb-flow-container INSIDE page-arbitrage: {flow_pos >= 0}')
print(f'arb-trade-log INSIDE page-arbitrage: {log_pos >= 0}')

# Find showPage function to see how it works
sp = t.find('function showPage(')
print(f'\nshowPage at {sp}')
# Get the function
brace = t.find('{', sp)
depth = 0; i = brace
while depth >= 0:
    i += 1
    if i >= len(t): break
    if t[i] == '{': depth += 1
    elif t[i] == '}': depth -= 1
showPageFn = t[sp:i+1]
# Check if it hides/shows pages
print('showPage has page hiding logic:')
for line in showPageFn.split('\n'):
    if any(x in line for x in ['style.display', 'classList', 'page-', 'arbitrage']):
        print(f'  {line.strip()[:120]}')
