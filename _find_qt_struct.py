import sys
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Find the quanttalk page HTML - look for the channel-list div and go backwards
idx = t.find('channel-list')
# Look for the containing page structure
for key in ['page-quant', 'page-chat', 'page-square', 'quantalk-container', 'chat-layout', 'chat-sidebar', 'ch-sidebar']:
    idx2 = t.find(key)
    if idx2 > 0:
        print(f'{key} at {idx2}')

# Find which page has the channel-list content
# Look for the closest div with an id containing "square" or "chat" or "quant"
idx = t.find('channel-list-area')
if idx < 0:
    # Try looking for the HTML structure directly
    idx = t.find('channel-list')
    sys.stdout.flush()
    # Go backwards to find the wrapping container
    # Search for '<div' or '<div '
    search_start = max(0, idx - 3000)
    block = t[search_start:idx+100]
    # Find the last <div with id= before this
    div_start = block.rfind('<div')
    if div_start > 0:
        actual_start = search_start + div_start
        print(f'\n--- Structure before channel-list ---')
        print(t[actual_start:idx+100])
