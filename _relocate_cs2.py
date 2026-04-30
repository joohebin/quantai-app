# -*- coding: utf-8 -*-
"""Move the AI客服 Widget FAB button from bottom-right to sidebar user card area"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# 1. Find the #cs-fab CSS + button in the widget section
fab_marker = 'id="cs-fab"'
fab_pos = t.find(fab_marker)
if fab_pos < 0:
    fab_pos = t.find('cs-fab')
print(f'cs-fab at: {fab_pos}')

if fab_pos > 0:
    # The cs-fab is a floating button div. Remove it but keep the rest of widget.
    # Find the full div: <div id="cs-fab" ...>...</div>
    div_start = fab_pos - 2  # Go to start of div tag
    # Scan backwards to find <div
    while div_start > 0 and t[div_start] != '<':
        div_start -= 1
        # Safety: if we go too far back 
        if fab_pos - div_start > 200:
            div_start = t.rfind('<div', fab_pos-200, fab_pos)
            break
    # Find closing </div> of cs-fab
    # The fab div is simple: <div id="cs-fab" onclick="toggleCS()">💬</div>
    div_end = t.find('</div>', fab_pos) + 6
    print(f'Removing cs-fab: {div_start} to {div_end}')
    print(f'Content: {repr(t[div_start:div_end])}')
    
    # Remove the FAB button
    before = t[:div_start].rstrip()
    after = t[div_end:].lstrip()
    t = before + '\n' + after
    
    print('Removed cs-fab button from bottom-right')

# 2. Add the CS entry to sidebar user card area
card_start = t.find('id="sidebar-user-card"')
if card_start < 0:
    card_start = t.find('sidebar-user-card')
print(f'sidebar-user-card at: {card_start}')

if card_start > 0:
    # Find the nav section after user card
    nav_start = t.find('id="sidebar-nav"', card_start)
    print(f'sidebar-nav at: {nav_start}')
    
    cs_sidebar_entry = '''
          <div onclick="toggleCS()" style="display:flex;align-items:center;gap:8px;padding:8px 16px;cursor:pointer;border-top:1px solid var(--border);margin-top:4px;transition:background 0.2s;border-radius:8px" onmouseover="this.style.background='var(--hover)'" onmouseout="this.style.background='transparent'">
            <span style="font-size:16px">💬</span>
            <span style="font-size:13px" data-i18n="cs_sidebar">官方客服</span>
          </div>'''
    
    t = t[:nav_start] + cs_sidebar_entry + t[nav_start:]
    print('Added CS entry to sidebar')

# 3. Add cs_sidebar i18n key if missing
if 'cs_sidebar' not in t:
    # Chinese
    zh_marker = "nav_dashboard:'仪表盘'"
    zh_pos = t.find(zh_marker)
    if zh_pos > 0:
        line_end = t.find('\n', zh_pos)
        t = t[:line_end+1] + f"    cs_sidebar:'官方客服',\n" + t[line_end+1:]
        print('Added cs_sidebar to ZH')
    
    # English
    en_marker = "nav_dashboard:'Dashboard'"
    en_pos = t.find(en_marker)
    if en_pos > 0:
        line_end = t.find('\n', en_pos)
        t = t[:line_end+1] + f"    cs_sidebar:'Customer Service',\n" + t[line_end+1:]
        print('Added cs_sidebar to EN')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')
print(f'\nFile: {len(data)/1024:.1f} KB')
print(f'cs-fab: {data.count(b"cs-fab")}')
print(f'cs_sidebar: {data.count(b"cs_sidebar")}')
print(f'toggleCS: {data.count(b"toggleCS")}')
