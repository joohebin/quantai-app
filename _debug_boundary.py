# -*- coding: utf-8 -*-
"""Debug the page-arbitrage div boundaries"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
arb_pos = t.find('id="page-arbitrage"')
ctx = t[arb_pos:arb_pos+500]
print(ctx[:500])
print('===')
# Track depth
depth = 1
i = t.find('>', t.find('<div', arb_pos-20)) + 1
while depth > 0:
    i = t.find('</', i)
    if i < 0: break
    e = t.find('>', i)
    if t[i+2:e].strip() == 'div': depth -= 1
    i = e + 1
print(f'\nClose at {i}')
print(t[i-60:i+60])
