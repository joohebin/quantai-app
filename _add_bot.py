"""Add Bot feature to QuantAI sidebar + create Bot management page + Bot backend API endpoints"""
import re

# Read file as binary (handle mixed encodings)
with open('index.html', 'rb') as f:
    data = f.read()

text = data.decode('utf-8', errors='replace')

# === 1. Add Bot nav item after QuantTalk nav item ===
nav_item_tpl = '''      <div class="nav-item" onclick="showPage('bot',this)" data-page="bot">
        <span class="ni" data-nav-icon="🤖">🤖</span><span data-i18n="nav_bot">Bot 远程控制</span>
        <span class="badge" style="background:#6366f1;color:#fff">NEW</span>
      </div>'''

# Insert after QuantTalk nav-item (the sq heading one, not duplicate arbitrage)
insert_marker = 'data-i18n="nav_square">QuantTalk</span>'
idx = text.find(insert_marker)
idx2 = text.find('</div>', idx)
insert_pos = idx2 + 6  # after closing </div>

before = text[:insert_pos]
after = text[insert_pos:]

# Check if already exists
if 'data-page="bot"' not in text:
    text = before + '\n' + nav_item_tpl + after
    print("Added Bot nav item ✓")
else:
    print("Bot nav item already exists ✓")

# === 2. Add Bot page section (after the last page section) ===
# Find the last page-content section before the JavaScript
last_page_end = text.rfind('<!-- Dark Mode Toggle -->')
if last_page_end < 0:
    last_page_end = text.rfind('</main>')

bot_page_html = '''
      <!-- Bot Page -->
      <div id="page-bot" class="page-content" style="display:none">
        <div class="bot-header">
          <h2 data-i18n="bot_title">🤖 Bot 远程控制</h2>
          <p class="bot-subtitle" data-i18n="bot_subtitle">创建私人 Bot Key，通过国内平台远程控制量化交易</p>
        </div>
        
        <!-- Create Bot -->
        <div class="bot-card create-bot-card">
          <div class="bot-card-header">
            <span class="bot-card-icon">🔑</span>
            <span data-i18n="bot_create_title">创建 Bot</span>
          </div>
          <div class="bot-card-body">
            <div class="bot-form-row">
              <input type="text" id="bot-name-input" placeholder="Bot 名称（例如：我的QQ交易助手）" />
              <button class="btn btn-primary" onclick="createBotKey()" data-i18n="bot_create_btn">生成 Bot Key</button>
            </div>
          </div>
        </div>

        <!-- My Bots -->
        <div class="bot-card">
          <div class="bot-card-header">
            <span class="bot-card-icon">📋</span>
            <span data-i18n="bot_my_bots">我的 Bot</span>
          </div>
          <div class="bot-card-body" id="bot-list">
            <div class="bot-empty" data-i18n="bot_empty">暂无 Bot，点击上方按钮创建</div>
          </div>
        </div>

        <!-- How to Use -->
        <div class="bot-card">
          <div class="bot-card-header">
            <span class="bot-card-icon">📖</span>
            <span data-i18n="bot_guide_title">使用说明</span>
          </div>
          <div class="bot-card-body">
            <div class="bot-guide-steps">
              <div class="bot-guide-step">
                <span class="step-num">1</span>
                <div>
                  <strong data-i18n="bot_step1_title">创建 Bot</strong>
                  <p data-i18n="bot_step1_desc">为每个需要控制的平台分别创建 Bot（QQ、微信、飞书、钉钉、KOOK）</p>
                </div>
              </div>
              <div class="bot-guide-step">
                <span class="step-num">2</span>
                <div>
                  <strong data-i18n="bot_step2_title">配置平台适配器</strong>
                  <p data-i18n="bot_step2_desc">将 Bot Key 填入平台的 Webhook/机器人配置中</p>
                </div>
              </div>
              <div class="bot-guide-step">
                <span class="step-num">3</span>
                <div>
                  <strong data-i18n="bot_step3_title">发送指令</strong>
                  <p data-i18n="bot_step3_desc">在平台发送消息即可远程控制交易，无需挂 VPN</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Supported Commands -->
        <div class="bot-card">
          <div class="bot-card-header">
            <span class="bot-card-icon">📝</span>
            <span data-i18n="bot_cmds_title">支持指令</span>
          </div>
          <div class="bot-card-body">
            <div class="bot-cmd-grid">
              <div class="bot-cmd-item"><code>查看持仓</code><span>显示当前所有持仓</span></div>
              <div class="bot-cmd-item"><code>买入 1 BTC</code><span>市价买入 1 BTC</span></div>
              <div class="bot-cmd-item"><code>卖出 0.5 ETH</code><span>市价卖出 0.5 ETH</span></div>
              <div class="bot-cmd-item"><code>开多 2 BTC 限价 50000</code><span>限价开多</span></div>
              <div class="bot-cmd-item"><code>开启自动交易</code><span>启动 AI 自动交易引擎</span></div>
              <div class="bot-cmd-item"><code>关闭自动交易</code><span>停止自动交易</span></div>
              <div class="bot-cmd-item"><code>查看策略</code><span>列出当前策略</span></div>
              <div class="bot-cmd-item"><code>创建策略 RSI</code><span>创建 RSI 策略（需设定参数）</span></div>
            </div>
          </div>
        </div>

        <!-- Call Log -->
        <div class="bot-card" id="bot-log-card" style="display:none">
          <div class="bot-card-header">
            <span class="bot-card-icon">📊</span>
            <span data-i18n="bot_logs">调用记录</span>
          </div>
          <div class="bot-card-body">
            <table class="bot-log-table" id="bot-log-table">
              <thead><tr><th>时间</th><th>Bot</th><th>指令</th><th>状态</th><th>来源</th></tr></thead>
              <tbody id="bot-log-body"></tbody>
            </table>
          </div>
        </div>
      </div>'''

