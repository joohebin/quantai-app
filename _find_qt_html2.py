import sys
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Find the QuantTalk HTML by looking at what's around sq-msgs id
idx = t.find('id="sq-msgs"')
if idx < 0:
    idx = t.find("id='sq-msgs'")
if idx > 0:
    print(f'sq-msgs html at: {idx}')
    print(t[max(0,idx-500):idx+100])
else:
    print('sq-msgs id not found in HTML')

# Search for channel-list id
idx = t.find('id="channel-list"')
if idx > 0:
    print(f'\n\nchannel-list id at: {idx}')
    print(t[max(0,idx-800):idx+50])
else:
    print('\nchannel-list id not found in HTML')
