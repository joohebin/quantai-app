import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
js = scripts[2]
lines = js.split('\n')

# 逐字符扫描，记录每个括号的开关配对
flat = js
i = 0
line_num = 1
in_str_single = False
in_str_double = False
in_str_backtick = False
in_comment_line = False
in_comment_block = False
backtick_depth = 0  # template literal nesting

brace_stack = []    # stack of (line_num, open/close)
paren_stack = []
bracket_stack = []

errors = []

while i < len(flat):
    ch = flat[i]
    nc = flat[i+1] if i+1 < len(flat) else ''

    if ch == '\n':
        line_num += 1
        in_comment_line = False
        i += 1
        continue

    if in_comment_block:
        if ch == '*' and nc == '/':
            in_comment_block = False
            i += 2
        else:
            i += 1
        continue

    if in_comment_line:
        i += 1
        continue

    if in_str_single:
        if ch == '\\': i += 2; continue
        if ch == "'": in_str_single = False
        i += 1; continue

    if in_str_double:
        if ch == '\\': i += 2; continue
        if ch == '"': in_str_double = False
        i += 1; continue

    if in_str_backtick:
        if ch == '\\': i += 2; continue
        if ch == '`': in_str_backtick = False
        # 注意：backtick 里的 ${ } 不处理（简化扫描）
        i += 1; continue

    if ch == '/' and nc == '/':
        in_comment_line = True; i += 2; continue
    if ch == '/' and nc == '*':
        in_comment_block = True; i += 2; continue
    if ch == "'": in_str_single = True; i += 1; continue
    if ch == '"': in_str_double = True; i += 1; continue
    if ch == '`': in_str_backtick = True; i += 1; continue

    if ch == '{':
        brace_stack.append(line_num)
    elif ch == '}':
        if brace_stack:
            brace_stack.pop()
        else:
            errors.append(f'Unmatched }} at JS line {line_num}: {lines[line_num-1].strip()[:80]}')
    elif ch == '(':
        paren_stack.append(line_num)
    elif ch == ')':
        if paren_stack:
            paren_stack.pop()
        else:
            errors.append(f'Unmatched ) at JS line {line_num}: {lines[line_num-1].strip()[:80]}')
    elif ch == '[':
        bracket_stack.append(line_num)
    elif ch == ']':
        if bracket_stack:
            bracket_stack.pop()
        else:
            errors.append(f'Unmatched ] at JS line {line_num}: {lines[line_num-1].strip()[:80]}')
    i += 1

print(f'=== Errors during scan ===')
for e in errors:
    print(' ', e)

print(f'\n=== Unclosed brackets ===')
print(f'Unclosed braces {{: {len(brace_stack)}')
for ln in brace_stack[-10:]:
    print(f'  JS-L{ln}: {lines[ln-1].strip()[:100]}')

print(f'Unclosed parens (: {len(paren_stack)}')
for ln in paren_stack[-10:]:
    print(f'  JS-L{ln}: {lines[ln-1].strip()[:100]}')

print(f'Unclosed brackets [: {len(bracket_stack)}')
for ln in bracket_stack[-10:]:
    print(f'  JS-L{ln}: {lines[ln-1].strip()[:100]}')

# 转换为 index.html 行号（主 script 在 scripts[2]，需要找起始行）
import re as _re
m = list(_re.finditer(r'<script[^>]*>', content))
# 第三个 <script>（index 2）
tag = m[2]
start_char = tag.end()  # script 内容开始字符位置
start_line = content[:start_char].count('\n') + 1
print(f'\nMain script starts at HTML line: {start_line}')
print('To get HTML line: JS-line + ' + str(start_line - 1))
for ln in brace_stack[-5:]:
    print(f'  => HTML-L{ln + start_line - 1}: {lines[ln-1].strip()[:100]}')
for ln in paren_stack[-5:]:
    print(f'  => HTML-L{ln + start_line - 1}: {lines[ln-1].strip()[:100]}')
for ln in bracket_stack[-5:]:
    print(f'  => HTML-L{ln + start_line - 1}: {lines[ln-1].strip()[:100]}')
