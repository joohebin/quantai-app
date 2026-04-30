"""Force-add Bot page HTML, i18n, and JS. Read JS from separate file to avoid quoting hell."""
import sys
sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)

with open('index.html', 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8', errors='replace')

# === 1. BOT PAGE HTML ===
bot_html = '''
      <!-- Bot Page -->
      <div id="page-bot" class="page-content" style="display:none">
        <div class="bot-header">
          <h2 data-i18n="bot_title">Bot 远程控制</h2>
          <p class="bot-subtitle" data-i18n="bot_subtitle">创建私人 Bot Key，通过国内平台远程控制量化交易</p>
        </div>
        <div class="bot-card create-bot-card">
          <div class="bot-card-header"><span class="bot-card-icon">&#x1F511;</span><span data-i18n="bot_create_title">创建 Bot</span></div>
          <div class="bot-card-body">
            <div class="bot-form-row">
              <input type="text" id="bot-name-input" placeholder="Bot 名称" />
              <button class="btn btn-primary" onclick="createBotKey()">生成 Bot Key</button>
            </div>
          </div>
        </div>
        <div class="bot-card">
          <div class="bot-card-header"><span class="bot-card-icon">&#x1F4CB;</span><span data-i18n="bot_my_bots">我的 Bot</span></div>
          <div class="bot-card-body" id="bot-list"><div class="bot-empty">暂无 Bot，点击上方按钮创建</div></div>
        </div>
        <div class="bot-card">
          <div class="bot-card-header"><span class="bot-card-icon">&#x1F4D6;</span><span data-i18n="bot_guide_title">使用说明</span></div>
          <div class="bot-card-body">
            <div class="bot-guide-steps">
              <div class="bot-guide-step"><span class="step-num">1</span><div><strong>创建 Bot</strong><p>为每个平台分别创建 Bot</p></div></div>
              <div class="bot-guide-step"><span class="step-num">2</span><div><strong>配置平台适配器</strong><p>将 Bot Key 填入平台的 Webhook/机器人配置中</p></div></div>
              <div class="bot-guide-step"><span class="step-num">3</span><div><strong>发送指令</strong><p>在平台发送消息即可远程控制交易，无需挂 VPN</p></div></div>
            </div>
          </div>
        </div>
        <div class="bot-card">
          <div class="bot-card-header"><span class="bot-card-icon">&#x1F4DD;</span><span data-i18n="bot_cmds_title">支持指令</span></div>
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
          <div class="bot-card-header"><span class="bot-card-icon">&#x1F4CA;</span><span data-i18n="bot_logs">调用记录</span></div>
          <div class="bot-card-body">
            <table class="bot-log-table"><thead><tr><th>时间</th><th>Bot</th><th>指令</th><th>状态</th><th>来源</th></tr></thead><tbody id="bot-log-body"></tbody></table>
          </div>
        </div>
      </div>'''

if 'id="page-bot"' in text:
    print("page-bot already exists")
else:
    market_pos = text.find('id="page-market"')
    calc_start = text.rfind('<', market_pos - 500, market_pos)
    if calc_start > 0:
        text = text[:calc_start] + '\n' + bot_html + '\n' + text[calc_start:]
        print("Added page-bot HTML")
    else:
        print("FAILED: could not find insertion point for page-bot")
        sys.exit(1)

# === 2. BOT JS — read from file ===
if 'loadBots' in text:
    print("Bot JS already exists")
else:
    # Read bot_js.txt
    has_js = False
    js_path = '_bot_js.txt'
    # Read the separate JS file
    with open(js_path, 'rb') as f:
        bot_js = f.read().decode('utf-8', errors='replace')
    
    body_pos = text.find('</body>')
    script_end = text.rfind('</script>', 0, body_pos)
    if script_end > 0:
        text = text[:script_end] + '\n' + bot_js + '\n' + text[script_end:]
        print("Added Bot JS functions")
        has_js = True
    
    if not has_js:
        print("FAILED: could not inject JS")
        sys.exit(1)

# === 3. PATCH showPage ===
if 'initBotPage' in text and 'page === ' in text:
    sp_idx = text.find('function showPage(page, el)')
    if sp_idx > 0:
        if 'initBotPage' not in text[sp_idx:sp_idx+3000]:
            active_line = text.find("el.classList.add('active')", sp_idx, sp_idx+3000)
            if active_line > 0:
                close_brace = text.find('}', active_line)
                if close_brace > 0:
                    text = text[:close_brace] + '\n  if (page === "bot") { initBotPage(); }' + text[close_brace:]
                    print("Patched showPage for bot init")

# === 4. Write back ===
with open('index.html', 'wb') as f:
    f.write(text.encode('utf-8', errors='replace'))

print('\n=== Final Verification ===')
with open('index.html', 'rb') as f:
    d2 = f.read().decode('utf-8', errors='replace')

all_ok = True
for k in ['page-bot', 'loadBots', 'createBotKey', 'initBotPage', '_botOrders', 'botExecute', 'parseBotCommand', 'data-page="bot"']:
    ok = k in d2
    if not ok: all_ok = False
    print(f'  {k}: {"OK" if ok else "MISSING!"}')

# === 5. JS syntax check ===
import subprocess, tempfile
# Extract JS
js_start = d2.find('loadBots')
js_end = d2.find('</script>', js_start) if js_start > 0 else -1
if js_start > 0 and js_end > 0:
    js_block = d2[js_start:js_end]
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.js', delete=False) as tf:
        tf.write(('function loadBotsCheckWrapper(){\n' + js_block + '\n}\n').encode('utf-8'))
        tfname = tf.name
    r = subprocess.run(['node', '--check', tfname], capture_output=True, text=True)
    import os
    os.unlink(tfname)
    if r.returncode != 0:
        print('\nJS SYNTAX ERROR:', r.stderr[:300])
    else:
        print('\nJS syntax: OK')

if all_ok:
    print('\nAll Bot features added successfully!')
else:
    print('\nSome features MISSING! Check above.')
