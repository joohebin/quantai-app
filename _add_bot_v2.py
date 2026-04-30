"""Force-add Bot page HTML, i18n, and JS to index.html"""
import sys
sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)

with open('index.html', 'rb') as f:
    d = bytearray(f.read())

text = d.decode('utf-8', errors='replace')

# === 1. BOT PAGE HTML ===
bot_html = '''
      <!-- Bot Page -->
      <div id="page-bot" class="page-content" style="display:none">
        <div class="bot-header">
          <h2 data-i18n="bot_title">🤖 Bot 远程控制</h2>
          <p class="bot-subtitle" data-i18n="bot_subtitle">创建私人 Bot Key，通过国内平台远程控制量化交易</p>
        </div>
        
        <div class="bot-card create-bot-card">
          <div class="bot-card-header"><span class="bot-card-icon">🔑</span><span data-i18n="bot_create_title">创建 Bot</span></div>
          <div class="bot-card-body">
            <div class="bot-form-row">
              <input type="text" id="bot-name-input" placeholder="Bot 名称（例如：我的QQ交易助手）" />
              <button class="btn btn-primary" onclick="createBotKey()" data-i18n="bot_create_btn">生成 Bot Key</button>
            </div>
          </div>
        </div>

        <div class="bot-card">
          <div class="bot-card-header"><span class="bot-card-icon">📋</span><span data-i18n="bot_my_bots">我的 Bot</span></div>
          <div class="bot-card-body" id="bot-list"><div class="bot-empty">暂无 Bot，点击上方按钮创建</div></div>
        </div>

        <div class="bot-card">
          <div class="bot-card-header"><span class="bot-card-icon">📖</span><span data-i18n="bot_guide_title">使用说明</span></div>
          <div class="bot-card-body">
            <div class="bot-guide-steps">
              <div class="bot-guide-step"><span class="step-num">1</span><div><strong>创建 Bot</strong><p>为每个平台分别创建 Bot</p></div></div>
              <div class="bot-guide-step"><span class="step-num">2</span><div><strong>配置平台适配器</strong><p>将 Bot Key 填入平台的 Webhook/机器人配置中</p></div></div>
              <div class="bot-guide-step"><span class="step-num">3</span><div><strong>发送指令</strong><p>在平台发送消息即可远程控制交易，无需挂 VPN</p></div></div>
            </div>
          </div>
        </div>

        <div class="bot-card">
          <div class="bot-card-header"><span class="bot-card-icon">📝</span><span data-i18n="bot_cmds_title">支持指令</span></div>
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
          <div class="bot-card-header"><span class="bot-card-icon">📊</span><span data-i18n="bot_logs">调用记录</span></div>
          <div class="bot-card-body">
            <table class="bot-log-table"><thead><tr><th>时间</th><th>Bot</th><th>指令</th><th>状态</th><th>来源</th></tr></thead><tbody id="bot-log-body"></tbody></table>
          </div>
        </div>
      </div>'''

if 'id="page-bot"' in text:
    print("page-bot already exists ✓")
else:
    # Insert before the first page-content that's NOT dashboard (before market page)
    market_pos = text.find('id="page-market"')
    calc_start = text.rfind('<', market_pos - 500, market_pos)
    if calc_start > 0:
        text = text[:calc_start] + bot_html + '\n' + text[calc_start:]
        print("Added page-bot HTML ✓")

