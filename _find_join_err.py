import sys
with open('index.html', 'rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]

# Find the problematic area
lines = c.split(b'\n')
for i, l in enumerate(lines):
    if b'sent.length' in l or l.strip().startswith(b'}).join'):
        safe = l.decode('utf-8', errors='replace')
        sys.stdout.write(f'{i+1}: {safe}\n')
