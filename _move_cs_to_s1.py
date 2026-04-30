# -*- coding: utf-8 -*-
"""
Definitive fix: Move CS Widget OUT of Script 0 into Script 1.
Script 0 has been corrupted by prior merge attempts.
Script 1 (75 bytes, API_BASE) is trivial and will never fail to execute.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Locate scripts
s0_start = t.find('<script>', 910)
s0_end = t.find('</script>', s0_start) + 9

s1_start = t.find('<script>', s0_end)
s1_end = t.find('</script>', s1_start) + 9

s4_start = t.find('<script', t.find('<script', t.find('<script', t.find('<script', s1_end)+1)+1)+1)
s4_end = t.find('</script>', s4_start) + 9

print(f'S0: {s0_start}-{s0_end} (len={s0_end-s0_start})')
print(f'S1: {s1_start}-{s1_end} (len={s1_end-s1_start})')
print(f'S4: {s4_start}-{s4_end} (len={s4_end-s4_start})')

# Extract CS Widget content from S4 (the original CS Widget script)
# and S0 (the merged copy we need to remove)
# Strategy: S1 becomes the CS Widget script
#          S0 keeps SW code + AI Gateway but NOT CS Widget
#          Original S4 (diagnostic) stays

# The CS Widget code is currently embedded in S0 after '// ===== CS Widget'
# We need to:
# 1. Find where CS Widget starts in S0
# 2. Extract it
# 3. Remove it from S0
# 4. Insert it into S1 (replacing API_BASE)

s0_content = t[s0_start:s0_end]
cs_start = s0_content.find('// ===== CS Widget')
if cs_start < 0:
    print('ERROR: CS Widget not in S0!')
    exit(1)

# What's before CS Widget is SW registration + AI Gateway intro
# What's after is the CS Widget + AI Gateway code
# We need to keep: SW registration + AI Gateway code (NOT CS Widget)
# Actually, the AI Gateway code ('QuantAI AI GATEWAY') is also part of CS merge

# Let me separate: CS Widget goes to S1
# S0 keeps: SW code + '// ===== 客服 Widget' before the actual widget code
# Wait, let me look at S0 structure more carefully

# Actually, the SMARTEST approach:
# S0 is corrupted. Replace it with CLEAN Script 0 from git base.
# Then add CS Widget as S1.
# But that would lose the DeepSeek + AI Gateway changes.

# SIMPLEST: Just move the CS function declarations to S1
# Find all function declarations in S0 that are 'cs*' functions
# Move them to S1, keeping everything else in S0

# Find the CS Widget block boundaries
# The block starts at '// ===== CS Widget ...' and includes ALL code
# through the AI Gateway section. Let me find what's CS-only vs what's Gateway

# The Gateway section starts at:
# '// ═══════════════════ QuantAI AI GATEWAY'
# Everything above that line + the Gateway CS integration = CS Widget

cs_widget_line = s0_content.find('// ===== CS Widget')
gateway_line = s0_content.find('// ═══════════════════ QuantAI AI GATEWAY')

cs_widget_code = s0_content[cs_widget_line:gateway_line]
print(f'\nCS Widget code: {len(cs_widget_code)} chars')

# S1 replacement: API_BASE var at start, then CS widget code
# But CS widget uses CS_CONFIG, CS_KB, csOpen etc - all need to be there
s1_new = '<script>\n  // 后端API地址\n  window.API_BASE = \'http://54.151.143.233:8001\';\n\n' + cs_widget_code.strip() + '\n</script>'

# Remove CS widget from S0 content
# Keep: S0 head (through Gateway line) + Gateway code (from gateway_line)
# + any remaining code after CS Widget
s0_before = s0_content[:cs_widget_line]
s0_after = s0_content[gateway_line:]
s0_kept = s0_before + s0_after

print(f'S0 kept: {len(s0_kept)} chars')
print(f'S1 new: {len(s1_new)} chars')

# Also check: Gateway code references _csHistory which is defined in CS Widget
# We need to keep _csOpen, _csHistory etc in S0 or ensure they're accessible
# The easiest: also move the state variables/constants to S1
# But that would break Gateway code in S0.

# Wait - the better approach: keep EVERYTHING in S0 but ALSO put CS Widget in S1.
# This means duplicate definitions, but S0's definitions would be hoisted first
# and S1's duplicates would simply redeclare.
# But `const`/`let` can't be redeclared. So we need to be careful.

# Actually let's just put the ENTIRE Gateway + Widget in S1.
# S0 keeps ONLY the SW registration code.

# Find SW code: before CS Widget
sw_code = s0_content[8:cs_widget_line].strip()  # 8 = len('<script>\n')
# Keep SW code only in S0
s0_new = '<script>\n' + sw_code + '\n</script>'

# S1 gets everything: CS Widget + API_BASE + Gateway + Gateway-CS integration
cs_gateway = s0_content[cs_widget_line:]
s1_new = '<script>\n  window.API_BASE = \'http://54.151.143.233:8001\';\n\n' + cs_gateway.strip() + '\n</script>'

# Verify brace balance for S1
opens = (s1_new.split('<script>')[1].split('</script>')[0]).count('{')
closes = (s1_new.split('<script>')[1].split('</script>')[0]).count('}')
print(f'\nS1 braces: {{ = {opens}, }} = {closes}, diff = {opens - closes}')

# Rebuild file
t = t[:s0_start] + s0_new + t[s0_end:s1_start] + s1_new + t[s1_end:]

# Also remove the '}\n}' that was added by _remove_if_wrapper.py at S0 end
# Actually they should be there now matching the { from before

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Final verification
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Count all scripts  
scripts = []
pos = 0
while True:
    s = t.find('<script', pos)
    if s < 0: break
    e = t.find('</script>', s) + 9
    scripts.append((s, e, e-s))
    pos = e

print(f'\nFinal scripts: {len(scripts)}')
for i, (s, e, l) in enumerate(scripts):
    s_opens = t[s:e].count('{')
    s_closes = t[s:e].count('}')
    toggle = 'toggleCS' in t[s:e]
    csGreet = 'csGreet' in t[s:e]
    print(f'  S{i}: {l} chars, braces={{={s_opens},}}={s_closes} diff={s_opens-s_closes}, toggle={toggle}, csGreet={csGreet}')

# Check overall file
f_opens = t.count('{')
f_closes = t.count('}')
print(f'\nFile total: {{ = {f_opens}, }} = {f_closes}, diff = {f_opens - f_closes}')

# Node check S1
import subprocess
s1_content = t[s1_start:s1_end]
s1_js = s1_content.split('>')[1].rsplit('<', 1)[0]
with open('/tmp/s1_check.js', 'w', encoding='utf-8') as f:
    f.write(s1_js)
result = subprocess.run(['node', '--check', '/tmp/s1_check.js'], capture_output=True, text=True, timeout=10)
print(f'Node S1 check: {result.returncode}')
if result.stderr:
    print(f'  {result.stderr[:300]}')
else:
    print('  No errors!')
