"""Fix delete button conditional render - construct via JS instead of inline HTML"""
import subprocess

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# The issue: conditional delete button has onclick= with single quotes inside single-quoted string

# Better approach: always render a placeholder, then JS fills it
# Look for the current delete button line and replace with a simpler approach

old_del_btn = "'+(!defaultIds||defaultIds.indexOf(ch.id)<0?'<button onclick=\"deleteChannel()\" style=\"width:100%;padding:12px;border:1px solid var(--red,#e74c3c);border-radius:10px;background:transparent;color:var(--red,#e74c3c);font-size:14px;cursor:pointer\">\xf0\x9f\x97\x91\xef\xb8\x8f \xe5\x88\xa0\xe9\x99\xa4\xe9\xa2\x91\xe9\x81\x93</button>':'<div style=\"text-align:center;padding:8px;font-size:11px;color:var(--muted,#888);border-top:1px solid var(--border,#2a3a5e);margin-top:8px\">\xe9\xbb\x98\xe8\xae\xa4\xe9\xa2\x91\xe9\x81\x93\xe4\xb8\x8d\xe5\x8f\xaf\xe5\x88\xa0\xe9\x99\xa4</div>')+'"

new_del_btn = "'+ch.id+'</div>';"  # close the string + give a marker ID

if old_del_btn in t:
    t = t.replace(old_del_btn, new_del_btn)
    print('1. Replaced conditonal delete button with marker')
else:
    print('1. Pattern not found')
    # Try simpler search
    idx = t.find('!defaultIds||defaultIds.indexOf(ch.id)<0')
    if idx > 0:
        print(f'Found at {idx}: {t[idx:idx+80]}')
    else:
        idx = t.find('默认频道不可删除')
        if idx > 0:
            print(f'Found default msg at {idx}: {t[idx-100:idx+50]}')

# Now add the JS logic at end of showChannelSettings (before toast)
# Look for the last + that closes the innerHTML
old_settings_end = """  document.body.appendChild(m);
  setTimeout(function(){document.getElementById('ch-set-av-preview').focus();},100);
}"""

new_settings_end = """  document.body.appendChild(m);
  // Add delete button (or default notice) programmatically
  var delArea=m.querySelector('[data-delete-area]');
  if(delArea){
    if(defaultIds.indexOf(ch.id)>=0){
      delArea.innerHTML='<div style=\"text-align:center;padding:8px;font-size:11px;color:var(--muted,#666);border-top:1px solid var(--border,#2a3a5e);margin-top:8px\">默认频道不可删除</div>';
    }else{
      var btn=document.createElement('button');
      btn.textContent='\ud83d\uddd1\ufe0f \u5220\u9664\u9891\u9053';
      btn.style.cssText='width:100%;padding:12px;border:1px solid #e74c3c;border-radius:10px;background:transparent;color:#e74c3c;font-size:14px;cursor:pointer;display:block;margin-top:8px';
      btn.onclick=function(){
        if(!confirm('\u786e\u5b9a\u8981\u5220\u9664\u9891\u9053\u300c#'+ch.name+'\u300d\uff1f')) return;
        _sqChannels=_sqChannels.filter(function(c){return c.id!==ch.id;});
        delete _sqMessages[ch.id];
        saveSQ();
        document.getElementById('ch-settings-modal').remove();
        if(_sqChannels.length>0) switchChannel(_sqChannels[0].id);
        else renderChannelList();
        toast('\ud83d\uddd1\ufe0f \u9891\u9053\u5df2\u5220\u9664','info');
      };
      delArea.appendChild(btn);
    }
  }
  setTimeout(function(){document.getElementById('ch-set-av-preview').focus();},100);
}"""

# The settings end should have the original close, not our modified one
# Let me check what the current end looks like
idx = t.find('document.getElementById(\'ch-set-av-preview\').focus();},100);')
if idx > 0:
    print(f'Settings end found at {idx}')
    # Find the closing }
    rest = t[idx:]
    bracket = rest.find('}')
    # Check next 200 chars
    print(f'End context: {rest[:300]}')

# Actually let me find where the settings modal innerHTML string ends
# The original had '+  '</div>'; at the end
old_html_close = "  '</div>';\n  document.body.appendChild(m);"
new_html_close = "  '</div><div id=\"delete-area-wrapper\" data-delete-area></div>';\n  document.body.appendChild(m);"

if old_html_close in t:
    t = t.replace(old_html_close, new_html_close)
    print('2. Added delete-area wrapper')
else:
    print('2. old_html_close not found')
    idx = t.find('</div>\';\n  document.body.appendChild(m);')
    if idx > 0:
        context = t[idx-5:idx+60]
        print(f'Close context: {repr(context)}')
        # The previous modification might have changed it
        # Check if our '+ch.id+'</div>'; is there
        idx2 = t.find('+ch.id+')
        if idx2 > 0:
            print(f'+ch.id+ found at {idx2}: {t[idx2-30:idx2+60]}')

r = t.encode('utf-8', errors='replace')
with open(filepath, 'wb') as f:
    f.write(r)
print(f'Saved: {len(r)} bytes')

# Check syntax
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c)
res = subprocess.run(['node','--check','/tmp/sc.js'],capture_output=True,timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    with open('/tmp/node_err.txt', 'wb') as f:
        f.write(res.stderr)
    print(f'Error stderr size: {len(res.stderr)}')
else:
    print('Syntax OK!')
