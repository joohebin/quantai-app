import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
main_js = scripts[2]

brace = paren = bracket = 0
errors = []
lines = main_js.split('\n')
for i, line in enumerate(lines, 1):
    in_str = False
    str_char = None
    for j, c in enumerate(line):
        if not in_str:
            if c in ('"', "'", '`'):
                in_str = True
                str_char = c
            elif c == '{': brace += 1
            elif c == '}': brace -= 1
            elif c == '(': paren += 1
            elif c == ')': paren -= 1
            elif c == '[': bracket += 1
            elif c == ']': bracket -= 1
        else:
            if c == str_char and (j == 0 or line[j-1] != '\\'):
                in_str = False
    if brace < 0 or paren < 0 or bracket < 0:
        errors.append(f'Line {i}: brace={brace} paren={paren} bracket={bracket}  >>> {line[:80]}')
        brace = max(0, brace)
        paren = max(0, paren)
        bracket = max(0, bracket)

print(f'最终: brace={brace}, paren={paren}, bracket={bracket}')
if errors:
    print('异常行:')
    for e in errors[:10]:
        print(e)
else:
    print('括号基本平衡')
print(f'总行数: {len(lines)}')
