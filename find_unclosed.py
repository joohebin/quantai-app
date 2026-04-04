import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
main_js = scripts[2]

lines = main_js.split('\n')

# 追踪每个括号的开位置
brace_stack = []
paren_stack = []
bracket_stack = []

for i, line in enumerate(lines, 1):
    in_str = False
    str_char = None
    in_comment = False
    for j, c in enumerate(line):
        # 单行注释
        if not in_str and j+1 < len(line) and line[j:j+2] == '//':
            break
        if not in_str:
            if c in ('"', "'", '`'):
                in_str = True
                str_char = c
            elif c == '{':
                brace_stack.append(i)
            elif c == '}':
                if brace_stack: brace_stack.pop()
            elif c == '(':
                paren_stack.append(i)
            elif c == ')':
                if paren_stack: paren_stack.pop()
            elif c == '[':
                bracket_stack.append(i)
            elif c == ']':
                if bracket_stack: bracket_stack.pop()
        else:
            if c == str_char and (j == 0 or line[j-1] != '\\'):
                in_str = False

print(f"未闭合的 {{ : {len(brace_stack)} 个, 最后几个在JS行: {brace_stack[-5:]}")
print(f"未闭合的 ( : {len(paren_stack)} 个, 最后几个在JS行: {paren_stack[-5:]}")
print(f"未闭合的 [ : {len(bracket_stack)} 个, 最后几个在JS行: {bracket_stack[-5:]}")

# 打印对应行内容
print("\n--- 未闭合的 ( 所在行 ---")
for ln in paren_stack[-5:]:
    print(f"JS行 {ln}: {lines[ln-1][:100]}")

print("\n--- 未闭合的 [ 所在行 ---")
for ln in bracket_stack[-5:]:
    print(f"JS行 {ln}: {lines[ln-1][:100]}")
