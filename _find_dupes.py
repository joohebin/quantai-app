# -*- coding: utf-8 -*-
"""Find and fix duplicate function declarations - remove OLD ones, keep NEW ones"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find all function definitions with their offsets
import re
fns = [(m.start(), m.group(1)) for m in re.finditer(r'function (\w+)\(', t)]
print('All function definitions:')
for pos, name in fns:
    print(f'  {pos:>8}: {name}')

# Find duplicates
from collections import Counter
name_counts = Counter(name for _, name in fns)
dupes = {name for name, count in name_counts.items() if count > 1}
print(f'\nDupes: {dupes}')

# Show duplicate positions
for pos, name in fns:
    if name in dupes:
        print(f'\n{name} at {pos}:')
        print(t[pos:pos+80])
