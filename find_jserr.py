import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取主script块（第3个，最大的那个）
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
js = scripts[2]  # 主JS块

lines = js.split('\n')
print(f'Main script lines: {len(lines)}')

# 1. 检查 toast 是否被重定义为对象
toast_defs = []
for i, line in enumerate(lines):
    if 'toast' in line and ('=' in line or 'const ' in line or 'let ' in line or 'var ' in line):
        toast_defs.append((i+1, line.strip()[:100]))

print(f'\n=== toast definitions ({len(toast_defs)}) ===')
for ln, l in toast_defs[:20]:
    print(f'  L{ln}: {l}')

# 2. 括号平衡检查 - 找到失衡位置
brace = 0
paren = 0
bracket = 0
in_str_single = False
in_str_double = False
in_str_backtick = False
in_comment_line = False
in_comment_block = False
err_line = -1
err_col = -1

# 重新逐字符扫描
flat = js
i = 0
line_num = 1
col_num = 0
last_open_brace = []  # stack of (line, col) for {
last_open_paren = []
last_open_bracket = []

while i < len(flat):
    ch = flat[i]
    nc = flat[i+1] if i+1 < len(flat) else ''
    
    if ch == '\n':
        line_num += 1
        col_num = 0
        in_comment_line = False
        i += 1
        continue
    col_num += 1

    # 注释处理
    if in_comment_block:
        if ch == '*' and nc == '/':
            in_comment_block = False
            i += 2
            continue
        i += 1
        continue
    if in_comment_line:
        i += 1
        continue
    
    # 字符串处理
    if in_str_single:
        if ch == '\\':
            i += 2
            continue
        if ch == "'":
            in_str_single = False
        i += 1
        continue
    if in_str_double:
        if ch == '\\':
            i += 2
            continue
        if ch == '"':
            in_str_double = False
        i += 1
        continue
    if in_str_backtick:
        if ch == '\\':
            i += 2
            continue
        if ch == '`':
            in_str_backtick = False
        i += 1
        continue

    # 开始注释/字符串
    if ch == '/' and nc == '/':
        in_comment_line = True
        i += 2
        continue
    if ch == '/' and nc == '*':
        in_comment_block = True
        i += 2
        continue
    if ch == "'":
        in_str_single = True
        i += 1
        continue
    if ch == '"':
        in_str_double = True
        i += 1
        continue
    if ch == '`':
        in_str_backtick = True
        i += 1
        continue

    # 括号计数
    if ch == '{':
        brace += 1
        last_open_brace.append((line_num, col_num))
    elif ch == '}':
        brace -= 1
        if last_open_brace:
            last_open_brace.pop()
        if brace < 0:
            print(f'\nERROR: Unmatched }} at line {line_num} col {col_num}')
            # 打印上下文
            ctx_lines = js.split('\n')
            for cl in range(max(0, line_num-3), min(len(ctx_lines), line_num+2)):
                print(f'  L{cl+1}: {ctx_lines[cl][:120]}')
            brace = 0
    elif ch == '(':
        paren += 1
        last_open_paren.append((line_num, col_num))
    elif ch == ')':
        paren -= 1
        if last_open_paren:
            last_open_paren.pop()
        if paren < 0:
            print(f'\nERROR: Unmatched ) at line {line_num} col {col_num}')
            paren = 0
    elif ch == '[':
        bracket += 1
        last_open_bracket.append((line_num, col_num))
    elif ch == ']':
        bracket -= 1
        if last_open_bracket:
            last_open_bracket.pop()
        if bracket < 0:
            print(f'\nERROR: Unmatched ] at line {line_num} col {col_num}')
            bracket = 0
    i += 1

print(f'\n=== Final Balance ===')
print(f'Braces  {{}}: {brace}  (should be 0)')
print(f'Parens  (): {paren}  (should be 0)')
print(f'Brackets []: {bracket}  (should be 0)')

if brace != 0:
    print(f'Last open braces: {last_open_brace[-5:]}')
if paren != 0:
    print(f'Last open parens: {last_open_paren[-5:]}')
if bracket != 0:
    print(f'Last open brackets: {last_open_bracket[-5:]}')

# 3. 检查 `toast` 变量冲突
print('\n=== Checking for `toast` variable conflict ===')
for i, line in enumerate(lines):
    stripped = line.strip()
    # 查找 const/let/var toast = {...} 或类似对象定义
    if re.search(r'(const|let|var)\s+toast\s*=\s*\{', stripped):
        print(f'  CONFLICT at L{i+1}: {stripped[:120]}')
    elif re.search(r'(const|let|var)\s+toast\b', stripped):
        print(f'  REDEFINED at L{i+1}: {stripped[:120]}')

print('\nDone.')
