# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
# Find the CS Widget section - show the HTML
cs_start = t.find('<!-- ===== 客服 Widget ===== -->')
if cs_start > 0:
    # Show next 3000 chars
    print(t[cs_start:cs_start+6000])
    print(f'\n...total {len(t[cs_start:cs_start+8000])} chars')
else:
    cs_start = t.find('客服 Widget')
    if cs_start > 0:
        print(t[cs_start:cs_start+6000])
    else:
        print('CS Widget section NOT FOUND')
        # Search for the closing script before widget
        p = t.find('});\n</script>')
        if p > 0:
            print(t[p:p+200])
