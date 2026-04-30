# -*- coding: utf-8 -*-
import re

filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()
text = raw.decode('gbk', errors='replace')

nav_start = text.find('<nav>')
nav_end = text.find('</nav>', nav_start)
nav = text[nav_start:nav_end+6]

print("=== 导航菜单标签文字 ===\n")

# Split by nav-item
parts = nav.split('<div class="nav-item')
for i, part in enumerate(parts[1:], 1):
    end_idx = part.find('</div>')
    item = part[:end_idx]
    
    pg = re.search(r"showPage\('(\w+)'", item)
    page = pg.group(1) if pg else '?'
    
    # Find the label text - between data-i18n span and </div>
    # Strategy: find all text nodes
    spans = re.findall(r'<span[^>]*>([^<]*)</span>', item)
    # Remove all HTML tags
    plain = re.sub(r'<[^>]*>', '|', item)
    plain = re.sub(r'\|+', ' ', plain).strip()
    
    badge = ''
    bm = re.search(r'<span class="badge">([^<]*)</span>', item)
    if bm:
        badge = ' [' + bm.group(1) + ']'
    
    # Clean up spaces
    plain = re.sub(r'\s+', ' ', plain)
    
    print(f"  #{i:2d} {page:20s} {plain[:35]:35s} {badge}")
