import os
filepath = 'index.html'
with open(filepath, 'rb') as f:
    raw = f.read()
print(f'Size: {len(raw)} bytes')
checks = [
    (b"wallet', this)", 'wallet btn'),
    (b'acc-tab-wallet', 'wallet tab'),
    (b'wallet-select', 'wallet select'),
    (b'channel-list', 'channel list'),
    (b'widget-tv', 'TV widget'),
    (b'widget-yt', 'YT widget'),
    (b'initQuantTalk', 'init fn'),
    (b'connectWallet', 'connectWallet fn'),
    (b'createChannel', 'createChannel fn'),
    (b's3.tradingview.com', 'TV script'),
    (b'youtube.com/embed', 'YT embed'),
]
for p, n in checks:
    if p in raw: print(f'  OK: {n}')
    else: print(f'  MISSING: {n}')
print(f'Script tags: {raw.count(b"<script>")}')
print(f'Valid encoding: {len(raw) == len(raw.decode("utf-8",errors="replace").encode("utf-8",errors="replace"))}')
