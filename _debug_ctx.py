with open('index.html', 'rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
lines = c.split(b'\n')
# Print lines 6375-6385
for i in range(6374, 6385):
    print(f'{i+1}: {lines[i]}')
