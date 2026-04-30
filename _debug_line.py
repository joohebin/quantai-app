with open('index.html', 'rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
lines = c.split(b'\n')
l = lines[6390]
print('repr:', repr(l))
print('opens:', l.count(b'('))
print('closes:', l.count(b')'))
print('quotes:', l.count(b"'"))
# Check what's right before .join
idx = l.find(b'.join')
if idx > 0:
    print('Before .join:', l[max(0,idx-20):idx], '|')
    print('After .join:', l[idx:idx+30])
