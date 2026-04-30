f=open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','rb')
c=f.read()
f.close()
t=c.decode('utf-8')

# Fix 5: Check sidebar corrupted chars
s='sidebar-plan-icon'
i3=t.find(s)
if i3>=0:
    context = t[i3-5:i3+80]
    print('Sidebar plan context found at', i3, repr(context.encode('ascii','backslashreplace').decode())[:200])

# Check all occurrences of '免费' to make sure none are corrupted
i4=0; count=0
while True:
    i4 = t.find('\u514d\u8d39', i4)
    if i4<0: break
    print('Free text OK at', i4)
    i4+=1; count+=1
    if count>5: break
if count==0:
    print('NO valid free text found!')
    # Check for different encoding
    for i in range(len(t)-4):
        if ord(t[i])>127 and ord(t[i+1])>127:
            print('Non-ASCII at', i, repr(t[i:i+6].encode('ascii','backslashreplace').decode()))
            break
