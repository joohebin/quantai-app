import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]

# Extract lines 6380-6410 as a standalone test
lines = c.split(b'\n')
test_code = b'\n'.join(lines[6379:6410])

with open('/tmp/test_render.js', 'wb') as f:
    f.write(test_code)

res = subprocess.run(['node', '--check', '/tmp/test_render.js'], capture_output=True, timeout=10)
print(f'Standalone check: {res.returncode}')
if res.returncode != 0:
    print(res.stderr.decode('utf-8', errors='replace')[:400])
else:
    print('Standalone OK!')
    # Try the full function
    # Find renderRequests function
    t = c.decode('utf-8', errors='replace')
    idx = t.find('function renderRequests')
    idx2 = t.find('function showAddFriend', idx)
    code = t[idx:idx2]
    with open('/tmp/test_render_fn.js', 'wb') as f:
        f.write(code.encode('utf-8'))
    res2 = subprocess.run(['node', '--check', '/tmp/test_render_fn.js'], capture_output=True, timeout=10)
    print(f'Function check: {res2.returncode}')
    if res2.returncode != 0:
        print(res2.stderr.decode('utf-8', errors='replace')[:400])
