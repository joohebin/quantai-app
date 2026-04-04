import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 这个问题的根本原因：
# 注入的 JS 代码用字符串拼接生成 HTML，内部 onclick 用 \\' 转义单引号
# 例如: onclick="sqLike(\\'' + p.id + '\\')"
# 在 JS 中字符串求值后变成: onclick="sqLike('xxx')"  - 功能上是对的
# 但 Node.js vm.Script / new Function 对 \\'' 组合的解析比浏览器严格
#
# 实际上浏览器能正常解析吗？让我们换一种思路：
# 如果浏览器报 showPage:undefined，那是因为整个 <script> 块在解析时
# 遇到了语法错误，导致所有函数定义都失败。
#
# 解决方案：把所有 onclick 里的 \\'' 改为 \\x27 (单引号的十六进制转义)
# 或者直接替换为 data-id + 事件委托
# 最简单：全局把 \\\\'' 替换为有效写法

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 统计所有 \\\\'...\\\\ 模式
# 在 Python 字符串里: \\\\'' 代表文件中的 \\'
# 文件中的实际字节: \ ' ( 或 \ \  ' '
count_before = content.count("\\\\''")
print(f"Occurrences of \\\\'' : {count_before}")

# 列出所有出现位置
lines_all = content.split('\n')
for i, line in enumerate(lines_all):
    if "\\\\'" in line:
        print(f'  L{i+1}: {line[:150]}')

print('\nDone listing')
