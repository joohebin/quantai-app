# -*- coding: utf-8 -*-
"""
Modify CS Widget's csDoSend to read user's selected AI provider/key from localStorage
and call the appropriate API (Groq or DeepSeek).
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find the csDoSend function in S5
s5_start = t.rfind('<script>', 0, t.rfind('</script>', t.rfind('</body>')))
s5_end = t.find('</script>', s5_start) + 9
s5 = t[s5_start:s5_end]

# Find the csDoSend function body
old_func_start = s5.find('  window.csDoSend = async function(){')
old_func_end = s5.find('\n  // Register', old_func_start)

new_csDoSend = """  // csDoSend: uses closure for _csSending, reads user AI config from localStorage
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
    // Check user's AI provider config from localStorage
    var provider = localStorage.getItem('user_own_provider') || 'groq';
    var apiKey = localStorage.getItem('user_own_key') || '';
    
    if(typeof window.csFetchGroqGateway === 'function'){
      // Main app AI gateway (preferred route if available)
      var result = await window.csFetchGroqGateway(text);
      reply = (result !== null && result !== undefined) ? result : window.csLocalReply(text);
    } else if(provider === 'deepseek' && apiKey){
      // DeepSeek route
      try{
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://api.deepseek.com/v1/chat/completions');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Authorization', 'Bearer ' + apiKey);
        xhr.onload = function(){
          if(xhr.status === 200){
            try{ var data = JSON.parse(xhr.responseText); reply = data.choices[0].message.content; }
            catch(e){ reply = window.csLocalReply(text); }
          } else { reply = window.csLocalReply(text); }
        };
        xhr.onerror = function(){ reply = window.csLocalReply(text); };
        xhr.send(JSON.stringify({ model: 'deepseek-chat', messages: [{role:'user', content: text}], max_tokens: 1024, temperature: 0.7 }));
      }catch(e){ reply = window.csLocalReply(text); }
    } else if(apiKey){
      // Groq route
      try{
        var history = [];
        var msgEls = document.querySelectorAll('#cs-msgs .cs-msg');
        for(var i=0;i<msgEls.length;i++){
          var role = msgEls[i].classList.contains('cs-user') ? 'user' : 'assistant';
          var bubble = msgEls[i].querySelector('.cs-bubble');
          if(bubble) history.push({role: role, content: bubble.textContent || bubble.innerText});
        }
        // Use user's Groq key or fallback
        var groqKey = apiKey;
        if(!groqKey) groqKey = _CS_CONFIG.groqKey;
        if(groqKey){
          var xhr2 = new XMLHttpRequest();
          xhr2.open('POST', 'https://api.groq.com/openai/v1/chat/completions');
          xhr2.setRequestHeader('Content-Type', 'application/json');
          xhr2.setRequestHeader('Authorization', 'Bearer ' + groqKey);
          xhr2.onload = function(){
            if(xhr2.status === 200){
              try{ var d2 = JSON.parse(xhr2.responseText); reply = d2.choices[0].message.content; }
              catch(e){ reply = window.csLocalReply(text); }
            } else { reply = window.csLocalReply(text); }
          };
          xhr2.onerror = function(){ reply = window.csLocalReply(text); };
          xhr2.send(JSON.stringify({ model: _CS_CONFIG.model, messages: history, max_tokens: _CS_CONFIG.maxTokens, temperature: 0.7 }));
        } else {
          reply = window.csLocalReply(text);
        }
      }catch(e){
        console.warn('[CS] API failed:', e);
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
  
  """

# Replace old csDoSend with new one
new_s5 = s5[:old_func_start] + new_csDoSend + s5[old_func_end:]
t = t[:s5_start] + new_s5 + t[s5_end:]

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Node check
import subprocess
start = t.rfind('// ============================================================')
end = t.find('</script>', start)
js = t[start:end]
with open('/tmp/s5_v3.js', 'w', encoding='utf-8') as f:
    f.write(js)
result = subprocess.run(['node', '--check', '/tmp/s5_v3.js'], capture_output=True, text=True, timeout=10)
print(f'Node check: {result.returncode} - {"OK" if result.returncode == 0 else result.stderr[:300]}')
print(f'File: {len(t)/1024:.1f} KB')
