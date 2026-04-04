import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 批量修复：把 \\\\\\\\ + ' + var + '\\\\\\\\' 替换为正确的转义
# 文件中实际字节: \\\\'  (4个char: \ \ \ ')
# 需要改成: \\' (2个char: \ ')
# 在JS字符串中: \' = 转义单引号 = 字面 '
# 这样字符串拼接后 onclick 里就能得到正确的单引号
# ============================================================

# 文件中 \\\\\\\\ 在Python repr里是 \\\\\\\\
# 我们用 bytes 操作更直接

raw = content.encode('utf-8')
# 文件中 \\\\'  字节序列: 5c 5c 5c 5c 27  (4个反斜杠 + 单引号)
old_bytes = b"\\\\\\\\'"  # = \\\\'
new_bytes = b"\\'"        # = \'

count = raw.count(old_bytes)
print(f'Found {count} occurrences of \\\\\\\\ pattern')

fixed_raw = raw.replace(old_bytes, new_bytes)

content_fixed = fixed_raw.decode('utf-8')
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content_fixed)
print('Saved index.html')

# 验证
raw2 = content_fixed.encode('utf-8')
remaining = raw2.count(b"\\\\\\\\")
print(f'Remaining \\\\\\\\ patterns: {remaining}')

# 重新生成 _check.js
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content_fixed, re.DOTALL)
js = scripts[2]
with open('_check.js', 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print(f'Regenerated _check.js: {js.count(chr(10))} lines')

# 显示修复后的样例行
lines = content_fixed.split('\n')
for i, line in enumerate(lines):
    if "sqLike" in line and "onclick" in line:
        print(f'\nSample fixed line L{i+1}:')
        print(line[:180])
        break
