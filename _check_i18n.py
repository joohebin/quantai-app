# -*- coding: utf-8 -*-
"""检查并修复未到位的中英文 i18n"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

text = raw.decode('utf-8')
lines = text.split('\n')

# 找所有包含 "nav_square:" 的行
print("所有 nav_square 定义:")
for i, line in enumerate(lines):
    if 'nav_square:' in line:
        lang = ''
        for j in range(max(0,i-3), i):
            if lines[j].strip().startswith('//'):
                lang = lines[j].strip()
                break
        # 取前 60 字符
        snippet = line[:60]
        print(f"  L{i}: {lang[:30]:30s} | {snippet}")

# 找我们已经插入的 zh i18n
print("\n仲裁引擎 i18n 定义:")
for i, line in enumerate(lines):
    if 'nav_arbitrage' in line:
        ctx = lines[max(0,i-2):i+3]
        for j, l in enumerate(ctx):
            prefix = '>>>' if j == 2 else '   '
            print(f"{prefix} L{i-2+j}: {l[:80]}")
