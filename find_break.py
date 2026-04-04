import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 主script块 L1329到L3205 (0-indexed 1328:3205)
script_lines = lines[1328:3205]

# 严格括号追踪，跳过字符串和注释
def get_depth_at(script_lines):
    """返回每行执行后的深度，以及是否在字符串内"""
    depth = 0
    in_string = None
    in_block_comment = False
    result = []
    
    for lineno, line in enumerate(script_lines, 1):
        in_line_comment = False
        i = 0
        while i < len(line):
            c = line[i]
            if c == '\n':
                in_line_comment = False
                i += 1
                continue
            if in_line_comment:
                i += 1
                continue
            if in_block_comment:
                if c == '*' and i+1 < len(line) and line[i+1] == '/':
                    in_block_comment = False
                    i += 2
                else:
                    i += 1
                continue
            if in_string:
                if c == '\\':
                    i += 2
                    continue
                if c == in_string and in_string != '`':
                    in_string = None
                elif c == '`' and in_string == '`':
                    in_string = None
                i += 1
                continue
            if c == '/' and i+1 < len(line):
                if line[i+1] == '/':
                    in_line_comment = True
                    i += 2
                    continue
                elif line[i+1] == '*':
                    in_block_comment = True
                    i += 2
                    continue
            if c in ('"', "'", '`'):
                in_string = c
                i += 1
                continue
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
            i += 1
        result.append((lineno, depth, line.rstrip()[:80]))
    return result

result = get_depth_at(script_lines)

# 找最后一次 depth=0 的位置
last_zero = 0
last_zero_line = ''
for lineno, depth, content in result:
    if depth == 0:
        last_zero = lineno
        last_zero_line = content

print(f"最终深度: {result[-1][1]}")
print(f"最后一次depth=0: script行 L{last_zero}, HTML行 L{last_zero+1328}")
print(f"内容: {last_zero_line}")
print()
print("=== L{}-{} 附近的深度变化 ===".format(last_zero-5, last_zero+20))
for lineno, depth, content in result[last_zero-6:last_zero+20]:
    html_line = lineno + 1328
    marker = " <<<<" if depth != 0 and result[lineno-2][1] == 0 else ""
    print(f"script L{lineno:4d} [HTML L{html_line:4d}] depth={depth:3d}  {content}{marker}")
