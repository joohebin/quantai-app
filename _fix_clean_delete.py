"""Clean approach: remove the broken ternary and use pure JS instead"""
import subprocess

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

# The problem area: innerHTML string with conditional delete button
# Find the ternary with !defaultIds
idx = r.find(b"!defaultIds||defaultIds.indexOf(ch.id)<0?'<button onclick=")
print(f'Found conditional delete binary at: {idx}')

if idx < 0:
    # Try without binary search
    # The HTML file might have different encoding
    idx2 = r.find(b'!defaultIds')
    print(f'!defaultIds at: {idx2}')
    idx = idx2

if idx > 0:
    # Find start: we need to find the preceding '+'
    # Scan backwards from idx to find the pattern
    pos = idx - 5
    while pos > 0:
        if r[pos:pos+3] == b"'+!":
            break
        pos -= 1
    
    # Find end: find the closing ")+'"
    end_pos = r.find(b")+'", idx)
    if end_pos < 0:
        # Try other patterns
        end_pos = r.find(b")+'", pos + 100)
    
    if end_pos < 0:
        # Manual scan forward
        end_pos = pos + 10
        depth = 0
        in_ternary = False
        while end_pos < len(r):
            if r[end_pos:end_pos+1] == b'(':
                depth += 1
            elif r[end_pos:end_pos+1] == b')':
                depth -= 1
                if depth < 0:
                    break
            end_pos += 1
    
    full_block = r[pos:min(end_pos+4, idx+500)]
    print(f'Full block ({len(full_block)} bytes) starts at {pos}')
    
    # Replace with empty string
    r = r[:pos] + r[pos+len(full_block):]
    print(f'Removed conditional delete block, new size: {len(r)}')
    
    # Now we need to add the delete button via JS in showChannelSettings
    # Find the after-appending location
    # Search for 'document.body.appendChild(m);' in the settings function
    # Actually let's find showChannelSettings function
    fn_start = r.find(b'function showChannelSettings')
    fn_end = r.find(b'function previewSetAvatar', fn_start)
    settings_js = r[fn_start:fn_end].decode('utf-8', errors='replace')
    
    # Find where appendChild happens and add our logic
    # Look for the last appendChild before the function ends
    last_append = settings_js.rfind('document.body.appendChild(m);')
    print(f'Last appendChild at offset {last_append} in settings')
    
    # Actually, let's append to the settings HTML string near where save + delete buttons are
    # Find the save button HTML
    save_btn_pos = settings_js.find('保存设置')
    if save_btn_pos > 0:
        # After the save button HTML, add a div with ID for delete area
        # The current HTML has the save button + delete button
        # Let's add a data-delete-area div after the save button
        insert_pos = settings_js.find('margin-bottom:8px\">保存设置</button>+', save_btn_pos)
        if insert_pos > 0:
            # After save button, add delete area wrapper
            print(f'Save button end at offset {insert_pos}')
            print(f'After save btn: {settings_js[insert_pos:insert_pos+120]}')

with open(filepath, 'wb') as f:
    f.write(r)

# Check syntax
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c)
res = subprocess.run(['node','--check','/tmp/sc.js'], capture_output=True, timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    err_data = res.stderr[:300]
    print(f'Error: {err_data}')
else:
    print('Syntax OK!')
