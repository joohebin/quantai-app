# -*- coding: utf-8 -*-
"""Fix: remove OLD initArbitragePage (last one) - keep our sim engine version"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find ALL initArbitragePage definitions and their line numbers
import re
for m in re.finditer(r'function initArbitragePage\(\)', t):
    # Find function body
    start = m.start()
    # Find opening brace
    brace = t.find('{', start)
    # Track nested braces to find end
    depth = 0
    for i in range(brace, len(t)):
        if t[i] == '{': depth += 1
        elif t[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    print(f'initArbitragePage: {start} to {end} ({end-start} chars)')
    print(f'  First 120: {repr(t[start:start+120])}')
    if end - start < 30:
        print(f'  FULL (minimal): {repr(t[start:end])}')
    else:
        print(f'  Last 120: {repr(t[end-120:end])}')
    print()
