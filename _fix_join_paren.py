import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Fix the join(''):''); pattern
# It's currently: }).join(''):'');
# Needs: }).join('')):
old = "}).join(''):'');"
new = "}).join('')):'');"

if old in t:
    t = t.replace(old, new)
    print('1. Fixed join paren')
else:
    print('1. Pattern not found')
    # Try binary
    idx = r.find(b"join(''):''")
    if idx > 0:
        old_b = b"join(''):'');"
        new_b = b"join('')):'');"
        r = r.replace(old_b, new_b)
        print(f'1. Binary fixed at {idx}')
        with open(filepath, 'wb') as f:
            f.write(r)

# Re-read if we did binary
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Also fix: the old right panel was only 110 chars so the replacement likely went wrong
# The old_right was found at 105519 with only 110 chars - that's just the closing </div>
# Let me check the full right panel structure
idx = t.find('id=\"fr-tabs\"')
if idx > 0:
    print(f'2. Friend right panel found at {idx}')
else:
    print('2. Friend right panel NOT found')
    idx2 = t.find('fr-rank-panel')
    if idx2 > 0:
        print(f'fr-rank-panel at {idx2}')
    else:
        print('fr-rank-panel NOT found')

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
    err = res.stderr[:500]
    print(f'Error: {err}')
else:
    print('Syntax OK!')
print(f'Saved: {len(r)} bytes')
