import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
js = scripts[2]

# 写出主JS为独立文件
with open('_main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print(f'Written _main.js, {len(js)} chars, {js.count(chr(10))} lines')
