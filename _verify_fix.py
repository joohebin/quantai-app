# -*- coding: utf-8 -*-
import re

filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()
text = raw.decode('gbk', errors='replace')

nav_start = text.find('<nav>')
nav_end = text.find('</nav>', nav_start)
nav = text[nav_start:nav_end+6]

items = re.findall(r'<div class="nav-item[^>]*>(.*?)</div>', nav, re.DOTALL)
print('导航菜单:')
for item in items:
    page_m = re.search(r"showPage\('([^']+)'", item)
    label_m = re.search(r'data-i18n="([^"]+)"[^>]*>([^<]*)<', item)
    if page_m:
        page = page_m.group(1)
        i18n_key = label_m.group(1) if label_m else '-'
        label = label_m.group(2) if label_m else '-'
        out = label.strip()[:30]
        try:
            print(f"  {page}: [{i18n_key}] {out}")
        except:
            print(f"  {page}: [{i18n_key}] (label)")

print()
for page_id in ['square', 'arbitrage']:
    idx = text.find(f'id="page-{page_id}"')
    if idx >= 0:
        end = text.find('<div class="page"', idx+10)
        if end < 0:
            end = idx + 2000
        section = text[idx:end]
        title_m = re.search(r'data-i18n="([^"]+)"[^>]*>([^<]*)<', section)
        if title_m:
            title = title_m.group(2).strip()[:40]
            try:
                print(f"页面 {page_id}: [{title_m.group(1)}] {title}")
            except:
                print(f"页面 {page_id}: [标题] (content)")
        else:
            print(f"页面 {page_id}: 标题未找到")
            print(f"  前300字符: {section[:300].strip()}")

# 额外检查仲裁页面是否存在
arb_page = text.find('跨交易所聚合引擎')
print(f"\n仲裁引擎页面存在: {arb_page >= 0}")
if arb_page >= 0:
    ctx = text[arb_page-50:arb_page+100]
    print(f"  context: {ctx[:150]}")

print("\n验证统计:")
print(f"  QuantTalk: {text.count('QuantTalk')}")
print(f"  nav_arbitrage: {text.count('nav_arbitrage')}")
print(f"  跨交易所聚合引擎: {text.count('跨交易所聚合引擎')}")
print(f"  交易广场 (中文): {text.count('交易广场')}")
