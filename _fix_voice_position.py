"""
Fix: Move voice JS inside the last <script> tag, before its </script>.
The last script (CS Widget) ends at 729990 with </script>.
Voice JS was appended at end of file - move it.
"""
import os, subprocess
TMP = os.environ.get('TEMP', '/tmp')

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# Extract voice JS from end of file
vi = t.find('// ---- Voice Input (Web Speech API) ----')
if vi < 0:
    print('Voice JS not found at all!')
    exit(1)

# Find where it ends (next function or file end)
# Voice JS functions: startVoiceInput, then maybe end of file
voice_end = t.find('\n// ----', vi + 5)
if voice_end < 0:
    voice_end = len(t)

voice_js = t[vi:voice_end]
print(f'Voice JS found: {vi}->{voice_end} ({len(voice_js)} chars)')

# Remove it from end
t = t[:vi] + t[voice_end:]

# Find the last </script> in the CS Widget section (script 4)
# The last script is around 729990
ls = t.rfind('</script>', 700000)
print(f'Last </script> at: {ls}')

# Insert voice JS before this </script>
t = t[:ls] + '\n' + voice_js + '\n' + t[ls:]
print('Voice JS moved inside script tag')

# Write
r = t.encode('utf-8')
with open(filepath, 'wb') as f:
    f.write(r)
print(f'File: {len(r)} bytes')

# Check
vi_new = t.find('function startVoiceInput')
before = t[vi_new-200:vi_new]
last_script_open = before.rfind('<script>') 
last_script_close = before.rfind('</script>')
if last_script_open > last_script_close:
    print('✅ Voice JS is now inside a <script> tag!')
else:
    print('❌ Still outside script tags')

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