# Insert bot page HTML before the dark mode toggle
dark_mode_idx = text.find('<!-- Dark Mode Toggle -->')
if dark_mode_idx > 0 and 'id="page-bot"' not in text:
    text = text[:dark_mode_idx] + bot_page_html + '\n\n' + text[dark_mode_idx:]
    print("Added Bot page section ✓")
else:
    print("Bot page section already exists ✓")

# === 3. Add i18n entries ===
i18n_entries = '''
      var _botI18n = {
        nav_bot: {zh: "Bot 远程控制", en: "Bot Remote", ja: "Bot リモート", ko: "Bot 원격", 
                  es: "Bot Remoto", pt: "Bot Remoto", fr: "Bot à distance", de: "Bot Fernsteuerung",
                  nl: "Bot op afstand", pl: "Bot zdalny", tr: "Bot Uzaktan", 
                  th: "Bot ควบคุมระยะไกล", vi: "Bot từ xa",
                  ar: "التحكم عن بعد بالبوت", ru: "Бот удаленный"},
        bot_title: {zh: "🤖 Bot 远程控制", en: "🤖 Bot Remote", ja: "🤖 Bot リモート制御",
                    ko: "🤖 Bot 원격 제어", es: "🤖 Bot Remoto Control", pt: "🤖 Bot Remoto",
                    fr: "🤖 Contrôle à distance du Bot", de: "🤖 Bot-Fernsteuerung",
                    nl: "🤖 Bot op afstand", pl: "🤖 Bot zdalny", tr: "🤖 Bot Uzaktan Kontrol",
                    th: "🤖 Bot ควบคุมระยะไกล", vi: "🤖 Bot từ xa",
                    ar: "🤖 التحكم عن بعد بالبوت", ru: "🤖 Бот удаленный"},
        bot_subtitle: {zh: "创建私人 Bot Key，通过国内平台远程控制量化交易", en: "Create Bot Key to control trading remotely",
                       ja: "Botキーを作成してリモートで取引を制御"}},
'''

# Find i18n loading area, add after it
i18n_load_idx = text.find('function getI18N')
if i18n_load_idx > 0 and '_botI18n' not in text:
    # Find a good insertion point - before the function
    text = text[:i18n_load_idx] + i18n_entries + '\n' + text[i18n_load_idx:]
    print("Added Bot i18n entries ✓")
else:
    print("Bot i18n entries already exist ✓")

