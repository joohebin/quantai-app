# -*- coding: utf-8 -*-
"""
Root cause: Script 5 (CS Widget) is NEVER executed by the browser.
All CS functions (csGreet, csAddMsg, csSendQuick, csFormatText etc.) are undefined.
Solution: Move ALL CS functions from Script 5 into Script 4 (diagnostic script that IS executed).
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Script 5 content
s5_marker = '// ===== 客服 Widget 逻辑 ====='
s5_start = t.find(s5_marker)
if s5_start < 0:
    s5_start = t.find('客服 Widget 逻辑')
    if s5_start > 0:
        s5_start = t.rfind('<script', s5_start-200, s5_start)
        if s5_start < 0: s5_start = t.find('<script>', s5_start-50)

print(f'S5 marker first char: {repr(t[s5_start:s5_start+30])}')

# Find the full script tag containing CS Widget
script_start = t.rfind('<script', s5_start-200, s5_start)
if script_start < 0:
    script_start = s5_start
script_close = t.find('</script>', s5_start) + 9

print(f'Script 5: {script_start} to {script_close} ({script_close-script_start} chars)')

# Extract the JS content (without <script> tags)
js_content = t[script_start:script_close]
js_clean = js_content.replace('<script>', '').replace('</script>', '').strip()

print(f'JS content: {len(js_clean)} chars')

# Find script 4 (diagnostic)
s4_marker = '// 快速诊断：检查函数可用性'
s4_start = t.find(s4_marker)
s4_close = t.find('</script>', s4_start) + 9

print(f'Script 4: {s4_start} to {s4_close} ({s4_close-s4_start} chars)')

# Insert ALL CS Widget JS into script 4, right before closing </script>
# Remove the wrapper from script 5 content
insert_point = s4_close - 9  # before </script>
indent = '  '

# Also remove the toggleCS stub we already added (since the full version is in script 5)
existing_stub = t.find("// ---- 客服按钮逻辑（必放在此script以确保可用） ----", s4_start)
if existing_stub > 0:
    # Find the end of this stub
    stub_end = t.find('};', existing_stub) + 2
    stub_end_line = t.find('\n', stub_end)
    t = t[:existing_stub] + t[stub_end_line:]
    print(f'Removed existing toggleCS stub from script 4 ({stub_end_line - existing_stub} chars)')
    # Recalculate positions
    s4_start = t.find(s4_marker)
    s4_close = t.find('</script>', s4_start) + 9

# Now add all CS JS from script 5 into script 4
# But we need to handle the differences:
# Script 5 has const CS_CONFIG = ... etc which define the CS behavior
# The toggleCS in script 5 also references _csOpen which is defined there

# Simplify: just copy the entire content of script 5 into script 4
# But dedupe function definitions that already exist in script 4
insert_point = s4_close - 9
t = t[:insert_point] + '\n' + js_clean + '\n' + t[insert_point:]
print(f'Added CS Widget JS ({len(js_clean)} chars) to script 4')

# Now remove script 5 entirely (the original)
# First find the script tag boundaries again (they shifted)
new_s5_start = t.find('// ===== 客服 Widget 逻辑 =====')
new_script_start = t.rfind('<script', new_s5_start-200, new_s5_start)
new_script_close = t.find('</script>', new_s5_start) + 9
print(f'Old script 5 (to remove): {new_script_start} to {new_script_close}')

t = t[:new_script_start] + t[new_script_close:]
print(f'Removed original script 5')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')

# Check functions in script 4
s4_start_new = text.find(s4_marker)
s4_end_new = text.find('</script>', s4_start_new)
s4_content = text[s4_start_new:s4_end_new]

print(f'\n=== Verification ===')
print(f'File: {len(data)/1024:.1f} KB')
funcs = ['toggleCS', 'csGreet', 'csAddMsg', 'csSendQuick', 'csFormatText', 'csShowTyping', 'csGoHuman']
for fn in funcs:
    in_s4 = fn in s4_content
    print(f'  {fn}: in script 4 = {in_s4}')

# Check no more script with toggleCS outside script 4
script_bodies = []
i = 0
while True:
    s_tag = text.find('<script>', i)
    if s_tag < 0: break
    e_tag = text.find('</script>', s_tag) + 9
    script_bodies.append(text[s_tag:e_tag])
    i = e_tag

print(f'\nTotal scripts: {len(script_bodies)}')
for idx, body in enumerate(script_bodies):
    has_cs = 'toggleCS' in body
    size = len(body)
    print(f'  Script {idx}: {size} chars, has toggleCS: {has_cs}')
