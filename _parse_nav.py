# -*- coding: utf-8 -*-
"""用 lxml 或 html.parser 解析导航菜单结构"""
import re

filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# 用 GBK 解码完整内容
text = raw.decode('gbk', errors='replace')

# 提取 <nav> 内容
nav_start = text.find('<nav>')
nav_end = text.find('</nav>', nav_start)
nav_html = text[nav_start:nav_end+6]

# 提取每个 nav-item
items = re.findall(
    r'<div class="nav-item[^"]*"(?:\s+[^>]*)?>\s*'
    r'(.*?)</div>', 
    nav_html, re.DOTALL
) if False else []

# 改用更简单的方法 - 按 <div class="nav-item 分割
parts = nav_html.split('<div class="nav-item')
if len(parts) <= 1:
    parts = nav_html.split('<div class="nav-item ')

print(f"=== 导航菜单 ({len(parts)-1} 项，考虑 {len(parts)} 个片段) ===\n")

for i, part in enumerate(parts[1:], 1):
    # 找到结尾 </div>
    end_idx = part.find('</div>')
    if end_idx < 0:
        continue
    item_html = part[:end_idx]
    
    # 提取 showPage
    page_match = re.search(r"showPage\('([^']+)'", item_html)
    page = page_match.group(1) if page_match else '?'
    
    # 提取 data-i18n key
    i18n_match = re.search(r'data-i18n="([^"]+)"', item_html)
    i18n_key = i18n_match.group(1) if i18n_match else '?'
    
    # 提取显示文本（最后一个 > 到 < 之间）
    # 移除嵌套标签
    text_content = re.sub(r'<[^>]*>', '', item_html).strip()
    # 简化空格
    text_content = re.sub(r'\s+', ' ', text_content)
    
    has_badge = 'badge' in item_html or 'New' in text_content
    
    print(f"{'NEW' if has_badge else '   '} #{i:2d} {page:20s} [{i18n_key:20s}] {text_content[:40]}")