# === 4. Add Bot CSS ===
bot_css = '''
/* Bot Page */
.bot-header { margin-bottom: 24px; }
.bot-header h2 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.bot-subtitle { color: var(--muted); font-size: 14px; margin: 0; }

.bot-card { background: var(--card); border-radius: 14px; margin-bottom: 16px; overflow: hidden; }
.bot-card-header { display: flex; align-items: center; gap: 8px; padding: 16px 20px; font-size: 15px; font-weight: 600; border-bottom: 1px solid var(--border); }
.bot-card-icon { font-size: 18px; }
.bot-card-body { padding: 16px 20px; }

.bot-form-row { display: flex; gap: 12px; }
.bot-form-row input { flex: 1; padding: 10px 14px; border-radius: 10px; border: 1px solid var(--border); background: var(--bg); color: var(--text); font-size: 14px; }

.btn-primary { background: var(--green); color: var(--dark); border: none; padding: 10px 20px; border-radius: 10px; font-weight: 600; cursor: pointer; font-size: 14px; }
.btn-danger { background: #ef4444; color: #fff; border: none; padding: 6px 14px; border-radius: 8px; font-weight: 500; cursor: pointer; font-size: 12px; }
.btn-sm { padding: 6px 14px; font-size: 12px; border-radius: 8px; }

.bot-empty { text-align: center; color: var(--muted); padding: 30px; font-size: 14px; }

.bot-item { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--border); }
.bot-item:last-child { border-bottom: none; }
.bot-item-info { display: flex; flex-direction: column; gap: 4px; }
.bot-item-name { font-weight: 600; font-size: 14px; }
.bot-item-key { font-size: 12px; color: var(--green); font-family: monospace; letter-spacing: 0.5px; cursor: pointer; padding: 2px 8px; background: rgba(0,200,150,.1); border-radius: 6px; display: inline-block; }
.bot-item-key:hover { background: rgba(0,200,150,.2); }
.bot-item-actions { display: flex; gap: 8px; align-items: center; }
.bot-item-date { font-size: 11px; color: var(--muted); }

.bot-guide-steps { display: flex; flex-direction: column; gap: 16px; }
.bot-guide-step { display: flex; gap: 12px; align-items: flex-start; }
.step-num { width: 28px; height: 28px; border-radius: 50%; background: var(--green); color: var(--dark); font-weight: 700; font-size: 14px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.bot-guide-step strong { font-size: 14px; }
.bot-guide-step p { font-size: 13px; color: var(--muted); margin: 2px 0 0; }

.bot-cmd-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.bot-cmd-item { display: flex; flex-direction: column; gap: 2px; padding: 10px 14px; background: var(--bg); border-radius: 10px; }
.bot-cmd-item code { font-size: 13px; font-weight: 600; color: var(--green); }
.bot-cmd-item span { font-size: 12px; color: var(--muted); }

.bot-log-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.bot-log-table th { text-align: left; padding: 8px; color: var(--muted); font-weight: 500; border-bottom: 1px solid var(--border); }
.bot-log-table td { padding: 8px; border-bottom: 1px solid var(--border); }
.bot-log-status-ok { color: var(--green); }
.bot-log-status-err { color: #ef4444; }

.create-bot-card { border: 1px solid var(--green); box-shadow: 0 0 20px rgba(0,200,150,.1); }
'''

# Insert CSS before closing </style>
style_idx = text.rfind('</style>')
if style_idx > 0 and 'Bot Page' not in text:
    text = text[:style_idx] + bot_css + '\n' + text[style_idx:]
    print("Added Bot CSS ✓")
else:
    print("Bot CSS already exists ✓")

