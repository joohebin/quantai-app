# -*- coding: utf-8 -*-
"""Add channel settings modal + channel header settings button"""
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# 1. Add channel settings button + modal handler functions
# Insert after createChannelSubmit function
ch_submit_end = t.find('function createChannelSubmit')
ch_submit_body = t.find('}\n//', ch_submit_end)
# Actually find the exact end of createChannelSubmit
# Search for the toast line that ends it
toast_end = t.rfind("toast('✅ #'+name+' 已创建','success');", ch_submit_end, ch_submit_end + 800)
if toast_end > 0:
    fn_end = t.find('}', toast_end) + 1
else:
    # Fallback - find end of createChannelSubmit
    cn = t.find("createChannelSubmit", ch_submit_end + 200)
    if cn > 0:
        fn_end = t.find('}', cn) + 1
    
    # Find the next function after showCreateChannelModal... need the actual close
    # Let me search for the toast line
    fn_end = t.find("toast('✅ #'+name+' 已创建','success');", ch_submit_end)
    if fn_end > 0:
        fn_end = t.find('}', fn_end) + 1
    else:
        fn_end = t.find('function loadTV', ch_submit_end)

toast_end = t.rfind("toast('✅ #'+name+' 已创建','success');", ch_submit_end, ch_submit_end + 1000)
print(f'toast_end at: {toast_end}')
# Find the } that closes this function
bracket_pos = t.find('}', toast_end + 1)
while bracket_pos > 0:
    # Check if this is the last } before next function
    rest = t[bracket_pos+1:bracket_pos+50].strip()
    if rest.startswith('function') or rest.startswith('//'):
        fn_end = bracket_pos + 1
        break
    bracket_pos = t.find('}', bracket_pos + 1)

print(f'fn_end at: {fn_end}')
print(f'Next 100 chars: {t[fn_end:fn_end+100]}')
