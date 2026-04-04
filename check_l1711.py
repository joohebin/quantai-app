import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
js = scripts[2]
lines = js.split('\n')

# 显示 L1709-1715 的完整内容，包括repr
print('=== Lines 1709-1715 (full repr) ===')
for i in range(1707, 1716):
    line = lines[i]
    print(f'L{i+1} ({len(line)} chars): {line}')
    # 检查是否有问题字符
    for j, ch in enumerate(line):
        if ord(ch) > 127:
            print(f'  [col{j}] U+{ord(ch):04X} = {repr(ch)}')

# 特别检查L1711
print('\n=== L1711 hex dump ===')
line1711 = lines[1710]  # 0-indexed
raw = line1711.encode('utf-8')
print('UTF-8 hex:', raw.hex())
print('Length:', len(line1711))

# 查找 \u{1F947} 写法
print('\n=== u{...} usage ===')
pattern = r'\\u\{[0-9A-Fa-f]+\}'
for i, line in enumerate(lines):
    matches = re.findall(pattern, line)
    if matches:
        print(f'  L{i+1}: {matches} in {line[:100]}')
