# -*- coding: utf-8 -*-
import os

filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

cn_arb = '跨交易所聚合引擎'.encode('utf-8')
cn_arb_sub = '实时监控加密货币交易所价差'.encode('utf-8')
cn_arb_gbk = '跨交易所聚合引擎'.encode('gbk')

checks = [
    ('导航 QuantTalk', b'data-i18n="nav_square">QuantTalk'),
    ('导航 跨交易所聚合引擎', b'data-i18n="nav_arbitrage">' + cn_arb),
    ('arb 页面 div', b'id="page-arbitrage"'),
    ('zh i18n nav_arbitrage', b"nav_arbitrage:'" + cn_arb + b"'"),
    ('en i18n nav_arbitrage', b"nav_arbitrage:'Cross-Exchange Arbitrage'"),
    ('GBK 中文定义存在', cn_arb_gbk),
    ('arb_online i18n', b"arb_online:'Online'"),
    ('zh arb_subtitle', b"arb_subtitle:'" + cn_arb_sub),
    ('New badge 存在', b'class="badge"'),
    ('arb refresh button', b'onclick="refreshArbitrageStatus'),
    ('arb exec button', b'onclick="executeArbitrage'),
    ('showPage 通用路由', b'document.getElementById(\'page-\'+name)'),
]

print('=== 最终验证 ===')
all_ok = True
for name, target in checks:
    cnt = raw.count(target)
    found = cnt > 0
    if not found:
        all_ok = False
    icon = 'OK' if found else 'XX'
    print(f'  [{icon}] {name}: {cnt}')

print()
if all_ok:
    print('全部通过！')
else:
    print('有问题需要修复')

fsize = os.path.getsize(filepath)
print(f'文件大小: {fsize/1024:.1f} KB')