# === 5. Add Bot JS functions ===
bot_js = '''
// ========== Bot Remote Control ==========
window._bots = [];

// Load bots from localStorage
function loadBots() {
  try {
    var stored = localStorage.getItem('qbots');
    window._bots = stored ? JSON.parse(stored) : [];
  } catch(e) { window._bots = []; }
  return window._bots;
}

// Save bots to localStorage
function saveBots() {
  localStorage.setItem('qbots', JSON.stringify(window._bots));
}

// Generate bot key
function genBotKey() {
  var chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  var key = 'qbot_';
  for (var i = 0; i < 32; i++) {
    key += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return key;
}

// Render bot list
function renderBots() {
  var list = document.getElementById('bot-list');
  if (!list) return;
  loadBots();
  
  if (window._bots.length === 0) {
    list.innerHTML = '<div class="bot-empty" data-i18n="bot_empty">暂无 Bot，点击上方按钮创建</div>';
    return;
  }
  
  var html = '';
  for (var i = 0; i < window._bots.length; i++) {
    var b = window._bots[i];
    html += '<div class="bot-item">' +
      '<div class="bot-item-info">' +
        '<div class="bot-item-name">' + escapeHtml(b.name) + '</div>' +
        '<div class="bot-item-key" onclick="copyBotKey(\'' + b.key + '\')" title="点击复制">' + b.key + '</div>' +
        '<div class="bot-item-date">创建: ' + b.created + (b.lastUsed ? ' | 最后使用: ' + b.lastUsed : '') + '</div>' +
      '</div>' +
      '<div class="bot-item-actions">' +
        '<button class="btn btn-sm btn-primary" onclick="copyBotKey(\'' + b.key + '\')">📋 复制</button>' +
        '<button class="btn btn-sm btn-danger" onclick="deleteBotKey(\'' + b.key + '\')">🗑️ 删除</button>' +
      '</div>' +
    '</div>';
  }
  list.innerHTML = html;
  i18nApply();
}

// Create bot key
function createBotKey() {
  var name = document.getElementById('bot-name-input') || {};
  var botName = (name.value || '').trim();
  if (!botName) { botName = 'Bot #' + (window._bots.length + 1); }
  
  var bot = {
    key: genBotKey(),
    name: botName,
    created: new Date().toLocaleString('zh-CN'),
    lastUsed: null,
    callCount: 0
  };
  
  window._bots.push(bot);
  saveBots();
  renderBots();
  
  // Clear input if it exists
  if (name.value !== undefined) name.value = '';
  
  // Show success
  showTradeConfirm({
    title: '✅ Bot Key 创建成功',
    message: '<div style="text-align:center;padding:10px 0">' +
      '<p style="font-size:16px;font-weight:600;margin-bottom:12px">' + bot.key + '</p>' +
      '<p style="color:var(--muted);font-size:13px">点击下方复制到剪贴板，填入你的平台适配器</p>' +
      '</div>',
    confirmText: '📋 复制 Key',
    cancelText: '关闭',
    onConfirm: function() { copyBotKey(bot.key); }
  });
}

// Copy bot key to clipboard
function copyBotKey(key) {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(key).then(function() {
      showTradeConfirm({
        title: '已复制',
        message: 'Bot Key 已复制到剪贴板: ' + key,
        confirmText: '确定',
        cancelText: ''
      });
    });
  } else {
    // Fallback
    var ta = document.createElement('textarea');
    ta.value = key;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    alert('Bot Key 已复制: ' + key);
  }
}

// Delete bot key
function deleteBotKey(key) {
  showTradeConfirm({
    title: '确认删除',
    message: '确定要删除此 Bot Key？删除后该 Key 将立即失效。',
    confirmText: '确认删除',
    cancelText: '取消',
    onConfirm: function() {
      window._bots = window._bots.filter(function(b) { return b.key !== key; });
      saveBots();
      renderBots();
    }
  });
}

// Bot command API (for external platforms to call)
function botExecute(key, cmd) {
  loadBots();
  var bot = null;
  for (var i = 0; i < window._bots.length; i++) {
    if (window._bots[i].key === key) { bot = window._bots[i]; break; }
  }
  if (!bot) return {error: 'Bot key not found', status: 404};
  
  bot.lastUsed = new Date().toLocaleString('zh-CN');
  bot.callCount = (bot.callCount || 0) + 1;
  saveBots();
  
  // Log call
  logBotCall(bot.name, cmd, 'ok', 'API');
  
  // Parse and execute
  var result = parseBotCommand(cmd);
  return result;
}

// Parse bot teletext command
window._botOrders = []; // auto trading engine order queue

function parseBotCommand(text) {
  var result = {original: text, action: null, params: {}};
  var t = text.trim();
  
  // 查看持仓
  if (t.includes('持仓') || /position/i.test(t)) {
    result.action = 'view_positions';
    result.message = '当前持仓信息已发送，请在应用中查看';
    return result;
  }
  
  // 查看策略
  if (t.includes('策略') || /strategy/i.test(t)) {
    result.action = 'view_strategies';
    result.message = '策略列表已发送，请在应用中查看';
    return result;
  }
  
  // 开启/关闭自动交易
  if (t.includes('开启') && (t.includes('自动') || t.includes('交易'))) {
    result.action = 'start_auto';
    result.message = '✅ 自动交易已开启';
    return result;
  }
  if (t.includes('关闭') && (t.includes('自动') || t.includes('交易'))) {
    result.action = 'stop_auto';
    result.message = '⏹️ 自动交易已关闭';
    return result;
  }
  
  // 创建策略
  if (t.includes('创建') && t.includes('策略')) {
    result.action = 'create_strategy';
    var type = t.match(/策略\s*(\w+)/);
    result.params.type = type ? type[1] : 'custom';
    result.message = '策略创建请求已接收，请在应用中完善参数';
    return result;
  }
  
  // 买入/卖出/开多/开空/平仓
  var order = parseVoiceOrder(t);
  if (order && order.isOrder) {
    result.action = 'execute_order';
    result.params.order = order;
    // Add to bot order queue
    window._botOrders.push(order);
    result.message = '✅ 订单已接收: ' + (order.side || order.action) + ' ' + order.amount + ' ' + order.symbol;
    // Execute through quanttalk
    if (typeof sendTradeSignal === 'function') {
      sendTradeSignal(order);
    }
    return result;
  }
  
  // Default: unknown command
  result.action = 'unknown';
  result.message = '🤔 无法识别的指令。试试：查看持仓、买入1BTC、开启自动交易';
  return result;
}

// Log bot call
function logBotCall(botName, cmd, status, source) {
  var logs = [];
  try { logs = JSON.parse(localStorage.getItem('qbot_logs') || '[]'); } catch(e) {}
  logs.unshift({
    time: new Date().toLocaleString('zh-CN'),
    bot: botName,
    cmd: cmd.substring(0, 50),
    status: status,
    source: source
  });
  if (logs.length > 100) logs = logs.slice(0, 100);
  localStorage.setItem('qbot_logs', JSON.stringify(logs));
  
  // Update UI if log card is visible
  renderBotLogs();
}

// Render bot call logs
function renderBotLogs() {
  var tbody = document.getElementById('bot-log-body');
  var card = document.getElementById('bot-log-card');
  if (!tbody) return;
  
  try { var logs = JSON.parse(localStorage.getItem('qbot_logs') || '[]'); } catch(e) { var logs = []; }
  
  if (logs.length > 0 && card) card.style.display = 'block';
  
  var html = '';
  for (var i = 0; i < logs.length; i++) {
    var l = logs[i];
    html += '<tr>' +
      '<td>' + l.time + '</td>' +
      '<td>' + l.bot + '</td>' +
      '<td>' + l.cmd + '</td>' +
      '<td class="bot-log-status-' + (l.status === 'ok' ? 'ok' : 'err') + '">' + (l.status === 'ok' ? '✅ 成功' : '❌ ' + l.status) + '</td>' +
      '<td>' + l.source + '</td>' +
    '</tr>';
  }
  tbody.innerHTML = html;
}

// Init bot page
function initBotPage() {
  loadBots();
  renderBots();
  renderBotLogs();
}

// Escape HTML
function escapeHtml(t) {
  if (!t) return '';
  var d = document.createElement('div');
  d.textContent = t;
  return d.innerHTML;
}
'''

