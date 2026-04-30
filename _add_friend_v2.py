"""
Phase 1: Replace the right panel HTML (观点广场 → Friends/Rank tabs)
Phase 2: Insert friend system JS functions
Phase 3: Update initQuantTalk

Each phase verified by syntax check.
"""
import subprocess

filepath = 'index.html'

# ===== PHASE 1: HTML change =====
print('=== PHASE 1: Right Panel HTML ===')
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

old_right = '<!-- Right: Post Feed -->'
idx = t.find(old_right)
if idx < 0:
    print('ERROR: old right panel not found')
    exit(1)

# Find the wrapping div for the right panel
start = t.rfind('<div', idx - 10, idx)
end = t.find('</div>', t.find('</div>', idx) + 6) + 6  # two levels of div
# Find where the page-square ends (the next page element)
next_page = t.find('<!-- ===', end)
if next_page < 0:
    next_page = t.find('<div class="page" id="page-', end)

new_right = '''        <!-- Right: Friends & Leaderboard -->
        <div style="width:280px;min-width:280px;background:var(--card);border:1px solid var(--border);border-radius:12px;display:flex;flex-direction:column;overflow:hidden">
          <!-- Tabs -->
          <div style="display:flex;border-bottom:1px solid var(--border)">
            <div class="fr-tab active" data-tab="rank" onclick="window.switchFRTab('rank')" style="flex:1;padding:10px 0;text-align:center;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid var(--green);color:var(--green)">🏆 排行榜</div>
            <div class="fr-tab" data-tab="friends" onclick="window.switchFRTab('friends')" style="flex:1;padding:10px 0;text-align:center;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;color:var(--muted)">👥 好友</div>
            <div class="fr-tab" data-tab="requests" onclick="window.switchFRTab('requests')" style="flex:1;padding:10px 0;text-align:center;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;color:var(--muted)">📩 请求</div>
          </div>
          <div id="fr-rank-panel" style="flex:1;overflow-y:auto;padding:8px;display:block"></div>
          <div id="fr-friends-panel" style="flex:1;overflow-y:auto;padding:8px;display:none"></div>
          <div id="fr-requests-panel" style="flex:1;overflow-y:auto;padding:8px;display:none"></div>
        </div>'''

# Find the exact old block
old_block = t[start:end]
print(f'Old block ({len(old_block)} chars): {old_block[:120]}...')
t = t[:start] + new_right + t[end:]
print('HTML replaced OK')

r = t.encode('utf-8', errors='replace')
with open(filepath, 'wb') as f:
    f.write(r)
print(f'Saved phase 1: {len(r)} bytes')

# ===== PHASE 2: Add JS functions =====
print('\n=== PHASE 2: Friend System JS ===')
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Find insertion point: before the TradingView widget section
insert_point = t.find('// ---- TradingView Widget ----')
if insert_point < 0:
    insert_point = t.find('function loadTV(')
    if insert_point < 0:
        print('ERROR: loadTV not found')
        exit(1)

