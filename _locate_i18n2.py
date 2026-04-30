# -*- coding: utf-8 -*-
"""列出所有 nav_square 定义后的下一行，找到英文块插入点"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# 用 GBK 解码
text = raw.decode('gbk', errors='replace')
lines = text.split('\n')

# 找所有 nav_square: 开头
count = 0
for i, line in enumerate(lines):
    if line.startswith('    nav_square:'):
        count += 1
        # 显示注释
        cmt_lines = []
        for j in range(max(0, i-5), i):
            stripped = lines[j].strip()
            if stripped.startswith('//'):
                cmt_lines.append(stripped[2:].strip())
        cmt = ' / '.join(cmt_lines) if cmt_lines else '(无注释)'
        next_vals = lines[i][:60] if i < len(lines) else ''
        print(f"#{count} L{i}: [{cmt[:30]}] {next_vals[:60]}")

# 如果已插入中文 i18n，查找它
for i, line in enumerate(lines):
    if '跨交易所聚合引擎' in line or 'Arbitrage Engine' in line:
        print(f"\n仲裁引擎行 L{i}: {line[:80]}")
