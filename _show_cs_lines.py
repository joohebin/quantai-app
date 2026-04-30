# -*- coding: utf-8 -*-
"""Check the local file for syntax errors near CS Widget"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
# Find CS Widget and show lines around it
cs_start = t.find('// ===== CS Widget')
lines = t[cs_start:cs_start+3000].split('\n')
for i, l in enumerate(lines[:50]):
    print(f'{i:>3}: {l}')
