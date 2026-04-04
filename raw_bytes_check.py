import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找 sqLike 附近的行
lines = content.split('\n')
target_line = None
for i, line in enumerate(lines):
    if 'sqLike' in line and 'onclick' in line:
        target_line = (i, line)
        print(f'L{i+1}: {repr(line[:200])}')
        # 获取字节
        raw_bytes = line.encode('utf-8')
        print(f'Bytes hex: {raw_bytes[:200].hex()}')
        print()
        break

# 找 sqLike( 后面的字符
if target_line:
    i, line = target_line
    idx = line.find('sqLike(')
    if idx >= 0:
        after = line[idx:idx+30]
        print(f'After sqLike(: {repr(after)}')
        print(f'Bytes: {after.encode("utf-8").hex()}')
