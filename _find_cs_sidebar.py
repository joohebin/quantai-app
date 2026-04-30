# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
p = t.find('onclick="toggleCS()"')
ctx = t[p-150:p+120]
print(repr(ctx))
