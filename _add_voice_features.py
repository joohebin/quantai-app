"""
Add to index.html:
1. TTS reply (SpeechSynthesis) for CS Widget — auto-speak AI replies
2. Voice order parsing (NLP → trade commands)
"""
import os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
TMP = os.environ.get('TEMP', '/tmp')

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# === Voice features JS — to insert before // Friend System ===
voice_features = r'''

// ---- TTS: AI voice reply (SpeechSynthesis) ----
var _lastVoiceInput = null;
function speakText(text, lang){
  if(!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  var u = new SpeechSynthesisUtterance(text);
  u.lang = lang || 'zh-CN';
  u.rate = 1.0;
  u.pitch = 1.0;
  try{
    var voices = window.speechSynthesis.getVoices();
    var cn = voices.find(function(v){ return v.lang.startsWith('zh'); });
    if(cn) u.voice = cn;
  }catch(e){}
  window.speechSynthesis.speak(u);
}
function onVoiceInputDetected(){
  _lastVoiceInput = Date.now();
}

// ---- Voice Order Parser ----
var _tradeCommands = {
  actions: {
    '\u4e70\u5165': 'buy', '\u4e70': 'buy', '\u591a': 'buy',
    '\u5356\u51fa': 'sell', '\u5356': 'sell', '\u7a7a': 'sell',
    '\u5f00\u591a': 'buy', '\u5f00\u7a7a': 'sell', '\u5e73\u4ed3': 'close',
    '\u5e73\u591a': 'close_buy', '\u5e73\u7a7a': 'close_sell',
    '\u505c\u635f': 'stop', '\u6b62\u635f': 'stop',
    '\u6302\u5355': 'limit', '\u9650\u4ef7': 'limit'
  },
  amounts: {
    '\u5168\u90e8': 'all', '\u5168\u4ed3': 'all',
    '\u4e00\u624b': 1, '\u4e24\u624b': 2, '\u4e09\u624b': 3,
    '\u5341\u624b': 10, '\u767e\u5206\u4e4b\u5341': 0.1,
    '\u767e\u5206\u4e4b\u4e8c\u5341': 0.2, '\u767e\u5206\u4e4b\u4e94\u5341': 0.5,
    '\u767e\u5206\u4e4b\u4e00\u767e': 1.0
  },
  symbols: {
    '\u6bd4\u7279\u5e01': 'BTCUSDT', 'btc': 'BTCUSDT', '\u5927\u9526': 'BTCUSDT',
    '\u4ee5\u592a\u574a': 'ETHUSDT', 'eth': 'ETHUSDT', '\u4e8c\u9526': 'ETHUSDT',
    '\u73b0\u8d27': 'spot', '\u5408\u7ea6': 'futures'
  }
};

function parseVoiceOrder(text){
  if(!text || text.trim().length < 2) return null;
  text = text.toLowerCase().trim();
  
  var result = { action: null, symbol: null, amount: null, price: null, type: 'market' };
  
  // Parse action
  for(var key in _tradeCommands.actions){
    if(text.indexOf(key) >= 0){
      result.action = _tradeCommands.actions[key];
      break;
    }
  }
  if(!result.action) return null;
  
  // Parse symbol
  for(var key in _tradeCommands.symbols){
    if(text.indexOf(key) >= 0){
      result.symbol = _tradeCommands.symbols[key];
      break;
    }
  }
  
  // Parse amount
  for(var key in _tradeCommands.amounts){
    if(text.indexOf(key) >= 0){
      result.amount = _tradeCommands.amounts[key];
      break;
    }
  }
  
  // Parse price (number after 'at' or '@')
  var priceMatch = text.match(/(?:at|@|price|价)\s*(\d+(?:\.\d+)?)/i);
  if(priceMatch) result.price = parseFloat(priceMatch[1]);
  
  // Parse limit order
  if(text.indexOf('limit') >= 0 || text.indexOf('限价') >= 0 || text.indexOf('挂') >= 0){
    result.type = 'limit';
  }
  
  return result;
}

function showVoiceOrderConfirm(order){
  if(!order) return;
  var texts = [];
  texts.push('📋 <b>\u8bed\u97f3\u4e0b\u5355\u786e\u8ba4</b>');
  texts.push('<hr style="border-color:var(--border);margin:8px 0">');
  var actionMap = {buy:'🟢 \u4e70\u5165', sell:'🔴 \u5356\u51fa', close:'🔵 \u5e73\u4ed3', close_buy:'🔵 \u5e73\u591a', close_sell:'🔵 \u5e73\u7a7a'};
  texts.push((actionMap[order.action] || order.action) + ' ' + (order.symbol || '??'));
  if(order.amount) texts.push('数量: ' + (typeof order.amount === 'number' ? order.amount + ' 手' : order.amount));
  if(order.price) texts.push('价格: ' + order.price);
  texts.push('类型: ' + (order.type === 'limit' ? '限价单' : '市价单'));
  texts.push('<hr style="border-color:var(--border);margin:8px 0">');
  texts.push('<button onclick="executeVoiceOrder(\'' + JSON.stringify(order).replace(/'/g, "\\'") + '\')" style="padding:6px 14px;border:none;border-radius:8px;background:var(--green);color:#fff;cursor:pointer;font-size:13px">✅ \u786e\u8ba4\u4e0b\u5355</button>');
  texts.push('<button onclick="document.getElementById(\'voice-order-confirm\').remove()" style="padding:6px 14px;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--muted);cursor:pointer;font-size:13px;margin-left:8px">❌ \u53d6\u6d88</button>');
  
  var d = document.createElement('div');
  d.id = 'voice-order-confirm';
  d.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:var(--card);border:1px solid var(--green);border-radius:12px;padding:16px;z-index:9999;max-width:320px;width:90%;font-size:13px;box-shadow:0 4px 20px rgba(0,0,0,.4)';
  d.innerHTML = texts.join('');
  document.body.appendChild(d);
}

function executeVoiceOrder(orderStr){
  var order = JSON.parse(orderStr);
  var d = document.getElementById('voice-order-confirm');
  if(d) d.remove();
  
  // Send to chat as trade signal
  var symbol = order.symbol || 'BTCUSDT';
  var side = order.action === 'buy' ? 'BUY' : 'SELL';
  var msg = '📊 <b>\u8bed\u97f3\u4e0b\u5355\u5df2\u53d1\u9001</b>\n' +
    side + ' ' + symbol +
    (order.amount ? ' x' + order.amount : '') +
    (order.price ? ' @ ' + order.price : '') +
    ' [' + order.type.toUpperCase() + ']';
  
  toast(msg);
  
  // If in a channel, send a trade message
  if(typeof _sqCurrentChannel !== 'undefined'){
    window.sendTradeSignal(order);
  }
}

// Patch startVoiceInput to detect voice input and parse orders
var _origStartVoiceInput = window.startVoiceInput;
if(_origStartVoiceInput){
  window.startVoiceInput = function(inputId){
    var btn = inputId === 'sq-input' ? document.getElementById('qt-voice-btn') : document.getElementById('voice-btn');
    if(!btn) btn = document.getElementById('voice-btn');
    
    if(window._voiceListening){
      if(window._voiceRecognition) window._voiceRecognition.stop();
      if(btn) btn.textContent = '\U0001f399\ufe0f';
      if(btn) btn.style.color = '';
      window._voiceListening = false;
      return;
    }
    
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if(!SR){
      alert('\u60a8\u7684\u6d4f\u89c8\u5668\u4e0d\u652f\u6301\u8bed\u97f3\u8bc6\u522b\uff0c\u8bf7\u4f7f\u7528Chrome');
      return;
    }
    
    var recognition = new SR();
    recognition.lang = 'zh-CN';
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onstart = function(){
      window._voiceListening = true;
      if(btn) btn.textContent = '\U0001f3a4';
      if(btn) btn.style.color = 'var(--green)';
    };
    
    recognition.onresult = function(e){
      var transcript = e.results[0][0].transcript;
      var input = document.getElementById(inputId);
      if(input){
        input.value = transcript;
        // Try to parse as trade order
        var order = parseVoiceOrder(transcript);
        if(order){
          showVoiceOrderConfirm(order);
          return;
        }
        // Not a trade order, send as normal message
        onVoiceInputDetected();
        if(inputId === 'cs-input'){
          setTimeout(function(){ csDoSend(); }, 200);
        } else if(inputId === 'sq-input'){
          setTimeout(function(){ sendMsg(); }, 200);
        }
      }
    };
    
    recognition.onerror = function(e){
      console.log('Voice error:', e.error);
      if(btn) btn.textContent = '\U0001f399\ufe0f';
      if(btn) btn.style.color = '';
      window._voiceListening = false;
    };
    
    recognition.onend = function(){
      window._voiceListening = false;
      if(btn) btn.textContent = '\U0001f399\ufe0f';
      if(btn) btn.style.color = '';
    };
    
    window._voiceRecognition = recognition;
    recognition.start();
  };
}
'''

