import sys
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# sq-msgs at 104174
idx = 104174
# Print in ASCII-safe context
start = max(0, idx - 500)
end = min(len(t), idx + 100)
safe = t[start:end].encode('ascii', errors='replace').decode('ascii')
print(safe)

# Also find channel-list in html
idx2 = t.find('<div id="channel-list"')
if idx2 > 0:
    print(f'\n\nchannel-list html at {idx2}')
    safe2 = t[max(0,idx2-800):idx2+50].encode('ascii', errors='replace').decode('ascii')
    print(safe2)
else:
    print('\nchannel-list div not found')
