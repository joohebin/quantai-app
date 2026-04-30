# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find script 4 (the diagnostic script) - add the event listener there
# Script 4 starts after sidebar, has DOMContentLoaded listener
s4 = t.find('// 快速诊断：检查函数可用性')
print(f's4 at: {s4}')

if s4 > 0:
    # Find the closing of the DOMContentLoaded listener
    # The listener does show page hash and checks functions
    # Add our CS sidebar listener there
    add_code = '''
  // 绑定侧边栏客服按钮
  var csBtn = document.getElementById('cs-sidebar-btn');
  if(csBtn) csBtn.addEventListener('click', function(){ toggleCS(); });
'''
    # Insert after the hashcheck function
    insert_pos = t.find("showPage(page, null)", s4)
    if insert_pos > 0:
        line_end = t.find('\n', insert_pos)
        t = t[:line_end+1] + add_code + t[line_end+1:]
        print('Added CS click listener to script 4')
    else:
        # Insert before the function checks
        insert_pos = t.find("const fns =", s4)
        if insert_pos > 0:
            t = t[:insert_pos] + add_code + '\n' + t[insert_pos:]
            print('Added CS click listener before function checks')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))
    
# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')
print(f'cs-sidebar-btn: {text.count("cs-sidebar-btn")}')
print(f'addEventListener: {text.count("addEventListener")} (was 7)')
