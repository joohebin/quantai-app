import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
lines = c.split(b'\n')

# Find the error line from node
res = subprocess.run(['node','--check','/tmp/sc.js'], capture_output=True, timeout=10)
err = res.stderr.decode('utf-8', errors='replace')
for line in err.split('\n'):
    if 'SyntaxError' in line:
        import re
        m = re.search(r':(\d+):', line)
        if m:
            ln = int(m.group(1))
            print(f'Error line: {ln}')
            print(f'Line {ln}: {lines[ln-1]}')
            if ln > 2:
                print(f'Line {ln-1}: {lines[ln-2]}')
                print(f'Line {ln-2}: {lines[ln-3]}')
