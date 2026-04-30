# -*- coding: utf-8 -*-
"""补完：英文 i18n 定义 + 检查所有 18 个语言中的 nav_square"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

text = raw.decode('gbk', errors='surrogateescape')
lines = text.split('\n')

# 找所有 nav_square 定义行并定位每个语言块
nav_square_lines = []
for i, line in enumerate(lines):
    if "nav_square:'QuantTalk'" in line and '//' not in line:
        nav_square_lines.append(i)
        # 显示前五行（注释）
        ctx_start = max(0, i-3)
        ctx_end = min(len(lines), i+5)
        print(f"--- 语言块 #{len(nav_square_lines)} (行 {i}) ---")
        for j in range(ctx_start, ctx_end):
            prefix = ">" if j == i else " "
            print(f"{prefix} L{j}: {lines[j][:80]}")

print(f"\n找到 {len(nav_square_lines)} 个 nav_square QuantTalk 定义")
