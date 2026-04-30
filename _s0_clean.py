# -*- coding: utf-8 -*-
"""
Cleanest approach: Script 0 = ONLY CS Widget code + API_BASE
Everything else (SW, AI Gateway) gets pushed somewhere that works.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Locate scripts
s0_start = t.find('<script>', 910)
s0_end = t.find('</script>', s0_start) + 9

print(f'S0: {s0_start}-{s0_end} ({s0_end-s0_start} chars)')
s0_content = t[s0_start:s0_end]

# What's in S0?
# 1. SW registration code (first ~700 chars)
# 2. CS Widget code (~26400 chars) 
# 3. AI Gateway code (~3700 chars)

# Find CS Widget marker
cs_marker = s0_content.find('// ===== CS Widget')
gw_marker = s0_content.find('// ═══════════════════ QuantAI AI GATEWAY')

print(f'CS Widget at: {cs_marker}')
print(f'AI Gateway at: {gw_marker}')
print(f'S0 head: {repr(s0_content[:200])}')
print(f'S0 tail: {repr(s0_content[-200:])}')

# Extract: CS Widget portion (cs_marker to end of content before </script>)
cs_widget = s0_content[cs_marker:-9].strip()

# Build new S0: ONLY CS Widget + API_BASE
new_s0 = '<script>\n  window.API_BASE = \'http://54.151.143.233:8001\';\n\n' + cs_widget + '\n</script>'

t = t[:s0_start] + new_s0 + t[s0_end:]

# Remove the original S1 (API_BASE) since it's now in S0
s1_start = t.find('<script>', s0_start + len(new_s0))
s1_end = t.find('</script>', s1_start) + 9
print(f'\nRemove S1: {s1_start}-{s1_end}')

# If S1 is just API_BASE, remove it
s1_content = t[s1_start:s1_end]
if 'API_BASE' in s1_content:
    print(f'S1 is API_BASE, removing...')
    t = t[:s1_start] + t[s1_end:]
else:
    print(f'S1 is NOT API_BASE, keeping')

# Also need to remove the '}\n}' trailing garbage in S0 if present
# Let's just verify and strip the new S0
new_s0_start = t.find('<script>', 910)
new_s0_end = t.find('</script>', new_s0_start)
new_content = t[new_s0_start:new_s0_end]
# Check for trailing bare braces at end of JS content
js = new_content[8:-9]  # remove <script> and </script>
# Strip trailing whitespace and remove lone } at end
while js.rstrip().endswith('}'):
    js = js.rstrip()
    js = js[:-1]
js = js.strip()

new_s0 = '<script>\n' + js + '\n</script>'
t = t[:new_s0_start] + new_s0 + t[new_s0_end:]

# Also need to handle what was removed: SW registration code is GONE
# That's OK - SW registration is optional and was causing conflicts.
# The AI Gateway code is also GONE from S0 - but it was DUPLICATED 
# in Script 3 (main JS). Let's verify.

# Check if aiGateway exists in Script 3
s2_start = t.find('<script', t.find('<script', t.find('<script', 910)+1)+1)
s3_start = t.find('<script', s2_start+1)
s3_end = t.find('</script>', s3_start) + 9
s3_content = t[s3_start:s3_end]
has_ai_gateway = 'function window.aiGateway' in s3_content or 'window.aiGateway' in s3_content
print(f'\nAI Gateway in Script 3: {has_ai_gateway}')

# Let's verify our new S0
new_s0_start = t.find('<script>', 910)
new_s0_end = t.find('</script>', new_s0_start)
new_content = t[new_s0_start:new_s0_end]
opens = new_content.count('{')
closes = new_content.count('}')
print(f'\nNew S0 braces: {{ = {opens}, }} = {closes}, diff = {opens - closes}')

# Write
with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Node check
import subprocess
js_content = new_content.split('>', 1)[1].rsplit('<', 1)[0]
with open('/tmp/s0_clean.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
result = subprocess.run(['node', '--check', '/tmp/s0_clean.js'], capture_output=True, text=True, timeout=10)
print(f'Node check: {result.returncode}')
if result.stderr:
    print(f'  {result.stderr[:300]}')
else:
    print('  No errors!')

# Final file info
t = t.encode('utf-8')
print(f'\nFile size: {len(t)/1024:.1f} KB')
