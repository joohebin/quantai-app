# -*- coding: utf-8 -*-
"""最终验证 + 修复所有问题"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# 从 raw 中解码出文字
text = raw.decode('utf-8', errors='replace')

# 1. 检查导航菜单
nav_start = text.find('<nav>')
nav_end = text.find('</nav>', nav_start)
nav_html = text[nav_start:nav_end+6]
print("=== 导航菜单 ===")
import re
items = re.findall(r"showPage\('(\w+)',this\).*?data-i18n=\"([^\"]+)\"[^>]*>([^<]*)<", nav_html)
for page, key, label in items:
    label_clean = label.strip()[:30]
    print(f"  {page}: [{key}] {label_clean}")

print("\n=== i18n 定义检查 ===")
# 算所有 nav_arbitrage 定义
gkb_text = raw.decode('gbk', errors='replace')
for term in ["nav_arbitrage:", "arb_title:", "arb_subtitle:", "arb_monitored:", "arb_online:"]:
    cnt = gkb_text.count(term)
    print(f"  {term}: {cnt} 处")

print("\n=== 页面检查 ===")
for page_id in ['square', 'arbitrage', 'stratmarket']:
    marker = f'id="page-{page_id}"'
    if marker in text:
        idx = text.find(marker)
        # 看标题
        end = text.find('<div class="page"', idx+10)
        if end < 0: end = idx + 2000
        section = text[idx:end]
        title = re.search(r'data-i18n="([^"]+)"[^>]*>([^<]*)<', section)
        if title:
            print(f"  {page_id}: [{title.group(1)}] {title.group(2).strip()[:30]}")

# 检查 nav_arbitrage 菜单标签
nav_arb_idx = text.find('nav_arbitrage')
if nav_arb_idx >= 0:
    ctx = text[nav_arb_idx-20:nav_arb_idx+100]
    print(f"\nnav_arbitrage 菜单标签: ...{ctx[:80]}...")
    # 看 > 和 < 之间的文字
    start = ctx.find('>')
    end = ctx.find('<', start+1)
    if start >= 0 and end > start:
        label = ctx[start+1:end]
        print(f"  标签文字: {label}")
        if '?' in label or len(set(label)) < 3:
            print("  ⚠️ 标签损坏，需要修复")

# 清理临时脚本
import glob, os
# 不清理，保留到最后
