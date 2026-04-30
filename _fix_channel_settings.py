# -*- coding: utf-8 -*-
"""
1. Add channel settings button (gear icon) to channel header
2. Add showChannelSettings() modal function
3. Add renderChannelSettings() to update name/icon display
4. Add channel delete function
"""
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# === Step 1: Add gear button to channel header ===
old_header = """<div style="display:flex;gap:6px">
              <button onclick="toggleWidget('tv')" id="tv-widget-btn" style="padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer">📈 图表</button>
              <button onclick="toggleWidget('yt')" id="yt-widget-btn" style="padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer">🎥 直播</button>
            </div>"""

new_header = """<div style="display:flex;gap:6px">
              <button onclick="toggleWidget('tv')" id="tv-widget-btn" style="padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer">📈 图表</button>
              <button onclick="toggleWidget('yt')" id="yt-widget-btn" style="padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer">🎥 直播</button>
              <button onclick="showChannelSettings()" title="频道设置" style="padding:4px 8px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:13px;cursor:pointer">⚙️</button>
            </div>"""

if old_header in t:
    t = t.replace(old_header, new_header)
    print('✅ Added gear button to channel header')
else:
    print('❌ Header HTML not found')
    # Try to find the exact bytes
    idx = t.find('tv-widget-btn')
    print(f'Context: {repr(t[idx-20:idx+350])}')

# === Step 2: Add settings modal + delete channel functions ===
# Insert right before loadTV function
new_functions = """
// ---- Channel Settings ----
function showChannelSettings(){
  var ch=_sqCurrentChannel;
  if(!ch) return;
  var existing=document.getElementById('ch-settings-modal');
  if(existing) existing.remove();
  var m=document.createElement('div');
  m.id='ch-settings-modal';
  m.style.cssText='position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center';
  m.innerHTML='<div style="background:var(--card-bg,#1a1a2e);border:1px solid var(--border,#2a3a5e);border-radius:16px;padding:24px;width:380px;max-width:90vw;box-shadow:0 20px 60px rgba(0,0,0,.5)">'+
    '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">'+
      '<span style="font-size:18px;font-weight:700;color:var(--text,#e0e0e0)">⚙️ 频道设置</span>'+
      '<button onclick="this.parentElement.parentElement.parentElement.remove()" style="background:none;border:none;color:var(--muted,#888);font-size:20px;cursor:pointer">✕</button>'+
    '</div>'+
    '<div style="margin-bottom:14px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">图标</label>'+
      '<input id="ch-set-icon" type="text" maxlength="2" value="'+ch.icon+'" style="width:60px;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#151528);color:var(--text,#e0e0e0);font-size:16px;text-align:center;outline:none">'+
    '</div>'+
    '<div style="margin-bottom:14px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">频道名称</label>'+
      '<input id="ch-set-name" type="text" maxlength="20" value="'+ch.name+'" style="width:100%;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#151528);color:var(--text,#e0e0e0);font-size:14px;outline:none">'+
    '</div>'+
    '<div style="margin-bottom:20px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">描述</label>'+
      '<input id="ch-set-desc" type="text" maxlength="50" value="'+(ch.desc||'')+'" style="width:100%;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#151528);color:var(--text,#e0e0e0);font-size:14px;outline:none">'+
    '</div>'+
    '<button onclick="saveChannelSettings()" style="width:100%;padding:12px;border:none;border-radius:10px;background:var(--accent,#00c896);color:#fff;font-size:15px;font-weight:600;cursor:pointer;margin-bottom:8px">保存设置</button>'+
    '<button onclick="deleteChannel()" style="width:100%;padding:12px;border:1px solid var(--red,#e74c3c);border-radius:10px;background:transparent;color:var(--red,#e74c3c);font-size:14px;cursor:pointer">🗑️ 删除频道</button>'+
  '</div>';
  document.body.appendChild(m);
  setTimeout(function(){document.getElementById('ch-set-icon').focus();},100);
}
function saveChannelSettings(){
  var icon=document.getElementById('ch-set-icon').value.trim()||'💬';
  var name=document.getElementById('ch-set-name').value.trim();
  if(!name){toast('频道名称不能为空','warn');return;}
  var desc=document.getElementById('ch-set-desc').value.trim()||'';
  var ch=_sqCurrentChannel;
  if(!ch) return;
  ch.icon=icon; ch.name=name; ch.desc=desc;
  saveSQ(); renderChannelList();
  document.getElementById('channel-name-display').textContent='# '+name;
  document.getElementById('channel-desc-display').textContent=desc;
  var m=document.getElementById('ch-settings-modal');
  if(m) m.remove();
  toast('✅ 设置已保存','success');
}
function deleteChannel(){
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
}

"""

# Find insertion point - before loadTV function
insert_before = 'function loadTV(symbol)'
idx = t.find(insert_before)
if idx > 0:
    # Find the last of the create channel functions section
    # Insert right before loadTV
    t = t[:idx] + new_functions + t[idx:]
    print(f'✅ Inserted settings functions before loadTV')
else:
    print('❌ loadTV not found, trying alternative insertion point')
    # Find createChannelSubmit closing
    fn_end = t.find("toast('✅ #'+name+' 已创建','success');")
    if fn_end > 0:
        bracket = t.find('}', fn_end) + 1
        t = t[:bracket] + new_functions + t[bracket:]
        print(f'✅ Inserted after createChannelSubmit')

r = t.encode('utf-8', errors='replace')
with open(filepath, 'wb') as f:
    f.write(r)
print(f'Saved: {len(r)} bytes')

# Validate syntax
import subprocess
idx2 = 0
while True:
    sidx = r.find(b'<script', idx2)
    if sidx < 0: break
    if r[sidx:sidx+8] == b'<script>':
        cs = sidx + 8
    else:
        ct = r.find(b'>', sidx)
        cs = ct + 1
    eidx = r.find(b'</script>', cs)
    content = r[cs:eidx]
    if b'initQuantTalk' in content:
        fname = '/tmp/s_check.js'
        with open(fname, 'wb') as f2:
            f2.write(content)
        result = subprocess.run(['node', '--check', fname], capture_output=True, text=True, timeout=10)
        print(f'Node check: {result.returncode}')
        if result.returncode != 0:
            print(f'Error: {result.stderr[:300]}')
        else:
            print(f'Syntax OK!')
        break
    idx2 = eidx + 9
