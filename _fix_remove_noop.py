"""Fix: remove the +'' no-op from the ternary, fix unbalanced parens"""
import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# The problematic pattern is:
# }).join('')+'' : '');
# Where +'' is a no-op between .join('') and the ternary ':'.
# The fix: just remove the +''
old = "}).join('')+'':'');"
new = "}).join(''):'');"

if old in t:
    t = t.replace(old, new)
    print('1. Stripped + empty string')
else:
    print('1. Pattern not found')
    # Check binary
    if b"join('')+'':''" in r:
        print('Found in binary')
    else:
        # maybe the line split changed things
        pass

# Also check for the split version
old2 = "}).join('')+'':'')\n  ;"
new2 = "}).join(''):'')\n  ;"
if old2 in t:
    t = t.replace(old2, new2)
    print('2. Stripped + from split version')

r = t.encode('utf-8', errors='replace')
with open(filepath, 'wb') as f:
    f.write(r)

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
