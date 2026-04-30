f=open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','rb')
c=f.read()
f.close()
t=c.decode('utf-8')
i=t.find("id: 'basic'")
# write to file
with open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\tmp_basic.txt','w',encoding='utf-8') as fw:
    fw.write(t[i:i+120])
print('Written')
