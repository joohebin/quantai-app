f = open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'rb')
c = f.read()
f.close()
t = c.decode('utf-8')

# Find page-square HTML
idx = t.find('id="page-square"')
if idx < 0:
    idx = t.find('page-square')
print('page-square at', idx)

# Write from the start of the div to a good size
open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\_tmp_qt_html.txt', 'w', encoding='utf-8').write(t[idx:idx+6000])
print('Written')
