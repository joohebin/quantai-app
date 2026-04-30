f = open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'rb')
c = f.read()
f.close()
t = c.decode('utf-8')

# Find QuantTalk / square page area
idx = t.find('page-square')
if idx < 0:
    idx = t.find('page_quant')
if idx < 0:
    idx = t.find('QuantTalk')
print('QuantTalk related at', idx)
if idx > 0:
    open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\_tmp_area.txt', 'w', encoding='utf-8').write(t[idx-200:idx+4000])
    print('Written')

# Also find all avatar images or user-av elements
for kw in ['user-av', 'user-pic', 'profile-pic', 'avatar-img']:
    i = t.find(kw)
    count = 0
    while i >= 0 and count < 5:
        print(f'{kw} at {i}: {t[i:i+80]}')
        i = t.find(kw, i+1)
        count += 1
