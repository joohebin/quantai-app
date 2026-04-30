# -*- coding: utf-8 -*-
"""Verify the CS HTML structure is correct"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
# Find cs-related elements
for elem in ['cs-panel', 'cs-fab', 'cs-head', 'cs-msgs', 'cs-quickq', 'cs-foot', 'cs-input', 'cs-send', 'cs-av', 'cs-close', 'cs-status-txt']:
    p = t.find('id="' + elem + '"')
    if p > 0:
        ctx = t[p-30:p+80]
        print(f'✅ {elem} at {p}: {repr(ctx[:80])}')
    else:
        # Check if it's in CSS or JS
        ref = t.find(elem)
        if ref > 0:
            ctx = t[ref-20:ref+60]
            print(f'❌ {elem} (HTML id NOT found, but ref at {ref}: {repr(ctx[:60])})')
        else:
            print(f'❌ {elem}: COMPLETELY MISSING')
