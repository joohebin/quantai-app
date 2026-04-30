# -*- coding: utf-8 -*-
"""Fix: replace prompt() with inline modal for createChannel"""
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

t = r.decode('utf-8', errors='replace')

# Replace createChannel function to use a better UI
old_create = """function createChannel(){
  var name = prompt('输入频道名称:');
  if(!name||!name.trim()) return;
  var icon = prompt('输入图标 (如 🌐, 📊):') || '💬';
  var desc = prompt('输入描述:') || '';
  var id = 'ch-'+name.toLowerCase().replace(/\\s+/g,'-').replace(/[^a-z0-9\\-]/g,'');
  if(_sqChannels.find(function(c){ return c.id===id; })){ toast('频道已存在','warn'); return; }
  _sqChannels.push({id:id, name:name.trim(), desc:desc, icon:icon, widgetTV:'BTCUSDT', widgetYT:''});
  _sqMessages[id]=[];
  saveSQ(); renderChannelList(); switchChannel(id);
  toast('✅ #'+name.trim()+' 已创建', 'success');
}
"""

new_create = """function createChannel(){
  showCreateChannelModal();
}
function showCreateChannelModal(){
  var existing=document.getElementById('create-ch-modal');
  if(existing) existing.remove();
  var m=document.createElement('div');
  m.id='create-ch-modal';
  m.style.cssText='position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center';
  m.innerHTML='<div style="background:var(--card-bg,#1a1a2e);border:1px solid var(--border,#2a3a5e);border-radius:16px;padding:24px;width:380px;max-width:90vw;box-shadow:0 20px 60px rgba(0,0,0,.5)">'+
    '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">'+
      '<span style="font-size:18px;font-weight:700;color:var(--text,#e0e0e0)"># 创建频道</span>'+
      '<button onclick="this.closest(\'#create-ch-modal\').remove()" style="background:none;border:none;color:var(--muted,#888);font-size:20px;cursor:pointer">✕</button>'+
    '</div>'+
    '<div style="margin-bottom:14px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">频道名称</label>'+
      '<input id="ch-name-input" type="text" placeholder="例如: BTC策略讨论" maxlength="20" style="width:100%;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#151528);color:var(--text,#e0e0e0);font-size:14px;outline:none" onkeydown="if(event.key===\\'Enter\\') createChannelSubmit()">'+
    '</div>'+
    '<div style="margin-bottom:14px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">图标</label>'+
      '<input id="ch-icon-input" type="text" placeholder="🌐" maxlength="2" value="💬" style="width:60px;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#151528);color:var(--text,#e0e0e0);font-size:16px;text-align:center;outline:none">'+
    '</div>'+
    '<div style="margin-bottom:20px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">描述</label>'+
      '<input id="ch-desc-input" type="text" placeholder="频道简短描述" maxlength="50" style="width:100%;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#151528);color:var(--text,#e0e0e0);font-size:14px;outline:none">'+
    '</div>'+
    '<button onclick="createChannelSubmit()" style="width:100%;padding:12px;border:none;border-radius:10px;background:var(--accent,#00c896);color:#fff;font-size:15px;font-weight:600;cursor:pointer">创建频道</button>'+
  '</div>';
  document.body.appendChild(m);
  setTimeout(function(){document.getElementById('ch-name-input').focus();},100);
}
function createChannelSubmit(){
  var name=document.getElementById('ch-name-input').value.trim();
  if(!name){toast('请输入频道名称','warn');return;}
  var icon=document.getElementById('ch-icon-input').value.trim()||'💬';
  var desc=document.getElementById('ch-desc-input').value.trim()||'';
  var id='ch-'+name.toLowerCase().replace(/\\s+/g,'-').replace(/[^a-z0-9\\-]/g,'');
  if(_sqChannels.find(function(c){return c.id===id;})){toast('频道已存在','warn');return;}
  _sqChannels.push({id:id,name:name,desc:desc,icon:icon,widgetTV:'BTCUSDT',widgetYT:''});
  _sqMessages[id]=[];
  saveSQ();renderChannelList();switchChannel(id);
  var m=document.getElementById('create-ch-modal');
  if(m)m.remove();
  toast('✅ #'+name+' 已创建','success');
}
"""

t = t.replace(old_create, new_create)
r = t.encode('utf-8', errors='replace')

with open(filepath, 'wb') as f:
    f.write(r)
print(f'Saved: {len(r)} bytes')

# Verify syntax
sidx = r.find(b'<script>', 200000)
eidx = r.find(b'</script>', sidx+10)
content = r[sidx:eidx]
with open('/tmp/s4.js', 'wb') as f:
    f.write(content)
import subprocess
result = subprocess.run(['node', '--check', '/tmp/s4.js'], capture_output=True, text=True, timeout=10)
print(f'Node check: {result.returncode}')
if result.returncode != 0:
    print(f'Error: {result.stderr[:300]}')
