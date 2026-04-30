# -*- coding: utf-8 -*-
"""
Fix csDoSend in CS Widget: properly handle async XHR with Promise
and read user's AI provider/key from localStorage.
Uses csFetchGroq-style Promise wrapping for both DeepSeek and Groq.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

s5_start = t.rfind('<script>', 0, t.rfind('</script>', t.rfind('</body>')))
s5_end = t.find('</script>', s5_start) + 9
s5 = t[s5_start:s5_end]

old_func_start = s5.find('  window.csDoSend = async function(){')
old_func_end = s5.find('\n  // Register', old_func_start)

new_csDoSend = """  // Add ability to call any OpenAI-compatible API
  function csCallAPI(apiUrl, apiKey, body){
    return new Promise(function(resolve, reject){
      var xhr = new XMLHttpRequest();
      xhr.open('POST', apiUrl);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('Authorization', 'Bearer ' + apiKey);
      xhr.onload = function(){
        if(xhr.status === 200){
          try{ var data = JSON.parse(xhr.responseText); resolve(data.choices[0].message.content); }
          catch(e){ reject('Parse error: ' + e.message); }
        } else { reject('HTTP ' + xhr.status); }
      };
      xhr.onerror = function(){ reject('Network error'); };
      xhr.send(JSON.stringify(body));
    });
  }

  // csDoSend: reads user AI config from localStorage
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
    var provider = localStorage.getItem('user_own_provider') || 'groq';
    var apiKey = localStorage.getItem('user_own_key') || '';
    
    try{
      if(typeof window.csFetchGroqGateway === 'function'){
        // Main app AI gateway
        var result = await window.csFetchGroqGateway(text);
        reply = (result !== null && result !== undefined) ? result : null;
      }
      
      if(!reply && provider === 'deepseek' && apiKey){
        // DeepSeek V3
        reply = await csCallAPI(
          'https://api.deepseek.com/v1/chat/completions',
          apiKey,
          { model: 'deepseek-chat', messages: [{role:'user', content: text}], max_tokens: 1024, temperature: 0.7 }
        );
      }
      
      if(!reply && apiKey){
        // User's own Groq key
        var history = [];
        var msgEls = document.querySelectorAll('#cs-msgs .cs-msg');
        for(var i=0;i<msgEls.length;i++){
          var role = msgEls[i].classList.contains('cs-user') ? 'user' : 'assistant';
          var bubble = msgEls[i].querySelector('.cs-bubble');
          if(bubble) history.push({role: role, content: bubble.textContent || bubble.innerText});
        }
        reply = await csCallAPI(
          'https://api.groq.com/openai/v1/chat/completions',
          apiKey,
          { model: _CS_CONFIG.model, messages: history, max_tokens: _CS_CONFIG.maxTokens, temperature: 0.7 }
        );
      }
      
      if(!reply && _CS_CONFIG.groqKey){
        // Fallback to CS Widget's own Groq key
        reply = await csCallAPI(
          _CS_CONFIG.apiUrl,
          _CS_CONFIG.groqKey,
          { model: _CS_CONFIG.model, messages: [{role:'user', content: text}], max_tokens: _CS_CONFIG.maxTokens, temperature: 0.7 }
        );
      }
    }catch(e){
      console.warn('[CS] API error:', e);
    }
    
    window.csHideTyping();
    if(reply && reply.trim()){
      reply = reply.replace(/\\\\n/g, '<br>').replace(/\\\\*\\\\*(.+?)\\\\*\\\\*/g, '<strong>$1</strong>');
      window.csAddMsg('bot', reply);
    } else {
      window.csAddMsg('bot', window.csLocalReply(text));
    }
    if(sendBtn) sendBtn.disabled = false;
  };
  
  """

new_s5 = s5[:old_func_start] + new_csDoSend + s5[old_func_end:]
t = t[:s5_start] + new_s5 + t[s5_end:]

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

import subprocess
start = t.rfind('// ============================================================')
end = t.find('</script>', start)
js = t[start:end]
with open('/tmp/s5_v4.js', 'w', encoding='utf-8') as f:
    f.write(js)
result = subprocess.run(['node', '--check', '/tmp/s5_v4.js'], capture_output=True, text=True, timeout=10)
print(f'Node check: {result.returncode} - {"OK" if result.returncode == 0 else result.stderr[:300]}')
print(f'File: {len(t)/1024:.1f} KB')
