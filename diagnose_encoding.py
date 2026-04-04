import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到这一行并修复
# 原始错误行包含乱码字符 - 用正则匹配
import re

# 修复1：renderLbList中的 copy_following 乱码
# 找到包含 copy_following 且包含乱码的行
bad_patterns = [
    # 乱码版本 - 匹配任意字符代替乱码
    (r"t\('copy_following'\)\|\|'[^']*?'\)", "t('copy_following')||'已跟随')"),
]

for pattern, replacement in bad_patterns:
    matches = list(re.finditer(pattern, content))
    print(f'Pattern: {pattern}')
    for m in matches:
        # 显示匹配内容
        print(f'  Found: {repr(m.group())}')
        # 确认是否需要修复
        if m.group() != "t('copy_following')||'已跟随')":
            print(f'  => NEEDS FIX')

print('\n=== Scanning for non-UTF8 in JS ===')
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
js = scripts[2]
lines = js.split('\n')

# 找含有乱码的行（非可打印ASCII且不是合法CJK字符）
import unicodedata
suspicious = []
for i, line in enumerate(lines):
    for j, ch in enumerate(line):
        code = ord(ch)
        # 合法CJK范围 0x4E00-0x9FFF，日语 0x3040-0x30FF，韩语 0xAC00-0xD7AF，符号等
        if code > 127:
            name = unicodedata.name(ch, '')
            # 检查是否是奇怪的字符（如替换字符、乱码区域）
            if 0xE000 <= code <= 0xF8FF or code == 0xFFFD:  # 私用区或替换字符
                suspicious.append((i+1, j, hex(code), ch, line[:100]))
            # 检查CJK兼容区域的奇怪字符
            elif 0x3400 <= code <= 0x4DBF:  # CJK扩展A - 罕见字
                pass  # 暂时忽略
                
print(f'Suspicious chars: {len(suspicious)}')
for ln, col, hexval, ch, linetext in suspicious[:10]:
    print(f'  L{ln} col{col}: {hexval} {repr(ch)} in: {linetext[:80]}')

# 直接搜索乱码片段
garbled = '宸茶窡闅'
garbled2 = '宸茶窡闅?'
if garbled in content:
    idx = content.index(garbled)
    line_num = content[:idx].count('\n') + 1
    print(f'\nFound garbled text "{garbled}" at line {line_num}')
    # 显示该行
    lines_all = content.split('\n')
    print(f'Line: {lines_all[line_num-1][:200]}')
else:
    print(f'\nGarbled text "{garbled}" NOT found in UTF-8 content')
    print('Content might look fine in UTF-8 but node reads as GBK?')
    
    # 尝试找 copy_following 所在的所有行
    for i, line in enumerate(lines):
        if 'copy_following' in line:
            print(f'  L{i+1}: {line[:200]}')
