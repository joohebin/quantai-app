"""Find and replace the exact right panel HTML block"""
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

idx = t.find('<!-- Right: Post Feed -->')
print(f'Comment at: {idx}')

# Find the opening div: <div style="width:280px... before the comment
open_pos = t.rfind('<div ', 0, idx)
# Find the nearest style=\"width:280px
style_pos = t.find('width:280px', open_pos, idx)
if style_pos > 0:
    # Go back from style_pos to find the <div
    div_pos = t.rfind('<div', style_pos - 50, style_pos)
    print(f'Opening div at: {div_pos}')
    
    # Find 3 closing divs (title, sq-posts, outer)
    close1 = t.find('</div>', idx)
    close2 = t.find('</div>', close1 + 6)
    close3 = t.find('</div>', close2 + 6)
    print(f'Closes at: {close1}, {close2}, {close3}')
    
    old = t[div_pos:close3+6]
    print(f'Old block: {len(old)} chars')
    print(old[:200].encode('ascii', errors='replace').decode('ascii'))
    print('...')
    print(old[-200:].encode('ascii', errors='replace').decode('ascii'))
else:
    print('width:280px style not found')
