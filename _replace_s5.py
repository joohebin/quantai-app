# -*- coding: utf-8 -*-
"""Complete rewrite of independent CS Widget with all exports on window"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find S5 and replace it entirely
s5_start = t.rfind('<script>', 0, t.rfind('</script>', t.rfind('</body>')))
s5_end = t.find('</script>', s5_start) + 9
print(f'S5 bounds: {s5_start}-{s5_end}')

# Verify it's the right script
content = t[s5_start:s5_end]
if 'CS Widget - 完全独立' not in content:
    print('ERROR: Cannot find independent CS Widget script')
    exit(1)

new_s5 = '''<script>
// ============================================================
// CS Widget - 完全独立实现（所有函数绑定到 window）
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
  if(!_CS_CONFIG.groqKey || _CS_CONFIG.groqKey === 'USE_OWN') _CS_CONFIG.groqKey = '';
  if(!_CS_CONFIG.model) _CS_CONFIG.model = 'llama-3.3-70b-versatile';
  if(!_CS_CONFIG.maxTokens) _CS_CONFIG.maxTokens = 1024;
  if(!_CS_CONFIG.greetDelay) _CS_CONFIG.greetDelay = 500;
  if(!_CS_CONFIG.apiUrl) _CS_CONFIG.apiUrl = 'https://api.groq.com/openai/v1/chat/completions';
  
  // ---- 所有函数都绑定到 window ----
  
  window.toggleCS = function toggleCS(){
    _csOpen = !_csOpen;
    var panel = document.getElementById('cs-panel');
    if(!panel) return;
    if(_csOpen){
      panel.classList.add('open');
      var fab = document.getElementById('cs-fab');
      if(fab) fab.innerHTML = '💬';
      setTimeout(function(){ if(typeof window.csGreet === 'function') window.csGreet(); }, _CS_CONFIG.greetDelay);
      setTimeout(function(){ var inp=document.getElementById('cs-input'); if(inp) inp.focus(); }, 300);
    } else {
      panel.classList.remove('open');
      var fab = document.getElementById('cs-fab');
      if(fab) fab.innerHTML = '💬<span class="cs-badge" id="cs-badge" style="display:none"></span>';
    }
  };
  
  window.csGreet = function(){
    window.csAddMsg('bot', '👋 **你好！我是 QuantAI 客服助手。**\\\\n\\\\n我可以帮您解答平台功能、套餐升级、故障排查等问题。\\\\n\\\\n请问有什么可以帮您？');
  };
  
  window.csAddMsg = function(role, text){
    var msgs = document.getElementById('cs-msgs');
    if(!msgs) return;
    var div = document.createElement('div');
    div.className = 'cs-msg cs-' + role;
    div.innerHTML = '<div class="cs-bubble">' + text + '</div>';
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    var badge = document.getElementById('cs-badge');
    if(badge) badge.style.display = 'none';
  };
  
  window.csFormatText = function(t){
    return t.replace(/\\\\n/g, '<br>').replace(/\\\\*\\\\*(.+?)\\\\*\\\\*/g, '<strong>$1</strong>');
  };
  
  window.csShowTyping = function(){
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
  };
  
  window.csHideTyping = function(){
    var el = document.getElementById('cs-typing');
    if(el) el.remove();
  };
  
  window.csSendQuick = function(el){
    var text = el.textContent;
    document.getElementById('cs-input').value = text;
    if(typeof window.csDoSend === 'function') window.csDoSend();
  };
  
  window.csLocalReply = function(text){
    var replies = ['感谢您的咨询！我们会尽快为您处理。','好的，我理解您的需求。让我为您查询相关信息。','收到您的消息！我们的客服团队正在为您处理。','感谢您的耐心等待。请问您还有其他问题吗？'];
    return replies[Math.floor(Math.random() * replies.length)];
  };
  
  window.csFetchGroq = function(messages){
    return new Promise(function(resolve, reject){
      var xhr = new XMLHttpRequest();
      xhr.open('POST', _CS_CONFIG.apiUrl);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('Authorization', 'Bearer ' + _CS_CONFIG.groqKey);
      xhr.onload = function(){
        if(xhr.status === 200){
          try{ var data = JSON.parse(xhr.responseText); resolve(data.choices[0].message.content); }
          catch(e){ reject('Parse error: ' + e.message); }
        } else { reject('HTTP ' + xhr.status); }
      };
      xhr.onerror = function(){ reject('Network error'); };
      xhr.send(JSON.stringify({ model: _CS_CONFIG.model, messages: messages, max_tokens: _CS_CONFIG.maxTokens, temperature: 0.7 }));
    });
  };
  
  window.csShowHandoff = function(){
    window.csAddMsg('bot', '正在为您转接人工客服，请稍候...');
  };
  
  window.csGoHuman = function(){
    window.csShowHandoff();
  };
  
  window.csSendMessage = function(msg){
    document.getElementById('cs-input').value = msg;
    if(typeof window.csDoSend === 'function') window.csDoSend();
  };
  
  // csDoSend uses closure for _csSending, _CS_CONFIG, etc.
  window.csDoSend = async function(){
    if(_csSending) return;
    var inp = document.getElementById('cs-input');
    var text = inp.value.trim();
    if(!text) return;
    inp.value = '';
    inp.style.height = 'auto';
    window.csAddMsg('user', text);
    var sendBtn = document.getElementById('cs-send');
    if(sendBtn) sendBtn.disabled = true;
    window.csShowTyping();
    
    var reply;
    if(typeof window.csFetchGroqGateway === 'function'){
      var result = await window.csFetchGroqGateway(text);
      reply = (result !== null && result !== undefined) ? result : window.csLocalReply(text);
    } else if(_CS_CONFIG.groqKey){
      try{
        var history = [];
        var msgEls = document.querySelectorAll('#cs-msgs .cs-msg');
        for(var i=0;i<msgEls.length;i++){
          var role = msgEls[i].classList.contains('cs-user') ? 'user' : 'assistant';
          var bubble = msgEls[i].querySelector('.cs-bubble');
          if(bubble) history.push({role: role, content: bubble.textContent || bubble.innerText});
        }
        reply = await window.csFetchGroq(history);
      }catch(e){
        console.warn('[CS] Groq failed:', e);
        reply = window.csLocalReply(text);
      }
    } else {
      reply = window.csLocalReply(text);
    }
    
    window.csHideTyping();
    if(reply && reply.trim()){
      reply = reply.replace(/\\\\n/g, '<br>').replace(/\\\\*\\\\*(.+?)\\\\*\\\\*/g, '<strong>$1</strong>');
      window.csAddMsg('bot', reply);
    }
    if(sendBtn) sendBtn.disabled = false;
  };
  
  // Register keyboard handler on load
  window.addEventListener('load', function(){
    var inp = document.getElementById('cs-input');
    if(inp){
      inp.addEventListener('keydown', function(e){
        if(e.key === 'Enter' && !e.shiftKey){ e.preventDefault(); if(typeof window.csDoSend === 'function') window.csDoSend(); }
      });
    }
  });
  
  console.log('[CS] Independent Widget loaded. toggleCS=' + typeof window.toggleCS + ' csGreet=' + typeof window.csGreet);
})();
</script>'''

# Verify new S5 has valid syntax
import subprocess
with open('/tmp/s5_check.js', 'w', encoding='utf-8') as f:
    f.write(new_s5.replace('<script>', '').replace('</script>', '').strip())
result = subprocess.run(['node', '--check', '/tmp/s5_check.js'], capture_output=True, text=True, timeout=10)
print(f'Node check: {result.returncode} - {"OK" if result.returncode == 0 else result.stderr[:300]}')

t = t[:s5_start] + new_s5 + t[s5_end:]

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))
print(f'File: {len(t)/1024:.1f} KB')
print('Replaced S5 with window-exported CS Widget')
