# -*- coding: utf-8 -*-
import re
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
for m in re.finditer(r'cs-panel', t):
    ctx = t[max(0,m.start()-30):m.start()+100]
    print(f'  {m.start()}: {repr(ctx[:80])}')
