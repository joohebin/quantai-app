# -*- coding: utf-8 -*-
"""
ROOT CAUSE: CS Widget was injected INSIDE the SW registration if block!
All function declarations inside a block ({ }) are block-scoped in strict mode,
so toggleCS, csGreet etc never became global.

Fix: Inject CS Widget BEFORE the SW if block, at the top of Script 0.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find Script 0 boundaries
s0_script_open = t.find('<script>', 910)
s0_script_close = t.find('</script>', s0_script_open)
print(f'Script 0: {s0_script_open} to {s0_script_close} ({s0_script_close-s0_script_open} chars)')

# Find the CS Widget marker (currently inside the if block)
cs_marker = t.find('// ===== CS Widget')
print(f'CS Widget marker at: {cs_marker}')

# Show what's before it
before_cs = t[cs_marker-200:cs_marker]
print(f'Before CS Widget:')
# Check indent level
lines = before_cs.split('\n')
last_lines = lines[-3:]
for l in last_lines:
    print(f'  {repr(l)}')

# Find where the SW if block opens
sw_if = t.find("if('serviceWorker' in navigator", s0_script_open)
sw_if_open_brace = t.find('{', sw_if)
print(f'\nSW if at: {sw_if}, brace at: {sw_if_open_brace}')

# CS Widget is currently AFTER the if brace - needs to be moved BEFORE it
# OR: put CS Widget at the very beginning of Script 0, before SW if

# Extract CS Widget content
cs_content = t[cs_marker:]
# Find where CS Widget ends (trailing braces)
# The trailing "}" characters after CS Widget belong to the SW if block
# We need to find where CS Widget actually ends

# The CS Widget ends at the last `renderAIConfigCard` call
# After that, the remaining `}\n  }` is the if block closure
cs_end_sentinel = t.find("window.addEventListener('load'", cs_marker)
cs_line_end = t.find('\n', cs_end_sentinel)
# The CS Widget wants to add its own load listener - keep it
# But strip the trailing })

# Actually, let me just remove the CS from its current position and 
# insert it at the START of the script, before the SW stuff

# Remove CS Widget from current position (including its load listener)
# Find the actual end: after the `renderAIConfigCard` call, before the garbage braces
cs_payload_end = t.find('// 初始化时渲染一次', cs_marker)
if cs_payload_end < 0:
    cs_payload_end = cs_end_sentinel
# Find the next newline after the load listener
load_listener_end = t.find('\n', t.find('});', cs_marker, cs_marker+3000))
load_listener_end = t.find('});', cs_marker)
load_listener_end = t.find('});', load_listener_end+3)  # second }); for nested
print(f'\nCS payload: {cs_marker} to {load_listener_end+5}')

# Also need to get the complete CS content
# The CS content starts at cs_marker and includes the AI Gateway code
# Let's find where the SW code resumes after CS
# Look for the trailing code after CS
after_cs = t[load_listener_end+5:load_listener_end+100]
print(f'After CS: {repr(after_cs[:60])}')

# The rest of SW if block (just closing braces) - let's keep it clean
# Cut CS Widget from current position
t = t[:cs_marker-1] + t[load_listener_end+5:]  # -1 for blank line
print(f'After cut: {len(t)} chars')

# Now prepend CS Widget at the start of Script 0 (before SW if)
# Find new positions
s0_start_new = t.find('<script>', 910)
sw_if_new = t.find("if('serviceWorker'", s0_start_new)
print(f'New s0 start: {s0_start_new}, SW if: {sw_if_new}')

# CS content should go right after <script> but before SW if
cs_content = t[s0_start_new+8:sw_if_new-1]  # grab the content that was removed

# Actually wait - I cut the wrong content. The cut removed from CS marker to after load.
# But there's also the AI Gateway code that was part of CS Widget.
# Let me reconsider...

# The simplest correct fix: 
# 1. Find the CS Widget start
# 2. Move everything from there to 'load listener' to before the SW if
# 3. Keep only the SW if's closing braces where CS was

# Reset
