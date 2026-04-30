import subprocess

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Replace deleteChannel to use custom confirm instead of native confirm()
old_delete = """function deleteChannel(){
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

new_delete = """function deleteChannel(){
  var ch=_sqCurrentChannel;
  if(!ch) return;
  // Don't allow deleting default channels
  var defaultIds=['ch-general','ch-btc','ch-eth','ch-strategy','ch-livestream','ch-backtest'];
  if(defaultIds.indexOf(ch.id)>=0){toast('不能删除默认频道','warn');return;}
  // Show custom confirm modal
  var existing=document.getElementById('del-ch-modal');
  if(existing) existing.remove();
  var m=document.createElement('div');
  m.id='del-ch-modal';
  m.style.cssText='position:fixed;inset:0;z-index:10000;display:flex;align-items:center;justify-content:center';
  m.innerHTML='<div style="background:var(--card-bg,#1a1a2e);border:1px solid var(--border,#2a3a5e);border-radius:16px;padding:24px;width:360px;box-shadow:0 20px 60px rgba(0,0,0,.5)">'+
    '<div style="font-size:18px;font-weight:700;margin-bottom:8px;color:var(--red,#e74c3c)">⚠️ 删除频道</div>'+
    '<div style="font-size:14px;color:var(--text,#e0e0e0);margin-bottom:20px">确定要删除频道「#'+ch.name+'」？<br><span style="color:var(--muted,#888);font-size:12px">频道下的所有消息将被永久删除</span></div>'+
    '<div style="display:flex;gap:10px">'+
      '<button onclick="document.getElementById(\'del-ch-modal\').remove()" style="flex:1;padding:12px;border:1px solid var(--border,#2a3a5e);border-radius:10px;background:transparent;color:var(--text,#e0e0e0);font-size:14px;cursor:pointer">取消</button>'+
      '<button onclick="confirmDeleteChannel()" style="flex:1;padding:12px;border:none;border-radius:10px;background:var(--red,#e74c3c);color:#fff;font-size:14px;font-weight:600;cursor:pointer">确认删除</button>'+
    '</div>'+
  '</div>';
  document.body.appendChild(m);
}
function confirmDeleteChannel(){
  _sqChannels=_sqChannels.filter(function(c){return c.id!==_sqCurrentChannel.id;});
  delete _sqMessages[_sqCurrentChannel.id];
  saveSQ();
  var m=document.getElementById('ch-settings-modal');
  if(m) m.remove();
  var dm=document.getElementById('del-ch-modal');
  if(dm) dm.remove();
  if(_sqChannels.length>0) switchChannel(_sqChannels[0].id);
  else renderChannelList();
  toast('🗑️ 频道已删除','info');
}"""

if old_delete in t:
    t = t.replace(old_delete, new_delete)
    print('1. Replaced deleteChannel with custom modal')
else:
    print('1. Old deleteChannel not found')
    # Try to find it
    idx = t.find('function deleteChannel')
    if idx > 0:
        print(f'Found at {idx}, first 80 chars: {t[idx:idx+80]}')

r = t.encode('utf-8', errors='replace')
with open(filepath, 'wb') as f:
    f.write(r)
print(f'Saved: {len(r)} bytes')

# Syntax check
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c)
res = subprocess.run(['node', '--check', '/tmp/sc.js'], capture_output=True, timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    out = res.stderr.decode('utf-8', errors='replace')
    for line in out.split('\n'):
        if 'SyntaxError' in line or 'Unexpected' in line:
            print(line[:150])
else:
    print('Syntax OK!')