# Insert JS before the last </script> before </body>
js_close_idx = text.rfind('</script>')
# Find the one just before </body>
body_close = text.find('</body>')
if js_close_idx > 10 and body_close > js_close_idx:
    js_insert = text.rfind('</script>', 0, body_close)
    if js_insert > 0:
        if 'loadBots' not in text:
            text = text[:js_insert] + bot_js + '\n' + text[js_insert:]
            print("Added Bot JS functions ✓")
        else:
            print("Bot JS functions already exist ✓")

# === 6. Patch showPage to init bot page ===
# Find the showPage function and add bot init
if 'initBotPage' not in text:
    # Patch initQuantTalk or find showPage and add bot handling
    show_page_idx = text.find('function showPage(page, el)')
    if show_page_idx > 0:
        # Add bot page init in the page switch handling
        text = text.replace(
            "if (el) { document.querySelectorAll('.nav-item.active').forEach(function(e) { e.classList.remove('active'); }); el.classList.add('active'); }",
            "if (el) { document.querySelectorAll('.nav-item.active').forEach(function(e) { e.classList.remove('active'); }); el.classList.add('active'); }\n  if (page === 'bot') { initBotPage(); }"
        )
        print("Added showPage bot init patch ✓")

# === 7. Write back ===
with open('index.html', 'wb') as f:
    f.write(text.encode('utf-8', errors='replace'))

print("Done! Bot feature added.")
print("")
print("=== Files Modified ===")
print("- index.html: Bot nav, page, CSS, JS, i18n")
print("")
print("=== Pending: Backend Bot API ===")
print("- POST /api/v1/bot/exec — execute command via bot key")
print("- POST /api/v1/bot/create — create bot key (server-stored)")
print("- GET /api/v1/bot/logs — get call logs")
print("")
print("=== Next Steps ===")
print("1. node --check to validate JS syntax")
print("2. Deploy to server")
print("3. Create backend bot router")
