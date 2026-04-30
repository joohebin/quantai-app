"""Fix syntax error: unescaped single quotes in JS string literal"""
import subprocess

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

# Fix line 6110: change inner single quotes to escaped
# Old: onclick="document.getElementById('create-ch-modal').remove()"
# New: onclick="document.getElementById(\x27create-ch-modal\x27).remove()"
# In bytes this is: onlclick=\"document.getElementById(\\x27create-ch-modal\\x27).remove()\"

old_bytes = b"'<button onclick=\"document.getElementById('create-ch-modal').remove()\" style=\"background:none;border:none;color:var(--muted,#888);font-size:20px;cursor:pointer;padding:4px 8px;border-radius:6px"
new_bytes = b"'<button onclick=\"this.parentElement.parentElement.remove()\" style=\"background:none;border:none;color:var(--muted,#888);font-size:20px;cursor:pointer;padding:4px 8px;border-radius:6px"

if old_bytes in r:
    r = r.replace(old_bytes, new_bytes)
    print('1. Fixed unescaped quotes in create modal X button')
else:
    print('1. Pattern not found')
    # Try different approach - search for the key part
    idx = r.find(b"getElementById('create-ch-modal').remove()")
    if idx > 0:
        # Replace just the onclick value
        old2 = b"getElementById('create-ch-modal').remove()"
        new2 = b"closest('.create-ch-modal').remove()"  # won't work
        print(f'Found at {idx}')
        context = r[idx-5:idx+100]
        print(f'Context: {context}')

# Also fix the same issue in showChannelSettings (the code uses \x27 which is already escaped, should be fine)
# And saveChannelSettings

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
    # Print error lines only
    for line in res.stderr.decode('utf-8', errors='replace').split('\n'):
        if 'SyntaxError' in line:
            print(f'  {line}')
        elif '^' in line:
            pass  # the caret markers
else:
    print('Syntax OK!')

with open(filepath, 'wb') as f:
    f.write(r)
print(f'Saved: {len(r)} bytes')
