import re
f=open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','rb')
c=f.read()
f.close()
t=c.decode('utf-8')
scripts=[];idx=0
while True:
    si=t.find('<script',idx)
    if si<0:break
    sj=t.find('>',si)
    ei=t.find('</script>',sj)
    if ei<0:break
    c=t[sj+1:ei]
    if c.strip():scripts.append(c)
    idx=ei+9
all_js='\n'.join(scripts)
lines=all_js.split('\n')
# Line 4 is the 4th script start, check first few lines of each script
ln=0
for s_i,s in enumerate(scripts):
    s_lines=s.split('\n')
    print(f'Script {s_i+1}: {len(s_lines)} lines, starts with: {s_lines[0][:60]!r}')
    for i,l in enumerate(s_lines):
        if '\uff0c' in l:
            print(f'  FULLWIDTH COMMA at script {s_i+1} line {i}: {l[:80]!r}')
