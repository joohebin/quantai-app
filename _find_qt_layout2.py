import sys
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

for key in ['ch-header', 'widget-tv', 'sq-posts', 'viewpoint', 'ch-settings']:
    idx = t.find(key)
    if idx > 0:
        excerpt = t[max(0,idx-80):idx+120]
        print(f'{key} at {idx}')
        sys.stdout.flush()
    else:
        print(f'{key}: NOT FOUND')

# Also look for the actual QuantTalk page structure
# Check what's around the channel-list CSS
idx = t.find('channel-list')
if idx > 0:
    # Go backwards to find the page container
    start = max(0, idx - 2000)
    print(f'\n--- Channel list area (2000 bytes before) ---')
    print(t[start:idx+200])
