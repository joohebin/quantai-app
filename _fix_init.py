import os
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

# Fix the broken init
old = b'square\'){ initQuantTalk(); renderSquare(\'all\'); }market\')'
new = b"square'){ initQuantTalk(); renderSquare('all'); }\n  if(name==='market')"
r = r.replace(old, new)
# Verify fix
if old in r:
    print('ERROR: old still present')
else:
    print('Fixed! Check syntax...')
    
# Also verify the backup file
with open(filepath, 'wb') as f:
    f.write(r)
    
# Extract script 3 again
sidx = 204863 + len(b'<script>')
eidx = r.find(b'</script>', sidx)
content = r[sidx:eidx]
with open('/tmp/s3.js', 'wb') as f:
    f.write(content)

import subprocess
result = subprocess.run(['node', '--check', '/tmp/s3.js'], capture_output=True, text=True, timeout=10)
print(f'Node check: {result.returncode}')
if result.returncode != 0:
    print(f'Error: {result.stderr[:300]}')
else:
    print('Syntax OK!')
