import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]

# Wrap the .join('') in ( ... ) inside the ternary to make it unambiguous
# Pattern: }).join('') : '' -> }).join('')) : ''
# The .join('') needs to be wrapped so the : following it connects to the outer ternary

# Actually the REAL fix: the issue is that .join('') is inside a ternary expression
# but JS can't parse `.join('') :` because it looks like a label.
# Fix: wrap .join('') + any following + stuff in parens:
# }).join('')) : '')

# Let's find and fix the renderRequests function directly
# Find the function in binary
fn_start = c.find(b'function renderRequests')
fn_end = c.find(b'function showAddFriend', fn_start)
if fn_start > 0 and fn_end > 0:
    # Extract the function
    fn_bytes = c[fn_start:fn_end]
    print(f'Found renderRequests: {fn_start} -> {fn_end} ({len(fn_bytes)} bytes)')
    
    # Fix 1: wrap .join('') in the sent ternary in parens
    # Currently: }).join(''):'');
    # Fix to: }).join('')):'');
    old1 = b").join(''):'');"
    new1 = b").join('')):'');"
    
    count = fn_bytes.count(old1)
    print(f'Found pattern {count} times')
    
    if count > 0:
        fn_bytes = fn_bytes.replace(old1, new1)
    
    # Reconstruct the full C
    c = c[:fn_start] + fn_bytes + c[fn_end:]
    r = r[:cs] + c + r[eidx:]
    
    with open(filepath, 'wb') as f:
        f.write(r)
    
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
else:
    print('renderRequests not found')
