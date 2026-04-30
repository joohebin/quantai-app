# -*- coding: utf-8 -*-
"""
ROOT FIX: Script 5 (CS Widget) is never executed by the browser.
Don't merge - instead, just add `window.` prefix to every function in CS Widget.
We inject at the end of Script 0 with `window.fnName = function fnName(...`.

Actually, simplest: Add a tiny script at very end that exposes functions.

But wait - all functions in CS Widget are global func declarations.
They DON'T become window props because the script containing them has a syntax error
(2 extra } braces from prior botched edits).

The REAL fix: clean up the extra braces.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Count total braces
opens = t.count('{')
closes = t.count('}')
diff = opens - closes
print(f'Brace diff: {diff} ({opens} open, {closes} close)')

# Walk to find brace imbalance
if diff != 0:
    balance = 0
    min_balance = 0
    for i, ch in enumerate(t):
        if ch == '{': balance += 1
        elif ch == '}': balance -= 1
        if balance < min_balance:
            min_balance = balance
            print(f'  Min balance={balance} at char {i}: {repr(t[max(0,i-20):i+20])}')

# Check before the </html> tag for trailing braces
html_close = t.rfind('</html>')
before_html = t[html_close-500:html_close]
print(f'\nBefore </html> (last 500 chars):')
print(repr(before_html))
