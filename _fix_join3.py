"""Fix: add '' concatenation between .join() and ternary colon"""
import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

# Fix: }).join('')):''); -> we need }).join('')+'':'');
# But wait - the fix already added an extra ). Let me check current state
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
lines = c.split(b'\n')
print(f'Line 6391 current: {lines[6390]}')

# The issue: }).join('')+'':''); -- we need +'' between join('') and :
# Actually let me rethink. The structure is:
# (sent.length ? '...' + sent.map(...).join('') : '')
# 
# Since .join('') ends the expression and : starts the ternary else,
# we need the .join('') result to be connected. But JS sees .join('') as complete.
#
# Fix: }).join('')+'':''); 
# This adds + '' between .join('') and :

old = b").join('')):'');"  # current after 1st fix (extra paren)
new = b").join('')+'':'');"  # add empty string concat

if old in r:
    r = r.replace(old, new)
    print(f'1. Fixed join concat: {old.decode()} -> {new.decode()}')
else:
    # Try the original pattern
    old2 = b").join(''):'');"
    if old2 in r:
        r = r.replace(old2, new)
        print('1. Fixed join concat (original pattern)')
    else:
        print('1. Neither pattern found')
        # Check all occurrences of join('')
        for i, line in enumerate(lines):
            if b'join' in line and i >= 6380:
                print(f'  Line {i+1}: {line}')

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
