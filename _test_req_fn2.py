import subprocess
with open('index.html', 'rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
t = c.decode('utf-8', errors='replace')

idx = t.find('function renderRequests')
idx2 = t.find('function renderFriends', idx)
start = max(0, idx - 500)

with open('/tmp/test_fr.js', 'w', encoding='utf-8') as f:
    f.write(t[start:idx2])

res = subprocess.run(['node', '--check', '/tmp/test_fr.js'], capture_output=True, timeout=10)
print(f'Test check: {res.returncode}')
if res.returncode != 0:
    err = res.stderr.decode('utf-8', errors='replace')
    # Write to file for inspection
    with open('/tmp/test_err.txt', 'w') as f:
        f.write(err)
    print(f'Error lines: {len(err.split(chr(10)))}')
    for line in err.split(chr(10)):
        if 'SyntaxError' in line or 'Unexpected' in line:
            print(line[:200])
else:
    print('OK')
