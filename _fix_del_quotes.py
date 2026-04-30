import subprocess

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

# Fix: inner single quotes in onclick attributes inside JS string literals
# These appear in: document.getElementById('del-ch-modal').remove()
# Fix: use this.parentElement.parentElement.remove() instead

# Pattern 1: cancel button
old1 = b"getElementById('del-ch-modal').remove()"
new1 = b"closest('#del-ch-modal').remove()"  # Bad: same problem

# Better: use parent traversal
old1 = b"document.getElementById('del-ch-modal').remove()"
new1 = b"this.closest('#del-ch-modal').remove()"  # bad again with #

# Simplest: use this.parentElement traversal
# The HTML structure: cancel button is inside a div(button row) inside the dialog div(modal-content)
# button -> div(flex) -> div(container) -> div(overlay) which is #del-ch-modal
# So button.parentElement.parentElement = modal
old1_short = b"onclick=\"document.getElementById('del-ch-modal').remove()\" style=\"flex:1"
new1_short = b"onclick=\"this.parentElement.parentElement.remove()\" style=\"flex:1"

if old1_short in r:
    r = r.replace(old1_short, new1_short)
    print('1. Fixed cancel button onclick')
else:
    print('1. Pattern not found')
    idx = r.find(b'del-ch-modal')
    if idx > 0:
        print(f'Found at {idx}: {r[idx-40:idx+100]}')

with open(filepath, 'wb') as f:
    f.write(r)

# Verify
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c)
res = subprocess.run(['node','--check','/tmp/sc.js'],capture_output=True,timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    out = res.stderr.decode('utf-8',errors='replace')
    for ln in out.split('\n'):
        if 'SyntaxError' in ln or 'Unexpected' in ln:
            print(ln[:200])
else:
    print('Syntax OK!')

print(f'Saved: {len(r)} bytes')
