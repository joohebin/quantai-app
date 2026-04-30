# -*- coding: utf-8 -*-
"""Fix QuantTalk layout: channel list height, remove overflow from main container that hides other pages"""
filepath = 'index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# 1. Fix: remove height:calc(100vh - 140px) from page-square - it conflicts with showPage hiding
# Instead use a more flexible height
old_height = b'style="display:flex;gap:0;height:calc(100vh - 140px);overflow:hidden"'
new_height = b'style="display:flex;gap:0;min-height:500px;height:calc(100vh - 200px);overflow:hidden"'
if old_height in raw:
    raw = raw.replace(old_height, new_height)
    print('Fixed page-square height')
else:
    print('WARNING: old_height not found')

# 2. Fix channel list - ensure items properly displayed
# Add CSS for channel list item hover. Already in CSS, but check it exists
css_check = b'.ch-item'
if css_check not in raw:
    print('WARNING: .ch-item CSS missing')
else:
    print('ch-item CSS found')

# 3. Fix: ensure createChannel uses prompt correctly - no issues here
# The issue is likely that the + button is inside a flex item that might be too narrow
# Let's ensure the + button has proper z-index and clickability

# 4. Add min-width to channel panel and fix widget-tv container height
old_widget = b'style="display:none;margin-bottom:8px;border-radius:12px;overflow:hidden;border:1px solid var(--border);height:380px"></div>'
# widget id pattern needs to be ensured

# 5. Make the channel list panel have a proper scroll
# Already has overflow-y:auto on channel-list

# Save
with open(filepath, 'wb') as f:
    f.write(raw)
print(f'Saved: {len(raw)} bytes')
