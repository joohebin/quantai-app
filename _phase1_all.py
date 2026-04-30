# -*- coding: utf-8 -*-
"""
Phase 1: QuantTalk Upgrade + Wallet + TV Bridge + YouTube
Single comprehensive script modifying all sections of index.html.
"""
filepath = 'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# ============================================================
# 1. ADD Web3 Wallet Tab to Account Page
# ============================================================

# 1a. Add wallet tab button after exchanges tab button
tab_btns_marker = 'onclick=\"switchAccountTab(\'exchanges\', this)\">🏦 交易所</button>'
wallet_tab_btn = '\n            <button class="acc-tab" onclick="switchAccountTab(\'wallet\', this)">💳 钱包</button>\n          </div>\n\n          <div id="acc-tab-exchanges"'
# Find where exchanges tab starts and the button
wallet_btn_html = tab_btns_marker + '\n            <button class="acc-tab" onclick="switchAccountTab(\'wallet\', this)">💳 钱包</button>'
t = t.replace(tab_btns_marker, wallet_btn_html)

# 1b. Add wallet tab content BEFORE acc-tab-exchanges
wallet_content = """
            <div id="acc-tab-wallet" style="display:none">
            <div class="card" style="padding:16px">
              <div style="font-size:14px;font-weight:600;margin-bottom:12px">💳 绑定加密货币钱包</div>
              <div style="font-size:12px;color:var(--muted);margin-bottom:16px">绑定钱包用于购买套餐、策略等</div>
              
              <div style="margin-bottom:16px">
                <div style="font-size:12px;color:var(--muted);margin-bottom:8px">选择钱包</div>
                <select id="wallet-select" style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--input-bg);color:var(--text);font-size:14px">
                  <option value="">-- 请选择钱包 --</option>
                  <option value="metamask">🦊 MetaMask</option>
                  <option value="walletconnect">🔗 WalletConnect</option>
                  <option value="trustwallet">🛡️ Trust Wallet</option>
                  <option value="okx">🔶 OKX Wallet</option>
                  <option value="exchange">🏛️ 交易所钱包</option>
                  <option value="cold">❄️ 冷钱包</option>
                </select>
              </div>
              
              <div id="wallet-connect-area">
                <button id="wallet-connect-btn" onclick="connectWallet()" style="width:100%;padding:12px;border:none;border-radius:8px;background:var(--accent);color:#fff;font-size:14px;font-weight:600;cursor:pointer">🔗 连接钱包</button>
              </div>
              
              <div id="wallet-address-area" style="display:none;margin-top:12px;background:rgba(0,200,150,.1);border:1px solid rgba(0,200,150,.3);border-radius:8px;padding:12px">
                <div style="font-size:12px;color:var(--muted);margin-bottom:6px">✅ 已连接地址</div>
                <div id="wallet-display-address" style="font-size:13px;font-weight:600;color:var(--green);word-break:break-all;font-family:monospace"></div>
                <div style="margin-top:8px;display:flex;gap:8px">
                  <span style="font-size:12px;padding:4px 8px;background:rgba(0,200,150,.2);border-radius:4px;color:var(--green)" id="wallet-type-badge">MetaMask</span>
                  <span style="font-size:12px;padding:4px 8px;background:rgba(0,200,150,.2);border-radius:4px;color:var(--green)" id="wallet-balance">0.00 ETH</span>
                </div>
                <button onclick="disconnectWallet()" style="margin-top:10px;padding:8px 16px;border:1px solid var(--red);border-radius:6px;background:transparent;color:var(--red);font-size:12px;cursor:pointer">断开连接</button>
              </div>
              
              <div id="wallet-manual-input" style="display:none;margin-top:12px">
                <div style="font-size:12px;color:var(--muted);margin-bottom:6px">输入钱包地址</div>
                <input id="wallet-manual-address" type="text" placeholder="0x... 或 bc1..." style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--input-bg);color:var(--text);font-size:13px">
                <button onclick="saveManualWallet()" style="margin-top:8px;width:100%;padding:10px;border:none;border-radius:8px;background:var(--accent);color:#fff;font-size:14px;font-weight:600;cursor:pointer">💾 保存地址</button>
              </div>
              
              <div id="wallet-history" style="margin-top:16px;display:none">
                <div style="font-size:13px;font-weight:600;margin-bottom:8px;color:var(--muted)">📋 绑定历史</div>
                <div id="wallet-history-list"></div>
              </div>
            </div>
            </div>
            
            <div id="acc-tab-exchanges"""

