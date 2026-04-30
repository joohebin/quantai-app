f=open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','rb')
c=f.read()
f.close()
t=c.decode('utf-8')

# Fix getPlanPrice
i=t.find('window.getPlanPrice = function')
j=t.find('window.canUseNode', i)
old_block = t[i:j]
new_block = "window.getPlanPrice = function(planId){\n  var p = window.getPlanInfo(planId);\n  return p.price === 0 ? '\u514d\u8d39' : '$' + p.price + '/' + p.period;\n};\n"
t = t[:i] + new_block + t[j:]
print('getPlanPrice fixed')

# Fix REVENUE_SHARE thresholds (check if they got updated)
i=t.find('window.REVENUE_SHARE = [')
j=t.find('];',i)+2
print('REVENUE_SHARE:', repr(t[i:j]))

# Fix corrupt chars in plan grid "free" display
i2=t.find('window.getPlanPrice(id) +')
if i2>=0:
    print('Found getPlanPrice call in render')

with open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','w',encoding='utf-8') as f:
    f.write(t)
print('Saved')
