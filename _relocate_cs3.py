# -*- coding: utf-8 -*-
"""Fix: place CS entry right after sidebar-user-card, before </aside>"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find sidebar-user-card closing divs
card = t.find('id="sidebar-user-card"')
card_close = t.find('</div>', card)  # close user-card
card_close = t.find('</div>', card_close+5)  # close container
print(f'sidebar-user-card close at: {card_close}')
print(f'After: {repr(t[card_close:card_close+80])}')

# Find the </aside> that closes sidebar
aside_close = t.find('</aside>', card_close)
print(f'</aside> at: {aside_close}')
print(f'Before aside close: {repr(t[aside_close-30:aside_close])}')

# Remove the cs_sidebar entry that was inserted at wrong place
cs_sid = t.find('cs_sidebar', 49000)
if cs_sid > 0:
    # Find and remove the injected div
    # It was inserted before somewhere wrong - let's find toggleCS in sidebar context
    wrong = t.find('onclick="toggleCS()"')
    if wrong > 0:
        # Remove from start of div to next component
        div_s = t.rfind('<div', wrong-200, wrong)
        div_e = t.find('\n', t.find('\n', t.find('\n', wrong)))
        # Extend to end of the CS div
        div_e = t.find('\n', div_e+1) 
        if div_e > 0:
            t = t[:div_s] + t[div_e:]
            print(f'Removed misplaced CS entry from {div_s} to {div_e}')

# Insert CS entry right before </aside>
cs_sidebar_entry = '''
        <div onclick="toggleCS()" style="display:flex;align-items:center;gap:8px;padding:10px 16px;cursor:pointer;border-top:1px solid var(--border);margin-top:8px;transition:background 0.2s;border-radius:8px" onmouseover="this.style.background='var(--hover)'" onmouseout="this.style.background='transparent'">
          <span style="font-size:16px">💬</span>
          <span style="font-size:13px" data-i18n="cs_sidebar">官方客服</span>
        </div>'''

t = t[:aside_close] + cs_sidebar_entry + t[aside_close:]
print('Inserted CS entry before </aside>')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')
print(f'\nFile: {len(data)/1024:.1f} KB')
# Check cs-fab removed
fab_count = data.count(b'id="cs-fab"')
# Actually the button tag uses class, not id - let me check
print(f'cs-fab button remaining: {fab_count}')
print(f'toggleCS sidebar entry: {text.count("onclick=\"toggleCS()\"")}')
print(f'cs_sidebar: {data.count(b"cs_sidebar")}')
