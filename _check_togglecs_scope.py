# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
p = t.find('function toggleCS()')
print(f'toggleCS at {p}')
# Show 200 chars before
ctx = t[max(0,p-500):p]
print('Before toggleCS:')
print(repr(ctx))
