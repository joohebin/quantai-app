# -*- coding: utf-8 -*-
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

target = b"nav_square:'"
idx = 0
count = 0
while True:
    idx = raw.find(target, idx)
    if idx < 0:
        break
    count += 1
    chunk = raw[idx:idx+40]
    print(f'#{count} at {idx}: {chunk}')
    try:
        text = chunk.decode('utf-8')
        print(f'  UTF8: {repr(text)}')
    except:
        print('  (not utf8)')
    try:
        text2 = chunk.decode('gbk')
        print(f'  GBK: {repr(text2)}')
    except:
        print('  (not gbk)')
    print()
    idx += 1
