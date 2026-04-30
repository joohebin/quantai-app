# -*- coding: utf-8 -*-
"""
Add csSendMessage and keyboard handler to the v2 binder script.
csSendMessage was accidentally deleted during earlier cleanup.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find and extend the v2 binder script
binder_start = t.rfind('// ===== CS Function Global Binder v2')
binder_end = t.find('</script>', binder_start)

# Insert csSendMessage definition and keyboard handler BEFORE the closing
# of the IIFE (inside the IIFE)
inject_code = '''
  // ===== csSendMessage (was deleted in earlier cleanup) =====
  if(typeof window.csSendMessage === 'undefined'){
    window.csSendMessage = function(msg){
      csAddMsg('user', msg);
      csShowTyping();
      csDoSend();
    };
    console.log('[CS Bind] Added csSendMessage');
  }
  
  // ===== Keyboard handler for Enter key =====
  var csInput = document.getElementById('cs-input');
  if(csInput){
    csInput.addEventListener('keydown', function(e){
      if(e.key === 'Enter' && !e.shiftKey){
        e.preventDefault();
        csDoSend();
      }
    });
    console.log('[CS Bind] Added Enter key handler');
  }
  
'''

# Insert before the closing of the IIFE: "})();"
insert_pos = binder_end - 3  # before "</script>"
t = t[:insert_pos] + inject_code + t[insert_pos:]

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

print(f'File: {len(t)/1024:.1f} KB')
print('Added csSendMessage + keyboard handler to v2 binder')
