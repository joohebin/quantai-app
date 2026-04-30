# -*- coding: utf-8 -*-
"""Add a hidden cs-fab for JS compatibility"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find cs-panel opening
cs_panel = t.find('id="cs-panel"')
fab_insert = t.rfind('<div', cs_panel-200, cs_panel)
print(f'Insert before: {repr(t[fab_insert:fab_insert+60])}')

# Add hidden cs-fab
hidden_fab = '<!-- 悬浮按钮（隐藏，兼容旧代码） -->\n<div id="cs-fab" style="display:none" onclick="toggleCS()">💬<span class="cs-badge" id="cs-badge"></span></div>\n'
t = t[:fab_insert] + hidden_fab + t[fab_insert:]
print('Added hidden cs-fab')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))
    
# Verify
with open(filepath, 'rb') as f:
    data = f.read()
print('cs-fab count:', data.count(b'cs-fab'))
print('id="cs-fab":', data.count(b'id="cs-fab"'))
print('File: %.1f KB' % (len(data)/1024))
