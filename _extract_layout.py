import sys
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Extract the full QuantTalk/chat HTML layout
idx = t.find('chat-layout')
print(f'chat-layout at {idx}')
print('---')
print(t[idx:idx+5000])
