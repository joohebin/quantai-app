# -*- coding: utf-8 -*-
"""
用二分法把主 script 块分段注入到测试页，找到最早报错的位置。
通过生成一系列 test_bisect_N.html 页面，每个页面只包含前 N 行 JS。
查看哪个最早能运行、哪个开始报错，就能定位问题。

更简单的策略：直接用 Python 的 tokenize 或手动检查特殊结构。
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    all_lines = f.readlines()

# 主 script 块：L1329(0-indexed: 1328) 到 L3205(0-indexed: 3204)
# <script> 在 L1329，内容从 L1330 开始；</script> 在 L3205
SCRIPT_START = 1329  # 0-indexed，内容第一行
SCRIPT_END = 3204    # 0-indexed，内容最后一行（不含</script>）

js_lines = all_lines[SCRIPT_START:SCRIPT_END]
print(f'JS块共 {len(js_lines)} 行 (HTML L{SCRIPT_START+1} ~ L{SCRIPT_END})')

# 策略：把JS分成10段，每段生成一个测试页，页面里用 try{eval(code)}catch(e){...} 
# 但更好的方法是：找到所有的 function XXX() { 定义，测试每个函数体

# 找所有顶级函数定义的位置
func_positions = []
for i, line in enumerate(js_lines):
    stripped = line.strip()
    if re.match(r'^function\s+\w+\s*\(', stripped) or re.match(r'^(const|let|var)\s+\w+\s*=\s*(function|\(.*\)\s*=>)\s*\{', stripped):
        func_positions.append((i, stripped[:80]))

print(f'\n找到 {len(func_positions)} 个函数定义:')
for pos, name in func_positions[:50]:
    print(f'  JS L{pos+1} (HTML L{SCRIPT_START+1+pos}): {name}')
