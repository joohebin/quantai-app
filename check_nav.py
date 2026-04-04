import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

print('=== 所有showPage调用（导航按钮）===')
for i, line in enumerate(lines, 1):
    if 'showPage' in line and 'onclick' in line:
        print(f'L{i}: {line.strip()[:120]}')

print()
print('=== showPage函数定义 ===')
for i, line in enumerate(lines, 1):
    if 'function showPage' in line:
        print(f'L{i}: {line.strip()[:120]}')
        for j in range(i, min(i+25, len(lines))):
            print(f'L{j+1}: {lines[j].strip()[:120]}')
        break

print()
print('=== 导航栏HTML（前500行内找nav相关）===')
for i, line in enumerate(lines[:600], 1):
    if 'nav' in line.lower() and ('onclick' in line or 'btn' in line.lower() or 'item' in line.lower()):
        print(f'L{i}: {line.strip()[:120]}')
