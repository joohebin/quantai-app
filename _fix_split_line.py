"""Fix: separate the closing ); from the .join line to avoid any mysterious parse issue"""
import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
lines = c.split(b'\n')

# Find the problematic line
for i, l in enumerate(lines):
    if b").join('')+'':'');" in l or b").join('')+'':'';\r" in l:
        print(f'Found bad line {i+1}: {l}')
        # Replace )); with
        # ))
        # );
        old = l
        # The line is:     }).join('')+'':'');
        # Replace last   ;  with   \n  );
        # Find the last ;; Actually there's only one ; at the very end
        new = l[:-1] + b'\n' + b'  ' + l[-1:]  # split ; to new line
        lines[i] = new
        print(f'Fixed to: {new}')
        break

c = b'\n'.join(lines)
# Write back to index.html
sidx = r.find(b'<script>', 200000)
cs_orig = sidx + 8
eidx_orig = r.find(b'</script>', cs_orig)
r = r[:cs_orig] + c + r[eidx_orig:]

with open(filepath, 'wb') as f:
    f.write(r)

# Check syntax
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c2 = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c2)
res = subprocess.run(['node','--check','/tmp/sc.js'], capture_output=True, timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    err = res.stderr[:400]
    print(f'Error: {err}')
else:
    print('Syntax OK!')
print(f'Saved: {len(r)} bytes')
