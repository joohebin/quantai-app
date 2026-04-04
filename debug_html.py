import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

print(f'总行数: {len(lines)}')

# 找导航点击
print('\n=== 导航 onclick ===')
for i, line in enumerate(lines, 1):
    if 'onclick' in line and ('showPage' in line or 'nav' in line.lower()):
        print(f'L{i}: {line.strip()[:120]}')

# 找 showPage 函数定义
print('\n=== showPage 函数 ===')
for i, line in enumerate(lines, 1):
    if 'function showPage' in line or 'showPage = ' in line:
        print(f'L{i}: {line.strip()[:120]}')
        for j in range(i, min(i+20, len(lines))):
            print(f'  L{j+1}: {lines[j].strip()[:120]}')
        print()

# 找 DOMContentLoaded
print('\n=== DOMContentLoaded ===')
for i, line in enumerate(lines, 1):
    if 'DOMContentLoaded' in line or 'window.onload' in line:
        print(f'L{i}: {line.strip()[:120]}')

# 找 script 标签
print('\n=== script 标签 ===')
for i, line in enumerate(lines, 1):
    if '<script' in line or '</script>' in line:
        print(f'L{i}: {line.strip()[:120]}')

# 检查JS中是否有早期报错（try-catch之外的顶层代码）
print('\n=== 顶层危险语句（第一个函数之外）===')
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
for si, sc in enumerate(scripts):
    sc_lines = sc.split('\n')
    in_func = 0
    for li, ln in enumerate(sc_lines, 1):
        s = ln.strip()
        if s.startswith('function ') or 'function(' in s or '=>' in s:
            in_func += 1
        if in_func == 0 and s and not s.startswith('//') and not s.startswith('/*') and not s.startswith('*'):
            if any(kw in s for kw in ['const ', 'let ', 'var ', 'document.', 'window.']):
                print(f'  Script[{si}] L{li}: {s[:100]}')
