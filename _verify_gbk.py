# -*- coding: utf-8 -*-
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# Search in GBK bytes
g_arb = '跨交易所聚合引擎'.encode('gbk')
g_sub = '实时监控加密货币交易所价差'.encode('gbk')

cn_nav = b"nav_arbitrage:'" + g_arb + b"'"
cn_sub = b"arb_subtitle:'" + g_sub
cn_arb = b"arb_title:'" + g_arb + b"'"

print('=== GBK i18n 验证 ===')
print(f'zh nav_arbitrage: {raw.count(cn_nav)}')
print(f'zh arb_subtitle:  {raw.count(cn_sub)}')
print(f'zh arb_title:     {raw.count(cn_arb)}')
print(f'zh gbk total:     {raw.count(g_arb)}')

# Check arb_online etc
print()
print('=== 英文 i18n 验证 ===')
for t, n in [(b"nav_arbitrage:'Cross-Exchange Arbitrage'", 'nav_arbitrage'),
             (b"arb_title:'Cross-Exchange Arbitrage'", 'arb_title'),
             (b"arb_subtitle:'Real-time", 'arb_subtitle'),
             (b"arb_online:'Online'", 'arb_online')]:
    print(f'en {n}: {raw.count(t)}')

# Page content
print()
print('=== 页面内容 ===')
for t, n in [(b'id="page-arbitrage"', 'page-arbitrage'),
             (b"data-i18n=\"arb_title\"", 'arb_title in HTML'),
             (b"data-i18n=\"arb_subtitle\"", 'arb_subtitle in HTML'),
             (b'class="exchange-item', 'exchange-status section'),
             (b'onclick="executeArbitrage', 'executeArbitrage btn')]:
    print(f'{n}: {raw.count(t)}')
