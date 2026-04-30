"""
Replace right panel HTML + Insert friend system JS + Update initQuantTalk.
Uses actual emoji characters (no surrogate issues).
"""
import subprocess, os

filepath = 'index.html'
TMP = os.environ.get('TEMP', '/tmp')

with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# ===== 1. Replace right panel =====
idx = t.find('<!-- Right: Post Feed -->')
close1 = t.find('</div>', idx)
close2 = t.find('</div>', close1 + 6)
close3 = t.find('</div>', close2 + 6)
open_pos = t.find('<div ', idx, idx + 150)
print(f'Right panel: open={open_pos}, close={close3+6}, old_len={close3+6-open_pos}')

old = t[open_pos:close3+6]
print(f'Old: {old[:100]}...')

new_right = (
    '        <div style="width:280px;min-width:280px;background:var(--card);border:1px solid var(--border);border-radius:12px;display:flex;flex-direction:column;overflow:hidden">\n'
    '          <div style="display:flex;border-bottom:1px solid var(--border)">\n'
    '            <div class="fr-tab active" data-tab="rank" onclick="window.switchFRTab(\'rank\')" style="flex:1;padding:10px 0;text-align:center;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid var(--green);color:var(--green)">\U0001f3c6 \u6392\u884c\u699c</div>\n'
    '            <div class="fr-tab" data-tab="friends" onclick="window.switchFRTab(\'friends\')" style="flex:1;padding:10px 0;text-align:center;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;color:var(--muted)">\U0001f465 \u597d\u53cb</div>\n'
    '            <div class="fr-tab" data-tab="requests" onclick="window.switchFRTab(\'requests\')" style="flex:1;padding:10px 0;text-align:center;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;color:var(--muted)">\U0001f4e9 \u8bf7\u6c42</div>\n'
    '          </div>\n'
    '          <div id="fr-rank-panel" style="flex:1;overflow-y:auto;padding:8px;display:block"></div>\n'
    '          <div id="fr-friends-panel" style="flex:1;overflow-y:auto;padding:8px;display:none"></div>\n'
    '          <div id="fr-requests-panel" style="flex:1;overflow-y:auto;padding:8px;display:none"></div>\n'
    '        </div>'
)

t = t[:open_pos] + new_right + t[close3+6:]
print('Right panel replaced OK')

# ===== 2. Insert friend system JS =====
ins_idx = t.find('// ---- TradingView Widget ----')
print(f'JS insertion point: {ins_idx}')

# Read the JS from a separate file to avoid encoding issues
with open('_qt_functions.js', 'rb') as f:
    friend_js = f.read().decode('utf-8')

t = t[:ins_idx] + friend_js + t[ins_idx:]
print(f'Friend JS inserted ({len(friend_js)} chars)')

# ===== 3. Update initQuantTalk =====
old_init = (
    'function initQuantTalk(){\n'
    '  loadSQData();\n'
    '  renderChannelList();\n'
    '  if(_sqChannels.length > 0) switchChannel(_sqChannels[0].id);\n'
    '  initWalletUI();\n'
    '}'
)
new_init = old_init.replace('initWalletUI();', 'initWalletUI();\n  initFR();')
t = t.replace(old_init, new_init)
old_init_crlf = old_init.replace('\n', '\r\n')
new_init_crlf = new_init.replace('\n', '\r\n')
t = t.replace(old_init_crlf, new_init_crlf)
print('initQuantTalk updated')

# Write file
r = t.encode('utf-8')
with open(filepath, 'wb') as f:
    f.write(r)
print(f'File: {len(r)} bytes')

# ===== 4. Syntax check =====
print('\n=== Syntax Check ===')
sidx = r.find(b'<script>', 200000)
ce = r.find(b'</script>', sidx + 8)
c = r[sidx+8:ce]
with open(os.path.join(TMP, 'sc.js'), 'wb') as f:
    f.write(c)
res = subprocess.run(['node', '--check', os.path.join(TMP, 'sc.js')], capture_output=True, timeout=15)
if res.returncode == 0:
    print('Syntax OK!')
else:
    err = res.stderr.decode('utf-8', errors='replace')[:800]
    print(f'ERROR:\n{err}')
