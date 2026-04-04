import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html','r',encoding='utf-8') as f:
    content = f.read()

# 检查 EN/JA/KO 缺少的 i18n keys
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
js = scripts[2]

# 提取所有 I18N 的 zh keys
zh_match = re.search(r'I18N\s*=\s*\{.*?zh\s*:\s*\{(.*?)\}[\s,]*en\s*:', js, re.DOTALL)
en_match = re.search(r'en\s*:\s*\{(.*?)\}[\s,]*ja\s*:', js, re.DOTALL)
ja_match = re.search(r'ja\s*:\s*\{(.*?)\}[\s,]*ko\s*:', js, re.DOTALL)
ko_match = re.search(r'ko\s*:\s*\{(.*?)\}\s*\};\s*function t\b', js, re.DOTALL)

def extract_keys(block):
    return set(re.findall(r'\b(\w+)\s*:', block))

if zh_match and en_match and ja_match and ko_match:
    zh_keys = extract_keys(zh_match.group(1))
    en_keys = extract_keys(en_match.group(1))
    ja_keys = extract_keys(ja_match.group(1))
    ko_keys = extract_keys(ko_match.group(1))
    
    print(f'ZH keys: {len(zh_keys)}')
    print(f'EN keys: {len(en_keys)}')
    print(f'JA keys: {len(ja_keys)}')
    print(f'KO keys: {len(ko_keys)}')
    
    print(f'\nEN 缺少的 keys ({len(zh_keys - en_keys)}):')
    for k in sorted(zh_keys - en_keys):
        print(f'  {k}')
    
    print(f'\nJA 缺少的 keys ({len(zh_keys - ja_keys)}):')
    for k in sorted(zh_keys - ja_keys):
        print(f'  {k}')
    
    print(f'\nKO 缺少的 keys ({len(zh_keys - ko_keys)}):')
    for k in sorted(zh_keys - ko_keys):
        print(f'  {k}')
else:
    print('i18n 块匹配失败')
    if not zh_match: print('zh not found')
    if not en_match: print('en not found')
    if not ja_match: print('ja not found')
    if not ko_match: print('ko not found')