# Insert before // Friend System
fs_idx = t.find('// Friend System JS - read by')
if fs_idx < 0:
    print('Friend System NOT FOUND')
    exit(1)

# Remove old voice input code first (replace with new version)
old_voice_start = t.find('// ---- Voice Input')
old_voice_end = t.find('// ---- Voice Input', old_voice_start + 100)
if old_voice_end < 0:
    # There might be only one block
    old_voice_end = t.find('// Friend System') - 5
    if old_voice_end < 0:
        old_voice_end = fs_idx
    else:
        # Find the end of the old voice code
        pass

# Old voice code is everything from '// ---- Voice Input' to before '// Friend System'
old_voice_end = t.rfind('\n', 0, fs_idx - 2)

# Try to find the voice block more precisely
vstart = t.find('// ---- Voice Input')
vend = t.rfind('\n', 0, fs_idx - 2)
if vstart >= 0:
    old_block = t[vstart:vend]
    t = t[:vstart] + voice_features + t[fs_idx:]
else:
    t = t[:fs_idx] + voice_features + '\n' + t[fs_idx:]

# Write
r = t.encode('utf-8')
with open(filepath, 'wb') as f:
    f.write(r)
print(f'File saved: {len(r)} bytes')

# Syntax check
s2_start = t.find('// ===== \u5168\u5c40\u72b6\u6001')
script_open = t.rfind('<script>', max(0, s2_start-100), s2_start)
script_close = t.find('</script>', script_open + 8)
js = t[script_open+8:script_close]
with open(os.path.join(TMP, 'sc.js'), 'w', encoding='utf-8') as f:
    f.write(js)
res = subprocess.run(['node', '--check', os.path.join(TMP, 'sc.js')], capture_output=True, timeout=15)
if res.returncode == 0:
    print('Syntax OK!')
else:
    err = res.stderr.decode('utf-8', errors='replace')[:800]
    print(f'ERROR:\n{err}')
    # Restore
    with open(filepath, 'wb') as f:
        f.write(r)
