"""Replace QuantTalk right panel with Friends/Rank panel + add friend system JS"""
import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# ========== STEP 1: Replace right panel HTML ==========
old_right = """        <!-- Right: Post Feed -->
        <div style="width:280px;min-width:280px;background:var(--card);border:1px solid var(--border);border-radius:12px;display:flex;flex-direction:column;overflow:hidden">
          <div style="padding:10px 14px;border-bottom:1px solid var(--border);font-weight:600;font-size:13px">观点广场</div>
          <div id="sq-posts" style="flex:1;overflow-y:auto;padding:8px"></div>
        </div>"""

new_right = """        <!-- Right: Friends & Leaderboard -->
        <div style="width:280px;min-width:280px;background:var(--card);border:1px solid var(--border);border-radius:12px;display:flex;flex-direction:column;overflow:hidden">
          <!-- Tabs -->
          <div id="fr-tabs" style="display:flex;border-bottom:1px solid var(--border)">
            <div class="fr-tab active" data-tab="rank" onclick="switchFRTab('rank')" style="flex:1;padding:10px 0;text-align:center;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid var(--green);color:var(--green)">🏆 排行榜</div>
            <div class="fr-tab" data-tab="friends" onclick="switchFRTab('friends')" style="flex:1;padding:10px 0;text-align:center;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;color:var(--muted)">👥 好友</div>
            <div class="fr-tab" data-tab="requests" onclick="switchFRTab('requests')" style="flex:1;padding:10px 0;text-align:center;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;color:var(--muted)">📩 请求</div>
          </div>
          <!-- Tab Content -->
          <div id="fr-rank-panel" style="flex:1;overflow-y:auto;padding:8px;display:block"></div>
          <div id="fr-friends-panel" style="flex:1;overflow-y:auto;padding:8px;display:none"></div>
          <div id="fr-requests-panel" style="flex:1;overflow-y:auto;padding:8px;display:none"></div>
        </div>"""

if old_right in t:
    t = t.replace(old_right, new_right)
    print('1. Replaced right panel with Friends/Rank UI')
else:
    print('1. NOT FOUND - searching...')
    idx = t.find('观点广场')
    if idx > 0:
        print(f'Found at {idx}')
        # Find the div with 280px
        start = t.rfind('<div', idx - 200, idx)
        end = t.find('</div>', idx)
        print(f'From {start} to {end}')
        old_right = t[start:end+6]
        print(f'Old right panel: {len(old_right)} chars')
        t = t.replace(old_right, new_right)
        print('1. Replaced right panel')
    else:
        # Search for sq-posts
        idx2 = t.find('sq-posts')
        if idx2 > 0:
            print(f'sq-posts at {idx2}')
            start2 = t.rfind('<div', idx2 - 300, idx2)
            end2 = t.find('</div>', idx2 + 50)
            # Find sibling closing div
            # The parent div wraps both the title div and sq-posts div
            parent_div = t.rfind('<div', start2 - 200, start2)
            # Find the end of this content div
            end2 = t.find('</div>', end2 + 6)
            while t[end2+6:end2+12] != '</div>' and end2 < end2 + 100:
                end2 = t.find('</div>', end2 + 6)
            old_area = t[parent_div:end2+12]
            print(f'Found area: {len(old_area)} chars')
            new_area = new_right
            t = t.replace(old_area, new_area, 1)
            print('1. Replaced right panel')

# ========== STEP 2: Add Friend System JS ==========
# Insert after the createChannel function
fn_insert = t.find('function showCreateChannelModal()')
if fn_insert < 0:
    fn_insert = t.find('function createChannelSubmit')

