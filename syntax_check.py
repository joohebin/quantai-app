import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('check.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 严格括号追踪：跳过字符串和注释
def analyze(lines):
    depth = 0
    in_string = None  # None / '"' / "'" / '`'
    in_line_comment = False
    in_block_comment = False
    depth_history = []
    
    for lineno, line in enumerate(lines, 1):
        in_line_comment = False
        i = 0
        while i < len(line):
            c = line[i]
            
            # 换行结束行注释
            if c == '\n':
                in_line_comment = False
                i += 1
                continue
            
            # 跳过行注释
            if in_line_comment:
                i += 1
                continue
            
            # 处理块注释结束
            if in_block_comment:
                if c == '*' and i+1 < len(line) and line[i+1] == '/':
                    in_block_comment = False
                    i += 2
                else:
                    i += 1
                continue
            
            # 字符串内
            if in_string:
                if c == '\\':
                    i += 2  # 跳过转义
                    continue
                if c == in_string:
                    if in_string == '`' and c == '`':
                        in_string = None
                    elif c == in_string:
                        in_string = None
                i += 1
                continue
            
            # 检测注释开始
            if c == '/' and i+1 < len(line):
                if line[i+1] == '/':
                    in_line_comment = True
                    i += 2
                    continue
                elif line[i+1] == '*':
                    in_block_comment = True
                    i += 2
                    continue
            
            # 检测字符串开始
            if c in ('"', "'", '`'):
                in_string = c
                i += 1
                continue
            
            # 括号计数
            if c == '{':
                depth += 1
                depth_history.append((lineno, depth, '{', line.strip()[:60]))
            elif c == '}':
                depth -= 1
                depth_history.append((lineno, depth, '}', line.strip()[:60]))
            
            i += 1
    
    return depth, depth_history

depth, history = analyze(lines)
print(f"最终深度: {depth} (应为0)")
print(f"总共 {len(history)} 个括号事件")
print()

# 打印最后20个括号事件，看文件末尾是否正常
print("=== 末尾20个括号事件 ===")
for lineno, d, bracket, ctx in history[-20:]:
    print(f"  L{lineno:4d} [{bracket}] depth={d:3d}  {ctx}")

print()

# 找所有 depth < 0 的位置（意味着多余的 }）
negatives = [(ln, d, b, ctx) for ln, d, b, ctx in history if d < 0]
if negatives:
    print(f"=== depth<0 的位置（多余的}}）===")
    for ln, d, b, ctx in negatives:
        print(f"  L{ln:4d} depth={d} {ctx}")
else:
    print("没有 depth<0 的位置（无多余}）")

print()
# 打印所有深度回归到0的位置
zeros = [(ln, d, b, ctx) for ln, d, b, ctx in history if d == 0]
print(f"=== depth回到0的位置（函数/块结束） 共{len(zeros)}次 ===")
for ln, d, b, ctx in zeros[-10:]:
    print(f"  L{ln:4d} {ctx}")