t = t.replace('<div id="acc-tab-exchanges"', wallet_content)

# 1c. Add wallet JS functions to the switchAccountTab handler
# Find the tabIds list and add 'wallet'
t = t.replace("const tabIds = ['positions', 'trades', 'signals', 'manual', 'market', 'strategies', 'exchanges'];",
              "const tabIds = ['positions', 'trades', 'signals', 'manual', 'market', 'strategies', 'exchanges', 'wallet'];")

# ============================================================
# 2. QUANTTALK UPGRADE - Complete channel system
# ============================================================

# 2a. Replace the QuantTalk page HTML
sq_start = t.find('<!-- ===== QuantTalk ===== -->')
sq_html_start = t.find('<div class="page" id="page-square"', sq_start)
sq_html_end = t.find('<!-- ===== 策略市场 ===== -->', sq_html_start)

new_sq_html = '''<!-- ===== QuantTalk ===== -->
      <div class="page" id="page-square" style="display:flex;gap:0;height:calc(100vh - 140px);overflow:hidden">
        <!-- Left: Channel List -->
        <div style="width:200px;min-width:200px;background:var(--card);border:1px solid var(--border);border-radius:12px;display:flex;flex-direction:column;overflow:hidden">
          <div style="padding:12px 14px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between">
            <span style="font-weight:700;font-size:14px">💬 <span data-i18n="sq_channel">频道</span></span>
            <button onclick="createChannel()" style="width:28px;height:28px;border:none;border-radius:6px;background:var(--accent);color:#fff;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center">+</button>
          </div>
          <div id="channel-list" style="flex:1;overflow-y:auto;padding:6px">
            <!-- channels rendered by JS -->
          </div>
        </div>
        
        <!-- Middle: Chat Area -->
        <div style="flex:1;display:flex;flex-direction:column;margin:0 12px">
          <!-- Channel Header with Widgets -->
          <div id="channel-header" style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:10px 14px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between">
            <div>
              <span id="channel-name-display" style="font-weight:700;font-size:15px"># 全局</span>
              <span id="channel-desc-display" style="font-size:11px;color:var(--muted);margin-left:8px">闲聊</span>
            </div>
            <div style="display:flex;gap:6px">
              <button onclick="toggleChannelWidget('tv')" id="tv-widget-btn" style="padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer">📈 图表</button>
              <button onclick="toggleChannelWidget('youtube')" id="yt-widget-btn" style="padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer">🎥 直播</button>
            </div>
          </div>
          
          <!-- Widget containers (shown/hidden) -->
          <div id="widget-tv" style="display:none;margin-bottom:8px;border-radius:12px;overflow:hidden;border:1px solid var(--border);height:380px"></div>
          <div id="widget-youtube" style="display:none;margin-bottom:8px;border-radius:12px;overflow:hidden;border:1px solid var(--border);height:380px">
            <div id="youtube-player" style="width:100%;height:100%"></div>
          </div>
          
          <!-- Messages -->
          <div id="sq-msgs" style="flex:1;overflow-y:auto;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:12px;margin-bottom:8px">
            <!-- messages rendered by JS -->
          </div>
          
          <!-- Composer -->
          <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:10px 14px">
            <div style="display:flex;gap:8px">
              <div style="flex:1;display:flex;gap:6px">
                <input id="sq-input" type="text" placeholder="输入消息..." style="flex:1;padding:10px 14px;border:1px solid var(--border);border-radius:8px;background:var(--input-bg);color:var(--text);font-size:13px" onkeydown="if(event.key==='Enter') sendChannelMsg()">
                <button onclick="sqShareChart()" style="padding:8px 12px;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--muted);font-size:13px;cursor:pointer" title="分享K线图">📷</button>
                <button onclick="sqAttachImage()" style="padding:8px 12px;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--muted);font-size:13px;cursor:pointer" title="发送图片">🖼️</button>
              </div>
              <button onclick="sendChannelMsg()" style="padding:10px 20px;border:none;border-radius:8px;background:var(--accent);color:#fff;font-size:13px;font-weight:600;cursor:pointer">发送</button>
            </div>
          </div>
        </div>
        
        <!-- Right: Post Feed (existing posts) -->
        <div style="width:280px;min-width:280px;background:var(--card);border:1px solid var(--border);border-radius:12px;display:flex;flex-direction:column;overflow:hidden">
          <div style="padding:10px 14px;border-bottom:1px solid var(--border);font-weight:600;font-size:13px"><span data-i18n="sq_title">观点广场</span></div>
          <div id="sq-posts" style="flex:1;overflow-y:auto;padding:8px"></div>
        </div>
      </div>'''