# Find the end of QuantTalk functions - look for function loadTV
load_tv_idx = t.find('function loadTV(')
if load_tv_idx > fn_insert:
    # Insert friend functions before loadTV
    friend_js = """
// ---- Friend System ----
var _frData = null;
function loadFRData(){
  var d=localStorage.getItem('quantalk_friends');
  if(d){try{_frData=JSON.parse(d);}catch(e){}}
  if(!_frData) _frData = {friends:[], requests:[], sent:[], user:{id:'u1',name:'joohebin220',avatar:'👤',pnl:'+18.5%',winRate:'62%',totalPnl:'+$12,450'}};
  return _frData;
}
function saveFRData(){localStorage.setItem('quantalk_friends',JSON.stringify(_frData));}
function switchFRTab(tab){
  var tabs=document.querySelectorAll('.fr-tab');
  tabs.forEach(function(t){t.style.borderBottomColor='transparent';t.style.color='var(--muted)';t.classList.remove('active');});
  var panels=['fr-rank-panel','fr-friends-panel','fr-requests-panel'];
  panels.forEach(function(id){document.getElementById(id).style.display='none';});
  var el=document.querySelector('.fr-tab[data-tab=\"'+tab+'\"]');
  if(el){el.style.borderBottomColor='var(--green)';el.style.color='var(--green)';el.classList.add('active');}
  document.getElementById('fr-'+tab+'-panel').style.display='block';
  if(tab==='rank') renderRank();
  else if(tab==='friends') renderFriends();
  else renderRequests();
}
function renderRank(){
  var el=document.getElementById('fr-rank-panel');
  if(!el) return;
  // Mock leaderboard
  var data=[
    {rank:1,name:'量子猎手',pnl:'+$45,620',rate:'+156%',win:'78%',trades:142},
    {rank:2,name:'趋势捕手',pnl:'+$32,180',rate:'+89%',win:'71%',trades:98},
    {rank:3,name:'joohebin220',pnl:'+$12,450',rate:'+18.5%',win:'62%',trades:56},
    {rank:4,name:'BTC信徒',pnl:'+$8,920',rate:'+42%',win:'65%',trades:134},
    {rank:5,name:'量化女神',pnl:'+$6,350',rate:'+28%',win:'73%',trades:87},
    {rank:6,name:'波段王',pnl:'+$4,200',rate:'+15%',win:'55%',trades:203},
    {rank:7,name:'链上侦探',pnl:'+$3,100',rate:'+22%',win:'68%',trades:45},
    {rank:8,name:'对冲大师',pnl:'+$1,890',rate:'+8%',win:'59%',trades:312},
  ];
  el.innerHTML='<div style=\"margin-bottom:8px\">'+
    data.map(function(d){
      var isMe=d.name==='joohebin220';
      return '<div style=\"display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;margin-bottom:4px'+(isMe?';background:rgba(0,200,150,.1)':'')+'\" onclick=\"'+(isMe?'':'showUserProfile(\\''+d.name+'\\')')+'\">'+
        '<span style=\"width:20px;text-align:center;font-weight:'+(d.rank<=3?'800':'400')+';color:'+(d.rank===1?'gold':d.rank===2?'silver':d.rank===3?'#cd7f32':'var(--muted)')+';font-size:'+(d.rank<=3?'18':'13')+'px\">'+(d.rank<=3?'🥇🥈🥉'[d.rank-1]:d.rank)+'</span>'+
        '<span style=\"width:28px;height:28px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0\">'+(isMe?'👤':'🧑')+'</span>'+
        '<div style=\"flex:1;min-width:0\"><div style=\"font-size:12px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap\">'+d.name+'</div><div style=\"font-size:10px;color:var(--muted)\">'+d.trades+' 笔交易</div></div>'+
        '<div style=\"text-align:right\"><div style=\"font-size:12px;font-weight:700;color:'+(d.pnl[0]==='+'?'var(--green)':'var(--red)')+'\">'+d.pnl+'</div><div style=\"font-size:10px;color:'+(d.rate[0]==='+'?'var(--green)':'var(--red)')+'\">'+d.rate+'</div></div>'+
      '</div>';
    }).join('')+
  '</div>';
}
function renderFriends(){
  loadFRData();
  var el=document.getElementById('fr-friends-panel');
  if(!el) {console.log('fr-friends-panel not found');return;}
  var q=_frData.searchQ||'';
  var list=_frData.friends||[];
  if(q&&q.length>1) list=list.filter(function(f){return f.name.indexOf(q)>=0;});
  el.innerHTML='<div style=\"display:flex;gap:6px;margin-bottom:8px\"><input id=\"fr-search\" type=\"text\" placeholder=\"搜索用户名...\" value=\"'+q+'\" style=\"flex:1;padding:8px 12px;border:1px solid var(--border);border-radius:8px;background:var(--input-bg);color:var(--text);font-size:12px\" onkeyup=\"var v=this.value;loadFRData();_frData.searchQ=v;saveFRData();renderFriends()\"><button onclick=\"showAddFriend()\" style=\"padding:8px 12px;border:none;border-radius:8px;background:var(--accent);color:#fff;font-size:12px;cursor:pointer\">+ 添加</button></div>'+
    (list.length===0?'<div style=\"padding:20px;text-align:center;color:var(--muted);font-size:13px\">暂无好友<br><span style=\"font-size:11px\">点击上方添加按钮搜索用户</span></div>':
    list.map(function(f){
      var online=f.online?'<span style=\"width:6px;height:6px;border-radius:50%;background:var(--green);display:inline-block;margin-right:4px\"></span>':'';
      return '<div style=\"display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;margin-bottom:4px;cursor:pointer\" onclick=\"openFriendChat(\\''+f.id+'\\')\" onmouseover=\"this.style.background=\\'rgba(255,255,255,.05)\\';\" onmouseout=\"this.style.background=\\'transparent\\'\">'+
        '<span style=\"width:32px;height:32px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0\">'+(f.avatar||'🧑')+'</span>'+
        '<div style=\"flex:1;min-width:0\"><div style=\"font-size:13px;font-weight:600\">'+online+(f.name||'Unknown')+'</div><div style=\"font-size:10px;color:var(--muted)\">'+(f.online?'在线':'离线')+'</div></div>'+
        '<span style=\"font-size:11px;color:var(--muted)\">私聊</span>'+
      '</div>';
    }).join(''));
}
function renderRequests(){
  loadFRData();
  var el=document.getElementById('fr-requests-panel');
  if(!el) return;
  var pending=_frData.requests.filter(function(r){return r.status==='pending';});
  var sent=_frData.sent||[];
  el.innerHTML='<div style=\"font-size:12px;color:var(--muted);margin-bottom:8px\">待处理请求 ('+pending.length+')</div>'+
    (pending.length===0?'<div style=\"padding:20px;text-align:center;color:var(--muted);font-size:13px\">暂无待处理的请求</div>':
    pending.map(function(r){
      return '<div style=\"display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;margin-bottom:4px\">'+
        '<span style=\"width:28px;height:28px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0\">🧑</span>'+
        '<span style=\"flex:1;font-size:13px\">'+r.name+'</span>'+
        '<button onclick=\"acceptRequest(\\''+r.id+'\\')\" style=\"padding:4px 10px;border:none;border-radius:6px;background:var(--green);color:#fff;font-size:11px;cursor:pointer\">接受</button>'+
        '<button onclick=\"rejectRequest(\\''+r.id+'\\')\" style=\"padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer\">拒绝</button>'+
      '</div>';
    }).join('')+
    (sent.length?'<div style=\"font-size:12px;color:var(--muted);margin:8px 0 4px\">已发送的请求</div>'+
    sent.map(function(r){
      return '<div style=\"display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;margin-bottom:4px\">'+
        '<span style=\"width:28px;height:28px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0\">🧑</span>'+
        '<span style=\"flex:1;font-size:13px\">'+r.name+'</span>'+
        '<span style=\"font-size:11px;color:var(--muted)\">等待中</span>'+
      '</div>';
    }).join(''):'');
}
function showAddFriend(){
  var name=prompt('请输入要添加的用户名:');
  if(!name||name.trim().length<2) return;
  name=name.trim();
  loadFRData();
  // Check if already friends
  if(_frData.friends.some(function(f){return f.name===name;})){toast('已经是好友了','warn');return;}
  if(_frData.sent.some(function(f){return f.name===name;})){toast('已发送过请求','warn');return;}
  _frData.sent.push({id:'u'+Date.now(),name:name,status:'pending'});
  // Add to requests for them (mock)
  _frData.requests.push({id:'u'+Date.now()+1,name:name,status:'pending'});
  saveFRData();
  toast('已发送好友请求给 '+name,'success');
  renderRequests();
}
function acceptRequest(id){
  loadFRData();
  var r=_frData.requests.filter(function(x){return x.id===id;});
  if(r.length){
    _frData.friends.push({id:r[0].id,name:r[0].name,avatar:'🧑',online:false});
    _frData.requests=_frData.requests.filter(function(x){return x.id!==id;});
    saveFRData();
    toast('已添加 '+r[0].name+' 为好友','success');
    renderRequests();
  }
}
function rejectRequest(id){
  loadFRData();
  _frData.requests=_frData.requests.filter(function(x){return x.id!==id;});
  saveFRData();
  toast('已拒绝请求','info');
  renderRequests();
}
function showUserProfile(name){toast('用户 '+name+' 资料页（开发中）','info');}
function initFR(){
  loadFRData();
  var rp=document.getElementById('fr-rank-panel');
  if(rp) renderRank();
  var fp=document.getElementById('fr-friends-panel');
  if(fp) renderFriends();
  var rqp=document.getElementById('fr-requests-panel');
  if(rqp) renderRequests();
}

// ---- Private Chat ----
var _privateChat = {open:false, friend:null, messages:{}};
function openFriendChat(friendId){
  loadFRData();
  var f=_frData.friends.filter(function(x){return x.id===friendId;});
  if(!f.length) return;
  _privateChat.open=true;
  _privateChat.friend=f[0];
  if(!_privateChat.messages[friendId]) _privateChat.messages[friendId]=[];
  renderPrivateChat();
}
function closePrivateChat(){_privateChat.open=false;document.getElementById('private-chat-modal').remove();}
function renderPrivateChat(){
  var existing=document.getElementById('private-chat-modal');
  if(existing) existing.remove();
  var f=_privateChat.friend;
  var msgs=_privateChat.messages[f.id]||[];
  var m=document.createElement('div');
  m.id='private-chat-modal';
  m.style.cssText='position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center';
  m.onclick=function(e){if(e.target===this)closePrivateChat();};
  m.innerHTML='<div style=\"background:var(--card-bg,#1a1a2e);border:1px solid var(--border,#2a3a5e);border-radius:16px;width:420px;max-width:90vw;max-height:80vh;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,.5)\">'+
    '<div style=\"display:flex;justify-content:space-between;align-items:center;padding:14px 18px;border-bottom:1px solid var(--border,#2a3a5e)\">'+
      '<div style=\"display:flex;align-items:center;gap:8px\"><span style=\"font-size:18px\">'+(f.avatar||'🧑')+'</span><span style=\"font-weight:700;font-size:15px\">'+f.name+'</span>'+(f.online?'<span style=\"width:6px;height:6px;border-radius:50%;background:var(--green);display:inline-block\"></span>':'')+'</div>'+
      '<button onclick=\"closePrivateChat()\" style=\"background:none;border:none;color:var(--muted);font-size:20px;cursor:pointer\">&#10005;</button>'+
    '</div>'+
    '<div id=\"pc-msgs\" style=\"flex:1;overflow-y:auto;padding:12px 18px;display:flex;flex-direction:column;gap:8px\">'+
      (msgs.length===0?'<div style=\"text-align:center;color:var(--muted);padding:30px;font-size:13px\">开始私聊吧<br><span style=\"font-size:11px\">支持分享K线图、策略和回测结果</span></div>':
        msgs.map(function(msg){
          var isMe=msg.from==='me';
          return '<div style=\"display:flex;'+(isMe?'justify-content:flex-end':'')+';gap:6px;align-items:flex-end\">'+
            '<div style=\"max-width:75%;padding:10px 14px;border-radius:14px;font-size:13px;line-height:1.5;'+
              (isMe?'background:var(--green);color:var(--dark);border-bottom-right-radius:4px':
              'background:var(--card2);border:1px solid var(--border);border-bottom-left-radius:4px')+
            '\">'+msg.text+'</div>'+
          '</div>';
        }).join('')
    )+
    '</div>'+
    '<div style=\"display:flex;gap:8px;padding:10px 14px;border-top:1px solid var(--border,#2a3a5e)\">'+
      '<input id=\"pc-input\" type=\"text\" placeholder=\"发送消息...\" style=\"flex:1;padding:10px 14px;border:1px solid var(--border,#2a3a5e);border-radius:8px;background:var(--input-bg,#0f0f23);color:var(--text,#e0e0e0);font-size:13px\" onkeydown=\"if(event.key===\\'Enter\\')sendPrivateMsg()\">'+
      '<button onclick=\"sendPrivateMsg()\" style=\"padding:10px 16px;border:none;border-radius:8px;background:var(--green);color:var(--dark);font-size:13px;font-weight:600;cursor:pointer\">发送</button>'+
    '</div>'+
  '</div>';
  document.body.appendChild(m);
  setTimeout(function(){
    var input=document.getElementById('pc-input');
    if(input) input.focus();
    var msgsEl=document.getElementById('pc-msgs');
    if(msgsEl) msgsEl.scrollTop=msgsEl.scrollHeight;
  },100);
}
function sendPrivateMsg(){
  var input=document.getElementById('pc-input');
  if(!input||!input.value.trim()) return;
  var text=input.value.trim();
  input.value='';
  var f=_privateChat.friend;
  if(!_privateChat.messages[f.id]) _privateChat.messages[f.id]=[];
  _privateChat.messages[f.id].push({from:'me',text:text,time:Date.now()});
  renderPrivateChat();
}

// ---- Share Functions ----
function shareToFriend(type,data){
  loadFRData();
  var friends=_frData.friends||[];
  if(friends.length===0){toast('暂无好友可分享','warn');return;}
  var names=friends.map(function(f,i){return (i+1)+'. '+f.name;}).join('\\n');
  var choice=prompt('选择要分享的好友:\\n'+names+'\\n\\n输入编号 (0取消)');
  if(!choice) return;
  var idx=parseInt(choice)-1;
  if(idx<0||idx>=friends.length){toast('无效选择','warn');return;}
  var f=friends[idx];
  if(!_privateChat.messages[f.id]) _privateChat.messages[f.id]=[];
  var shareText='';
  if(type==='chart') shareText='📈 K线图截图 - '+new Date().toLocaleTimeString();
  else if(type==='strategy') shareText='⚡ 策略分享 - '+ (data||'趋势跟踪策略');
  else if(type==='backtest') shareText='🔬 回测报告 - '+(data||'BTCUSDT 30m');
  _privateChat.messages[f.id].push({from:'me',text:shareText,time:Date.now()});
  saveFRData();
  toast('已分享给 '+f.name,'success');
  if(_privateChat.open&&_privateChat.friend&&_privateChat.friend.id===f.id) renderPrivateChat();
}

// Inject share button into msg area
function injectShareBtns(){
  // Add share buttons to channel header
  var hdr=document.getElementById('channel-header');
  if(!hdr) return;
  var btnArea=hdr.querySelectorAll('div[style*=\"gap:6px\"]');
  if(btnArea.length){
    var area=btnArea[btnArea.length-1];
    var existing=area.querySelector('[onclick*=\"shareToFriend\"]');
    if(!existing){
      var btn=document.createElement('button');
      btn.onclick=function(){shareToFriend('chart');};
      btn.textContent='🤝 分享';
      btn.style.cssText='padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer';
      area.insertBefore(btn, area.firstChild);
    }
  }
}"""

    # Insert before loadTV (before the TradingView section)
    t = t[:load_tv_idx] + friend_js + t[load_tv_idx:]
    print('2. Inserted Friend System JS')
