import subprocess
with open('index.html','rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
res = subprocess.run(['node','--check','/tmp/sc.js'],capture_output=True,timeout=10)
out = res.stderr.decode('utf-8',errors='replace')
import re
for line in out.split('\n'):
    m = re.search(r'\((\d+):\d+\)', line)
    if m:
        ln = int(m.group(1))
        lns = c.split(b'\n')
        if ln <= len(lns):
            print(f'Line {ln}: {lns[ln-1][:250]}')
