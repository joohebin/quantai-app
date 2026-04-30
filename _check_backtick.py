# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Check S0's JS for unclosed backtick
s0 = t[t.find('<script>', 910):t.find('</script>', t.find('<script>', 910))]
js = s0.split('>', 1)[1].rsplit('<', 1)[0]

# Find modal.innerHTML template
idx = js.find('modal.innerHTML')
print(f'modal.innerHTML at: {idx}')
print(f'Context: {repr(js[idx:idx+200])}')
print()
# Find all backticks near it
for i in range(idx, min(idx+2000, len(js))):
    if js[i] == '`':
        ctx = js[max(0,i-40):i+40]
        print(f'Backtick at {i}: ...{repr(ctx)}...')

# Count ALL backticks
backtick_count = js.count('`')
print(f'\nTotal backticks: {backtick_count}')
