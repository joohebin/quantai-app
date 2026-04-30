import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Step 1: Replace deleteChannel with custom modal (no native confirm())
old_del = """function deleteChannel(){
  var ch=_sqCurrentChannel;
  if(!ch) return;
  if(!confirm('确定要删除频道「#'+ch.name+'」？频道下的所有消息将被删除！')) return;
  _sqChannels=_sqChannels.filter(function(c){return c.id!==ch.id;});
  delete _sqMessages[ch.id];
  saveSQ();
  var m=document.getElementById('ch-settings-modal');
  if(m) m.remove();
  // Switch to first available channel
  if(_sqChannels.length>0) switchChannel(_sqChannels[0].id);
  else renderChannelList();
  toast('🗑️ 频道已删除','info');
}"""

new_del = """function deleteChannel(){
  var ch=_sqCurrentChannel;
  if(!ch) return;
  // Don't allow deleting default channels
  var defs=['ch-general','ch-btc','ch-eth','ch-strategy','ch-livestream','ch-backtest'];
  if(defs.indexOf(ch.id)>=0){alert('默认频道不可删除');return;}
  // Show custom confirm modal
  var m=document.createElement('div');
  m.id='del-ch-modal';
  m.style.cssText='position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center';
  m.onclick=function(e){if(e.target===this)this.remove();};
  m.innerHTML='<div style="background:var(--card-bg,#1a1a2e);border:1px solid var(--border,#2a3a5e);border-radius:16px;padding:24px;width:360px;box-shadow:0 20px 60px rgba(0,0,0,.5)">'+
    '<div style="font-size:18px;font-weight:700;margin-bottom:8px;color:var(--red,#e74c3c)">\u26a0\ufe0f 删除频道</div>'+
    '<div style="font-size:14px;color:var(--text,#e0e0e0);margin-bottom:20px">确定要删除频道「#'+ch.name+'」？<br><span style="color:var(--muted,#888);font-size:12px">频道下的所有消息将被永久删除</span></div>'+
    '<div style="display:flex;gap:10px">'+
      '<button onclick="document.body.removeChild(this.closest(\\'#del-ch-modal\\'))" style="flex:1;padding:12px;border:1px solid var(--border,#2a3a5e);border-radius:10px;background:transparent;color:var(--text,#e0e0e0);font-size:14px;cursor:pointer">取消</button>'+
      '<button onclick="confirmDelChannel()" style="flex:1;padding:12px;border:none;border-radius:10px;background:var(--red,#e74c3c);color:#fff;font-size:14px;font-weight:600;cursor:pointer">确认删除</button>'+
    '</div>'+
  '</div>';
  document.body.appendChild(m);
}"""

# Wait, the onclick has # which breaks template literal again
# Let me use a completely different approach: no document.body.removeChild
# Instead, use this.parentElement.parentElement.parentElement.remove()
# button -> div(flex buttons) -> div(content) -> div(overlay) = del-ch-modal

# Actually the simplest: use this.parentElement.parentElement.remove()
# button -> div(button row) -> div(container)

new_del = """function deleteChannel(){
  var ch=_sqCurrentChannel;
  if(!ch) return;
  var defs=['ch-general','ch-btc','ch-eth','ch-strategy','ch-livestream','ch-backtest'];
  if(defs.indexOf(ch.id)>=0){alert('默认频道不可删除');return;}
  var m=document.createElement('div');
  m.id='del-ch-modal';
  m.style.cssText='position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center';
  m.onclick=function(e){if(e.target===this)this.remove();};
  m.innerHTML='<div style="background:var(--card-bg,#1a1a2e);border:1px solid var(--border,#2a3a5e);border-radius:16px;padding:24px;width:360px;box-shadow:0 20px 60px rgba(0,0,0,.5)">'+
    '<div style="font-size:18px;font-weight:700;margin-bottom:8px;color:var(--red,#e74c3c)">\u26a0\ufe0f 删除频道</div>'+
    '<div style="font-size:14px;color:var(--text,#e0e0e0);margin-bottom:20px">确定要删除频道\u300c#'+ch.name+'\u300d？<br><span style="color:var(--muted,#888);font-size:12px">频道下的所有消息将被永久删除</span></div>'+
    '<div style="display:flex;gap:10px">'+
      '<button onclick="document.body.removeChild(this.parentElement.parentElement.parentElement)" style="flex:1;padding:12px;border:1px solid var(--border,#2a3a5e);border-radius:10px;background:transparent;color:var(--text,#e0e0e0);font-size:14px;cursor:pointer">取消</button>'+
      '<button onclick="document.body.removeChild(this.parentElement.parentElement.parentElement);confirmDelChannel()" style="flex:1;padding:12px;border:none;border-radius:10px;background:var(--red,#e74c3c);color:#fff;font-size:14px;font-weight:600;cursor:pointer">确认删除</button>'+
    '</div>'+
  '</div>';
  document.body.appendChild(m);
}
function confirmDelChannel(){
  var ch=_sqCurrentChannel;
  _sqChannels=_sqChannels.filter(function(c){return c.id!==ch.id;});
  delete _sqMessages[ch.id];
  saveSQ();
  var sm=document.getElementById('ch-settings-modal');
  if(sm) sm.remove();
  if(_sqChannels.length>0) switchChannel(_sqChannels[0].id);
  else renderChannelList();
  toast('\ud83d\uddd1\ufe0f 频道已删除','info');
}"""

