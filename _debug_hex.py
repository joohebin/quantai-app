import subprocess
with open('index.html', 'rb') as f:
    r = f.read()

# Check for BOM
print('BOM:', r[:3])

sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]

# Extract the exact line that errors
lines = c.split(b'\n')
err_line = None

# Re-run node to confirm which line errors
res = subprocess.run(['node', '--check', '/tmp/sc.js'], capture_output=True, timeout=10)
import re
err_text = res.stderr.decode('utf-8', errors='replace')
m = re.search(r':(\d+):', err_text)
if m:
    ln = int(m.group(1))
    err_line = lines[ln-1]
    print(f'Error line {ln} (0-index: {ln-1})')
    print(f'Hex dump: {err_line.hex()}')
    print(f'Length: {len(err_line)} bytes')
    print(f'Repr: {repr(err_line)}')
    
    # Check for zero-width chars
    for i, ch in enumerate(err_line):
        if ch < 32 and ch not in (9, 10, 13, 32):  # non-standard whitespace
            print(f'  Non-standard char at pos {i}: {ch}')
    
    # Check for Unicode chars in the specific area
    decoded = err_line.decode('utf-8', errors='replace')
    print(f'Decoded: {decoded}')
    
    # Check each char
    for i, ch in enumerate(decoded):
        if ord(ch) > 255:
            print(f'  Unicode char at pos {i}: U+{ord(ch):04X} ({ch})')
