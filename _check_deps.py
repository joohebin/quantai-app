# -*- coding: utf-8 -*-
import re
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()
text = raw.decode('gbk', errors='replace')

scripts = re.findall(r'<script[^>]*src="([^"]+)"', text)
links = re.findall(r'<link[^>]*href="([^"]+)"', text)

print('Scripts:')
for s in scripts[:30]:
    print(f'  {s}')
print(f'\nLinks:')
for l in links[:20]:
    print(f'  {l}')
