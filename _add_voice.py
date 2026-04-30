"""
Add voice input button to CS Widget and QuantTalk input areas.
Uses Web Speech API (SpeechRecognition) - pure frontend, no backend needed.
"""
import sys, os, subprocess
sys.stdout.reconfigure(encoding='utf-8')
TMP = os.environ.get('TEMP', '/tmp')

filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# ===== 1. Add voice button to QuantTalk input =====
# Current: <button onclick="shareChart()" style="...">📷</button>
# Change to: 📷 button + 🎤 button side by side
old_qt = '<button onclick="shareChart()" style="padding:8px 12px;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--muted);font-size:13px;cursor:pointer" title="分享图表">📷</button>'
new_qt = '<button onclick="shareChart()" style="padding:8px 12px;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--muted);font-size:13px;cursor:pointer" title="分享图表">📷</button><button id="qt-voice-btn" onclick="startVoiceInput(\'sq-input\')" style="padding:8px 12px;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--muted);font-size:13px;cursor:pointer" title="语音输入">🎤</button>'

assert old_qt in t, 'QuantTalk old button not found!'
t = t.replace(old_qt, new_qt)
print('✅ QuantTalk voice button added')

# ===== 2. Add voice button to CS Widget input =====
# After the textarea, before send button: insert voice button
# Current: </textarea><button id="cs-send" onclick="csDoSend()">➤</button>
old_cs = '</textarea>\r\n    <button id="cs-send" onclick="csDoSend()">\u27a4</button>'
new_cs = '</textarea>\r\n    <button id="voice-btn" onclick="startVoiceInput(\'cs-input\')" style="padding:8px 12px;border:none;border-radius:8px;background:transparent;color:var(--muted);font-size:16px;cursor:pointer" title="\u8bed\u97f3\u8f93\u5165">\U0001f399\ufe0f</button>\r\n    <button id="cs-send" onclick="csDoSend()">\u27a4</button>'

assert old_cs in t, 'CS Widget old input not found!'
t = t.replace(old_cs, new_cs)
print('✅ CS Widget voice button added')

# ===== 3. Insert voice input JS function =====
ins_idx = t.find('// ---- Friend System ----')
print(f'JS insertion point: {ins_idx}')

voice_js = '''
// ---- Voice Input (Web Speech API) ----
var _voiceRecognition = null;
var _voiceListening = false;
function startVoiceInput(inputId){
  var btn = inputId === 'sq-input' ? document.getElementById('qt-voice-btn') : document.getElementById('voice-btn');
  if(!btn) btn = document.getElementById('voice-btn');
  
  if(_voiceListening){
    if(_voiceRecognition) _voiceRecognition.stop();
    if(btn) btn.textContent = '\U0001f3a4';
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
      // Auto trigger send for chat inputs
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

t = t[:ins_idx] + voice_js + t[ins_idx:]
print('✅ Voice input JS inserted')

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
    print(f'ERROR:\\n{err}')
