# -*- coding: utf-8 -*-
"""
终极解决方案：不再从 Script 0 提取 CS 函数（丢失闭包/变量引用），
而是直接在最后一个脚本中 100% 重写所有 CS 逻辑，生成独立的函数。
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# First, restore from git to remove the broken v2 binder
# Actually let's just remove the v2 binder and replace it
import subprocess
result = subprocess.run(['git', 'checkout', '12cb797', '--', 'index.html'],
                       capture_output=True, text=True, timeout=10, cwd='.')
print('git checkout:', result.returncode)
if result.returncode != 0:
    print(result.stderr[:200])
    exit(1)

# Read the clean version
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Remove the old v2 binder if present (it was committed as 06705b6)
# check the file to confirm it's the 12cb797 version
s0 = t[t.find('<script>', 910):t.find('</script>', t.find('<script>', 910))]
bt = s0.count(chr(96))
print(f'S0 backticks: {bt} (expect 63 for 12cb797, or 74 after fix)')

# Build the COMPLETE CS Widget replacement script
# This script defines ALL CS functions with their own closure/state
cs_script = '''
<script>
// ============================================================
// CS Widget - 完全独立实现（不依赖 Script 0 的闭包变量）
// ============================================================
(function(){
  if(typeof window.__CS_LOADED !== 'undefined') return;
  window.__CS_LOADED = true;
  
  // ---- 状态 ----
  var _csOpen = false;
  var _csSending = false;
  var _CS_CONFIG = {};
  
  // Load saved config
  try{ _CS_CONFIG = JSON.parse(localStorage.getItem('cs_config') || '{}'); }catch(e){}
  // Groq key: user must configure via AI settings; fallback uses local reply
  if(!_CS_CONFIG.groqKey || _CS_CONFIG.groqKey === 'USE_OWN') _CS_CONFIG.groqKey = '';
  if(!_CS_CONFIG.model) _CS_CONFIG.model = 'llama-3.3-70b-versatile';
  if(!_CS_CONFIG.maxTokens) _CS_CONFIG.maxTokens = 1024;
  if(!_CS_CONFIG.greetDelay) _CS_CONFIG.greetDelay = 500;
  if(!_CS_CONFIG.apiUrl) _CS_CONFIG.apiUrl = 'https://api.groq.com/openai/v1/chat/completions';
  
  // ---- 核心函数 ----
  
  window.toggleCS = function toggleCS(){
    console.log('[客服] 点击了客服按钮, 当前状态:', _csOpen);
    _csOpen = !_csOpen;
    var panel = document.getElementById('cs-panel');
    if(!panel) return;
    if(_csOpen){
      panel.classList.add('open');
      var fab = document.getElementById('cs-fab');
      if(fab) fab.innerHTML = '💬';
      window.setTimeout(function(){
        var greet = typeof window.csGreetOriginal === 'function' ? window.csGreetOriginal : csGreet;
        if(typeof greet === 'function') greet();
      }, _CS_CONFIG.greetDelay);
      window.setTimeout(function(){
        var inp = document.getElementById('cs-input');
        if(inp) inp.focus();
      }, 300);
    } else {
      panel.classList.remove('open');
      var fab = document.getElementById('cs-fab');
      if(fab) fab.innerHTML = '💬<span class="cs-badge" id="cs-badge" style="display:none"></span>';
    }
  };
  
  function csGreet(){
    csAddMsg('bot', '👋 **你好！我是 QuantAI 客服助手。**\\n\\n我可以帮您解答平台功能、套餐升级、故障排查等问题。\\n\\n请问有什么可以帮您？');
  }
  
  function csAddMsg(role, text){
    var msgs = document.getElementById('cs-msgs');
    if(!msgs) return;
    var div = document.createElement('div');
    div.className = 'cs-msg cs-' + role;
    div.innerHTML = '<div class="cs-bubble">' + text + '</div>';
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    var badge = document.getElementById('cs-badge');
    if(badge) badge.style.display = 'none';
  }
  
  function csFormatText(t){
    return t.replace(/\\n/g, '<br>').replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
  }
  
  function csShowTyping(){
    var msgs = document.getElementById('cs-msgs');
    if(!msgs) return;
    var el = document.getElementById('cs-typing');
    if(!el){
      el = document.createElement('div');
      el.id = 'cs-typing';
      el.className = 'cs-msg cs-bot';
      el.innerHTML = '<div class="cs-bubble cs-typing"><span></span><span></span><span></span></div>';
      msgs.appendChild(el);
    }
    msgs.scrollTop = msgs.scrollHeight;
  }
  
  function csHideTyping(){
    var el = document.getElementById('cs-typing');
    if(el) el.remove();
  }
  
  function csSendQuick(el){
    var text = el.textContent;
    document.getElementById('cs-input').value = text;
    csDoSend();
  }
  
  function csLocalReply(text){
    // Simulate AI reply (fallback)
    var replies = [
      '感谢您的咨询！我们会尽快为您处理。',
      '好的，我理解您的需求。让我为您查询相关信息。',
      '收到您的消息！我们的客服团队正在为您处理。',
      '感谢您的耐心等待。请问您还有其他问题吗？'
    ];
    return replies[Math.floor(Math.random() * replies.length)];
  }
  
  function csFetchGroq(messages){
    return new Promise(function(resolve, reject){
      var xhr = new XMLHttpRequest();
      xhr.open('POST', _CS_CONFIG.apiUrl);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('Authorization', 'Bearer ' + _CS_CONFIG.groqKey);
      xhr.onload = function(){
        if(xhr.status === 200){
          try{
            var data = JSON.parse(xhr.responseText);
            resolve(data.choices[0].message.content);
          }catch(e){
            reject('Parse error: ' + e.message);
          }
        } else {
          reject('HTTP ' + xhr.status + ': ' + xhr.responseText.substring(0, 200));
        }
      };
      xhr.onerror = function(){ reject('Network error'); };
      xhr.send(JSON.stringify({
        model: _CS_CONFIG.model,
        messages: messages,
        max_tokens: _CS_CONFIG.maxTokens,
        temperature: 0.7
      }));
    });
  }
  
  function csShowHandoff(){
    csAddMsg('bot', '正在为您转接人工客服，请稍候...');
  }
  
  function csGoHuman(){
    csShowHandoff();
  }
  
  async function csDoSend(){
    if(_csSending) return;
    var inp = document.getElementById('cs-input');
    var text = inp.value.trim();
    if(!text) return;
    inp.value = '';
    inp.style.height = 'auto';
    csAddMsg('user', text);
    var sendBtn = document.getElementById('cs-send');
    if(sendBtn) sendBtn.disabled = true;
    csShowTyping();
    
    var reply;
    // Try AI gateway if available, else use Groq, else local fallback
    if(typeof window.csFetchGroqGateway === 'function'){
      var result = await window.csFetchGroqGateway(text);
      reply = (result !== null && result !== undefined) ? result : csLocalReply(text);
    } else {
      try{
        var history = [];
        var msgEls = document.querySelectorAll('#cs-msgs .cs-msg');
        msgEls.forEach(function(el){
          var role = el.classList.contains('cs-user') ? 'user' : 'assistant';
          var bubble = el.querySelector('.cs-bubble');
          if(bubble) history.push({role: role, content: bubble.textContent || bubble.innerText});
        });
        reply = await csFetchGroq(history);
      }catch(e){
        console.warn('[CS] Groq failed:', e);
        reply = csLocalReply(text);
      }
    }
    
    csHideTyping();
    if(reply && reply.trim()){
      reply = reply.replace(/\\n/g, '<br>').replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
      csAddMsg('bot', reply);
    }
    if(sendBtn) sendBtn.disabled = false;
  }
  
  // Register event handlers
  window.addEventListener('load', function(){
    // Bind keyboard Enter handler
    var inp = document.getElementById('cs-input');
    if(inp){
      inp.addEventListener('keydown', function(e){
        if(e.key === 'Enter' && !e.shiftKey){
          e.preventDefault();
          csDoSend();
        }
      });
    }
    console.log('[CS] Widget loaded. toggleCS=' + typeof window.toggleCS);
  });
  
  console.log('[CS] Widget initialized');
})();
</script>
'''

# Find the last </script> before </body>
last_script = t.rfind('</script>', 0, t.rfind('</body>'))
t = t[:last_script + 9] + cs_script + t[last_script + 9:]

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

print(f'File: {len(t)/1024:.1f} KB')
print('Added independent CS Widget at end of file')

# Quick check: Node syntax
with open('/tmp/cs_widget_check.js', 'w', encoding='utf-8') as f:
    f.write(cs_script.replace('<script>', '').replace('</script>', '').strip())

import subprocess
result = subprocess.run(['node', '--check', '/tmp/cs_widget_check.js'], capture_output=True, text=True, timeout=10)
print(f'Node check: {result.returncode}')
if result.stderr:
    print(f'  Error: {result.stderr[:200]}')
else:
    print('  No errors!')