# === 2. BOT JS FUNCTIONS ===
bot_js = '''
// ========== Bot Remote Control ==========
window._bots = [];
window._botOrders = [];

function loadBots() {
  try { var stored = localStorage.getItem('qbots'); window._bots = stored ? JSON.parse(stored) : []; }
  catch(e) { window._bots = []; }
  return window._bots;
}
function saveBots() { localStorage.setItem('qbots', JSON.stringify(window._bots)); }

function genBotKey() {
  var chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  var key = 'qbot_';
  for (var i = 0; i < 32; i++) key += chars.charAt(Math.floor(Math.random() * chars.length));
  return key;
}

function renderBots() {
  var list = document.getElementById('bot-list');
  if (!list) return;
  loadBots();
  if (window._bots.length === 0) {
    list.innerHTML = '<div class="bot-empty">暂无 Bot，点击上方按钮创建</div>';
    return;
  }
  var h = '';
  for (var i = 0; i < window._bots.length; i++) {
    var b = window._bots[i];
    h += '<div class="bot-item"><div class="bot-item-info"><div class="bot-item-name">' + escHtml(b.name) + '</div><div class="bot-item-key" onclick="cpKey(''' + b.key + ''')" title="点击复制">' + b.key + '</div><div class="bot-item-date">' + (b.created || '') + (b.lastUsed ? ' | 使用: ' + b.lastUsed : '') + '</div></div><div class="bot-item-actions"><button class="btn btn-sm btn-primary" onclick="cpKey(''' + b.key + ''')">复制</button><button class="btn btn-sm btn-danger" onclick="delKey(''' + b.key + ''')">删除</button></div></div>';
  }
  list.innerHTML = h;
}

function createBotKey() {
  var inp = document.getElementById('bot-name-input');
  var name = inp ? inp.value.trim() : '';
  if (!name) name = 'Bot #' + (window._bots.length + 1);
  var bot = { key: genBotKey(), name: name, created: new Date().toLocaleString('zh-CN'), lastUsed: null, callCount: 0 };
  window._bots.push(bot);
  saveBots();
  renderBots();
  if (inp) inp.value = '';
  showTradeConfirm({title: 'Bot Key 创建成功', message: '<p style="font-size:18px;font-weight:600;text-align:center;padding:10px;word-break:break-all">' + bot.key + '</p><p style="color:var(--muted);text-align:center">点击确定复制 Key</p>', confirmText: '复制', cancelText: '关闭', onConfirm: function() { cpKey(bot.key); }});
}

function cpKey(key) {
  if (navigator.clipboard) { navigator.clipboard.writeText(key); }
  else { var ta = document.createElement('textarea'); ta.value = key; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); }
  showTradeConfirm({title: '已复制', message: 'Bot Key 已复制到剪贴板', confirmText: '确定', cancelText: ''});
}

function delKey(key) {
  showTradeConfirm({title: '确认删除', message: '删除后该 Key 立即失效。', confirmText: '删除', cancelText: '取消', onConfirm: function() { window._bots = window._bots.filter(function(b) { return b.key !== key; }); saveBots(); renderBots(); }});
}

function botExecute(key, cmd) {
  loadBots();
  var bot = null;
  for (var i = 0; i < window._bots.length; i++) { if (window._bots[i].key === key) { bot = window._bots[i]; break; } }
  if (!bot) return {error: 'Bot key not found'};
  bot.lastUsed = new Date().toLocaleString('zh-CN');
  bot.callCount = (bot.callCount || 0) + 1;
  saveBots();
  logBotCall(bot.name, cmd, 'ok', 'API');
  return parseBotCommand(cmd);
}

function parseBotCommand(text) {
  var t = text.trim();
  if (t.includes('持仓') || /positions?/i.test(t)) return {action:'view_positions',message:'持仓信息已发送'};
  if (t.includes('策略') && !t.includes('创建')) return {action:'view_strategies',message:'策略列表已发送'};
  if (t.includes('开启') && (t.includes('自动')||t.includes('AI'))) return {action:'start_auto',message:'自动交易已开启'};
  if (t.includes('关闭') && (t.includes('自动')||t.includes('AI'))) return {action:'stop_auto',message:'自动交易已关闭'};
  if (t.includes('创建') && t.includes('策略')) {
    var m = t.match(/策略[\s]*(\w+)/);
    return {action:'create_strategy',params:{type:m?m[1]:'custom'},message:'策略创建请求已接收'};
  }
  var order = parseVoiceOrder(t);
  if (order && order.isOrder) {
    window._botOrders.push(order);
    if (typeof sendTradeSignal === 'function') sendTradeSignal(order);
    return {action:'execute_order',params:{order:order},message:'订单已接收: '+(order.side||order.action)+' '+order.amount+' '+order.symbol};
  }
  return {action:'unknown',message:'无法识别的指令。试试：查看持仓、买入1BTC、开启自动交易'};
}

function logBotCall(botName, cmd, status, source) {
  try { var logs = JSON.parse(localStorage.getItem('qbot_logs') || '[]'); } catch(e) { var logs = []; }
  logs.unshift({time:new Date().toLocaleString('zh-CN'),bot:botName,cmd:cmd.substring(0,50),status:status,source:source});
  if (logs.length > 100) logs = logs.slice(0,100);
  localStorage.setItem('qbot_logs', JSON.stringify(logs));
  renderBotLogs();
}

function renderBotLogs() {
  var tbody = document.getElementById('bot-log-body');
  var card = document.getElementById('bot-log-card');
  if (!tbody) return;
  try { var logs = JSON.parse(localStorage.getItem('qbot_logs') || '[]'); } catch(e) { var logs = []; }
  if (logs.length > 0 && card) card.style.display = 'block';
  var h = '';
  for (var i = 0; i < logs.length; i++) {
    var l = logs[i];
    h += '<tr><td>' + l.time + '</td><td>' + l.bot + '</td><td>' + l.cmd + '</td><td class="bot-log-' + (l.status==='ok'?'ok':'err') + '">' + (l.status==='ok'?'成功':'失败') + '</td><td>' + l.source + '</td></tr>';
  }
  tbody.innerHTML = h;
}

function initBotPage() {
  loadBots();
  renderBots();
  renderBotLogs();
}

function escHtml(t) {
  if (!t) return '';
  var d = document.createElement('div');
  d.textContent = t;
  return d.innerHTML;
}
'''

if 'loadBots' in text:
    print("Bot JS already exists ✓")
else:
    # Find the last </script> before </body>
    body_pos = text.find('</body>')
    script_end = text.rfind('</script>', 0, body_pos)
    if script_end > 0:
        text = text[:script_end] + bot_js + '\n' + text[script_end:]
        print("Added Bot JS functions ✓")

# === 3. PATCH showPage to init bot page ===
if 'initBotPage' in text and 'page === ' in text:
    # Find showPage function and ensure bot init is called
    sp_idx = text.find('function showPage(page, el)')
    if sp_idx > 0:
        # Check if bot init is already present
        if 'initBotPage' not in text[sp_idx:sp_idx+3000]:
            # Add after the active class setting
            active_line = text.find("el.classList.add('active')", sp_idx, sp_idx+3000)
            if active_line > 0:
                close_brace = text.find('}', active_line)
                if close_brace > 0 and close_brace < active_line + 200:
                    text = text[:close_brace] + '\n' + '  if (page === "bot") { initBotPage(); }' + text[close_brace:]
                    print("Patched showPage for bot init ✓")

# === 4. Write back ===
with open('index.html', 'wb') as f:
    f.write(text.encode('utf-8', errors='replace'))

print('\n=== Verification ===')
with open('index.html', 'rb') as f:
    d2 = f.read().decode('utf-8', errors='replace')

for k in ['page-bot', 'loadBots', 'createBotKey', 'initBotPage', '_botOrders', 'botExecute', 'parseBotCommand', 'data-page="bot"']:
    print(f'  {k}: {"✓" if k in d2 else "✗ MISSING!"}')
