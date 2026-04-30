# -*- coding: utf-8 -*-
"""
Fix server-side extra braces. The server file has 2 extra } at the end of CS Widget.
Find them and remove them for a clean deploy.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find CS Widget content (should be in script 0)
cs_start = t.find('// ===== 客服 Widget 逻辑 =====')
if cs_start < 0:
    cs_start = t.find('// ===== CS Widget')

# Find end of CS Widget content in the script
# It ends when we hit either another comment block, or the original CS code finishes
print(f'CS Widget starts at: {cs_start}')

# Let's look for the pattern that causes the issue
# The CS Widget original should end with window.addEventListener or similar
# After the CS Widget code comes: "}\n  }" (extra braces)

# Search for the clean end of CS Widget
widget_end_sentinel = t.find("// 初始化时渲染一次", cs_start)
if widget_end_sentinel > 0:
    print(f'Widget end sentinel at: {widget_end_sentinel}')
    # Show what's before and after
    print(f'Before: {repr(t[widget_end_sentinel-100:widget_end_sentinel])}')
    end_of_file = t[widget_end_sentinel:]
    # Remove the extra trailing } characters
    print(f'After: {repr(end_of_file[:200])}')
    
    # Count trailing braces
    stripped = end_of_file.rstrip()
    extra = end_of_file[len(stripped):]
    print(f'Trailing whitespace: {repr(extra[:20])}')
    
    # Look for "}\n  }" at the end
    for i in range(len(end_of_file)-1, len(end_of_file)-20, -1):
        if end_of_file[i] == '}':
            # Remove this brace
            pass

# Alternative: just find and count all braces in the file
total_open = t.count('{')
total_close = t.count('}')
print(f'\nTotal: {{ = {total_open}, }} = {total_close}, diff = {total_open - total_close}')

# Find the mismatch location
# Walk through the file and track brace balance
balance = 0
mismatch_at = 0
for i, ch in enumerate(t):
    if ch == '{': balance += 1
    elif ch == '}':
        balance -= 1
        if balance < 0:
            # But this is fine in JS - some brackets close outer scopes
            pass

# The issue might be simpler - let's check if the CS Widget original file has this issue
# by looking at the raw CS Widget from Script 4 (in memory)
print(f'\nFile size: {len(t)/1024:.1f} KB')
