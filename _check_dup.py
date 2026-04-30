# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
print(f'page-arbitrage count: {t.count("id=\"page-arbitrage\"")}')
print(f'arb-flow-container count: {t.count("arb-flow-container")}')
print(f'arb-trade-log count: {t.count("arb-trade-log")}')
# Check where second flow container is
i = t.find('arb-flow-container')
j = t.find('arb-flow-container', i+1)
if j > 0:
    print(f'First: {i}, Second: {j}')
    print(f'Context: {repr(t[j-50:j+80])}')
