# -*- coding: utf-8 -*-
"""
Fix: replace XMLHttpRequest with fetch in csCallAPI.
DeepSeek API rejects XMLHttpRequest (CORS) but allows fetch.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Replace csCallAPI to use fetch instead of XMLHttpRequest
old = """  function csCallAPI(apiUrl, apiKey, body){
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
  }"""

new = """  function csCallAPI(apiUrl, apiKey, body){
    return fetch(apiUrl, { method:'POST', headers:{'Content-Type':'application/json','Authorization':'Bearer '+apiKey}, body:JSON.stringify(body) })
      .then(function(r){ if(!r.ok) throw new Error('HTTP '+r.status); return r.json(); })
      .then(function(data){ return data.choices[0].message.content; });
  }"""

count = t.count(old)
if count == 1:
    t = t.replace(old, new)
    print('Replaced csCallAPI')
else:
    print(f'Found {count} occurrences - using index')
    idx = t.find(old)
    t = t[:idx] + new + t[idx+len(old):]

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

import subprocess
start = t.rfind('// ============================================================')
end = t.find('</script>', start)
js = t[start:end]
with open('/tmp/s5_v5.js', 'w', encoding='utf-8') as f:
    f.write(js)
result = subprocess.run(['node', '--check', '/tmp/s5_v5.js'], capture_output=True, text=True, timeout=10)
print(f'Node: {result.returncode} - {"OK" if result.returncode == 0 else result.stderr[:200]}')
print(f'File: {len(t)/1024:.1f} KB')
