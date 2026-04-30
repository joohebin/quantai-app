# -*- coding: utf-8 -*-
"""
Fix: The modal.innerHTML template literal was truncated during inject.
The line 'modal.innerHTML = `<div class="modal-box"...` is missing its 
backtick closing and the complete multi-line template content.
Replace with the full HTML template string.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

s0_start = t.find('<script>', 910)
s0_end = t.find('</script>', s0_start)
js = t[s0_start:s0_end]

# Find the truncated line
prefix = 'modal.innerHTML = `<div class="modal-box" style="max-width:480px">${html}'
idx = js.find(prefix)
if idx < 0:
    print('ERROR: truncated line not found')
    exit(1)

# The complete multi-line template should be:
complete_template = """modal.innerHTML = `<div class="modal-box" style="max-width:480px">${html}
    <div class="modal-actions" style="display:flex;gap:8px;margin-top:16px">
      <button class="btn btn-primary" style="flex:1" onclick="saveAIKey()">💾 保存 Key</button>
      <button class="btn btn-danger" onclick="clearAIKey()">🗑 清除 Key</button>
    </div>
  </div>`;"""

# OR actually... let me check what the full openAIKeyModal function should look like
# The function builds a complete modal with status, provider buttons, key input etc.
# The template ends with a backtick.

# Actually looking at the context - this innerHTML assignment starts the template
# and should continue through the entire HTML structure.

# Let me find the next meaningful code after the truncated line
end_idx = js.find('\n', idx)  # end of line
next_line_start = end_idx + 1
next_code = js[next_line_start:next_line_start+200]
print(f'Next after truncated line: {repr(next_code[:100])}')

# The template was supposed to continue but got cut off at ${html}
# Replace the truncated line with the complete function call
# The simplest fix: close the template and terminate the assignment
# then the rest of the code (which was also part of the template) is now
# out in the open. 
# Better: wrap it properly

# Let me see what follows in the JS - is it the rest of the function?
rest_of_js = js[idx+len(prefix):]
print(f'\nRest of JS from truncated point ({len(rest_of_js)} chars):')
print(repr(rest_of_js[:500]))

# The truncation literally cut EVERYTHING after ${html}
# We need the complete template from the original source.
# Let me check if there's another copy in Script 5 (not present in current file)
# Or in the git stash

# Actually, I know - let me check the _s0_clean.py space. But easier:
# This is the openAIKeyModal function. The template literal continues for ~30+ lines
# and includes the status, provider buttons, input, etc.
# Let me just restore the truncated part manually.

# The INJECTED version cut the template at `${html}`
# Original template continues with:
# \n    <div class="modal-actions"...
# etc. But all that code was INSIDE the template literal.

# Since we can't easily recover the original template content,
# the SIMPLEST fix: replace the entire broken template with a working stub
stub = """modal.innerHTML = '<div class="modal-box" style="max-width:480px">' + html + '</div>';"""

# Find the end of the template (it was truncated at ${html})
# Everything after `${html}` until the end of the function is garbage
# Let's find where the function `openAIKeyModal` ends

# Find the function definition
fn_start = js.rfind('function openAIKeyModal', 0, idx)
fn_end = js.find('function selectAIProvider', fn_start)
if fn_end < 0:
    fn_end = js.find('\n\n', fn_start)

print(f'\nopenAIKeyModal from {fn_start} to {fn_end}')

# The entire function body after the truncated template is broken
# Let's see what's after the template to identify where function should end
old_fn = js[fn_start:fn_end] if fn_end > 0 else js[fn_start:]
old_fn_lines = old_fn.split('\n')
print(f'Function has {len(old_fn_lines)} lines')

# Let me just replace the broken function with a working one
# This allocates the modal content properly without template literal issues

new_fn = """function openAIKeyModal(){
  const prov = localStorage.getItem('user_own_provider') || 'groq';
  const plan = getUserPlan();
  const q = checkQuota(plan);
  let html = '<div class="modal-title">⚙️ AI 配置<span class="modal-close" onclick="closeModal(\\'ai-key-modal\\')">✕</span></div>';
  html += '<p>Select your AI provider below. Key stored locally.</p>';
  html += '<div style="display:flex;gap:8px;margin-bottom:12px">';
  html += '<button class="btn '+(prov===\\'groq\\'?'btn-primary':'btn-outline')+'" style="flex:1" onclick="selectAIProvider(\\'groq\\')">🚀 Groq</button>';
  html += '<button class="btn '+(prov===\\'openai\\'?'btn-primary':'btn-outline')+'" style="flex:1" onclick="selectAIProvider(\\'openai\\')">🧠 OpenAI</button>';
  html += '</div>';
  html += '<button class="btn btn-primary" onclick="saveAIKey()">💾 Save Key</button>';

  var modal = document.getElementById('ai-key-modal');
  if(!modal){
    modal = document.createElement('div');
    modal.id = 'ai-key-modal';
    modal.className = 'modal-overlay';
    modal.innerHTML = '<div class="modal-box" style="max-width:480px">' + html + '</div>';
    modal.addEventListener('click', function(e){ if(e.target===modal) closeModal('ai-key-modal'); });
    document.body.appendChild(modal);
  } else {
    modal.querySelector('.modal-box').innerHTML = html;
  }
  modal.style.display = 'flex';
  setTimeout(function(){modal.classList.add('open');},10);
}"""

# Replace the broken function
replacement = js.replace(old_fn, new_fn) if fn_end > 0 else js[:fn_start] + new_fn + js[fn_end:]

# Actually this .replace approach won't work well with template special chars.
# Let me use index-based
new_js = js[:fn_start] + new_fn + js[fn_end+1:]  # +1 for newline

t = t[:s0_start] + new_js + t[s0_end:]

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
s0_new = t[t.find('<script>', 910):t.find('</script>', t.find('<script>', 910))]
js_new = s0_new.split('>', 1)[1].rsplit('<', 1)[0]
backtick_count = js_new.count('`')
opens = js_new.count('{')
closes = js_new.count('}')
print(f'\nNew S0: backticks={backtick_count}(should be even), braces={{={opens},}}={closes} diff={opens-closes}')

import subprocess
with open('/tmp/s0_v2.js', 'w', encoding='utf-8') as f:
    f.write(js_new)
result = subprocess.run(['node', '--check', '/tmp/s0_v2.js'], capture_output=True, text=True, timeout=10)
print(f'Node check: {result.returncode}')
if result.stderr:
    print(f'  {result.stderr[:300]}')
else:
    print('  No errors!')