# Hmm, the document.body.removeChild pattern is also problematic.
# Let me use the SIMPLEST approach: just use this.parentElement.parentElement.remove()

new_del = """function deleteChannel(){
  var ch=_sqCurrentChannel;
  if(!ch) return;
  var defs=['ch-general','ch-btc','ch-eth','ch-strategy','ch-livestream','ch-backtest'];
  if(defs.indexOf(ch.id)>=0){alert('默认频道不可删除');return;}
  var m=document.createElement('div');
  m.id='del-ch-modal';
  m.style.cssText='position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center';
  m.onclick=function(e){if(e.target===this)this.remove();};
  m.innerHTML='<div style="background:var(--card-bg,#1a1a2e);border:1px solid var(--border,#2a3a5e);border-radius:16px;padding:24px;width:360px;box-shadow:0 20px 60px rgba(0,0,0,.5)">'+
    '<div style="font-size:18px;font-weight:700;margin-bottom:8px;color:var(--red,#e74c3c)">\u26a0\ufe0f 删除频道</div>'+
    '<div style="font-size:14px;color:var(--text,#e0e0e0);margin-bottom:20px">确定要删除频道\u300c#'+ch.name+'\u300d？<br><span style="color:var(--muted,#888);font-size:12px">频道下的所有消息将被永久删除</span></div>'+
    '<div style="display:flex;gap:10px">'+
      '<button onclick="this.parentElement.parentElement.remove()" style="flex:1;padding:12px;border:1px solid var(--border,#2a3a5e);border-radius:10px;background:transparent;color:var(--text,#e0e0e0);font-size:14px;cursor:pointer">取消</button>'+
      '<button onclick="this.parentElement.parentElement.remove();setTimeout(function(){confirmDelChannel()},50)" style="flex:1;padding:12px;border:none;border-radius:10px;background:var(--red,#e74c3c);color:#fff;font-size:14px;font-weight:600;cursor:pointer">确认删除</button>'+
    '</div>'+
  '</div>';
  document.body.appendChild(m);
}
function confirmDelChannel(){
  _sqChannels=_sqChannels.filter(function(c){return c.id!==_sqCurrentChannel.id;});
  delete _sqMessages[_sqCurrentChannel.id];
  saveSQ();
  var sm=document.getElementById('ch-settings-modal');
  if(sm) sm.remove();
  if(_sqChannels.length>0) switchChannel(_sqChannels[0].id);
  else renderChannelList();
  toast('\ud83d\uddd1\ufe0f 频道已删除','info');
}"""

if old_del in t:
    t = t.replace(old_del, new_del)
    print('1. Replaced deleteChannel with custom modal + default protection')
else:
    print('1. Old deleteChannel not found')
    idx = t.find('function deleteChannel')
    if idx > 0:
        print(f'Found: {t[idx:idx+80]}')

r = t.encode('utf-8', errors='replace')
with open(filepath, 'wb') as f:
    f.write(r)

# Syntax check
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c)
res = subprocess.run(['node','--check','/tmp/sc.js'], capture_output=True, timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    err_data = res.stderr[:400]
    print(f'Error: {err_data}')
else:
    print('Syntax OK!')
print(f'Saved: {len(r)} bytes')
