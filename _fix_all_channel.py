# -*- coding: utf-8 -*-
"""
Fixes all issues in one shot:
1. Create modal: add close button + background-click-close
2. Avatar upload (file input -> data URL)
3. Add YT video URL input on create + settings
4. Channel list shows avatar images
5. loadYT fixed to use extractYtId
6. Default YT video changed to working ID
"""
import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# 1. Replace showCreateChannelModal
old_create_modal = """function showCreateChannelModal(){
  var existing=document.getElementById('create-ch-modal');
  if(existing) existing.remove();
  var m=document.createElement('div');
  m.id='create-ch-modal';
  m.style.cssText='position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center';
  m.innerHTML='<div style="background:var(--card-bg,#1a1a2e);border:1px solid var(--border,#2a3a5e);border-radius:16px;padding:24px;width:380px;max-width:90vw;box-shadow:0 20px 60px rgba(0,0,0,.5)">'+
    '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">'+
      '<span style="font-size:18px;font-weight:700;color:var(--text,#e0e0e0)"># 创建频道</span>'+
      '<button onclick="this.parentElement.remove()  // close modal" style="background:none;border:none;color:var(--muted,#888);font-size:20px;cursor:pointer">✕</button>'+
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
}"""

new_create_modal = """function showCreateChannelModal(){
  var existing=document.getElementById('create-ch-modal');
  if(existing) existing.remove();
  var m=document.createElement('div');
  m.id='create-ch-modal';
  m.style.cssText='position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center';
  m.onclick=function(e){if(e.target===this)this.remove();};
  m.innerHTML='<div style="background:var(--card-bg,#1a1a2e);border:1px solid var(--border,#2a3a5e);border-radius:16px;padding:24px;width:400px;max-width:90vw;box-shadow:0 20px 60px rgba(0,0,0,.5)">'+
    '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">'+
      '<span style="font-size:18px;font-weight:700;color:var(--text,#e0e0e0)"># 创建频道</span>'+
      '<button onclick="document.getElementById(\'create-ch-modal\').remove()" style="background:none;border:none;color:var(--muted,#888);font-size:20px;cursor:pointer;padding:4px 8px;border-radius:6px">✕</button>'+
    '</div>'+
    '<div style="margin-bottom:14px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">频道名称</label>'+
      '<input id="ch-name-input" type="text" placeholder="例如: BTC策略讨论" maxlength="20" style="width:100%;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#151528);color:var(--text,#e0e0e0);font-size:14px;outline:none" onkeydown="if(event.key===\\'Enter\\') createChannelSubmit()">'+
    '</div>'+
    '<div style="margin-bottom:14px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">频道头像 <span style="color:var(--muted,#666);font-size:10px">(可选，上传图片)</span></label>'+
      '<div style="display:flex;align-items:center;gap:10px">'+
        '<div id="ch-avatar-preview" style="width:44px;height:44px;border-radius:50%;background:var(--input-bg,#151528);border:2px solid var(--border,#2a3a5e);display:flex;align-items:center;justify-content:center;font-size:18px;overflow:hidden;flex-shrink:0">💬</div>'+
        '<input type="file" accept="image/*" onchange="previewChannelAvatar(this)" style="font-size:12px;color:var(--text,#e0e0e0);cursor:pointer;flex:1">'+
      '</div>'+
      '<input id="ch-icon-input" type="hidden" value="💬">'+
    '</div>'+
    '<div style="margin-bottom:14px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">描述</label>'+
      '<input id="ch-desc-input" type="text" placeholder="频道简短描述" maxlength="50" style="width:100%;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#151528);color:var(--text,#e0e0e0);font-size:14px;outline:none">'+
    '</div>'+
    '<div style="margin-bottom:20px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">直播房间 <span style="color:var(--muted,#666);font-size:10px">(可选，输入 YouTube 链接或视频ID)</span></label>'+
      '<input id="ch-yt-input" type="text" placeholder="例如: dQw4w9WgXcQ 或 https://youtu.be/..." style="width:100%;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#151528);color:var(--text,#e0e0e0);font-size:13px;outline:none">'+
    '</div>'+
    '<button onclick="createChannelSubmit()" style="width:100%;padding:12px;border:none;border-radius:10px;background:var(--accent,#00c896);color:#fff;font-size:15px;font-weight:600;cursor:pointer">创建频道</button>'+
  '</div>';
  document.body.appendChild(m);
  setTimeout(function(){document.getElementById('ch-name-input').focus();},100);
}
function previewChannelAvatar(input){
  var preview=document.getElementById('ch-avatar-preview');
  if(!preview) return;
  if(input.files&&input.files[0]){
    var reader=new FileReader();
    reader.onload=function(e){
      preview.innerHTML='<img src="'+e.target.result+'" style="width:44px;height:44px;border-radius:50%;object-fit:cover">';
      document.getElementById('ch-icon-input').value=e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  } else {
    preview.textContent='💬';
    document.getElementById('ch-icon-input').value='💬';
  }
}"""

