# -*- coding: utf-8 -*-
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

idx = raw.find(b'nav_arbitrage', 200000)
chunk = raw[idx:idx+200]
zh_needle = '跨交易所聚合引擎'.encode('utf-8')
print(f'Contains 跨交易所聚合引擎: {zh_needle in chunk}')
print(f'Cross-Exchange Arbitrage: {b"Cross-Exchange Arbitrage" in raw}')
print(f'arb_online: {b"arb_online" in raw}')
print(f'arb_online Online: {b"arb_online:\'Online\'" in raw}')
