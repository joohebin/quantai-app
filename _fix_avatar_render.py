# -*- coding: utf-8 -*-
"""Fix: renderChannelList - replace icon span with conditional avatar"""
import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

# Binary-level replacement for renderChannelList
old = b"return '<div class=\"ch-item\"+(active?' active':'')+'\" onclick=\"switchChannel(\\''+ch.id+'\\')\">'+\n      '<span>'+ch.icon+'</span><span># '+ch.name+'</span>'+"
new = b"return '<div class=\"ch-item\"+(active?' active':'')+'\" onclick=\"switchChannel(\\''+ch.id+'\\')\">'+\n      (ch.icon&&ch.icon.indexOf('data:')===0?'<img src=\"'+ch.icon+'\" style=\"width:20px;height:20px;border-radius:50%;object-fit:cover;vertical-align:middle\">':'<span>'+ch.icon+'</span>')+'<span># '+ch.name+'</span>'+"

if old in r:
    r = r.replace(old, new)
    print('1. Fixed renderChannelList')
else:
    print('1. WARN: renderChannelList not found in binary')

# Fix the node check issue: let me just verify syntax by extracting and checking
sidx = r.find(b'<script>', 200000)
if r[sidx:sidx+8] != b'<script>':
    ct = r.find(b'>', sidx)
    sidx = ct + 1
else:
    sidx = sidx + 8
eidx = r.find(b'</script>', sidx)
content = r[sidx:eidx]
with open('/tmp/s_check.js', 'wb') as f2:
    f2.write(content)
result = subprocess.run(['node', '--check', '/tmp/s_check.js'], capture_output=True, text=True, timeout=10)
print(f'Node check: {result.returncode}')
if result.returncode != 0:
    print(f'Error: {result.stderr[:400]}')
else:
    print(f'Syntax OK!')

with open(filepath, 'wb') as f:
    f.write(r)
print(f'Saved: {len(r)} bytes')