if old_create_modal in t:
    t = t.replace(old_create_modal, new_create_modal)
    print('1. Replaced create modal with avatar upload + close btn')
else:
    print('1. WARN: old create modal not found')

# 2. Replace createChannelSubmit
old_create_submit = """function createChannelSubmit(){
  var name=document.getElementById('ch-name-input').value.trim();
  if(!name){toast('请输入频道名称','warn');return;}
  var icon=document.getElementById('ch-icon-input').value.trim()||'💬';
  var desc=document.getElementById('ch-desc-input').value.trim()||'';
  var id='ch-'+name.toLowerCase().replace(/\s+/g,'-').replace(/[^a-z0-9\-]/g,'');
  if(_sqChannels.find(function(c){return c.id===id;})){toast('频道已存在','warn');return;}
  _sqChannels.push({id:id,name:name,desc:desc,icon:icon,widgetTV:'BTCUSDT',widgetYT:''});
  _sqMessages[id]=[];
  saveSQ();renderChannelList();switchChannel(id);
  var m=document.getElementById('create-ch-modal');
  if(m)m.remove();
  toast('✅ #'+name+' 已创建','success');
}"""

new_create_submit = """function createChannelSubmit(){
  var name=document.getElementById('ch-name-input').value.trim();
  if(!name){toast('请输入频道名称','warn');return;}
  var icon=document.getElementById('ch-icon-input').value.trim()||'💬';
  var desc=document.getElementById('ch-desc-input').value.trim()||'';
  var ytInput=document.getElementById('ch-yt-input').value.trim();
  var ytId='';
  if(ytInput){
    ytId=extractYtId(ytInput);
    if(!ytId){toast('YouTube 链接无效','warn');document.getElementById('ch-yt-input').focus();return;}
  }
  var id='ch-'+name.toLowerCase().replace(/\s+/g,'-').replace(/[^a-z0-9\-]/g,'');
  if(_sqChannels.find(function(c){return c.id===id;})){toast('频道已存在','warn');return;}
  _sqChannels.push({id:id,name:name,desc:desc,icon:icon,widgetTV:'BTCUSDT',widgetYT:ytId});
  _sqMessages[id]=[];
  saveSQ();renderChannelList();switchChannel(id);
  var m=document.getElementById('create-ch-modal');
  if(m)m.remove();
  toast('✅ #'+name+' 已创建','success');
}
function extractYtId(input){
  var id=input.trim();
  if(!id) return '';
  if(/^[a-zA-Z0-9_-]{11}$/.test(id)) return id;
  var m=id.match(/(?:youtube\\.com\\/(?:watch\\?v=|embed\\/|v\\/)|youtu\\.be\\/)([a-zA-Z0-9_-]{11})/);
  if(m) return m[1];
  return '';
}"""

if old_create_submit in t:
    t = t.replace(old_create_submit, new_create_submit)
    print('2. Replaced createChannelSubmit with YT support')
