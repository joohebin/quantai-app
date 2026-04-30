# -*- coding: utf-8 -*-
"""Move the customer service button from bottom-right to sidebar user card area"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# 1. Find the customer service button and remove it
# Look for "官方客服" or similar
cs_markers = ['官方客服', 'customer service', 'customer-service', '客服']
cs_info = None

for m in cs_markers:
    i = t.find(m)
    if i >= 0:
        # Find the container element
        start = t.rfind('<', i-300, i)
        # Try to find parent div that contains it
        parent_start = t.rfind('<div', start-100, i)
        if parent_start < 0: parent_start = start
        # Find where this block ends
        end = t.find('</', i)
        # Extend to find full container closure
        end_block = t.find('\n\n', end)  # look for next block
        if end_block < 0: end_block = end + 200
        cs_info = (parent_start, end_block, t[parent_start:end_block+50])
        print(f'Found "{m}" at {i}')
        print(f'Block: {parent_start} to {end_block}')
        print(f'Content: {repr(cs_info[2][:200])}')
        break

if cs_info:
    # Remove it
    rm_start = cs_info[0]
    rm_end = cs_info[1]
    # Make sure we don't leave empty space
    before = t[:rm_start].rstrip()
    after = t[rm_end:].lstrip()
    t = before + '\n' + after
    print(f'Removed CS block ({rm_end-rm_start} chars)')
else:
    print('NOT FOUND: customer service button')

# 2. Add CS button to sidebar user card area
# Find the sidebar-user-card div
card_start = t.find('id="sidebar-user-card"')
if card_start < 0:
    card_start = t.find('sidebar-user-card')
print(f'sidebar-user-card at {card_start}')

if card_start > 0:
    # Find closing </div> of the user card
    card_close = t.find('</div>', card_start)
    # Actually find the full card - search for the div that follows
    # Usually after card there's sidebar nav items
    insert_pos = t.find('<div class="nav-', card_start)
    if insert_pos < 0:
        insert_pos = t.find('<nav', card_start)
    
    if insert_pos < 0:
        # Fallback: insert before the sidebar nav section
        insert_pos = t.find('id="sidebar-nav"', card_start)
        if insert_pos < 0:
            insert_pos = card_close + 10
    
    print(f'Insert CS button before offset {insert_pos}')
    cs_button = '''
          <div onclick="openCustomerService()" style="display:flex;align-items:center;gap:8px;padding:10px 16px;cursor:pointer;border-top:1px solid var(--border);margin-top:4px;transition:background 0.2s" onmouseover="this.style.background='var(--hover)'" onmouseout="this.style.background='transparent'">
            <span style="font-size:18px">💬</span>
            <div>
              <div style="font-size:13px;font-weight:600" data-i18n="cs_title">官方客服</div>
              <div style="font-size:11px;color:var(--muted)" data-i18n="cs_desc">在线为您服务</div>
            </div>
          </div>'''
    t = t[:insert_pos] + cs_button + t[insert_pos:]
    print('Inserted CS button in sidebar')
    
    # Add CSS for CS button
    # Add data-i18n keys for CS if not present
    for lang_key, en_val, cn_val in [
        ("cs_title", "Customer Service", "官方客服"),
        ("cs_desc", "Here to help", "在线为您服务"),
    ]:
        # Check if key exists
        if cn_val not in t:
            # Add to Chinese block
            zh_pos = t.find('// 侧边栏导航')
            if zh_pos > 0:
                line_end = t.find('\n', zh_pos)
                t = t[:line_end+1] + f'    {lang_key}:\'{cn_val}\',\n' + t[line_end+1:]
                print(f'Added {lang_key} to ZH')
            # Add to English
            en_pos = t.find("nav_dashboard:'Dashboard'")
            if en_pos > 0:
                line_end = t.find('\n', en_pos)
                t = t[:line_end+1] + f'    {lang_key}:\'{en_val}\',\n' + t[line_end+1:]
                print(f'Added {lang_key} to EN')

# 3. Add the openCustomerService function
# Find a good place to insert - near other utility functions
util_pos = t.find('function openAIKeyConfig')
if util_pos < 0:
    util_pos = t.find('// ===== 工具函数')

if util_pos > 0:
    cs_fn = '''

// 客服
function openCustomerService(){
  // 如果是Telegram环境，打开Telegram客服
  if(window.Telegram && Telegram.WebApp){
    Telegram.WebApp.openTelegramLink('https://t.me/ant_umihamabot');
  } else {
    // 否则显示客服联系方式
    alert('客服微信: umihama_bot\\n客服邮箱: support@quantai.app\\n回复时间: 工作日 9:00-18:00');
  }
}'''
    t = t[:util_pos] + cs_fn + t[util_pos:]
    print('Added openCustomerService function')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')
print(f'\nFile: {len(data)/1024:.1f} KB')
cs_count = text.count('官方客服')
print(f'官方客服 occurrences: {cs_count}')
print(f'openCustomerService: {data.count(b"openCustomerService")}')
print(f'cs_title: {data.count(b"cs_title")}')
