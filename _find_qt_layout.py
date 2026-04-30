import sys
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Find the QuantTalk-related HTML structure
# Look for channel-list, ch-header etc.
for key in ['channel-list', 'ch-header', 'widget-tv', 'sq-posts', 'viewpoint']:
    idx = t.find(key)
    if idx > 0:
        print(f'{key} at {idx}: {t[max(0,idx-80):idx+120]}')
        print('---')
    else:
        print(f'{key}: NOT FOUND')

# Find the QuantTalk main HTML container
for key in ['页面不存在', 'page-square', 'QuantTalk']:
    idx = t.find(key)
    if idx > 0:
        print(f'\n{key} at {idx}:')
        print(t[max(0,idx-100):idx+200])
