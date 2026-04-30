"""Extract renderRequests and surrounding context"""
with open('index.html', 'rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
t = c.decode('utf-8', errors='replace')

# Find renderRequests and surrounding functions
idx = t.find('function renderRequests')
idx2 = t.find('function renderFriends', idx)
# Also include a few lines before the function
start = max(0, idx - 500)

with open('/tmp/test_fr.js', 'w', encoding='utf-8') as f:
    f.write(t[start:idx2])

import subprocess
res = subprocess.run(['node', '--check', '/tmp/test_fr.js'], capture_output=True, timeout=10)
print(f'Test check: {res.returncode}')
if res.returncode != 0:
    print(res.stderr.decode('utf-8', errors='replace')[:400])
else:
    print('OK')
