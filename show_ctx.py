import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
js = scripts[2]
lines = js.split('\n')

print('=== Around L1430-1500 ===')
for i in range(1428, min(1505, len(lines))):
    print(f'  JS-L{i+1}: {lines[i][:130]}')

print('\n=== Around L2005-2015 ===')
for i in range(2003, min(2018, len(lines))):
    print(f'  JS-L{i+1}: {lines[i][:130]}')

print('\n=== Around L2555-2570 ===')
for i in range(2553, min(2572, len(lines))):
    print(f'  JS-L{i+1}: {lines[i][:130]}')
