# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
# Find the sidebar CS button
p = t.find('onclick="toggleCS()"')
sidebar_start = t.rfind('<!-- 悬浮按钮', 0, p)
print(f'Found at {p}')
# Replace just the div opening tag
old_tag = t[p-30:p-15]
print(f'Tag prefix: {repr(old_tag)}')
# Find the <div before onclick
div_start = t.rfind('<div', p-50, p)
div_end = t.find('>', div_start)
tag_text = t[div_start:div_end+1]
new_tag_text = '<div id="cs-sidebar-btn" onclick="toggleCS()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;cursor:pointer;border-top:1px solid var(--border);margin-top:8px;transition:all 0.2s;border-radius:8px;background:var(--card2);font-size:13px;font-weight:600">'
print(f'Tag: {repr(tag_text)}')
t = t.replace(tag_text, new_tag_text)
with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))
print(f'cs-sidebar-btn: {t.count("cs-sidebar-btn")}')
