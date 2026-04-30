import sys
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# search for QuantTalk channel list HTML
for key in ['channel-list', 'ch-sidebar', 'ch-item', 'sq-msgs', 'widget-tv', 'yt-widget']:
    idx = t.find(key)
    if idx > 0:
        sys.stdout.flush()
        if key == 'channel-list':
            start = max(0, idx - 500)
            end = min(len(t), idx + 100)
            print(f'=== {key} context ({start}-{end}) ===')
            print(t[start:end])
            print('---END---\n')
        else:
            print(f'{key} at {idx}: {t[max(0,idx-30):idx+60]}')
