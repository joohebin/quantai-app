"""Fix: wrap .join() result in parens before ternary colon"""
import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

# The old pattern in raw bytes
old = b").join(''):'');"
new = b").join('')):'');"

count = r.count(old)
print(f'Found {count} occurrences')

if count > 0:
    r = r.replace(old, new)
    with open(filepath, 'wb') as f:
        f.write(r)

    # Verify
    count2 = r.count(new)
    old_count = r.count(old)
    print(f'After fix: {count2} fixed, {old_count} remaining old')
else:
    # Try looking for exact line
    sidx = r.find(b'<script>', 200000)
    cs = sidx + 8
    eidx = r.find(b'</script>', cs)
    c = r[cs:eidx]
    lines = c.split(b'\n')
    for i, l in enumerate(lines):
        if b"join('')" in l and b"'" in l and i >= 6389:
            print(f'Line {i+1}: {l}')

# Check syntax
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c)
res = subprocess.run(['node','--check','/tmp/sc.js'], capture_output=True, timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    err = res.stderr[:400]
    print(f'Error: {err}')
else:
    print('Syntax OK!')
print(f'Saved: {len(r)} bytes')
