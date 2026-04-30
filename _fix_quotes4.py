import subprocess

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

# Fix the settings modal X button
old = b"'<button onclick=\"document.getElementById('ch-settings-modal').remove()\" style=\"background:none;border:none;color:var(--muted,#888);font-size:20px;cursor:pointer;padding:4px 8px;border-radius:6px"
new = b"'<button onclick=\"this.parentElement.parentElement.parentElement.remove()\" style=\"background:none;border:none;color:var(--muted,#888);font-size:20px;cursor:pointer;padding:4px 8px;border-radius:6px"

if old in r:
    r = r.replace(old, new)
    print('Fixed ch-settings-modal X button')
else:
    print('Pattern not found')
    idx = r.find(b'ch-settings-modal')
    if idx > 0:
        print(f'Context: {r[idx:idx+200]}')

with open(filepath, 'wb') as f:
    f.write(r)

sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c)
res = subprocess.run(['node', '--check', '/tmp/sc.js'], capture_output=True, timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    out = res.stderr.decode('utf-8', errors='replace')
    for line in out.split('\n'):
        if 'SyntaxError' in line or 'Unexpected' in line:
            print(line[:150])
else:
    print('Syntax OK!')
    
print(f'Saved: {len(r)} bytes')