friend_js = r'''
// ---- Friend System ----
function loadFRData(){
  var d=localStorage.getItem("quantalk_friends");
  var _frData=null;
  if(d){try{_frData=JSON.parse(d);}catch(e){}}
  if(!_frData) _frData = {friends:[], requests:[], sent:[], user:{id:"u1",name:"joohebin220",avatar:"\ud83d\udc64",pnl:"+18.5%",winRate:"62%",totalPnl:"+$12,450"}};
  return _frData;
}
function saveFRData(v){localStorage.setItem("quantalk_friends",JSON.stringify(v));}
function switchFRTab(tab){
  var tabs=document.querySelectorAll(".fr-tab");
  for(var i=0;i<tabs.length;i++){tabs[i].style.borderBottomColor="transparent";tabs[i].style.color="var(--muted)";}
  var el=document.querySelector(".fr-tab[data-tab=\""+tab+"\"]");
  if(el){el.style.borderBottomColor="var(--green)";el.style.color="var(--green)";}
  var panels=["fr-rank-panel","fr-friends-panel","fr-requests-panel"];
  for(var i=0;i<panels.length;i++){var p=document.getElementById(panels[i]);if(p)p.style.display="none";}
  var target=document.getElementById("fr-"+tab+"-panel");
  if(target) target.style.display="block";
  if(tab==="rank") renderRank();
  else if(tab==="friends") renderFriends();
  else renderRequests();
}
function renderRank(){
  var el=document.getElementById("fr-rank-panel");
  if(!el) return;
  var data=[
    {rank:1,name:"\u91cf\u5b50\u730e\u624b",pnl:"+$45,620",rate:"+156%",win:"78%",trades:142},
    {rank:2,name:"\u8d8b\u52bf\u6355\u624b",pnl:"+$32,180",rate:"+89%",win:"71%",trades:98},
    {rank:3,name:"joohebin220",pnl:"+$12,450",rate:"+18.5%",win:"62%",trades:56},
    {rank:4,name:"BTC\u4fe1\u5f92",pnl:"+$8,920",rate:"+42%",win:"65%",trades:134},
    {rank:5,name:"\u91cf\u5316\u5973\u795e",pnl:"+$6,350",rate:"+28%",win:"73%",trades:87},
    {rank:6,name:"\u6ce2\u6bb5\u738b",pnl:"+$4,200",rate:"+15%",win:"55%",trades:203},
    {rank:7,name:"\u94fe\u4e0a\u4fa6\u63a2",pnl:"+$3,100",rate:"+22%",win:"68%",trades:45},
    {rank:8,name:"\u5bf9\u51b2\u5927\u5e08",pnl:"+$1,890",rate:"+8%",win:"59%",trades:312}
  ];
  var html="<div>";
  for(var i=0;i<data.length;i++){
    var d=data[i];var isMe=(d.name==="joohebin220");
    var medal="";if(d.rank===1)medal="\ud83e\udd47";else if(d.rank===2)medal="\ud83e\udd48";else if(d.rank===3)medal="\ud83e\udd49";
    html+="<div style=\"display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;margin-bottom:4px"+(isMe?";background:rgba(0,200,150,.1)":"")+"\">"+
      "<span style=\"width:24px;text-align:center;font-weight:"+(d.rank<=3?"800":"400")+";color:"+(d.rank===1?"gold":d.rank===2?"silver":d.rank===3?"#cd7f32":"var(--muted)")+";font-size:"+(d.rank<=3?"18":"13")+"px\">"+(medal?medal:d.rank)+"</span>"+
      "<span style=\"width:28px;height:28px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0\">"+(isMe?"\ud83d\udc64":"\ud83e\uddd1")+"</span>"+
      "<div style=\"flex:1;min-width:0\"><div style=\"font-size:12px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap\">"+d.name+"</div><div style=\"font-size:10px;color:var(--muted)\">"+d.trades+" \u7b14\u4ea4\u6613</div></div>"+
      "<div style=\"text-align:right\"><div style=\"font-size:12px;font-weight:700;color:"+(d.pnl.charAt(0)==="+"?"var(--green)":"var(--red)")+"\">"+d.pnl+"</div><div style=\"font-size:10px;color:"+(d.rate.charAt(0)==="+"?"var(--green)":"var(--red)")+"\">"+d.rate+"</div></div>"+
    "</div>";
  }
  html+="</div>";
  el.innerHTML=html;
}
function renderFriends(){
  var _frData=loadFRData();
  var el=document.getElementById("fr-friends-panel");
  if(!el) return;
  var q=_frData.searchQ||"";
  var list=_frData.friends||[];
  if(q.length>1) list=list.filter(function(f){return f.name.indexOf(q)>=0;});
  var html="<div style=\"display:flex;gap:6px;margin-bottom:8px\"><input id=\"fr-search\" type=\"text\" placeholder=\"\u641c\u7d22\u7528\u6237\u540d...\" value=\""+q+"\" style=\"flex:1;padding:8px 12px;border:1px solid var(--border);border-radius:8px;background:var(--input-bg);color:var(--text);font-size:12px\" onkeyup=\"var d=loadFRData();d.searchQ=this.value;saveFRData(d);renderFriends()\"><button onclick=\"showAddFriendModal()\" style=\"padding:8px 12px;border:none;border-radius:8px;background:var(--accent);color:#fff;font-size:12px;cursor:pointer\">+ \u6dfb\u52a0</button></div>";
  if(list.length===0){
    html+="<div style=\"padding:20px;text-align:center;color:var(--muted);font-size:13px\">\u6682\u65e0\u597d\u53cb<br><span style=\"font-size:11px\">\u70b9\u51fb\u4e0a\u65b9\u6dfb\u52a0\u6309\u94ae\u641c\u7d22\u7528\u6237</span></div>";
  }else{
    for(var i=0;i<list.length;i++){
      var f=list[i];
      var online=f.online?"<span style=\"width:6px;height:6px;border-radius:50%;background:var(--green);display:inline-block;margin-right:4px\"></span>":"";
      html+="<div style=\"display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;margin-bottom:4px;cursor:pointer\" onclick=\"openFriendChat(\\""+f.id+"\\")\" onmouseover=\"this.style.background=\\'rgba(255,255,255,.05)\\';\" onmouseout=\"this.style.background=\\'transparent\\'\">"+
        "<span style=\"width:32px;height:32px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0\">"+(f.avatar||"\ud83e\uddd1")+"</span>"+
        "<div style=\"flex:1;min-width:0\"><div style=\"font-size:13px;font-weight:600\">"+online+(f.name||"Unknown")+"</div><div style=\"font-size:10px;color:var(--muted)\">"+(f.online?"\u5728\u7ebf":"\u79bb\u7ebf")+"</div></div>"+
        "<span style=\"font-size:11px;color:var(--muted)\">\u79c1\u804a</span>"+
      "</div>";
    }
  }
  el.innerHTML=html;
}
function renderRequests(){
  var _frData=loadFRData();
  var el=document.getElementById("fr-requests-panel");
  if(!el) return;
  var pending=[];
  for(var i=0;i<_frData.requests.length;i++){if(_frData.requests[i].status==="pending")pending.push(_frData.requests[i]);}
  var sent=_frData.sent||[];
  var html="<div style=\"font-size:12px;color:var(--muted);margin-bottom:8px\">\u5f85\u5904\u7406\u8bf7\u6c42 ("+pending.length+")</div>";
  if(pending.length===0){
    html+="<div style=\"padding:20px;text-align:center;color:var(--muted);font-size:13px\">\u6682\u65e0\u5f85\u5904\u7406\u7684\u8bf7\u6c42</div>";
  }else{
    for(var i=0;i<pending.length;i++){
      var r=pending[i];
      html+="<div style=\"display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;margin-bottom:4px\">"+
        "<span style=\"width:28px;height:28px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0\">\ud83e\uddd1</span>"+
        "<span style=\"flex:1;font-size:13px\">"+r.name+"</span>"+
        "<button onclick=\"acceptFriend(\\""+r.id+"\\")\" style=\"padding:4px 10px;border:none;border-radius:6px;background:var(--green);color:#fff;font-size:11px;cursor:pointer\">\u63a5\u53d7</button>"+
        "<button onclick=\"rejectFriend(\\""+r.id+"\\")\" style=\"padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer\">\u62d2\u7edd</button>"+
      "</div>";
    }
  }
  if(sent.length>0){
    html+="<div style=\"font-size:12px;color:var(--muted);margin:8px 0 4px\">\u5df2\u53d1\u9001\u7684\u8bf7\u6c42</div>";
    for(var i=0;i<sent.length;i++){
      var s=sent[i];
      html+="<div style=\"display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;margin-bottom:4px\">"+
        "<span style=\"width:28px;height:28px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0\">\ud83e\uddd1</span>"+
        "<span style=\"flex:1;font-size:13px\">"+s.name+"</span>"+
        "<span style=\"font-size:11px;color:var(--muted)\">\u7b49\u5f85\u4e2d</span>"+
      "</div>";
    }
  }
  el.innerHTML=html;
}
function showAddFriendModal(){
  var d=loadFRData();
  var name=prompt("\u8bf7\u8f93\u5165\u8981\u6dfb\u52a0\u7684\u7528\u6237\u540d:");
  if(!name||name.trim().length<2) return;
  name=name.trim();
  if(d.friends.some(function(f){return f.name===name;})){alert("\u5df2\u7ecf\u662f\u597d\u53cb\u4e86");return;}
  if(d.sent.some(function(f){return f.name===name;})){alert("\u5df2\u53d1\u9001\u8fc7\u8bf7\u6c42");return;}
  d.sent.push({id:"u"+Date.now(),name:name,status:"pending"});
  d.requests.push({id:"u"+(Date.now()+1),name:name,status:"pending"});
  saveFRData(d);
  renderRequests();
}
function acceptFriend(id){
  var d=loadFRData();
  for(var i=0;i<d.requests.length;i++){
    if(d.requests[i].id===id){
      d.friends.push({id:d.requests[i].id,name:d.requests[i].name,avatar:"\ud83e\uddd1",online:false});
      d.requests.splice(i,1);
      saveFRData(d);
      renderRequests();
      return;
    }
  }
}
function rejectFriend(id){
  var d=loadFRData();
  for(var i=0;i<d.requests.length;i++){
    if(d.requests[i].id===id){
      d.requests.splice(i,1);
      saveFRData(d);
      renderRequests();
      return;
    }
  }
}
function initFR(){
  var rp=document.getElementById("fr-rank-panel");
  if(rp) renderRank();
  var fp=document.getElementById("fr-friends-panel");
  if(fp) renderFriends();
  var rqp=document.getElementById("fr-requests-panel");
  if(rqp) renderRequests();
}

// ---- Private Chat ----
var _privateChat={open:false,friend:null,messages:{}};
function openFriendChat(friendId){
  var d=loadFRData();
  var f=null;
  for(var i=0;i<d.friends.length;i++){if(d.friends[i].id===friendId){f=d.friends[i];break;}}
  if(!f) return;
  _privateChat.open=true;
  _privateChat.friend=f;
  if(!_privateChat.messages[friendId]) _privateChat.messages[friendId]=[];
  renderPrivateChat();
}
function closePrivateChat(){
  _privateChat.open=false;
  var m=document.getElementById("private-chat-modal");
  if(m) m.remove();
}
function renderPrivateChat(){
  var existing=document.getElementById("private-chat-modal");
  if(existing) existing.remove();
  var f=_privateChat.friend;
  var msgs=_privateChat.messages[f.id]||[];
  var m=document.createElement("div");
  m.id="private-chat-modal";
  m.style.cssText="position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center";
  m.onclick=function(e){if(e.target===this)closePrivateChat();};
  var html="<div style=\"background:var(--card-bg,#1a1a2e);border:1px solid var(--border,#2a3a5e);border-radius:16px;width:420px;max-width:90vw;max-height:80vh;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,.5)\">"+
    "<div style=\"display:flex;justify-content:space-between;align-items:center;padding:14px 18px;border-bottom:1px solid var(--border,#2a3a5e)\">"+
      "<div style=\"display:flex;align-items:center;gap:8px\"><span style=\"font-size:18px\">"+(f.avatar||"\ud83e\uddd1")+"</span><span style=\"font-weight:700;font-size:15px\">"+f.name+"</span>"+(f.online?"<span style=\"width:6px;height:6px;border-radius:50%;background:var(--green);display:inline-block\"></span>":"")+"</div>"+
      "<button onclick=\"closePrivateChat()\" style=\"background:none;border:none;color:var(--muted,#888);font-size:20px;cursor:pointer\">\u2715</button>"+
    "</div>"+
    "<div id=\"pc-msgs\" style=\"flex:1;overflow-y:auto;padding:12px 18px;display:flex;flex-direction:column;gap:8px\">";
  if(msgs.length===0){
    html+="<div style=\"text-align:center;color:var(--muted);padding:30px;font-size:13px\">\u5f00\u59cb\u79c1\u804a\u5427<br><span style=\"font-size:11px\">\u652f\u6301\u5206\u4eabK\u7ebf\u56fe\u3001\u7b56\u7565\u548c\u56de\u6d4b\u7ed3\u679c</span></div>";
  }else{
    for(var i=0;i<msgs.length;i++){
      var msg=msgs[i];
      var isMe=(msg.from==="me");
      html+="<div style=\"display:flex;"+(isMe?"justify-content:flex-end":"")+";gap:6px;align-items:flex-end\">"+
        "<div style=\"max-width:75%;padding:10px 14px;border-radius:14px;font-size:13px;line-height:1.5;"+(isMe?"background:var(--green);color:var(--dark);border-bottom-right-radius:4px":"background:var(--card2);border:1px solid var(--border);border-bottom-left-radius:4px")+"\">"+msg.text+"</div>"+
      "</div>";
    }
  }
  html+="</div>"+
    "<div style=\"display:flex;gap:8px;padding:10px 14px;border-top:1px solid var(--border,#2a3a5e)\">"+
      "<input id=\"pc-input\" type=\"text\" placeholder=\"\u53d1\u9001\u6d88\u606f...\" style=\"flex:1;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#0f0f23);color:var(--text,#e0e0e0);font-size:13px\" onkeydown=\"if(event.key===\\'Enter\\')sendPrivateMsg()\">"+
      "<button onclick=\"sendPrivateMsg()\" style=\"padding:10px 16px;border:none;border-radius:8px;background:var(--green);color:var(--dark);font-size:13px;font-weight:600;cursor:pointer\">\u53d1\u9001</button>"+
    "</div>"+
  "</div>";
  m.innerHTML=html;
  document.body.appendChild(m);
  var input=document.getElementById("pc-input");
  if(input) setTimeout(function(){input.focus();},100);
  var msgsEl=document.getElementById("pc-msgs");
  if(msgsEl) setTimeout(function(){msgsEl.scrollTop=msgsEl.scrollHeight;},100);
}
function sendPrivateMsg(){
  var input=document.getElementById("pc-input");
  if(!input||!input.value.trim()) return;
  var text=input.value.trim();
  input.value="";
  var f=_privateChat.friend;
  if(!_privateChat.messages[f.id]) _privateChat.messages[f.id]=[];
  _privateChat.messages[f.id].push({from:"me",text:text,time:Date.now()});
  renderPrivateChat();
}

// ---- Friend Share Integration ----
function shareToFriend(type,data){
  var d=loadFRData();
  var friends=d.friends||[];
  if(friends.length===0){alert("\u6682\u65e0\u597d\u53cb\u53ef\u5206\u4eab");return;}
  var names="";
  for(var i=0;i<friends.length;i++) names+=(i+1)+". "+friends[i].name+"\\n";
  var choice=prompt("\u9009\u62e9\u8981\u5206\u4eab\u7684\u597d\u53cb:\\n"+names+"\\n\u8f93\u5165\u7f16\u53f7 (0\u53d6\u6d88)");
  if(!choice) return;
  var idx=parseInt(choice)-1;
  if(idx<0||idx>=friends.length){alert("\u65e0\u6548\u9009\u62e9");return;}
  var f=friends[idx];
  if(!_privateChat.messages[f.id]) _privateChat.messages[f.id]=[];
  var shareText="";
  if(type==="chart") shareText="\ud83d\udcc8 K\u7ebf\u56fe\u622a\u56fe - "+new Date().toLocaleTimeString();
  else if(type==="strategy") shareText="\u26a1 \u7b56\u7565\u5206\u4eab - "+(data||"\u8d8b\u52bf\u8ddf\u8e2a\u7b56\u7565");
  else if(type==="backtest") shareText="\ud83d\udd2c \u56de\u6d4b\u62a5\u544a - "+(data||"BTCUSDT 30m");
  _privateChat.messages[f.id].push({from:"me",text:shareText,time:Date.now()});
  saveFRData(d);
  var fName=f.name;
  if(_privateChat.open&&_privateChat.friend&&_privateChat.friend.id===f.id) renderPrivateChat();
}
'''

