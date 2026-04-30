"""
Insert voice JS into Script 2 (the QuantTalk script, 193124-718558).
Need to insert it right before the Friend System comment.
"""
import os, subprocess
TMP = os.environ.get('TEMP', '/tmp')

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# Find voice JS at the end (inserted by previous script)
vi = t.find('// ---- Voice Input (Web Speech API) ----')
print(f'Voice JS at: {vi}')

# Find its end - the next section
ve = t.find('\n// ----', vi + 5)
if ve < 0:
    # Should be near end of file
    ve = len(t)
    
voice_js = t[vi:ve]
print(f'Voice JS length: {len(voice_js)} chars')

# Remove from current position
t = t[:vi] + t[ve:]

# Find Friend System comment (still in correct position)
fs = t.find('// ---- Friend System ----')
print(f'Friend System comment at: {fs}')

# Insert voice JS before friend system
t = t[:fs] + '\n' + voice_js + '\n' + t[fs:]
print('Voice JS inserted before Friend System in Script 2')

# Write
r = t.encode('utf-8')
with open(filepath, 'wb') as f:
    f.write(r)
print(f'File: {len(r)} bytes')

# Verify
vi_new = t.find('function startVoiceInput')
fs_new = t.find('// ---- Friend System ----')
print(f'Voice: {vi_new}')
print(f'Friend: {fs_new}')
print(f'Friend is after voice: {fs_new > vi_new}')

# Syntax check
print('\n=== Syntax Check ===')
# Get Script 2 JS content
s2_open = 193132  # after <script>
s2_close = t.find('</script>', 193124)
c = t[193132:s2_close].encode('utf-8')
with open(os.path.join(TMP, 'sc.js'), 'wb') as f:
    f.write(c)
res = subprocess.run(['node', '--check', os.path.join(TMP, 'sc.js')], capture_output=True, timeout=15)
if res.returncode == 0:
    print('Syntax OK!')
else:
    err = res.stderr.decode('utf-8', errors='replace')[:800]
    print(f'ERROR:\n{err}')
