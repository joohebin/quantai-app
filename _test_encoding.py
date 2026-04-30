# -*- coding: utf-8 -*-
"""Find key positions in index.html"""
filepath = 'index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# 1. Find account tab buttons area
keywords = [
    (b'acc-tab', 'tab buttons'),
    (b'switchAccountTab', 'switch function'),
    (b"tabIds = ['positions'", 'tabIds array'),
    (b'QuantTalk', 'QuantTalk refs'),
    (b'===== QuantTalk =====', 'QTalk CSS'),
    (b'function renderSquare', 'renderSquare fn'),
]
for kw, name in keywords:
    idx = raw.find(kw)
    print(f'{name}: idx={idx}, context={raw[idx:idx+60] if idx>=0 else "NOT FOUND"}')

# Find all page-* divs
idx = 0
pages = []
while True:
    idx = raw.find(b'class="page" id="page-', idx)
    if idx < 0:
        idx = raw.find(b'class="page" id=\'page-', idx)
    if idx < 0:
        break
    # Get the page name
    start = raw.find(b'page-', idx) + 5
    end = raw.find(b'"', start)
    if end < 0:
        end = raw.find(b"'", start)
    name = raw[start:end]
    pages.append((idx, name.decode('utf-8', errors='replace')))
    idx = end + 1

print(f'\nAll pages:')
for idx, name in pages:
    print(f'  {idx}: #{name}')

# Find exchanges tab button more carefully
ex_ref = b"'exchanges', this)"
ex_idx = raw.find(ex_ref)
if ex_idx > 0:
    start = max(0, ex_idx - 40)
    print(f'\nExchanges ref context: {raw[start:ex_idx+30]}')

# Check if tabIds has 'wallet' already
tab_idx = raw.find(b"tabIds")
if tab_idx > 0:
    print(f'\ntabIds context: {raw[tab_idx:tab_idx+150]}')