else:
    print('2. WARN: old createChannelSubmit not found')

# 3. Replace renderChannelList with avatar support
old_render = """function renderChannelList(){
  var el = document.getElementById('channel-list');
  if(!el) return;
  if(!_sqChannels) return;
  el.innerHTML = _sqChannels.map(function(ch){
    var active = _sqCurrentChannel && _sqCurrentChannel.id === ch.id;
    return '<div class="ch-item'+(active?' active':'')+'" onclick="switchChannel(\\''+ch.id+'\\')">'+
      '<span>'+ch.icon+'</span><span># '+ch.name+'</span>'+
      '<span style="margin-left:auto;font-size:11px;color:var(--muted)">'+((_sqMessages[ch.id]||[]).length)+'</span>'+
    '<\\/div>';
  }).join('');
}"""

new_render = """function renderChannelList(){
  var el = document.getElementById('channel-list');
  if(!el) return;
  if(!_sqChannels) return;
  el.innerHTML = _sqChannels.map(function(ch){
    var active = _sqCurrentChannel && _sqCurrentChannel.id === ch.id;
    var av = ch.icon && ch.icon.indexOf('data:')===0 ? '<img src="'+ch.icon+'" style="width:20px;height:20px;border-radius:50%;object-fit:cover;vertical-align:middle">' : '<span>'+ch.icon+'</span>';
    return '<div class="ch-item'+(active?' active':'')+'" onclick="switchChannel(\\''+ch.id+'\\')">'+
      av+
      '<span># '+ch.name+'</span>'+
      '<span style="margin-left:auto;font-size:11px;color:var(--muted)">'+((_sqMessages[ch.id]||[]).length)+'</span>'+
    '<\\/div>';
  }).join('');
}"""

if old_render in t:
    t = t.replace(old_render, new_render)
    print('3. Replaced renderChannelList with avatar support')
else:
    print('3. WARN: old renderChannelList not found')

# 4. Replace showChannelSettings modal
old_settings = """function showChannelSettings(){
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
}"""