# Use bytes to insert to avoid encoding issues
r = r[:insert_point] + friend_js.encode('utf-8') + r[insert_point:]
with open(filepath, 'wb') as f:
    f.write(r)
print(f'Friend JS inserted ({len(friend_js)} chars)')
print(f'Saved phase 2: {len(r)} bytes')

# ===== PHASE 3: Update initQuantTalk =====
print('\n=== PHASE 3: Update initQuantTalk ===')
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

old_init = """function initQuantTalk(){
  loadSQData();
  renderChannelList();
  if(_sqChannels.length > 0) switchChannel(_sqChannels[0].id);
  initWalletUI();
}"""

new_init = """function initQuantTalk(){
  loadSQData();
  renderChannelList();
  if(_sqChannels.length > 0) switchChannel(_sqChannels[0].id);
  initWalletUI();
  initFR();
}"""

if old_init in t:
    t = t.replace(old_init, new_init)
    print('initQuantTalk updated OK')
else:
    print('initQuantTalk not found')
    # Try alternative
    idx = t.find('function initQuantTalk')
    if idx > 0:
        end = t.find('function renderChannelList', idx) - 2
        print(f'Found at {idx}: {t[idx:end]}')

r = t.encode('utf-8', errors='replace')
with open(filepath, 'wb') as f:
    f.write(r)

# ===== Syntax check =====
print('\n=== Syntax Check ===')
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c)
res = subprocess.run(['node','--check','/tmp/sc.js'], capture_output=True, timeout=15)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    err = res.stderr[:500]
    print(f'ERROR: {err}')
else:
    print('Syntax OK!')
print(f'Final size: {len(r)} bytes')
