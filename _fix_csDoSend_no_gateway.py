# -*- coding: utf-8 -*-
"""
Fix: csDoSend should NOT rely on csFetchGroqGateway (has broken closure refs).
Instead, directly use user's DeepSeek/Groq config from localStorage.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

s5_start = t.rfind('<script>', 0, t.rfind('</script>', t.rfind('</body>')))
s5_end = t.find('</script>', s5_start) + 9
s5 = t[s5_start:s5_end]

old_func_start = s5.find('  window.csDoSend = async function(){')
old_func_end = s5.find('\n  // Register', old_func_start)

new_csDoSend = """  window.csDoSend = async function(){
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
      // Try csFetchGroqGateway FIRST - it's the main app AI pipeline
      // But it has broken closure refs (_csHistory missing). Wrap in try/catch.
      try{
        if(typeof window.csFetchGroqGateway === 'function'){
          reply = await window.csFetchGroqGateway(text);
        }
      }catch(gwErr){
        console.warn('[CS] csFetchGroqGateway failed:', gwErr);
        reply = null;
      }
      
      if(!reply && provider === 'deepseek' && apiKey){
        reply = await fetch('https://api.deepseek.com/v1/chat/completions', {
          method:'POST',
          headers:{'Content-Type':'application/json','Authorization':'Bearer '+apiKey},
          body:JSON.stringify({model:'deepseek-chat', messages:[{role:'user', content:text}], max_tokens:1024, temperature:0.7})
        }).then(function(r){ if(!r.ok) throw Error('HTTP '+r.status); return r.json(); })
        .then(function(d){ return d.choices[0].message.content; });
      }
      
      if(!reply && apiKey && provider === 'groq'){
        var history = [];
        var msgEls = document.querySelectorAll('#cs-msgs .cs-msg');
        for(var i=0;i<msgEls.length;i++){
          var role = msgEls[i].classList.contains('cs-user') ? 'user' : 'assistant';
          var bubble = msgEls[i].querySelector('.cs-bubble');
          if(bubble) history.push({role: role, content: bubble.textContent || bubble.innerText});
        }
        reply = await fetch('https://api.groq.com/openai/v1/chat/completions', {
          method:'POST',
          headers:{'Content-Type':'application/json','Authorization':'Bearer '+apiKey},
          body:JSON.stringify({model:'llama-3.3-70b-versatile', messages:history, max_tokens:1024, temperature:0.7})
        }).then(function(r){ if(!r.ok) throw Error('HTTP '+r.status); return r.json(); })
        .then(function(d){ return d.choices[0].message.content; });
      }
      
      if(!reply && _CS_CONFIG.groqKey){
        reply = await fetch(_CS_CONFIG.apiUrl, {
          method:'POST',
          headers:{'Content-Type':'application/json','Authorization':'Bearer '+_CS_CONFIG.groqKey},
          body:JSON.stringify({model:_CS_CONFIG.model, messages:[{role:'user', content:text}], max_tokens:_CS_CONFIG.maxTokens, temperature:0.7})
        }).then(function(r){ if(!r.ok) throw Error('HTTP '+r.status); return r.json(); })
        .then(function(d){ return d.choices[0].message.content; });
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
with open('/tmp/s5_v6.js', 'w', encoding='utf-8') as f:
    f.write(js)
result = subprocess.run(['node', '--check', '/tmp/s5_v6.js'], capture_output=True, text=True, timeout=10)
print(f'Node: {result.returncode} - {"OK" if result.returncode == 0 else result.stderr[:200]}')
print(f'File: {len(t)/1024:.1f} KB')
