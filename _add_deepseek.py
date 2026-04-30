# -*- coding: utf-8 -*-
"""
1. Add DeepSeek button to AI provider selector
2. Add DeepSeek route in _callAI
3. Style CS sidebar entry to look more like a button
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# --- 1. Add DeepSeek button after OpenAI button ---
openai_btn = t.find('🧠 OpenAI GPT')
if openai_btn > 0:
    # Find the closing </button> and </div> of the provider button group
    openai_btn_end = t.find('</button>', openai_btn) + 9
    deepseek_btn = '''
        <button class="btn ${prov==='deepseek'?'btn-primary':'btn-outline'}" style="flex:1;font-size:13px" onclick="selectAIProvider('deepseek')">
          🎯 DeepSeek V3
        </button>
      </div>'''
    t = t[:openai_btn_end] + deepseek_btn + t[openai_btn_end:]
    print('Added DeepSeek button')

# --- 2. Add DeepSeek route in selectAIProvider ---
# Find the selectAIProvider function
sp = t.find('function selectAIProvider(')
if sp > 0:
    # Add deepseek case
    brace = t.find('{', sp)
    # Find where providers are stored
    store = t.find("localStorage.setItem", brace)
    if store > 0:
        # After the setItem, add the deepseek handler
        line_end = t.find('\n', store)
        t = t[:line_end+1] + "  if(prov==='deepseek') localStorage.setItem('user_own_provider','deepseek');\n" + t[line_end+1:]
        print('Added deepseek to selectAIProvider')

# --- 3. Add DeepSeek route in _callAI ---
call = t.find('function _callAI(')
if call > 0:
    brace = t.find('{', call)
    # Find the openai block
    openai_block = t.find("provider === 'openai'", brace)
    if openai_block > 0:
        # Find the else block
        else_block = t.find('} else {', openai_block)
        if else_block > 0:
            deepseek_route = '''
  } else if(provider === 'deepseek'){
    url = 'https://api.deepseek.com/v1/chat/completions';
    headers = { 'Content-Type':'application/json', 'Authorization': `Bearer ${apiKey}` };
    body = JSON.stringify({ model: 'deepseek-chat', messages: allMsgs, max_tokens: 400, temperature: 0.6 });
'''
            t = t[:else_block] + deepseek_route + t[else_block:]
            print('Added DeepSeek route in _callAI')

# --- 4. Style CS sidebar entry better ---
# Find the CS sidebar entry
cs_entry = t.find('onclick="toggleCS()"')
if cs_entry > 0:
    # Find style attributes
    style_start = t.find('style="', t.rfind('<div', cs_entry-200, cs_entry))
    style_end = t.find('"', style_start+7)
    
    old_style = t[style_start:style_end]
    new_style = 'style="display:flex;align-items:center;gap:8px;padding:12px 16px;cursor:pointer;border-top:1px solid var(--border);margin-top:8px;transition:all 0.2s;border-radius:8px;background:var(--card2);font-size:13px;font-weight:600"'
    
    t = t[:style_start] + new_style + t[style_end+1:]
    print('Updated CS sidebar style')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')
print(f'\nFile: {len(data)/1024:.1f} KB')
print(f'DeepSeek buttons: {text.count("deepseek")}')
print(f'DeepSeek route: {text.count("api.deepseek.com")}')
print(f'CS style updated: {"font-weight:600" in text[cs_entry-100:cs_entry+200]}' if 'cs_entry' in dir() else '')
