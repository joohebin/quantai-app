# -*- coding: utf-8 -*-
"""Show the HTML structure around page-arbitrage"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
arb_pos = t.find('id="page-arbitrage"')
# Show from page-arbitrage start for 3000 chars
ctx = t[arb_pos:arb_pos+3000]
print(ctx)
