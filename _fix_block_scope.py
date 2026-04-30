# -*- coding: utf-8 -*-
"""
Definitive fix: CS Widget was accidentally injected inside SW if block {}
Move it to BEFORE the SW if block so functions are global.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Locate key positions
s0_open = t.find('<script>', 910)
s0_close = t.find('</script>', s0_open)

# Find SW if block
sw_if = t.find("if('serviceWorker' in navigator", s0_open)
sw_open_brace = t.find('{', sw_if)
sw_close_brace = s0_close - 9  # before </script>

# Find CS Widget marker
cs_marker = t.find('// ===== CS Widget', s0_open)

print(f'SW if: {sw_if}')
print(f'SW open brace: {sw_open_brace}')
print(f'CS Widget: {cs_marker}')
print(f'Inside if block: {cs_marker > sw_open_brace}')

# The content BEFORE CS Widget (inside if) is SW registration code
sw_content = t[sw_open_brace+1:cs_marker]
print(f'\nSW if content ({len(sw_content)} chars):')
print(sw_content[:100])

# The CS Widget content starts at cs_marker
# and the remaining if block closing braces are at the end

# Strategy:
# 1. Move CS Widget content to BEFORE the SW if
# 2. Keep SW registration code properly scoped inside if

# Build new script 0:
# <script>
# // CS Widget code (global scope) 
# if('serviceWorker'...) { SW_registration code }
# </script>

cs_widget_end_line = t.find("window.addEventListener('load'", cs_marker)
# Actually find where the LAST CS-related code ends
# The last meaningful line is: window.addEventListener('load', ()=>{ setTimeout(renderAIConfigCard, 500); });
# After that is just closing braces for the if block

# Find the SW if closing braces
# There's: \n\n\n }\n  }\n</script>
# These close: the addEventListener callback }, the if block }, and the if's {

# Let me identify the exact boundary
# Search for the pattern: 3 newlines then }
after_cs = t.find('\n\n\n }', cs_marker+500)
print(f'\nAfter CS Widget (end): {after_cs}')
print(f'Content: {repr(t[after_cs:after_cs+20])}')

# cs_marker to after_cs is the CS Widget code + AI Gateway code
# after_cs+4 to s0_close-9 is the SW if block's remaining closing braces

cs_code = t[cs_marker:after_cs]
sw_if_closing = t[after_cs:s0_close-9]

print(f'\nCS code length: {len(cs_code)}')
print(f'SW closing ({len(sw_if_closing)} chars): {repr(sw_if_closing[:20])}')

# Also need the SW content from within the if block
sw_inner = t[sw_open_brace+1:cs_marker].rstrip()

# Rebuild
new_s0 = (
    '<script>\n'
    '#x#x# CS Widget (must be global scope) #x#x#\n'
    + cs_code.strip() + '\n\n'
    '#x#x# SW Registration (block scoped) #x#x#\n'
    "if('serviceWorker' in navigator && location.hostname !== 'localhost' && location.hostname !== '127.0.0.1'){\n"
    + sw_inner + '\n'
    + sw_if_closing.strip() + '\n'
    + '}\n'
    + '</script>'
)

t = t[:s0_open] + new_s0 + t[s0_close:]
print(f'\nFile updated: {len(t)/1024:.1f} KB')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Quick verify: check CS functions are global
s0_new_open = t.find('<script>', 910)
s0_new_close = t.find('</script>', s0_new_open)
content = t[s0_new_open:s0_new_close]
print(f'csGreet global: {"function csGreet" in content}')
print(f'toggleCS global: {"function toggleCS" in content}')
print(f'No if-block wrapping: {not ("// ==== CS Widget" in content and content.find("// ==== CS Widget") > content.find("if("))}')
