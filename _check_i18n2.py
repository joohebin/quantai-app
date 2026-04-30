# -*- coding: utf-8 -*-
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

target = b'nav_arbitrage'
idx = raw.find(target, 250000)
if idx >= 0:
    chunk = raw[idx:idx+200]
    decoded = chunk.decode('utf-8', errors='replace')
    print(f'At {idx}: {decoded[:150]}')
    
    # Check if 跨交易所聚合引擎 proper UTF-8
    zh_needle = '跨交易所聚合引擎'.encode('utf-8')
    if zh_needle in chunk:
        print('\nContains correct 跨交易所聚合引擎 UTF-8: YES')
    else:
        print('\nContains correct UTF-8: NO')
        # Show actual bytes after nav_arbitrage:'
        after = chunk[chunk.find(b"'")+1:]
        print(f'Raw after quote: {after[:30]}')