else:
    print('2. loadTV not found, cannot insert')

# ========== STEP 3: Init friend system in initQuantTalk ==========
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
  injectShareBtns();
}"""

if old_init in t:
    t = t.replace(old_init, new_init)
    print('3. Updated initQuantTalk with friend init')
else:
    print('3. initQuantTalk not found')

# ========== STEP 4: Update shareChart to support friend sharing ==========
old_share = """function shareChart(){
  var m = _tvInstance;
  if(m && typeof m.takeScreenshot === 'function'){
    m.takeScreenshot().then(function(b){
      var txt = '📈 图表截图 '+new Date().toLocaleString();
      _sqMessages[_sqCurrentChannel.id].push({id:'m'+Date.now(), text:txt, img:b, time:Date.now(), likes:0, liked:false, reply:null});
      saveSQ();
      renderMessages();
      toast('✅ 图表已分享到频道','success');
    }).catch(function(){toast('截图失败','error');});
  } else {
    // Fallback: just share link
    var txt = '📈 BTCUSDT 图表查看 - https://www.tradingview.com/chart/?symbol=BINANCE%3ABTCUSDT';
    _sqMessages[_sqCurrentChannel.id].push({id:'m'+Date.now(), text:txt, time:Date.now(), likes:0, liked:false, reply:null});
    saveSQ();
    renderMessages();
    toast('✅ 图表已分享到频道','success');
  }
}"""

new_share = """function shareChart(){
  // Show share options
  var opts='<div style=\"padding:16px 14px\"><div style=\"font-size:14px;font-weight:700;margin-bottom:12px\">📤 分享图表</div>'+
    '<button onclick=\"this.parentElement.parentElement.remove();shareChartToChannel()\" style=\"width:100%;padding:12px;border:1px solid var(--border);border-radius:10px;background:transparent;color:var(--text);font-size:13px;cursor:pointer;margin-bottom:8px;display:block\">📢 分享到频道</button>'+
    '<button onclick=\"this.parentElement.parentElement.remove();shareToFriend(\\'chart\\')\" style=\"width:100%;padding:12px;border:1px solid var(--border);border-radius:10px;background:transparent;color:var(--text);font-size:13px;cursor:pointer;display:block\">👤 分享给好友</button>'+
    '</div>';
  var existing=document.getElementById('share-chart-modal');
  if(existing) existing.remove();
  var m=document.createElement('div');
  m.id='share-chart-modal';
  m.style.cssText='position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center';
  m.onclick=function(e){if(e.target===this)this.remove();};
  m.innerHTML='<div style=\"background:var(--card-bg,#1a1a2e);border:1px solid var(--border,#2a3a5e);border-radius:16px;width:300px;box-shadow:0 20px 60px rgba(0,0,0,.5)\">'+opts+'</div>';
  document.body.appendChild(m);
}
function shareChartToChannel(){
  var m=_tvInstance;
  if(m&&typeof m.takeScreenshot==='function'){
    m.takeScreenshot().then(function(b){
      var txt='📈 图表截图 '+new Date().toLocaleString();
      _sqMessages[_sqCurrentChannel.id].push({id:'m'+Date.now(),text:txt,img:b,time:Date.now(),likes:0,liked:false,reply:null});
      saveSQ();
      renderMessages();
      toast('✅ 图表已分享到频道','success');
    }).catch(function(){toast('截图失败','error');});
  }else{
    var txt='📈 BTCUSDT 图表 - https://www.tradingview.com/chart/?symbol=BINANCE%3ABTCUSDT';
    _sqMessages[_sqCurrentChannel.id].push({id:'m'+Date.now(),text:txt,time:Date.now(),likes:0,liked:false,reply:null});
    saveSQ();
    renderMessages();
    toast('✅ 图表已分享到频道','success');
  }
}"""

if old_share in t:
    t = t.replace(old_share, new_share)
    print('4. Updated shareChart with friend sharing options')
else:
    print('4. shareChart not found')
    idx = t.find('function shareChart(')
    if idx > 0:
        print(f'Found at {idx}: {t[idx:idx+60]}')
    else:
        print('shareChart function not found at all')

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
    err = res.stderr[:500]
    print(f'Error: {err}')
else:
    print('Syntax OK!')
print(f'Saved: {len(r)} bytes')
