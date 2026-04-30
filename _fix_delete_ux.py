"""Improve delete channel UX: hide delete button on default channels, show visible error"""
import subprocess

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# In showChannelSettings, conditionally show the delete button
# Only show delete button for non-default channels
# Current delete button line:
old_del_btn = "'<button onclick=\"deleteChannel()\" style=\"width:100%;padding:12px;border:1px solid var(--red,#e74c3c);border-radius:10px;background:transparent;color:var(--red,#e74c3c);font-size:14px;cursor:pointer\">🗑️ 删除频道</button>'+"

new_del_btn = "'+(!defaultIds||defaultIds.indexOf(ch.id)<0?'<button onclick=\"deleteChannel()\" style=\"width:100%;padding:12px;border:1px solid var(--red,#e74c3c);border-radius:10px;background:transparent;color:var(--red,#e74c3c);font-size:14px;cursor:pointer\">🗑️ 删除频道</button>':'<div style=\"text-align:center;padding:8px;font-size:11px;color:var(--muted,#888);border-top:1px solid var(--border,#2a3a5e);margin-top:8px\">默认频道不可删除</div>')+'"

if old_del_btn in t:
    t = t.replace(old_del_btn, new_del_btn)
    print('1. Fixed delete button to be conditional on default channels')
else:
    print('1. Delete button not found')
    idx = t.find('🗑️ 删除频道')
    if idx > 0:
        print(f'Found at {idx}: {t[idx-50:idx+50]}')

# Also update deleteChannel to accept a channel reference instead of using _sqCurrentChannel only
# And make it NOT show toast for defaults (since button is now hidden)

# And fix: the settings modal's ch variable needs defaultIds available
# Add defaultIds at the top of showChannelSettings or make it global
# Actually, defaultIds is defined inside deleteChannel. Let's add it to the settings function too.

old_settings_header = """function showChannelSettings(){
  var ch=_sqCurrentChannel;
  if(!ch) return;
  var existing=document.getElementById('ch-settings-modal');"""

new_settings_header = """function showChannelSettings(){
  var ch=_sqCurrentChannel;
  if(!ch) return;
  var defaultIds=['ch-general','ch-btc','ch-eth','ch-strategy','ch-livestream','ch-backtest'];
  var existing=document.getElementById('ch-settings-modal');"""

if old_settings_header in t:
    t = t.replace(old_settings_header, new_settings_header)
    print('2. Added defaultIds to showChannelSettings')
else:
    print('2. Settings header not found')

# Also simplify deleteChannel to not check defaults (button is hidden now)
old_delete_ch = """function deleteChannel(){
  var ch=_sqCurrentChannel;
  if(!ch) return;
  // Don't allow deleting default channels
  var defaultIds=['ch-general','ch-btc','ch-eth','ch-strategy','ch-livestream','ch-backtest'];
  if(defaultIds.indexOf(ch.id)>=0){toast('不能删除默认频道','warn');return;}
  // Show custom confirm modal"""

new_delete_ch = """function deleteChannel(){
  var ch=_sqCurrentChannel;
  if(!ch) return;
  // Show custom confirm modal"""

if old_delete_ch in t:
    t = t.replace(old_delete_ch, new_delete_ch)
    print('3. Simplified deleteChannel')
else:
    print('3. deleteChannel header not found')

r = t.encode('utf-8', errors='replace')
with open(filepath, 'wb') as f:
    f.write(r)

# Syntax check
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c)
res = subprocess.run(['node','--check','/tmp/sc.js'],capture_output=True,timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    out = res.stderr.decode('utf-8',errors='replace')
    for line in out.split('\n'):
        if 'SyntaxError' in line or 'Unexpected' in line:
            print(line[:200])
else:
    print('Syntax OK!')
print(f'Saved: {len(r)} bytes')
