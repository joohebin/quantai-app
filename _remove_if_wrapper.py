# -*- coding: utf-8 -*-
"""Simple fix: remove the if block wrapping from Script 0.
CS Widget was accidentally put inside if('serviceWorker'...) { }.
Remove the if block wrapper, keep SW registration as a standalone check.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find key points  
s0_open = t.find('<script>', 910)
s0_close = t.find('</script>', s0_open)

content = t[s0_open:s0_close]
print(f'Script 0: {len(content)} chars')
print(f'First 350 chars:')
print(content[:350])
print(f'\nLast 200 chars:')
print(content[-200:])

# The structure is:
# <script>
#   // SW comment
#   if(condition){
#     window.addEventListener('load', ()=>{ SW register... });
#   }
#   // dev if...
#   if(localhost){
#     SW unregister + cache clear
#   
# // ===== CS Widget =====
# ... all CS code (WORLD's content, unintentionally inside outer if block)
# window.addEventListener('load', ...)
# 
# 
#  }      <- closes inner if block
#   }     <- closes outer if block
# </script>

# Looking at the content - there are TWO if blocks inside script 0
# The first if is SW registration
# The second if is dev SW unregister

# Both are closed BEFORE CS Widget starts, with their own braces
# Then CS Widget content is outside any block...
# But the trailing }} suggests there's an outer if block wrapping CS Widget

# Actually looking at the trailing chars: 
#  }     <- closes the load listener callback
#   }    <- closes the conditional if
# This matches: if(cond){ load listener }

# BUT the CS Widget content is AFTER the inner if('localhost')'s opening {
# and the closing } of that if is at the end
# So there's an accidental wrapper

# SIMPLEST FIX: 
# 1. Find the outer if('serviceWorker'){ and remove the { and its matching }
# 2. Find the second if(localhost){ and remove the { and its matching }
# 3. Keep all content

# Actually the simplest: Replace the whole script 0 content
# Build it properly

# Find the start of CS Widget content within the script
cs_start = content.find('// ===== CS Widget')
print(f'\nCS Widget at offset: {cs_start}')

# Content before CS Widget is the SW registration code
sw_part = content[8:cs_start].strip()  # 8 = len('<script>')
# After CS Widget is everything else until </script>
cs_part = content[cs_start:-9].strip()  # -9 = len('</script>')

print(f'SW part ({len(sw_part)} chars):')
print(sw_part[:200])
print('...')
print(sw_part[-100:])
print(f'\nCS part ({len(cs_part)} chars)')
print(cs_part[-200:])

# Rebuild: keep SW part (but clean up the if blocks), then CS part
# SW part has extra closing braces at the end from if blocks
# We need to remove the if {} wrapping

# Remove the outer if block:
# Replace: "if('serviceWorker' in navigator && ...){\n    window.addEventListener..." 
# With: "window.addEventListener..."
import re

# Remove first if block wrapper
sw_clean = re.sub(
    r"if\('serviceWorker' in navigator.*?\{\s*\n",
    "",
    sw_part,
    count=1
)
print(f'\nAfter removing first if: {repr(sw_clean[:100])}')

# The inner if block's "}" that closed the first if is still there
# Let me just show what we have
# The pattern should be:
# if('serviceWorker' ...){
#   window.addEventListener('load', ()=>{...});
# }
# if(localhost){
#   SW unregister
#   cache clear
# 
# The extra "}" at end of sw_part closes the if(localhost)

# Also remove the second if wrapper
sw_clean = re.sub(
    r"if\(location\.hostname === 'localhost'.*?\{\s*\n",
    "",
    sw_clean,
    count=1
)
print(f'After removing second if: {repr(sw_clean[:150])}')

# Also remove trailing "\n  " (indentation from if block)
sw_clean = sw_clean.rstrip()
# Remove trailing single } that closed blocks
lines = sw_clean.split('\n')
# Find and remove lines that are just whitespace + single }
lines = [l for l in lines if l.strip() != '}']
# Also remove lines that are just whitespace
lines = [l for l in lines if l.strip() != '']

sw_clean = '\n'.join(lines)
print(f'SW clean ({len(sw_clean)} chars):')
print(sw_clean)

# CS part is fine - just strip trailing whitespace and clean up
cs_clean = cs_part.strip()
# Remove the trailing }} at the very end if they exist
cs_clean = cs_clean.rstrip('}').strip()

new_s0 = '<script>\n' + sw_clean + '\n\n' + cs_clean + '\n</script>'
t = t[:s0_open] + new_s0 + t[s0_close:]

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')

# Count braces
opens = text.count('{')
closes = text.count('}')
print(f'\n=== Final ===')
print(f'File: {len(data)/1024:.1f} KB')
print(f'Braces: {{ = {opens}, }} = {closes}, diff = {opens-closes}')

# Check csGreet is not inside any block
s0_new_start = text.find('<script>', 910)
s0_new_end = text.find('</script>', s0_new_start)
s0_new = text[s0_new_start:s0_new_end]
print(f'csGreet in script 0: {"function csGreet" in s0_new}')

# Check the first 500 chars of script 0
print(f'\nNew script 0 start:')
print(s0_new[:400])
