"""
Fix: Put voice JS into the QuantTalk script (Script 3, ~206KB-799KB).
Script 3 starts at 206344 (after <script>), ends at 799727 (before </script>).
Insert voice JS before the friend system section.
"""
import os, subprocess
TMP = os.environ.get('TEMP', '/tmp')

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# Find script 3 boundaries: <script> at ~206KB, </script> at ~799KB
s3_open = t.find('<script>', 200000)
s3_close = t.find('</script>', s3_open + 8)
print(f'Script 3: {s3_open} -> {s3_close}')

# Find friend system section
fs = t.find('// ---- Friend System ----', s3_open, s3_close)
print(f'Friend System comment at: {fs}')

# Find voice JS at end of file
vi = t.find('// ---- Voice Input (Web Speech API) ----')
if vi >= 0:
    # Find end of voice section (next // ---- or end of file)
    ve = t.find('\n// ----', vi + 5)
    if ve < 0:
        ve = len(t)
    voice_js = t[vi:ve]
    print(f'Voice JS found at {vi}->{ve} ({len(voice_js)} chars)')
    
    # Remove it from end of file
    t = t[:vi] + t[ve:]
    print('Removed from end')
    
    # Insert it into script 3, before friend system
    t = t[:fs] + voice_js + '\n' + t[fs:]
    print('Inserted into Script 3 before Friend System')
    
    # Write
    r = t.encode('utf-8')
    with open(filepath, 'wb') as f:
        f.write(r)
    print(f'File: {len(r)} bytes')
    
    # Verify
    vi_new = t.find('function startVoiceInput')
    before = t[vi_new-100:vi_new]
    ls_open = before.rfind('<script>')
    ls_close = before.rfind('</script>')
    print(f'Before voice: ...{before[-80:]}...')
    print(f'Last tag: script_open={ls_open}, script_close={ls_close}')
    if ls_open > ls_close:
        print('Voice is INSIDE a script tag')
    else:
        print('Voice is OUTSIDE - still wrong')
else:
    print('Voice JS not found')
    print('Looking for startVoiceInput...')
    svi = t.find('function startVoiceInput')
    if svi >= 0:
        print(f'Found at {svi}')
        before = t[svi-100:svi]
        print(f'Context: {before}')

# Syntax check
print('\n=== Syntax Check ===')
sidx = r.find(b'<script>', 200000)
ce = r.find(b'</script>', sidx + 8)
c = r[sidx+8:ce]
with open(os.path.join(TMP, 'sc.js'), 'wb') as f:
    f.write(c)
res = subprocess.run(['node', '--check', os.path.join(TMP, 'sc.js')], capture_output=True, timeout=15)
if res.returncode == 0:
    print('Syntax OK!')
else:
    err = res.stderr.decode('utf-8', errors='replace')[:800]
    print(f'ERROR:\n{err}')
