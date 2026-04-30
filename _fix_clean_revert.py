"""Clean fix: revert to original simple delete button, fix deleteChannel UX with custom modal"""
import subprocess

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Revert the showChannelSettings to use simple delete button (original working version)
# Find the conditional delete string and replace with plain button
old_cond = "'+(!defaultIds||defaultIds.indexOf(ch.id)<0?'<button onclick=\"deleteChannel()\" style=\"width:100%;padding:12px;border:1px solid var(--red,#e74c3c);border-radius:10px;background:transparent;color:var(--red,#e74c3c);font-size:14px;cursor:pointer\">"
new_plain = "'<button onclick=\"deleteChannel()\" style=\"width:100%;padding:12px;border:1px solid var(--red,#e74c3c);border-radius:10px;background:transparent;color:var(--red,#e74c3c);font-size:14px;cursor:pointer\">"

if old_cond in t:
    t = t.replace(old_cond, new_plain)
    print('1. Reverted conditional button to plain')
else:
    print('1. Conditional not found')
    # Check what IS at that position
    idx = t.find('!defaultIds||defaultIds')
    if idx > 0:
        print(f'Found ternary at {idx}: {t[idx:idx+80]}')
    else:
        # No conditional — maybe already clean from revert
        print('No ternary found - file might already be clean')

# Also fix the second part of the ternary (default msg)
old_cond2 = "':'<div style=\"text-align:center;padding:8px;font-size:11px;color:var(--muted,#888);border-top:1px solid var(--border,#2a3a5e);margin-top:8px\">"
if old_cond2 in t:
    print('2. Conditional msg still present')
    # Find the full pattern and remove it
    # It ends with "')+'" 
    idx2 = t.find(old_cond2)
    end_ternary = t.find("')+'", idx2 + 200)
    if end_ternary > 0 and end_ternary - idx2 < 300:
        full = t[idx2-2:end_ternary+4]
        t = t.replace(full, "'+ch.id+'")  # just close cleanly
        print('2. Removed conditional msg')
    
# Also remove the "<div id='delete-area-wrapper'>" that was added by previous script
old_wrapper = '<div id="delete-area-wrapper" data-delete-area></div>'
if old_wrapper in t:
    t = t.replace(old_wrapper, '')
    print('3. Removed delete-area wrapper')

# Also remove the defaultIds line from showChannelSettings (added by _fix_delete_ux.py)
old_default = 'var defaultIds=[\'ch-general\',\'ch-btc\',\'ch-eth\',\'ch-strategy\',\'ch-livestream\',\'ch-backtest\'];\n  var existing=document.getElementById(\'ch-settings-modal\');'
new_original = 'var existing=document.getElementById(\'ch-settings-modal\');'

if old_default in t:
    t = t.replace(old_default, new_original)
    print('4. Removed defaultIds from settings header')

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
res = subprocess.run(['node','--check','/tmp/sc.js'], capture_output=True, timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    err_data = res.stderr[:400]
    print(f'Error: {err_data}')
else:
    print('Syntax OK!')
print(f'Saved: {len(r)} bytes')
