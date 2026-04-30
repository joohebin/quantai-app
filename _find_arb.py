# -*- coding: utf-8 -*-
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# Find ALL occurrences of nav_arbitrage
pos = 0
count = 0
while True:
    idx = raw.find(b'nav_arbitrage', pos)
    if idx < 0:
        break
    count += 1
    chunk = raw[max(0,idx-10):idx+80]
    try:
        decoded = chunk.decode('utf-8', errors='replace')
        print(f'#{count} at {idx}: {decoded}')
    except:
        print(f'#{count} at {idx}: [binary: {chunk[:15]}]')
    pos = idx + 1

if count == 0:
    print("nav_arbitrage not found in file!")
    # Search for the bytes we inserted
    zh = '跨交易所聚合引擎'.encode('utf-8')
    idx2 = raw.find(zh)
    print(f'跨交易所聚合引擎 UTF-8 found: {idx2 >= 0} at {idx2 if idx2 >= 0 else -1}')
