# -*- coding: utf-8 -*-
import re
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8')

print('=== 全面验证 ===')
checks = [
    ('导航 QuantTalk', 'QuantTalk' in text[text.find('<nav>'):text.find('</nav>')]),
    ('导航 跨交易所聚合引擎', '跨交易所聚合引擎' in text[text.find('<nav>'):text.find('</nav>')]),
    ('nav_arbitrage menu', 'data-i18n="nav_arbitrage"' in text),
    ('page-arbitrage div', 'id="page-arbitrage"' in text),
    ('New badge in nav', 'badge' in text[text.find('<nav>'):text.find('</nav>')]),
    ('showPage arbitrage', "showPage('arbitrage'" in text),
    ('Chinese i18n', "nav_arbitrage:'跨交易所聚合引擎'" in text),
    ('English i18n', "nav_arbitrage:'Cross-Exchange Arbitrage'" in text),
    ('arb_online CN', "arb_online:'在线'" in text),
    ('arb_online EN', "arb_online:'Online'" in text),
]
for name, result in checks:
    print(f'  {"OK" if result else "XX"} {name}')

nav = text[text.find('<nav>'):text.find('</nav>')]
items = re.findall(r"showPage\('\w+'", nav)
print(f'\n导航菜单 ({len(items)}):')
pages = re.findall(r'id="page-\w+"', text)
print(f'页面 ({len(pages)}):')
for p in pages:
    print(f'  - {p}')
