import re, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html','r',encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
js = scripts[2]

# 找所有 t('key') 调用
t_calls = set(re.findall(r"t\('([^']+)'\)", js))

# 找HTML中所有 data-i18n="key"
html_keys = set(re.findall(r'data-i18n="([^"]+)"', content))

# 所有需要翻译的key
all_needed = html_keys | t_calls
# 过滤掉明显不是key的
real_keys = {k for k in all_needed if re.match(r'^[a-z][a-z0-9_]+$', k)}

def extract_keys(text):
    return set(re.findall(r"(\w+):\s*['\"]", text))

zh_match = re.search(r'zh:\s*\{(.+?)\},\s*en:', content, re.DOTALL)
en_match = re.search(r'en:\s*\{(.+?)\},\s*ja:', content, re.DOTALL)
ja_match = re.search(r'ja:\s*\{(.+?)\},\s*ko:', content, re.DOTALL)
ko_match = re.search(r'ko:\s*\{(.+?)\},\s*ru:', content, re.DOTALL)
ru_match = re.search(r'ru:\s*\{(.+?)\},\s*ar:', content, re.DOTALL)
ar_match = re.search(r'ar:\s*\{(.+?)\},?\s*\}', content, re.DOTALL)

zh_keys = extract_keys(zh_match.group(1)) if zh_match else set()
en_keys = extract_keys(en_match.group(1)) if en_match else set()
ja_keys = extract_keys(ja_match.group(1)) if ja_match else set()
ko_keys = extract_keys(ko_match.group(1)) if ko_match else set()
ru_keys = extract_keys(ru_match.group(1)) if ru_match else set()
ar_keys = extract_keys(ar_match.group(1)) if ar_match else set()

for lang, keys in [('EN', en_keys), ('JA', ja_keys), ('KO', ko_keys), ('RU', ru_keys), ('AR', ar_keys)]:
    missing = real_keys - keys
    if missing:
        print(f'\n=== {lang} missing ({len(missing)}) ===')
        for k in sorted(missing):
            zh_val = ''
            if zh_match:
                zm = re.search(rf"'{k}':\s*'([^']*)'|{k}:\s*'([^']*)'", zh_match.group(1))
                if zm:
                    zh_val = zm.group(1) or zm.group(2)
            print(f'  {k}: zh="{zh_val}"')
