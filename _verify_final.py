# -*- coding: utf-8 -*-
import re

filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'

with open(filepath, 'rb') as f:
    raw = f.read()

# 验证函数：检查关键字符串是否存在（用二进制比较）
tool_cn_arb = '跨交易所聚合引擎'.encode('utf-8')
tool_cn_mon = '实时监控加密货币交易所价差'.encode('utf-8')
tool_cn_menu = 'data-i18n="nav_arbitrage">'.encode('utf-8') + tool_cn_arb
tool_qt = b'QuantTalk'

checks = {
    'QuantTalk (nav)': b'data-i18n="nav_square">QuantTalk',
    'QuantTalk (title)': b'data-i18n="sq_title">QuantTalk',
    'nav_arbitrage def': b"nav_arbitrage:'" + tool_cn_arb + b"'",
    'arb_title def': b"arb_title:'" + tool_cn_arb + b"'",
    'arb_subtitle def': b"arb_subtitle:'" + tool_cn_mon,
    'arb_page title': b'<span data-i18n="arb_title">',
    'arb_page subtitle': b'data-i18n="arb_subtitle">',
    'nav_arbitrage menu label': tool_cn_menu,
    '页面标题 QuantTalk': tool_qt,
    '页面标题 跨交易所聚合引擎': tool_cn_arb,
}

for name, target in checks.items():
    try:
        found = target in raw
        if found:
            idx = raw.find(target)
            print(f"✅ {name} (at {idx})")
        else:
            print(f"❌ {name} - NOT FOUND")
    except Exception as e:
        print(f"⚠️ {name} - {e}")

# 用 GBK 解码验证中文内容
text_gbk = raw.decode('gbk', errors='replace')

# 检查导航菜单
nav_start = text_gbk.find('<nav>')
nav_end = text_gbk.find('</nav>', nav_start)
nav = text_gbk[nav_start:nav_end+6]
items = re.findall(r'<div class="nav-item[^>]*>(.*?)</div>', nav, re.DOTALL)
print('\n导航菜单 (GBK解码):')
for item in items:
    page_m = re.search(r"showPage\('([^']+)'", item)
    label_m = re.search(r'data-i18n="([^"]+)"[^>]*>([^<]*)<', item)
    label_m2 = re.search(r'data-i18n="([^"]+)"[^>]*>([^<]+)</span', item)
    if page_m:
        page = page_m.group(1)
        if label_m:
            lbl = label_m.group(2).strip()[:30]
        elif label_m2:
            lbl = label_m2.group(2).strip()[:30]
        else:
            lbl = '?'
        print(f'  {page}: {lbl}')

print(f'\ni18n 中文定义中有 arb_title: {"arb_title" in text_gbk}')
print(f'i18n 中文定义中有 nav_arbitrage: {"nav_arbitrage" in text_gbk}')

# 检查仲裁页面
arb_idx = text_gbk.find('id="page-arbitrage')
if arb_idx >= 0:
    # 找标题
    end = text_gbk.find('<div class="page"', arb_idx+10)
    if end < 0: end = arb_idx + 1000
    arb_section = text_gbk[arb_idx:end]
    title_m = re.search(r'data-i18n="([^"]+)"[^>]*>([^<]*)<', arb_section)
    if title_m:
        print(f'仲裁页面标题: [{title_m.group(1)}] {title_m.group(2).strip()[:40]}')
    print(f'页面内容包含 监控交易对: {"监控交易对" in arb_section}')
    print(f'页面内容包含 交易所连接状态: {"交易所连接状态" in arb_section}')

    # 找第一个字段
    for field in ['监控交易对', '活跃套利机会', '24h 套利收益', '已执行套利', 'BTC/USDT(', 'Binance(', 'OKX(']:
        if field in arb_section:
            idx2 = arb_section.find(field)
            print(f'包含字段: {field} (at {idx2})')

# 检查文件大小
fsize = len(raw)
print(f'\n文件大小: {fsize/1024:.1f} KB')
