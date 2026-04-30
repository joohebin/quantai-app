import subprocess

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

# Find the problematic script tag area
# The issue: in the create modal innerHTML string, there's:
# onclick="document.getElementById('create-ch-modal').remove()"
# Inside a single-quoted JS string, the ' closes the string.
# Fix: replace the single quotes with \x27

# Binary search for the pattern
idx = r.find(b'document.getElementById(\'create-ch-modal\').remove()')
if idx > 0:
    print(f'Found at {idx}')
else:
    print('Not found directly')
    # Try with escaped quotes in the binary
    # In the HTML file, the JS source has the inner quotes as single quotes
    # The outer template literal also uses single quotes
    # So the bytes look like: onclick="document.getElementById(\'create-ch-modal\').remove()"
    # No wait, in the source code it's:
    # m.innerHTML='...<button onclick="document.getElementById(\'create-ch-modal\').remove()"...
    # The backslash is in the JS source! So the bytes have: \'create-ch-modal\'
    idx2 = r.find(b"\\'create-ch-modal\\'")
    print(f'With backslash: {idx2}')
    
    if idx2 < 0:
        # The bytes might be the actual single quotes without backslash
        # because m.innerHTML uses '+ +' concatenation, so:
        # m.innerHTML='<div...>'+  (outer string)
        #   '<button onclick="document.getElementById('  (new string starts)
        #   +'create-ch-modal'+  (this breaks)
        # That's the exact bug!
        
        # Let's find the area around create-ch-modal
        pos = 0
        count = 0
        while True:
            pos = r.find(b'create-ch-modal', pos)
            if pos < 0: break
            count += 1
            ctx = r[pos-30:pos+80]
            print(f'  [{count}] at {pos}: {ctx}')
            pos += 1

print('\n---')
# Now let's check syntax to see what line 6111 looks like
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c)
res = subprocess.run(['node', '--check', '/tmp/sc.js'], capture_output=True, timeout=10)
print(f'Node check: {res.returncode}')
out = res.stderr.decode('utf-8', errors='replace')
for line in out.split('\n'):
    if 'SyntaxError' in line or '^' in line or 'create' in line.lower():
        print(line)
# Print context around line 6111
lines = c.split(b'\n')
if len(lines) > 6111:
    print(f'\nLine 6111: {lines[6111][:200]}')
    print(f'Line 6110: {lines[6110][:200]}')
