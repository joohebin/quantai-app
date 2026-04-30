import subprocess

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

old = b"'<span>'+ch.icon+'</span><span># '+ch.name+'</span>'+"
new = b"(ch.icon&&ch.icon.indexOf('data:')===0?'<img src=\"'+ch.icon+'\" style=\"width:20px;height:20px;border-radius:50%;object-fit:cover;vertical-align:middle\">':'<span>'+ch.icon+'</span>')+'<span># '+ch.name+'</span>'+"

if old in r:
    r = r.replace(old, new)
    print('1. Fixed renderChannelList')
else:
    print('1. NOT FOUND')
    idx = r.find(b'renderChannelList')
    if idx > 0:
        print(repr(r[idx:idx+550]))

with open(filepath, 'wb') as f:
    f.write(r)

# Syntax check
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c)
res = subprocess.run(['node', '--check', '/tmp/sc.js'], capture_output=True, timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    print(f'Error: {res.stderr.decode("utf-8", errors="replace")[:400]}')
else:
    print('Syntax OK!')
