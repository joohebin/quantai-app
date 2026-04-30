f = open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'rb')
c = f.read()
f.close()
t = c.decode('utf-8')
idx = t.find('id="app"')
print('id=app at', idx)
if idx > 0:
    open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\_tmp_app.txt', 'w', encoding='utf-8').write(t[idx:idx+8000])
    print('Written')
else:
    print('Not found, trying to find other landmarks')
    for kw in ['#app', '<div id=', '<div class=', 'channel', 'QT']:
        i = t.find(kw)
        if i >= 0:
            print(f'{kw} at {i}')
            break
