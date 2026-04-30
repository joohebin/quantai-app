# -*- coding: utf-8 -*-
"""
Problem: Script 5 (CS Widget) is NEVER executed.
Evidence: toggleCS, csGreet, csAddMsg all undefined despite being in the script.
Solution: Move toggleCS and the CS open/close logic into Script 4 (diagnostic/init script)
which IS executed. Keep the CS Widget HTML intact.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find script 4 (diagnostic script)
s4_start = t.find('// 快速诊断：检查函数可用性')
print(f's4 at: {s4_start}')

if s4_start > 0:
    # Find the end of script 4
    s4_close = t.find('</script>', s4_start)
    print(f's4 ends at: {s4_close}')
    
    # Add toggleCS function right at the start of script 4
    # But we also need _csOpen variable and panel handling
    toggle_stub = '''
  // ---- 客服按钮逻辑（必放在此script以确保可用） ----
  var _csOpen = false;
  window.toggleCS = function toggleCS(){
    console.log('[客服] 点击了客服按钮, 当前状态:', _csOpen);
    try{
      _csOpen = !_csOpen;
      var panel = document.getElementById('cs-panel');
      if(!panel){console.log('[客服] cs-panel not found'); return;}
      if(_csOpen){
        panel.classList.add('open');
        var fab = document.getElementById('cs-fab');
        if(fab) fab.innerHTML = '\\u2715<span class="cs-badge" id="cs-badge" style="display:none"></span>';
        var badge = document.getElementById('cs-badge');
        if(badge) badge.style.display = 'none';
        setTimeout(function(){var inp=document.getElementById("cs-input"); if(inp)inp.focus();}, 300);
      } else {
        panel.classList.remove('open');
        var fab = document.getElementById('cs-fab');
        if(fab) fab.innerHTML = '\\uD83D\\uDCAC<span class="cs-badge" id="cs-badge" style="display:none"></span>';
      }
    }catch(e){console.log("[客服] toggleCS error:", e);}
  };
'''
    
    # Check if we already added it
    if 'window.toggleCS' in t[s4_start:s4_close]:
        print('toggleCS stub already in script 4')
    else:
        # Insert after the first line of script 4
        first_newline = t.find('\n', s4_start) + 1
        t = t[:first_newline] + toggle_stub + t[first_newline:]
        print('Added toggleCS stub to script 4')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')
print(f'\nwindow.toggleCS: {data.count(b"window.toggleCS")}')
print(f'toggleCS stubs: {text.count("_csOpen = false")}')
print(f'File: {len(data)/1024:.1f} KB')

# Also double check: remove the redundant CS sidebar event listener
# (the addEventListener we added earlier could conflict)
