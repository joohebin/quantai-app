"""Add Bot feature: sidebar, page, CSS, JS. Read JS from _bot_js.txt."""
import sys, subprocess, tempfile, os
sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)

with open('index.html', 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8', errors='replace')

# PHASE 1: Add nav item (after QuantTalk, before stratmarket)
if 'data-page="bot"' in text:
    print("nav item already exists")
else:
    nav_bot = '\n      <div class="nav-item" onclick="showPage(\'bot\',this)" data-page="bot">\n        <span class="ni" data-nav-icon="\U0001F916">\U0001F916</span><span data-i18n="nav_bot">Bot 远程控制</span>\n        <span class="badge" style="background:#6366f1;color:#fff">NEW</span>\n      </div>'
    # Find stratmarket and insert before it
    sm_idx = text.find('data-i18n="nav_stratmarket"')
    if sm_idx > 0:
        li_start = text.rfind('<div', 0, sm_idx)
        text = text[:li_start] + nav_bot + '\n' + text[li_start:]
        print("Added nav item ✓")
    else:
        print("FAIL: could not find stratmarket nav item")
        sys.exit(1)

# PHASE 2: Add bot page HTML
if 'id="page-bot"' in text:
    print("page HTML already exists")
else:
    bot_html_part = '''      <!-- Bot Page -->
      <div id="page-bot" class="page-content" style="display:none">
        <div class="bot-header">
          <h2 data-i18n="bot_title">\U0001F916 Bot 远程控制</h2>
          <p class="bot-subtitle" data-i18n="bot_subtitle">创建私人 Bot Key，通过国内平台远程控制量化交易，无需挂 VPN</p>
        </div>
        <div class="bot-card create-bot-card">
          <div class="bot-card-header"><span class="bot-card-icon">\U0001F511</span><span data-i18n="bot_create_title">创建 Bot</span></div>
          <div class="bot-card-body">
            <div class="bot-form-row">
              <input type="text" id="bot-name-input" placeholder="Bot 名称" />
              <button class="btn btn-primary" onclick="createBotKey()">生成 Bot Key</button>
            </div>
          </div>
        </div>
        <div class="bot-card">
          <div class="bot-card-header"><span class="bot-card-icon">\U0001F4CB</span><span data-i18n="bot_my_bots">我的 Bot</span></div>
          <div class="bot-card-body" id="bot-list"><div class="bot-empty">暂无 Bot，点击上方按钮创建</div></div>
        </div>
        <div class="bot-card">
          <div class="bot-card-header"><span class="bot-card-icon">\U0001F4D6</span><span data-i18n="bot_guide_title">使用说明</span></div>
          <div class="bot-card-body">
            <div class="bot-guide-steps">
              <div class="bot-guide-step"><span class="step-num">1</span><div><strong>创建 Bot</strong><p>为每个平台分别创建 Bot</p></div></div>
              <div class="bot-guide-step"><span class="step-num">2</span><div><strong>配置平台适配器</strong><p>将 Bot Key 填入平台的 Webhook/机器人配置</p></div></div>
              <div class="bot-guide-step"><span class="step-num">3</span><div><strong>发送指令</strong><p>在平台直接发消息即可远程控制，无需 VPN</p></div></div>
            </div>
          </div>
        </div>
        <div class="bot-card">
          <div class="bot-card-header"><span class="bot-card-icon">\U0001F4DD</span><span data-i18n="bot_cmds_title">支持指令</span></div>
          <div class="bot-card-body">
            <div class="bot-cmd-grid">
              <div class="bot-cmd-item"><code>查看持仓</code><span>显示当前所有持仓</span></div>
              <div class="bot-cmd-item"><code>买入 1 BTC</code><span>市价买入 1 BTC</span></div>
              <div class="bot-cmd-item"><code>卖出 0.5 ETH</code><span>市价卖出 0.5 ETH</span></div>
              <div class="bot-cmd-item"><code>开多 2 BTC 限价 50000</code><span>限价开多</span></div>
              <div class="bot-cmd-item"><code>开启自动交易</code><span>启动 AI 自动交易引擎</span></div>
              <div class="bot-cmd-item"><code>关闭自动交易</code><span>停止自动交易</span></div>
              <div class="bot-cmd-item"><code>查看策略</code><span>列出当前策略</span></div>
              <div class="bot-cmd-item"><code>创建策略 RSI</code><span>创建 RSI 策略</span></div>
            </div>
          </div>
        </div>
        <div class="bot-card" id="bot-log-card" style="display:none">
          <div class="bot-card-header"><span class="bot-card-icon">\U0001F4CA</span><span data-i18n="bot_logs">调用记录</span></div>
          <div class="bot-card-body">
            <table class="bot-log-table"><thead><tr><th>时间</th><th>Bot</th><th>指令</th><th>状态</th><th>来源</th></tr></thead><tbody id="bot-log-body"></tbody></table>
          </div>
        </div>
      </div>
'''
    # Insert before <script> tag (after all page-content divs)
    script_idx = text.rfind('\n<script', 190000, 220000)
    if script_idx < 0:
        script_idx = text.find('\n<script', 200000)
    if script_idx > 0:
        text = text[:script_idx] + '\n' + bot_html_part + '\n' + text[script_idx:]
        print("Added page HTML ✓")
    else:
        print("FAIL: could not find insertion point")
        sys.exit(1)

# PHASE 3: Add Bot CSS
if '/* Bot Page */' in text:
    print("Bot CSS already exists")
else:
    bot_css = '''/* Bot Page */
.bot-header h2 { font-size:24px;font-weight:700;margin:0 0 8px }
.bot-subtitle { color:var(--muted);font-size:14px;margin:0 0 24px }
.bot-card { background:var(--card);border-radius:14px;margin-bottom:16px;overflow:hidden }
.bot-card-header { display:flex;align-items:center;gap:8px;padding:16px 20px;font-size:15px;font-weight:600;border-bottom:1px solid var(--border) }
.bot-card-icon { font-size:18px }
.bot-card-body { padding:16px 20px }
.bot-form-row { display:flex;gap:12px }
.bot-form-row input { flex:1;padding:10px 14px;border-radius:10px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-size:14px }
.create-bot-card { border:1px solid var(--green);box-shadow:0 0 20px rgba(0,200,150,.1) }
.bot-empty { text-align:center;color:var(--muted);padding:30px;font-size:14px }
.bot-item { display:flex;align-items:center;justify-content:space-between;padding:12px 0;border-bottom:1px solid var(--border) }
.bot-item:last-child { border-bottom:none }
.bot-item-info { display:flex;flex-direction:column;gap:4px }
.bot-item-name { font-weight:600;font-size:14px }
.bot-item-key { font-size:12px;color:var(--green);font-family:monospace;cursor:pointer;padding:2px 8px;background:rgba(0,200,150,.1);border-radius:6px;display:inline-block }
.bot-item-date { font-size:11px;color:var(--muted) }
.bot-item-actions { display:flex;gap:8px;align-items:center }
.bot-guide-steps { display:flex;flex-direction:column;gap:16px }
.bot-guide-step { display:flex;gap:12px;align-items:flex-start }
.step-num { width:28px;height:28px;border-radius:50%;background:var(--green);color:var(--dark);font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0 }
.bot-guide-step strong { font-size:14px }
.bot-guide-step p { font-size:13px;color:var(--muted);margin:2px 0 0 }
.bot-cmd-grid { display:grid;grid-template-columns:1fr 1fr;gap:10px }
.bot-cmd-item { display:flex;flex-direction:column;gap:2px;padding:10px 14px;background:var(--bg);border-radius:10px }
.bot-cmd-item code { font-size:13px;font-weight:600;color:var(--green) }
.bot-cmd-item span { font-size:12px;color:var(--muted) }
.bot-log-table { width:100%;border-collapse:collapse;font-size:13px }
.bot-log-table th { text-align:left;padding:8px;color:var(--muted);font-weight:500;border-bottom:1px solid var(--border) }
.bot-log-table td { padding:8px;border-bottom:1px solid var(--border) }
.bot-log-ok { color:var(--green) }
.bot-log-err { color:#ef4444 }
'''
    style_end = text.find('</style>')
    if style_end > 0:
        text = text[:style_end] + '\n' + bot_css + '\n' + text[style_end:]
        print("Added Bot CSS ✓")

# PHASE 4: Add Bot JS
if 'initBotPage' in text:
    print("Bot JS already exists")
else:
    with open('_bot_js.txt', 'rb') as f:
        bot_js = f.read().decode('utf-8')
    
    body_pos = text.find('</body>')
    last_script_end = text.rfind('</script>', 0, body_pos)
    if last_script_end > 0:
        text = text[:last_script_end] + '\n' + bot_js + '\n' + text[last_script_end:]
        print("Added Bot JS ✓")

# PHASE 5: Patch showPage
if 'initBotPage' in text and 'page ===' in text:
    sp_idx = text.find('function showPage(page, el)')
    if sp_idx > 0 and 'initBotPage' not in text[sp_idx:sp_idx+3000]:
        act_idx = text.find("el.classList.add('active')", sp_idx, sp_idx+3000)
        if act_idx > 0:
            brace = text.find('}', act_idx)
            if brace > brace-1:
                text = text[:brace] + '\n  if (page === "bot") { initBotPage(); }' + text[brace:]
                print("Patched showPage ✓")

# Write
with open('index.html', 'wb') as f:
    f.write(text.encode('utf-8', errors='replace'))

# Verify
print('\n--- Verification ---')
with open('index.html', 'rb') as f:
    d2 = f.read().decode('utf-8', errors='replace')

checks = ['page-bot', 'loadBots', 'createBotKey', 'initBotPage', '_botOrders',
          'botExecute', 'parseBotCommand', 'data-page="bot"', 'Bot Page']
ok_count = 0
for k in checks:
    found = k in d2
    print(f'  {k}: {"OK" if found else "MISSING"}')
    if found: ok_count += 1

if ok_count == len(checks):
    print('\nAll features added!')
    # JS syntax check
    js_start = d2.find('loadBots = function')
    if js_start > 0:
        js_end = d2.find('\n// ========== AI', js_start)  # Find next section
        if js_end < 0: js_end = d2.find('\n</script>', js_start)
        js_block = d2[js_start:js_end]
        wrapped = '(function(){\n' + js_block + '\n})();'
        tf = tempfile.NamedTemporaryFile(mode='wb', suffix='.js', delete=False)
        tf.write(wrapped.encode('utf-8'))
        tfname = tf.name
        tf.close()
        r = subprocess.run(['node', '--check', tfname], capture_output=True, text=True)
        os.unlink(tfname)
        if r.returncode != 0:
            print(f'JS syntax: ERROR ({r.stderr[:200]})')
        else:
            print('JS syntax: OK')
else:
    print(f'\n{len(checks)-ok_count} features missing!')
