# -*- coding: utf-8 -*-
"""Show tail of page-arbitrage"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
arb_start = t.find('id="page-arbitrage"')
next_page = t.find('id="page-', arb_start + 50)
print(t[next_page-500:next_page])
