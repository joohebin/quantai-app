# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

old = '<div onclick="toggleCS()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;cursor:pointer;border-top:1px solid var(--border);margin-top:8px;transition:all 0.2s;border-radius:8px;background:var(--card2);font-size:13px;font-weight:600">\n          <span style="font-size:16px">💬</span>\n          <span style="font-size:13px" data-i18n="cs_sidebar">官方客服</span>\n        </div>'
new = '<div id="cs-sidebar-btn" onclick="toggleCS()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;cursor:pointer;border-top:1px solid var(--border);margin-top:8px;transition:all 0.2s;border-radius:8px;background:var(--card2);font-size:13px;font-weight:600">\n          <span style="font-size:16px">💬</span>\n          <span style="font-size:13px" data-i18n="cs_sidebar">官方客服</span>\n        </div>'

if old in t:
    t = t.replace(old, new)
    print('Replaced!')
else:
    # Try with \r\n
    old2 = old.replace('\n', '\r\n')
    new2 = new.replace('\n', '\r\n')
    if old2 in t:
        t = t.replace(old2, new2)
        print('Replaced with CRLF!')
    else:
        print('NOT FOUND')
        # Debug
        p = t.find('onclick="toggleCS()" style=')
        print(repr(t[p:p+180]))

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))
