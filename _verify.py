import os
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
print('Size:', len(r))
print('wallet btn:', b"wallet',this)" in r)
print('wallet tab:', b'acc-tab-wallet' in r)
print('channel list:', b'channel-list' in r)
print('initQuantTalk:', b'initQuantTalk' in r)
print('connectWallet:', b'connectWallet' in r)
print('createChannel:', b'createChannel' in r)
print('wallet in tabIds:', b"'wallet'" in r)
