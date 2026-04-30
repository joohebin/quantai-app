# -*- coding: utf-8 -*-
"""Fix: verify syntax properly"""
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

# Find Script 4 (main app with initQuantTalk)
idx = 0
snum = 0
while True:
    sidx = r.find(b'<script', idx)
    if sidx < 0: break
    snum += 1
    if r[sidx:sidx+8] == b'<script>':
        cs = sidx + 8
    else:
        ct = r.find(b'>', sidx)
        cs = ct + 1
    eidx = r.find(b'</script>', cs)
    content = r[cs:eidx]
    
    if b'initQuantTalk' in content:
        print(f'Script {snum}: {sidx}->{eidx} ({len(content)} bytes)')
        fname = f'/tmp/s{snum}_check.js'
        with open(fname, 'wb') as f2:
            f2.write(content)
        import subprocess
        result = subprocess.run(['node', '--check', fname], capture_output=True, text=True, timeout=10)
        print(f'  Node check: {result.returncode}')
        if result.returncode != 0:
            print(f'  Error: {result.stderr[:300]}')
        else:
            print(f'  SYNTAX OK!')
        break
    
    idx = eidx + 9
    if snum > 20: break
