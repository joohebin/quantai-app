with open('index.html', 'rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
lines = c.split(b'\n')
ln = 6390  # 0-indexed
err_line = lines[ln]
print('Hex dump of line 6391:')
for i in range(0, len(err_line), 16):
    chunk = err_line[i:i+16]
    hex_part = ' '.join(f'{b:02x}' for b in chunk)
    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
    print(f'{i:4d}: {hex_part:<48s} {ascii_part}')
print(f'\nRepr: {repr(err_line)}')
