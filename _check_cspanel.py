# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
print('cs-panel:', t.count('id="cs-panel"'))
print('cs-fab:', t.count('cs-fab'))
print('cs-input:', t.count('cs-input'))
print('cs-head:', t.count('id="cs-head"'))
print('toggleCS calls:', t.count('toggleCS()'))
# Find cs-panel
p = t.find('id="cs-panel"')
print(f'cs-panel at: {p}')
if p > 0:
    print(t[p-50:p+200])