new_settings = """function showChannelSettings(){
  var ch=_sqCurrentChannel;
  if(!ch) return;
  var existing=document.getElementById('ch-settings-modal');
  if(existing) existing.remove();
  var isImg = ch.icon && ch.icon.indexOf('data:')===0;
  var avHtml = isImg ? '<img src="'+ch.icon+'" style="width:44px;height:44px;border-radius:50%;object-fit:cover">' : '<span style="font-size:22px">'+ch.icon+'</span>';
  var m=document.createElement('div');
  m.id='ch-settings-modal';
  m.style.cssText='position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center';
  m.onclick=function(e){if(e.target===this)this.remove();};
  m.innerHTML='<div style="background:var(--card-bg,#1a1a2e);border:1px solid var(--border,#2a3a5e);border-radius:16px;padding:24px;width:400px;max-width:90vw;box-shadow:0 20px 60px rgba(0,0,0,.5)">'+
    '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">'+
      '<span style="font-size:18px;font-weight:700;color:var(--text,#e0e0e0)">⚙️ 频道设置</span>'+
      '<button onclick="document.getElementById(\'ch-settings-modal\').remove()" style="background:none;border:none;color:var(--muted,#888);font-size:20px;cursor:pointer;padding:4px 8px;border-radius:6px">✕</button>'+
    '</div>'+
    '<div style="margin-bottom:14px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">频道头像 <span style="color:var(--muted,#666);font-size:10px">(上传图片替换当前图标)</span></label>'+
      '<div style="display:flex;align-items:center;gap:10px">'+
        '<div id="ch-set-av-preview" style="width:44px;height:44px;border-radius:50%;background:var(--input-bg,#151528);border:2px solid var(--border,#2a3a5e);display:flex;align-items:center;justify-content:center;overflow:hidden;flex-shrink:0">'+avHtml+'</div>'+
        '<input type="file" accept="image/*" onchange="previewSetAvatar(this)" style="font-size:12px;color:var(--text,#e0e0e0);cursor:pointer;flex:1">'+
      '</div>'+
      '<input id="ch-set-icon" type="hidden" value="'+ch.icon+'">'+
    '</div>'+
    '<div style="margin-bottom:14px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">频道名称</label>'+
      '<input id="ch-set-name" type="text" maxlength="20" value="'+ch.name+'" style="width:100%;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#151528);color:var(--text,#e0e0e0);font-size:14px;outline:none">'+
    '</div>'+
    '<div style="margin-bottom:14px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">描述</label>'+
      '<input id="ch-set-desc" type="text" maxlength="50" value="'+(ch.desc||'')+'" style="width:100%;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#151528);color:var(--text,#e0e0e0);font-size:14px;outline:none">'+
    '</div>'+
    '<div style="margin-bottom:20px">'+
      '<label style="font-size:12px;color:var(--muted,#888);display:block;margin-bottom:6px">直播房间 <span style="color:var(--muted,#666);font-size:10px">(输入 YouTube 链接或视频ID)</span></label>'+
      '<input id="ch-set-yt" type="text" placeholder="例如: dQw4w9WgXcQ" value="'+(ch.widgetYT||'')+'" style="width:100%;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#151528);color:var(--text,#e0e0e0);font-size:13px;outline:none">'+
    '</div>'+
    '<button onclick="saveChannelSettings()" style="width:100%;padding:12px;border:none;border-radius:10px;background:var(--accent,#00c896);color:#fff;font-size:15px;font-weight:600;cursor:pointer;margin-bottom:8px">保存设置</button>'+
    '<button onclick="deleteChannel()" style="width:100%;padding:12px;border:1px solid var(--red,#e74c3c);border-radius:10px;background:transparent;color:var(--red,#e74c3c);font-size:14px;cursor:pointer">🗑️ 删除频道</button>'+
  '</div>';
  document.body.appendChild(m);
  setTimeout(function(){document.getElementById('ch-set-av-preview').focus();},100);
}
function previewSetAvatar(input){
  var preview=document.getElementById('ch-set-av-preview');
  if(!preview) return;
  if(input.files&&input.files[0]){
    var reader=new FileReader();
    reader.onload=function(e){
      preview.innerHTML='<img src="'+e.target.result+'" style="width:44px;height:44px;border-radius:50%;object-fit:cover">';
      document.getElementById('ch-set-icon').value=e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  }
}"""

if old_settings in t:
    t = t.replace(old_settings, new_settings)
    print('4. Replaced settings modal with avatar/YT/close')
else:
    print('4. WARN: old settings modal not found')

# 5. Replace saveChannelSettings to save YT ID
old_save = """function saveChannelSettings(){
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
}"""

new_save = """function saveChannelSettings(){
  var icon=document.getElementById('ch-set-icon').value.trim()||'💬';
  var name=document.getElementById('ch-set-name').value.trim();
  if(!name){toast('频道名称不能为空','warn');return;}
  var desc=document.getElementById('ch-set-desc').value.trim()||'';
  var ytId='';
  var ytInput=document.getElementById('ch-set-yt').value.trim();
  if(ytInput){
    ytId=extractYtId(ytInput);
    if(!ytId){toast('YouTube 链接无效','warn');return;}
  }
  var ch=_sqCurrentChannel;
  if(!ch) return;
  ch.icon=icon; ch.name=name; ch.desc=desc; ch.widgetYT=ytId;
  saveSQ(); renderChannelList();
  document.getElementById('channel-name-display').textContent='# '+name;
  document.getElementById('channel-desc-display').textContent=desc;
  // Update avatar
  var av=document.getElementById('channel-av-display');
  if(av){
    if(icon.indexOf('data:')===0) av.innerHTML='<img src="'+icon+'" style="width:22px;height:22px;border-radius:50%;object-fit:cover">';
    else av.textContent=icon;
  }
  var m=document.getElementById('ch-settings-modal');
  if(m) m.remove();
  if(_ytVisible&&ytId) loadYT(ytId);
  toast('✅ 设置已保存','success');
}"""

