import re, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html','r',encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
js = scripts[2]

# 找所有 t('key') 调用
t_calls = set(re.findall(r"t\('([^']+)'\)", js))
print('=== JS t() calls ===')
for k in sorted(t_calls):
    print(' ', k)

# 找HTML中所有 data-i18n="key"
html_keys = set(re.findall(r'data-i18n="([^"]+)"', content))
print(f'\n=== HTML data-i18n keys ({len(html_keys)}) ===')
for k in sorted(html_keys):
    print(' ', k)

# 找i18n定义里的zh keys
zh_match = re.search(r'zh:\s*\{(.+?)\},\s*en:', content, re.DOTALL)
zh_keys = set(re.findall(r"(\w+):\s*['\"]", zh_match.group(1))) if zh_match else set()
print(f'\n=== ZH defined keys ({len(zh_keys)}) ===')

# 找en keys
en_match = re.search(r'en:\s*\{(.+?)\},\s*ja:', content, re.DOTALL)
en_keys = set(re.findall(r"(\w+):\s*['\"]", en_match.group(1))) if en_match else set()

# 找ja keys
ja_match = re.search(r'ja:\s*\{(.+?)\},\s*ko:', content, re.DOTALL)
ja_keys = set(re.findall(r"(\w+):\s*['\"]", ja_match.group(1))) if ja_match else set()

# 找ko keys
ko_match = re.search(r'ko:\s*\{(.+?)\},\s*ru:', content, re.DOTALL)
ko_keys = set(re.findall(r"(\w+):\s*['\"]", ko_match.group(1))) if ko_match else set()

# 找ru keys
ru_match = re.search(r'ru:\s*\{(.+?)\},\s*ar:', content, re.DOTALL)
ru_keys = set(re.findall(r"(\w+):\s*['\"]", ru_match.group(1))) if ru_match else set()

# 找ar keys
ar_match = re.search(r'ar:\s*\{(.+?)\},?\s*\}', content, re.DOTALL)
ar_keys = set(re.findall(r"(\w+):\s*['\"]", ar_match.group(1))) if ar_match else set()

# 所有需要翻译的key = html_keys + js t() keys
all_needed = html_keys | t_calls

# 检查zh缺失
zh_missing = all_needed - zh_keys
print(f'\n=== ZH missing ({len(zh_missing)}) ===')
for k in sorted(zh_missing): print(' ', k)

en_missing = all_needed - en_keys
print(f'\n=== EN missing ({len(en_missing)}) ===')
for k in sorted(en_missing): print(' ', k)

ja_missing = all_needed - ja_keys
print(f'\n=== JA missing ({len(ja_missing)}) ===')
for k in sorted(ja_missing): print(' ', k)

ko_missing = all_needed - ko_keys
print(f'\n=== KO missing ({len(ko_missing)}) ===')
for k in sorted(ko_missing): print(' ', k)

ru_missing = all_needed - ru_keys
print(f'\n=== RU missing ({len(ru_missing)}) ===')
for k in sorted(ru_missing): print(' ', k)

ar_missing = all_needed - ar_keys
print(f'\n=== AR missing ({len(ar_missing)}) ===')
for k in sorted(ar_missing): print(' ', k)

# 检查HTML里没有data-i18n但含中文的地方
print('\n=== HTML hardcoded Chinese (no data-i18n) ===')
# 只检查非script非style部分
html_body = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
html_body = re.sub(r'<script[^>]*>.*?</script>', '', html_body, flags=re.DOTALL)
lines = html_body.split('\n')
for i, line in enumerate(lines):
    stripped = line.strip()
    if not stripped: continue
    if stripped.startswith('//') or stripped.startswith('*'): continue
    has_cn = any('\u4e00' <= c <= '\u9fff' for c in line)
    has_i18n = 'data-i18n' in line or 'i18n-ph' in line
    if has_cn and not has_i18n:
        print(f'  L{i+1}: {line.rstrip()[:120]}')
