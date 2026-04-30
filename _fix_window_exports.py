# -*- coding: utf-8 -*-
"""
Fix: all CS functions must be assigned to window (not just declared inside IIFE)
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find the independent CS Widget IIFE
# Replace function declarations with window.X = function
replacements = [
    ('function csGreet(){\n    csAddMsg', '  window.csGreet = function(){\n    csAddMsg'),
    ('function csAddMsg(role, text){\n    var msgs', '  window.csAddMsg = function(role, text){\n    var msgs'),
    ('function csFormatText(t){\n    return t', '  window.csFormatText = function(t){\n    return t'),
    ('function csShowTyping(){\n    var msgs', '  window.csShowTyping = function(){\n    var msgs'),
    ('function csHideTyping(){\n    var el', '  window.csHideTyping = function(){\n    var el'),
    ('function csSendQuick(el){\n    var text', '  window.csSendQuick = function(el){\n    var text'),
    ('function csLocalReply(text){\n    var replies', '  window.csLocalReply = function(text){\n    var replies'),
    ('function csFetchGroq(messages){\n    return new Promise', '  window.csFetchGroq = function(messages){\n    return new Promise'),
    ('function csShowHandoff(){\n    csAddMsg', '  window.csShowHandoff = function(){\n    csAddMsg'),
    ('function csGoHuman(){\n    csShowHandoff', '  window.csGoHuman = function(){\n    csShowHandoff'),
]

for old, new in replacements:
    count = t.count(old)
    if count == 1:
        t = t.replace(old, new)
    elif count > 1:
        # Only replace the one in the independent widget (last one)
        idx = t.rfind(old)
        t = t[:idx] + new + t[idx+len(old):]
    else:
        print(f'WARN: not found: {old[:30]}...')

# Also: csSendMessage needs to be defined
send_msg = ';\n\n  function csSendMessage(msg){\n    csAddMsg('
send_msg_new = ';\n\n  window.csSendMessage = function(msg){\n    csAddMsg('
if send_msg in t:
    t = t.replace(send_msg, send_msg_new)
else:
    # csSendMessage doesn't exist yet, add it
    # It should be called by csSendQuick -> currently csSendQuick calls csDoSend directly
    # Let's check if it's needed
    print('csSendMessage not found in file - adding it')
    insert_marker = ';\n\n  function csGoHuman(){'
    if insert_marker in t:
        idx = t.find(insert_marker)
        t = t[:idx] + ''';

// Send message API for external use
window.csSendMessage = function(msg){
  document.getElementById('cs-input').value = msg;
  var doSend = typeof window.csDoSend === 'function' ? window.csDoSend : null;
  if(doSend) doSend();
}''' + t[idx:]
        print('Added csSendMessage')

# Also add the missing csSendMessage reference in csSendQuick
# csSendQuick should call csSendMessage (not csDoSend directly) for external compatibility
# But since csSendQuick is in the IIFE, it uses the closure's csDoSend which is fine

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Node check
import subprocess
start = t.rfind('// ===== CS Widget')
end = t.find('</script>', start)
js = t[start:end]
with open('/tmp/cs_widget_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
result = subprocess.run(['node', '--check', '/tmp/cs_widget_v2.js'], capture_output=True, text=True, timeout=10)
print(f'Node check: {result.returncode} - {"OK" if result.returncode == 0 else result.stderr[:200]}')

print(f'\nFile: {len(t)/1024:.1f} KB')
