import re
s = open('quantai-app/index.html', encoding='utf-8').read()

m = re.search(r'free_daily:\s*(\d+)', s)
print('free_daily:', m.group(1) if m else 'NOT FOUND')

m2 = re.search(r"const PLATFORM_GROQ_KEY = '(.{20})", s)
print('GROQ_KEY starts with:', m2.group(1) if m2 else 'NOT FOUND')

m3 = re.search(r"QUOTA_VERSION = '([^']+)'", s)
print('QUOTA_VERSION:', m3.group(1) if m3 else 'NOT FOUND')

# count script blocks
starts = re.findall(r'<script[^>]*>', s)
print(f'Total script blocks: {len(starts)}')

# check for duplicate const
for kw in ['const PLATFORM_GROQ_KEY', 'const QUOTA =', 'async function aiGateway']:
    cnt = s.count(kw)
    print(f'  {kw}: {cnt}x')
