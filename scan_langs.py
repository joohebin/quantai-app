import re, sys
sys.stdout.reconfigure(encoding='utf-8')
s = open('quantai-app/index.html', encoding='utf-8').read()

idx = s.find('const I18N')
chunk = s[idx:idx+300000]

# 找所有顶层语言key
langs = re.findall(r'^\s{2}([a-z]{2}):\s*\{', chunk, re.MULTILINE)
print('Languages in I18N:', langs)

# 提取zh的所有key
zh_start = chunk.find('zh: {')
en_start = chunk.find('  en: {')
zh_block = chunk[zh_start:en_start]
keys = re.findall(r"(\w+):\s*['\"]", zh_block)
print(f'zh key count: {len(keys)}')
print('Keys:', keys)
