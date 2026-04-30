"""Fix all unescaped single quotes in JS innerHTML strings"""
import subprocess

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

# Fix 1: create-ch-modal X button
old1 = b"'<button onclick=\"document.getElementById('ch-settings-modal').remove()\" style=\"background:none;border:none;color:var(--muted,#888);font-size:20px;cursor:pointer;padding:4px 8px;border-radius:6px"
new1 = b"'<button onclick=\"this.parentElement.parentElement.parentElement.remove()\" style=\"background:none;border:none;color:var(--muted,#888);font-size:20px;cursor:pointer;padding:4px 8px;border-radius:6px"

if old1 in r:
    r = r.replace(old1, new1)
    print('1. Fixed ch-settings-modal X button')
else:
    print('1. ch-settings-modal X button not found')
    idx = r.find(b'ch-settings-modal').remove')
    if idx > 0:
        print(f'Found ch-settings at {idx}')
    else:
        idx = r.find(b'ch-settings-modal')
        if idx > 0:
            print(f'Found ch-settings-modal at {idx}: {r[idx:idx+120]}')

# Fix 2: saveChannelSettings also uses document.getElementById - check
# Actually the first fix for create-ch-modal was already applied. Now fix ch-settings-modal.

with open(filepath, 'wb') as f:
    f.write(r)

# Syntax check
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c)
res = subprocess.run(['node', '--check', '/tmp/sc.js'], capture_output=True, timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    for line in res.stderr.decode('utf-8', errors='replace').split('\n'):
        if 'SyntaxError' in line:
            print(f'  {line.split("Error: ")[-1][:120]}')
        elif 'Unexpected' in line:
            print(f'  {line.strip()[:120]}')
else:
    print('Syntax OK!')

print(f'Saved: {len(r)} bytes')
