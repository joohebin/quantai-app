# -*- coding: utf-8 -*-
"""Fix: escape # in onclick string"""
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Fix: replace the problematic .closest('#create-ch-modal') with a workaround
# Use .parentElement.closest or pass 'this' differently
# Actually the issue is: in a string literal, # creates a comment
# Fix: use document.getElementById instead

old_bad = ".closest('#create-ch-modal').remove()"
new_fixed = ".parentElement.remove()  // close modal"
t = t.replace(old_bad, new_fixed)

r = t.encode('utf-8', errors='replace')
with open(filepath, 'wb') as f:
    f.write(r)

# Quick syntax check
import subprocess
sidx = r.find(b'<script>', 200000)
# Actually let's find the script with initQuantTalk
scripts = []
idx = 0
while True:
    sidx = r.find(b'<script', idx)
    if sidx < 0: break
    snum = len(scripts) + 1
    if r[sidx:sidx+8] == b'<script>':
        cs = sidx + 8
    else:
        ct = r.find(b'>', sidx)
        cs = ct + 1
    eidx = r.find(b'</script>', cs)
    scripts.append((snum, cs, eidx, sidx))
    idx = eidx + 9
    if snum > 20: break

for snum, cs, eidx, sidx in scripts:
    content = r[cs:eidx]
    if b'initQuantTalk' in content:
        fname = f'/tmp/s{snum}_fix.js'
        with open(fname, 'wb') as f2:
            f2.write(content)
        result = subprocess.run(['node', '--check', fname], capture_output=True, text=True, timeout=10)
        print(f'Script {snum}: {result.returncode}')
        if result.returncode != 0:
            print(f'  Error: {result.stderr[:300]}')
        else:
            print(f'  ✅ SYNTAX OK!')
        break
