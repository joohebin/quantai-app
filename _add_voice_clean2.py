"""
SINGLE SCRIPT: Add voice buttons + JS to index.html.
File is clean (committed with friend system).
"""
import os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
TMP = os.environ.get('TEMP', '/tmp')

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# === 1. QuantTalk voice button ===
qt_old = '<button onclick="shareChart()" style="padding:8px 12px;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--muted);font-size:13px;cursor:pointer" title="\u5206\u4eab\u56fe\u8868">\U0001f4f7</button>'
qt_new = qt_old + '<button id="qt-voice-btn" onclick="startVoiceInput(\'sq-input\')" style="padding:8px 12px;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--muted);font-size:13px;cursor:pointer" title="\u8bed\u97f3\u8f93\u5165">\U0001f399\ufe0f</button>'

if qt_old in t:
    t = t.replace(qt_old, qt_new)
    print('1. QT voice button OK')
else:
    print(f'1. QT NOT FOUND: searching for shareChart...')
    idx = t.find('shareChart')
    print(f'At {idx}: {t[idx:idx+200]}')

# === 2. CS Widget voice button (add after textarea, before send button) ===
cs_old = '</textarea>\r\n    <button id="cs-send" onclick="csDoSend()">\u27a4</button>'
cs_new = '</textarea>\r\n    <button id="voice-btn" onclick="startVoiceInput(\'cs-input\')" style="padding:8px 12px;border:none;border-radius:8px;background:transparent;color:var(--muted);font-size:16px;cursor:pointer" title="\u8bed\u97f3\u8f93\u5165">\U0001f399\ufe0f</button>\r\n    <button id="cs-send" onclick="csDoSend()">\u27a4</button>'

if cs_old in t:
    t = t.replace(cs_old, cs_new)
    print('2. CS voice button OK')
else:
    print(f'2. CS NOT FOUND')
    idx = t.find('cs-send')
    print(f'cs-send at {idx}: {repr(t[max(0,idx-150):idx+100])}')

# === 3. Insert voice JS before Friend System ===
voice_code = r"""
// ---- Voice Input (Web Speech API) ----
var _voiceRecognition = null;
var _voiceListening = false;
function startVoiceInput(inputId){
  var btn = inputId === 'sq-input' ? document.getElementById('qt-voice-btn') : document.getElementById('voice-btn');
  if(!btn) btn = document.getElementById('voice-btn');
  
  if(_voiceListening){
    if(_voiceRecognition) _voiceRecognition.stop();
    if(btn) btn.textContent = '\U0001f399\ufe0f';
    if(btn) btn.style.color = '';
    _voiceListening = false;
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
    _voiceListening = true;
    if(btn) btn.textContent = '\U0001f3a4';
    if(btn) btn.style.color = 'var(--green)';
  };
  
  recognition.onresult = function(e){
    var transcript = e.results[0][0].transcript;
    var input = document.getElementById(inputId);
    if(input){
      input.value = transcript;
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
    _voiceListening = false;
  };
  
  recognition.onend = function(){
    _voiceListening = false;
    if(btn) btn.textContent = '\U0001f399\ufe0f';
    if(btn) btn.style.color = '';
  };
  
  _voiceRecognition = recognition;
  recognition.start();
}
"""

# Find friend system - exact comment in _qt_functions.js starts with:
# // Friend System JS - read by _build_friend_v4.py
# But the insert should go RIGHT before that comment
fs_idx = t.find('// Friend System JS - read by')
if fs_idx < 0:
    print(f'3. Friend System NOT FOUND')
    exit(1)
    
t = t[:fs_idx] + voice_code + '\n' + t[fs_idx:]
print(f'3. Voice JS inserted before Friend System at {fs_idx}')

# Write
r = t.encode('utf-8')
with open(filepath, 'wb') as f:
    f.write(r)
print(f'File saved: {len(r)} bytes')

# Syntax check
print('\n=== Syntax Check ===')
# Find Script 2
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
