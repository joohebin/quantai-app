# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
p = t.find('onclick="toggleCS()"')
print(f'toggleCS onclick at: {p}')
if p > 0:
    ctx = t[p-100:p+150]
    print(repr(ctx))
print('toggleCS defined:', t.find('function toggleCS()'))
print('toggleCS calls:', t.count('onclick="toggleCS()"'))