t = t[:sq_html_start] + new_sq_html + t[sq_html_end:]

# ============================================================
# 3. REPLACE QuantTalk JS (renderSquare, etc) with new channel system
# ============================================================

# Find the old QuantTalk JS
old_qt_marker = '// ===== QuantTalk ====='
old_qt_end_marker = '// ===== 策略市场 ====='

s_qt = t.rfind(old_qt_marker, 600000)  # the main QuantTalk JS block, not CSS
while s_qt > 0:
    prev = t[s_qt-100:s_qt]
    if 'renderSquare' in prev or 'function renderSquare' in t[s_qt:s_qt+200]:
        break
    s_qt = t.rfind(old_qt_marker, 0, s_qt-1)

# If not found by function name, find the actual renderSquare
s_qt = t.find('function renderSquare')
e_qt = t.find('// ===== 策略市场 =====', s_qt)

new_qt_js = '''// ===================================================
// ===== QuantTalk - Channel System =====
// ===================================================

// Channel data
var _sqChannels = [];
var _sqMessages = {};
var _sqCurrentChannel = null;
var _widgetTVVisible = false;
var _widgetYTVisible = false;
var _tvWidget = null;
var _sqLikes = {};
var _sqComments = {};

// Load/Save
function loadSQData(){
  var saved = localStorage.getItem('quantalk_data');
  if(saved){
    try{
      var d = JSON.parse(saved);
      _sqChannels = d.channels || [];
      _sqMessages = d.messages || {};
      _sqLikes = d.likes || {};
      _sqComments = d.comments || {};
    }catch(e){}
  }
  if(!_sqChannels.length){
    _sqChannels = [
      {id:'ch-general', name:'全局', desc:'闲聊', icon:'🌐', widgets:{tv:'BTCUSDT', yt:''}},
      {id:'ch-btc', name:'BTC讨论', desc:'比特币行情分析', icon:'₿', widgets:{tv:'BTCUSDT', yt:''}},
      {id:'ch-eth', name:'ETH分析', desc:'以太坊技术讨论', icon:'⟠', widgets:{tv:'ETHUSDT', yt:''}},
      {id:'ch-strategy', name:'策略分享', desc:'量化策略交流', icon:'⚡', widgets:{tv:'', yt:''}},
      {id:'ch-livestream', name:'官方直播', desc:'操盘手实时交易', icon:'📺', widgets:{tv:'BTCUSDT', yt:''}},
      {id:'ch-backtest', name:'回测心得', desc:'策略回测讨论', icon:'🔬', widgets:{tv:'', yt:''}}
    ];
    _sqMessages['ch-general'] = [
      {id:'msg1', uid:'system', name:'System', av:'🤖', text:'欢迎来到 QuantTalk！在这里可以讨论行情、分享策略。', time:Date.now()-3600000, likes:0, liked:false, comments:[]}
    ];
    for(var i=1;i<_sqChannels.length;i++){
      _sqMessages[_sqChannels[i].id] = [];
    }
  }
}
function saveSQData(){
  localStorage.setItem('quantalk_data', JSON.stringify({
    channels: _sqChannels,
    messages: _sqMessages,
    likes: _sqLikes,
    comments: _sqComments
  }));
}

// Render channel list
function renderChannels(){
  var el = document.getElementById('channel-list');
  if(!el) return;
  el.innerHTML = _sqChannels.map(function(ch){
    var active = _sqCurrentChannel && _sqCurrentChannel.id === ch.id ? 'background:rgba(0,200,150,.15);color:var(--green)' : '';
    return '<div class="ch-item" onclick="switchChannel(\''+ch.id+'\')" style="padding:8px 10px;border-radius:8px;cursor:pointer;margin-bottom:2px;font-size:13px;'+active+'display:flex;align-items:center;gap:6px" onmouseover="this.style.background=\'rgba(255,255,255,.05)\'" onmouseout="this.style.background=\'\'">'+
      '<span>'+ch.icon+'</span>'+
      '<span># '+ch.name+'</span>'+
      '<span style="margin-left:auto;font-size:11px;color:var(--muted)">'+((_sqMessages[ch.id]||[]).length)+'</span>'+
    '</div>';
  }).join('');
}

// Switch channel
function switchChannel(chId){
  _sqCurrentChannel = _sqChannels.find(function(c){ return c.id === chId; });
  if(!_sqCurrentChannel) return;
  document.getElementById('channel-name-display').textContent = '# '+_sqCurrentChannel.name;
  document.getElementById('channel-desc-display').textContent = _sqCurrentChannel.desc;
  renderChannelMessages();
  renderChannels();
  // Load TV widget
  if(_widgetTVVisible && _sqCurrentChannel.widgets && _sqCurrentChannel.widgets.tv){
    loadTVWidget(_sqCurrentChannel.widgets.tv);
  }
  // Load YT widget
  if(_widgetYTVisible && _sqCurrentChannel.widgets && _sqCurrentChannel.widgets.yt){
    loadYTWidget(_sqCurrentChannel.widgets.yt);
  }
}

// Render messages for current channel
function renderChannelMessages(){
  var el = document.getElementById('sq-msgs');
  if(!el || !_sqCurrentChannel) return;
  var msgs = _sqMessages[_sqCurrentChannel.id] || [];
  if(!msgs.length){
    el.innerHTML = '<div style="text-align:center;padding:40px;color:var(--muted)">暂无消息，开始聊天吧</div>';
    return;
  }
  el.innerHTML = msgs.map(function(m){
    var timeStr = new Date(m.time).toLocaleTimeString();
    var likeIcon = m.liked ? '❤️' : '🤍';
    return '<div class="sq-post" style="margin-bottom:10px">'+
      '<div class="sq-header">'+
        '<div style="display:flex;align-items:center;gap:8px">'+
          '<div class="copy-av" style="width:30px;height:30px;font-size:13px">'+(m.av||'👤')+'</div>'+
          '<div>'+
            '<span style="font-weight:600;font-size:13px">'+(m.name||'User')+'</span>'+
            '<span style="font-size:11px;color:var(--muted);margin-left:6px">'+timeStr+'</span>'+
          '</div>'+
        '</div>'+
      '</div>'+
      '<div class="sq-content" style="font-size:13px;margin:6px 0 4px 14px">'+(m.text || '')+'</div>'+
      '<div class="sq-actions" style="margin-left:14px">'+
        '<button class="sq-action" onclick="sqLikeMsg(\''+m.id+'\')" style="font-size:12px">'+likeIcon+' <span>'+m.likes+'</span></button>'+
        '<button class="sq-action" onclick="sqReplyMsg(\''+m.id+'\')" style="font-size:12px">💬 '+((m.comments||[]).length)+'</button>'+
      '</div>'+
    '</div>';
  }).join('');
  el.scrollTop = el.scrollHeight;
}

// Send message
function sendChannelMsg(){
  if(!_sqCurrentChannel) { toast('请先选择一个频道', 'warn'); return; }
  var inp = document.getElementById('sq-input');
  var text = inp.value.trim();
  if(!text) return;
  inp.value = '';
  var msg = {
    id: 'msg'+Date.now(),
    uid: 'me',
    name: localStorage.getItem('user_name') || 'User',
    av: '👤',
    text: text,
    time: Date.now(),
    likes: 0,
    liked: false,
    comments: []
  };
  if(!_sqMessages[_sqCurrentChannel.id]) _sqMessages[_sqCurrentChannel.id] = [];
  _sqMessages[_sqCurrentChannel.id].push(msg);
  saveSQData();
  renderChannelMessages();
  renderChannels();
}

// Like message
function sqLikeMsg(msgId){
  if(!_sqCurrentChannel) return;
  var msgs = _sqMessages[_sqCurrentChannel.id];
  if(!msgs) return;
  var m = msgs.find(function(x){ return x.id === msgId; });
  if(!m) return;
  if(m.liked){
    m.liked = false;
    m.likes = Math.max(0, m.likes - 1);
  } else {
    m.liked = true;
    m.likes = (m.likes || 0) + 1;
  }
  saveSQData();
  renderChannelMessages();
}

// Reply / comment on a message
function sqReplyMsg(msgId){
  var reply = prompt('输入回复内容:');
  if(!reply || !reply.trim()) return;
  if(!_sqCurrentChannel) return;
  var msgs = _sqMessages[_sqCurrentChannel.id];
  if(!msgs) return;
  var m = msgs.find(function(x){ return x.id === msgId; });
  if(!m){
    m = {id:msgId, comments:[]};
    msgs.push(m);
  }
  if(!m.comments) m.comments = [];
  m.comments.push({text:reply.trim(), time:Date.now(), name:localStorage.getItem('user_name') || 'User'});
  saveSQData();
  renderChannelMessages();
}

// Share current TV chart snapshot
function sqShareChart(){
  if(!_widgetTVVisible || !_tvWidget){
    toast('请先打开图表', 'warn');
    return;
  }
  if(!_sqCurrentChannel) return;
  var msg = {
    id: 'msg'+Date.now(),
    uid: 'me',
    name: localStorage.getItem('user_name') || 'User',
    av: '👤',
    text: '📈 分享了当前图表 ['+(_sqCurrentChannel.widgets && _sqCurrentChannel.widgets.tv||'BTCUSDT')+']',
    time: Date.now(),
    likes: 0,
    liked: false,
    comments: [],
    isChart: true
  };
  if(!_sqMessages[_sqCurrentChannel.id]) _sqMessages[_sqCurrentChannel.id] = [];
  _sqMessages[_sqCurrentChannel.id].push(msg);
  saveSQData();
  renderChannelMessages();
  renderChannels();
  toast('✅ 图表已分享到频道', 'success');
}

// Attach image
function sqAttachImage(){
  var inp = document.createElement('input');
  inp.type = 'file';
  inp.accept = 'image/*';
  inp.onchange = function(){
    var file = inp.files[0];
    if(!file || !_sqCurrentChannel) return;
    var reader = new FileReader();
    reader.onload = function(e){
      var msg = {
        id: 'msg'+Date.now(),
        uid: 'me',
        name: localStorage.getItem('user_name') || 'User',
        av: '👤',
        text: '🖼️ <img src="'+e.target.result+'" style="max-width:300px;border-radius:8px">',
        time: Date.now(),
        likes: 0,
        liked: false,
        comments: [],
        isImage: true
      };
      if(!_sqMessages[_sqCurrentChannel.id]) _sqMessages[_sqCurrentChannel.id] = [];
      _sqMessages[_sqCurrentChannel.id].push(msg);
      saveSQData();
      renderChannelMessages();
      renderChannels();
    };
    reader.readAsDataURL(file);
  };
  inp.click();
}

// Create channel
function createChannel(){
  var name = prompt('输入频道名称:');
  if(!name || !name.trim()) return;
  var icon = prompt('输入频道图标(如 🌐, ₿, 📊):') || '💬';
  var desc = prompt('输入频道描述:') || '';
  var id = 'ch-'+name.toLowerCase().replace(/\\s+/g,'-').replace(/[^a-z0-9\\-]/g,'');
  if(_sqChannels.find(function(c){ return c.id === id; })){
    toast('频道已存在', 'warn'); return;
  }
  _sqChannels.push({id:id, name:name.trim(), desc:desc, icon:icon, widgets:{tv:'BTCUSDT', yt:''}});
  _sqMessages[id] = [];
  saveSQData();
  renderChannels();
  switchChannel(id);
  toast('✅ #'+name.trim()+' 频道已创建', 'success');
}

// Widget: TradingView
function loadTVWidget(symbol){
  var container = document.getElementById('widget-tv');
  if(!container || _widgetTVVisible === false) { container.innerHTML = ''; return; }
  if(typeof TradingView === 'undefined'){
    var s = document.createElement('script');
    s.src = 'https://s3.tradingview.com/tv.js';
    s.onload = function(){ initTVWidget(symbol || 'BINANCE:BTCUSDT'); };
    document.head.appendChild(s);
  } else {
    initTVWidget(symbol || 'BINANCE:BTCUSDT');
  }
}
function initTVWidget(symbol){
  var container = document.getElementById('widget-tv');
  if(!container) return;
  container.innerHTML = '';
  try{
    _tvWidget = new TradingView.widget({
      container_id: 'widget-tv',
      symbol: symbol.indexOf(':') > 0 ? symbol : 'BINANCE:'+symbol,
      interval: '60',
      theme: 'dark',
      style: '1',
      locale: 'zh_CN',
      toolbar_bg: '#1a1a2e',
      enable_publishing: true,
      allow_symbol_change: true,
      hide_top_toolbar: false,
      save_image: true,
      width: '100%',
      height: '100%',
      studies: ['RSI@tv-basicstudies', 'MASimple@tv-basicstudies'],
      disabled_features: ['use_localstorage_for_settings', 'go_to_date', 'header_symbol_search'],
      enabled_features: ['study_templates']
    });
  } catch(e){
    console.warn('TV widget error:', e);
  }
}
function toggleChannelWidget(type){
  if(type === 'tv'){
    _widgetTVVisible = !_widgetTVVisible;
    document.getElementById('widget-tv').style.display = _widgetTVVisible ? 'block' : 'none';
    document.getElementById('tv-widget-btn').style.background = _widgetTVVisible ? 'rgba(0,200,150,.2)' : 'transparent';
    document.getElementById('tv-widget-btn').style.color = _widgetTVVisible ? 'var(--green)' : 'var(--muted)';
    if(_widgetTVVisible && _sqCurrentChannel && _sqCurrentChannel.widgets){
      loadTVWidget(_sqCurrentChannel.widgets.tv);
    }
  } else if(type === 'youtube'){
    _widgetYTVisible = !_widgetYTVisible;
    document.getElementById('widget-youtube').style.display = _widgetYTVisible ? 'block' : 'none';
    document.getElementById('yt-widget-btn').style.background = _widgetYTVisible ? 'rgba(0,200,150,.2)' : 'transparent';
    document.getElementById('yt-widget-btn').style.color = _widgetYTVisible ? 'var(--green)' : 'var(--muted)';
    if(_widgetYTVisible && _sqCurrentChannel && _sqCurrentChannel.widgets){
      loadYTWidget(_sqCurrentChannel.widgets.yt);
    }
  }
}

// Widget: YouTube
function loadYTWidget(ytUrl){
  var container = document.getElementById('youtube-player');
  if(!container) return;
  if(!ytUrl){
    // Default quant trading education video
    var defaultId = 'jfKfPfyJRdk';
    container.innerHTML = '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/'+defaultId+'?autoplay=0&rel=0&modestbranding=1&showinfo=0&iv_load_policy=3" frameborder="0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen style="border-radius:8px"></iframe>';
    return;
  }
  var videoId = ytUrl;
  // Extract video ID from URL
  var match = ytUrl.match(/(?:youtube\\.com\\/(?:watch\\?v=|embed\\/|v\\/)|youtu\\.be\\/)([a-zA-Z0-9_-]{11})/);
  if(match) videoId = match[1];
  container.innerHTML = '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/'+videoId+'?autoplay=0&rel=0&modestbranding=1&showinfo=0&iv_load_policy=3" frameborder="0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen style="border-radius:8px"></iframe>';
}

// Init QuantTalk
function initQuantTalk(){
  loadSQData();
  renderChannels();
  if(_sqChannels.length > 0) switchChannel(_sqChannels[0].id);
}

// WALLET FUNCTIONS
function connectWallet(){
  var sel = document.getElementById('wallet-select');
  var walletType = sel.value;
  if(!walletType){
    toast('请先选择钱包类型', 'warn');
    return;
  }
  if(walletType === 'metamask'){
    if(typeof window.ethereum !== 'undefined'){
      window.ethereum.request({method: 'eth_requestAccounts'}).then(function(accounts){
        showWalletConnected('metamask', accounts[0]);
      }).catch(function(e){
        toast('连接失败: '+e.message, 'warn');
      });
    } else {
      toast('未检测到 MetaMask，请安装扩展', 'warn');
      showManualInput('metamask');
    }
  } else if(walletType === 'okx'){
    if(typeof window.okxwallet !== 'undefined'){
      window.okxwallet.request({method: 'eth_requestAccounts'}).then(function(accounts){
        showWalletConnected('okx', accounts[0]);
      }).catch(function(e){
        toast('连接失败: '+e.message, 'warn');
      });
    } else {
      toast('未检测到 OKX Wallet，请安装扩展或使用手动输入', 'warn');
      showManualInput('okx');
    }
  } else if(walletType === 'trustwallet'){
    if(typeof window.trustwallet !== 'undefined'){
      window.trustwallet.request({method: 'eth_requestAccounts'}).then(function(accounts){
        showWalletConnected('trustwallet', accounts[0]);
      }).catch(function(e){
        toast('连接失败: '+e.message, 'warn');
      });
    } else {
      toast('未检测到 Trust Wallet，请安装扩展或使用手动输入', 'warn');
      showManualInput('trustwallet');
    }
  } else if(walletType === 'walletconnect'){
    toast('WalletConnect 功能即将上线，请先使用手动输入', 'warn');
    showManualInput('walletconnect');
  } else if(walletType === 'exchange'){
    showManualInput('exchange');
  } else if(walletType === 'cold'){
    showManualInput('cold');
  }
}
function showManualInput(type){
  document.getElementById('wallet-connect-area').style.display = 'none';
  var inputArea = document.getElementById('wallet-manual-input');
  inputArea.style.display = 'block';
  inputArea.dataset.walletType = type;
}
function saveManualWallet(){
  var addr = document.getElementById('wallet-manual-address').value.trim();
  if(!addr){
    toast('请输入钱包地址', 'warn');
    return;
  }
  var type = document.getElementById('wallet-manual-input').dataset.walletType || 'manual';
  showWalletConnected(type, addr);
}
function showWalletConnected(type, address){
  var names = {metamask:'🦊 MetaMask', walletconnect:'🔗 WalletConnect', trustwallet:'🛡️ Trust Wallet', okx:'🔶 OKX Wallet', exchange:'🏛️ 交易所钱包', cold:'❄️ 冷钱包'};
  document.getElementById('wallet-connect-area').style.display = 'none';
  document.getElementById('wallet-manual-input').style.display = 'none';
  document.getElementById('wallet-address-area').style.display = 'block';
  document.getElementById('wallet-display-address').textContent = address;
  document.getElementById('wallet-type-badge').textContent = names[type] || type;
  localStorage.setItem('wallet_type', type);
  localStorage.setItem('wallet_address', address);
  // Add to history
  var hist = JSON.parse(localStorage.getItem('wallet_history') || '[]');
  hist.unshift({type: names[type] || type, address: address, time: new Date().toLocaleString()});
  localStorage.setItem('wallet_history', JSON.stringify(hist));
  renderWalletHistory();
  toast('✅ 钱包已绑定: '+address.substring(0,10)+'...', 'success');
}
function disconnectWallet(){
  if(!confirm('确认断开钱包连接?')) return;
  document.getElementById('wallet-address-area').style.display = 'none';
  document.getElementById('wallet-connect-area').style.display = 'block';
  localStorage.removeItem('wallet_type');
  localStorage.removeItem('wallet_address');
  toast('钱包已断开', '');
}
function renderWalletHistory(){
  var el = document.getElementById('wallet-history');
  var list = document.getElementById('wallet-history-list');
  if(!el || !list) return;
  var hist = JSON.parse(localStorage.getItem('wallet_history') || '[]');
  if(!hist.length){ el.style.display = 'none'; return; }
  el.style.display = 'block';
  list.innerHTML = hist.slice(0,5).map(function(h){
    return '<div style="font-size:12px;padding:6px 0;border-bottom:1px solid var(--border)">'+
      '<span style="color:var(--muted)">'+h.time+'</span> '+
      '<span>'+h.type+'</span> '+
      '<span style="color:var(--green);font-family:monospace">'+h.address.substring(0,8)+'...'+h.address.slice(-4)+'</span>'+
    '</div>';
  }).join('');
}

// Override existing functions to prevent conflict
window.sqLike = window.sqLike || function(){};
window.sqComment = window