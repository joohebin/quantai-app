"""Fix: add background backdrop to delete modal"""
import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

old = b"z-index:10000;display:flex;align-items:center;justify-content:center'"
# The old CSS text without background
# Looking at m.style.cssText='position:fixed;inset:0;z-index:10000;display:flex...'

# Find the style.cssText pattern more carefully
idx = r.find(b'z-index:10000;display:flex')
if idx > 0:
    print(f'Found at {idx}: {r[idx:idx+100]}')
    # Replace just the z-index part to include background
    old_part = b'z-index:10000;display:flex'
    new_part = b'z-index:10000;background:rgba(0,0,0,.7);display:flex'
    r = r.replace(old_part, new_part)
    print('Added background backdrop')
else:
    print('Not found')

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
if res.returncode == 0:
    print('Syntax OK!')
print(f'Saved: {len(r)} bytes')
