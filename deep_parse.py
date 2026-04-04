# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找主script块的开始
start = -1
for i, line in enumerate(lines):
    if '<script>' in line and i > 1300:
        start = i
        break

print(f'Script开始行(HTML): {start+1}')

js_lines = lines[start+1:]

depth_brace = 0
depth_paren = 0
depth_bracket = 0
in_str_single = False
in_str_double = False
in_template = 0
in_comment = False
in_line_comment = False

errors = []
last_zero_line = start + 1  # HTML行号

for idx, raw_line in enumerate(js_lines):
    html_line_no = start + 2 + idx  # 1-based HTML行号
    line = raw_line.rstrip()
    i = 0
    in_line_comment = False
    prev_brace = depth_brace
    prev_paren = depth_paren
    
    while i < len(line):
        c = line[i]
        nc = line[i+1] if i+1 < len(line) else ''
        
        if in_line_comment:
            break
        if in_comment:
            if c == '*' and nc == '/':
                in_comment = False
                i += 2
                continue
            i += 1
            continue
        if in_str_single:
            if c == '\\':
                i += 2
                continue
            if c == "'":
                in_str_single = False
            i += 1
            continue
        if in_str_double:
            if c == '\\':
                i += 2
                continue
            if c == '"':
                in_str_double = False
            i += 1
            continue
        if in_template > 0:
            if c == '\\':
                i += 2
                continue
            if c == '`':
                in_template -= 1
                i += 1
                continue
            if c == '$' and nc == '{':
                depth_brace += 1
                i += 2
                continue
            i += 1
            continue
        
        # 正常上下文
        if c == '/' and nc == '/':
            in_line_comment = True
            break
        if c == '/' and nc == '*':
            in_comment = True
            i += 2
            continue
        if c == "'":
            in_str_single = True
        elif c == '"':
            in_str_double = True
        elif c == '`':
            in_template += 1
        elif c == '{':
            depth_brace += 1
        elif c == '}':
            depth_brace -= 1
        elif c == '(':
            depth_paren += 1
        elif c == ')':
            depth_paren -= 1
        elif c == '[':
            depth_bracket += 1
        elif c == ']':
            depth_bracket -= 1
        i += 1
    
    # 记录深度回零的位置
    if depth_brace == 0 and depth_paren == 0 and depth_bracket == 0 and not in_str_single and not in_str_double:
        last_zero_line = html_line_no
    
    # 检查异常
    if depth_brace < 0:
        errors.append(f'多余}} HTML L{html_line_no}: brace={depth_brace}  {line[:80]}')
        depth_brace = 0
    if depth_paren < -1:
        errors.append(f'多余) HTML L{html_line_no}: paren={depth_paren}  {line[:80]}')
        depth_paren = 0
    if depth_bracket < -1:
        errors.append(f'多余] HTML L{html_line_no}: bracket={depth_bracket}  {line[:80]}')
        depth_bracket = 0
    
    # 检查行尾未闭合字符串（单行字符串跨行是错误）
    if in_str_single:
        errors.append(f'未闭合单引号 HTML L{html_line_no}: {line[:100]}')
        in_str_single = False
    if in_str_double:
        errors.append(f'未闭合双引号 HTML L{html_line_no}: {line[:100]}')
        in_str_double = False

print(f'\n最终状态: brace={depth_brace} paren={depth_paren} bracket={depth_bracket} template={in_template}')
print(f'最后深度回零的HTML行号: {last_zero_line}')

if errors:
    print(f'\n发现 {len(errors)} 个错误:')
    for e in errors[:30]:
        print('  ' + e)
else:
    print('\n未发现明显语法错误')

# 显示最后回零点之后的内容（问题区域）
print(f'\n=== 深度回零后的内容（HTML L{last_zero_line} ~ L{last_zero_line+20}）===')
for i in range(last_zero_line-1, min(last_zero_line+20, len(lines))):
    print(f'L{i+1}: {lines[i].rstrip()[:120]}')
