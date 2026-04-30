# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

s0 = t.find('<script>', 910)
s0_close = t.find('</script>', s0)
content = t[s0+8:s0_close].strip()

# Track template literals
in_template = False
template_start = -1
for i, c in enumerate(content):
    if c == '`' and (i == 0 or content[i-1] != '\\'):
        if not in_template:
            in_template = True
            template_start = i
        else:
            in_template = False

if in_template:
    print(f'UNCLOSED backtick at pos {template_start}')
    ctx = content[max(0, template_start-100):template_start+100]
    print(f'Context: {repr(ctx)}')
else:
    print('All backticks paired')

opens = content.count('{')
closes = content.count('}')
print(f'S0: open={opens} close={closes} diff={opens-closes}')

# Also count template literals with regex
import re
backticks = [m.start() for m in re.finditer('`', content)]
print(f'Backtick positions: {len(backticks)} (should be even)')
if len(backticks) > 0 and len(backticks) % 2 == 1:
    last_open = backticks[-1]
    ctx = content[max(0, last_open-80):last_open+80]
    print(f'Last backtick (unclosed?): ...{repr(ctx)}...')
