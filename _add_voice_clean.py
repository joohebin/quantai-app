"""
Clean voice input addition - apply to committed file.
Changes:
1. Add 🎤 button next to QuantTalk shareChart button
2. Add 🎤 button next to CS Widget send button
3. Add startVoiceInput() JS function before Friend System section
"""
import os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
TMP = os.environ.get('TEMP', '/tmp')

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# 1. QuantTalk voice button
old_qt = '<button onclick="shareChart()" style="padding:8px 12px;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--muted);font-size:13px;cursor:pointer" title="分享图表">📷</button>'
new_qt = (old_qt[:-1] + ' />'
    '<button id="qt-voice-btn" onclick="startVoiceInput(\'sq-input\')" '
    'style="padding:8px 12px;border:1px solid var(--border);border-radius:8px;'
    'background:transparent;color:var(--muted);font-size:13px;cursor:pointer" '
    'title="\u8bed\u97f3\u8f93\u5165">\U0001f399\ufe0f</button>')
# Actually just do it simply
new_qt_simple = (
    '<button onclick="shareChart()" style="padding:8px 12px;border:1px solid var(--border);'
    'border-radius:8px;background:transparent;color:var(--muted);font-size:13px;'
    'cursor:pointer" title="\u5206\u4eab\u56fe\u8868">\U0001f4f7</button>'
    '<button id="qt-voice-btn" onclick="startVoiceInput(\'sq-input\')" '
    'style="padding:8px 12px;border:1px solid var(--border);border-radius:8px;'
    'background:transparent;color:var(--muted);font-size:13px;cursor:pointer" '
    'title="\u8bed\u97f3\u8f93\u5165">\U0001f399\ufe0f</button>'
)

if old_qt in t:
    t = t.replace(old_qt, new_qt_simple)
    print('QT voice button added')
else:
    print('QT pattern NOT FOUND - trying close match')
    # Try to find it
    idx = t.find('shareChart')
    if idx > 0:
        print(f'Context: {t[idx:idx+200]}')

# 2. CS Widget voice button
old_cs = '</textarea>\r\n    <button id="cs-send" onclick="csDoSend()">\u27a4</button>'
new_cs = (
    '</textarea>\r\n'
    '    <button id="voice-btn" onclick="startVoiceInput(\'cs-input\')" '
    'style="padding:8px 12px;border:none;border-radius:8px;background:transparent;'
    'color:var(--muted);font-size:16px;cursor:pointer" '
    'title="\u8bed\u97f3\u8f93\u5165">\U0001f399\ufe0f</button>\r\n'
    '    <button id="cs-send" onclick="csDoSend()">\u27a4</button>'
)

if old_cs in t:
    t = t.replace(old_cs, new_cs)
    print('CS voice button added')
else:
    print('CS pattern NOT FOUND')
    print(f'Searching for cs-send pattern:')
    idx = t.find('cs-send')
    if idx > 0:
        print(f'CS send at {idx}: {repr(t[max(0,idx-100):idx+100])}')

# 3. Insert voice JS before Friend System section
voice_js = '''
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
'''

fs_idx = t.find('// ---- Friend System ----')
if fs_idx < 0:
    # Try to find anyway
    fs_idx = t.find('Friend System')
if fs_idx >= 0:
    t = t[:fs_idx] + voice_js + '\n' + t[fs_idx:]
    print(f'Voice JS inserted at {fs_idx}')
else:
    print('Could not find Friend System section!')

# Write file
r = t.encode('utf-8')
with open(filepath, 'wb') as f:
    f.write(r)
print(f'File: {len(r)} bytes')

# Syntax check
print('\n=== Syntax Check ===')
sidx = r.find(b'<script>', 200000)
ce = r.find(b'</script>', sidx + 8)
c = r[sidx+8:ce]
with open(os.path.join(TMP, 'sc.js'), 'wb') as f:
    f.write(c)
res = subprocess.run(['node', '--check', os.path.join(TMP, 'sc.js')], capture_output=True, timeout=15)
if res.returncode == 0:
    print('Syntax OK!')
else:
    err = res.stderr.decode('utf-8', errors='replace')[:800]
    print(f'ERROR:\n{err}')
