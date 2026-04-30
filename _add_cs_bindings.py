# -*- coding: utf-8 -*-
"""
Fix: Server CS Widget has 2 extra } at end (brace mismatch).
Solution: Strip them during deployment or add a compatibility fix.
But easier: just hardcode window.cxGreet = function()... etc at file end.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find the end of file area after all scripts
# Find last </script>
last_script_close = t.rfind('</script>') + 9
print(f'Last script closes at: {last_script_close}')

# Find near end of file
end = len(t)
tail = t[last_script_close:]
print(f'Tail after last script ({len(tail)} chars):')
# Show last 200 chars
print(repr(tail[-200:]))

# The issue is likely in script 4 being merged - let me check the CS Widget portion
# Actually, the simpler fix: add window.fn = fn bindings at the very end of the file
binding_code = '''
<script>
// Ensure CS functions are globally accessible
window.csGreet = typeof csGreet !== 'undefined' ? csGreet : function(){};
window.csAddMsg = typeof csAddMsg !== 'undefined' ? csAddMsg : function(){};
window.csFormatText = typeof csFormatText !== 'undefined' ? csFormatText : function(){};
window.csShowTyping = typeof csShowTyping !== 'undefined' ? csShowTyping : function(){};
window.csHideTyping = typeof csHideTyping !== 'undefined' ? csHideTyping : function(){};
window.csSendQuick = typeof csSendQuick !== 'undefined' ? csSendQuick : function(){};
window.csGoHuman = typeof csGoHuman !== 'undefined' ? csGoHuman : function(){};
window.csShowHandoff = typeof csShowHandoff !== 'undefined' ? csShowHandoff : function(){};
</script>
'''

# Insert at end of body (before </html>)
html_close = t.rfind('</html>')
t = t[:html_close] + binding_code + '\n' + t[html_close:]
print(f'Added CS function bindings before </html>')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

print(f'File: {len(t)/1024:.1f} KB')
