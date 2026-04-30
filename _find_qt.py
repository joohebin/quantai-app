f = open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'rb')
c = f.read()
f.close()
t = c.decode('utf-8')

# Find the QuantTalk page HTML area — look for the channel container
for kw in ['channel-container', 'quantalk-container', 'qt-container', 'qt-content', 'channel-list', 'channel-panel']:
    i = t.find(kw)
    if i >= 0:
        print(f'{kw} at {i}')
        open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\_tmp_qt.txt', 'w', encoding='utf-8').write(t[max(0,i-300):i+3000])
        break

# Also find id containing square or quant
i = t.find('channel')
print(f'channel at {i}')