if old_save in t:
    t = t.replace(old_save, new_save)
    print('5. Replaced saveChannelSettings with YT support')
else:
    print('5. WARN: old saveChannelSettings not found')

# 6. Replace loadYT
old_loadyt = """function loadYT(vid){
  var c=document.getElementById('yt-player');
  if(!c) return;
  var id=vid||'jfKfPfyJRdk';
  var m=id.match(/(?:youtube\\.com\\/(?:watch\\?v=|embed\\/|v\\/)|youtu\\.be\\/)([a-zA-Z0-9_-]{11})/);
  if(m) id=m[1];
  c.innerHTML='<iframe width="100%" height="100%" src="https://www.youtube.com/embed/'+id+'?autoplay=0&rel=0&modestbranding=1&showinfo=0&iv_load_policy=3" frameborder="0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen style="border-radius:12px"></iframe>';
}"""

new_loadyt = """function loadYT(vid){
  var c=document.getElementById('yt-player');
  if(!c) return;
  var id=vid||'dQw4w9WgXcQ';
  id=extractYtId(id)||id;
  if(!id||id.length!==11){
    c.innerHTML='<div style="padding:40px;text-align:center;color:var(--muted)"><div style="font-size:40px;margin-bottom:12px">🎥</div>未配置直播房间<br><span style="font-size:12px">在频道设置中输入 YouTube 视频 ID</span></div>';
    return;
  }
  c.innerHTML='<iframe width="100%" height="100%" src="https://www.youtube.com/embed/'+id+'?autoplay=0&rel=0&modestbranding=1&showinfo=0&iv_load_policy=3" frameborder="0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen style="border-radius:12px"></iframe>';
}"""

if old_loadyt in t:
    t = t.replace(old_loadyt, new_loadyt)
    print('6. Replaced loadYT')
else:
    print('6. WARN: old loadYT not found')

# 7. Update channel header to show avatar
old_header = """<div><span id="channel-name-display" style="font-weight:700;font-size:15px"># 全局</span><span id="channel-desc-display" style="font-size:11px;color:var(--muted);margin-left:8px">闲聊</span></div>"""
new_header = """<div style="display:flex;align-items:center;gap:8px"><span id="channel-av-display" style="font-size:18px">🌐</span><div><span id="channel-name-display" style="font-weight:700;font-size:15px"># 全局</span><span id="channel-desc-display" style="font-size:11px;color:var(--muted);margin-left:8px">闲聊</span></div></div>"""
if old_header in t:
    t = t.replace(old_header, new_header)
    print('7. Updated channel header with avatar span')
else:
    print('7. WARN: old channel header not found')

# 8. Update switchChannel to set avatar
old_switch_r = "renderChannelList();\n  renderMessages();"
new_switch_r = """renderChannelList();
  renderMessages();
  var av=document.getElementById('channel-av-display');
  if(av){
    if(ch.icon&&ch.icon.indexOf('data:')===0) av.innerHTML='<img src=\"'+ch.icon+'\" style=\"width:22px;height:22px;border-radius:50%;object-fit:cover\">';
    else av.textContent=ch.icon;
  }"""

t = t.replace(old_switch_r, new_switch_r)
print('8. Updated switchChannel with avatar update')

# 9. Update default YT video
t = t.replace("widgetYT:'jfKfPfyJRdk'", "widgetYT:'dQw4w9WgXcQ'")
print('9. Updated default YT video to dQw4w9WgXcQ')

r = t.encode('utf-8', errors='replace')
with open(filepath, 'wb') as f:
    f.write(r)
print(f'\nSaved: {len(r)} bytes')

# Validate syntax
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
        fname = '/tmp/s_final.js'
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
