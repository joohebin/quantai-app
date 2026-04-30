import re
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# The right panel div is right after the Middle: Chat Area
idx = t.find('<!-- Right: Post Feed -->')
print(f'Comment at: {idx}')
# Show the 500 chars before
before = t[max(0, idx-500):idx]
print('Before:', before.encode('ascii', errors='replace').decode('ascii'))

# Find the opening <div> of the right panel by looking at the HTML structure
# The page-square is a flex row with 3 children: left | middle | right
# The right div should be right before the comment
prev_div_close = t.rfind('</div>', max(0, idx-500), idx)
print(f'Prev close: {prev_div_close}')
# The right opening div is after this
open_div = t.find('<div ', prev_div_close)
print(f'Open div after prev close: {open_div}')
if open_div == idx:  # wrong
    # Try again
    pass
