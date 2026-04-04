import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
js = scripts[2]

# 写为 .mjs（module语法更严格，会报更详细的错）
# 但先用普通 .js，并在首行加严格模式
# 去掉可能触发 module-specific 错误的内容
with open('_check.js', 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)

lines = js.split('\n')
print(f'Wrote _check.js: {len(lines)} lines')
# 打印前5行确认编码正常
for i in range(5):
    print(f'  L{i+1}: {repr(lines[i][:80])}')
