# -*- coding: utf-8 -*-
"""
Clean rebuild from d340005 base:
1. Remove old page-arbitrage (first one)
2. Add sim engine JS 
3. Move CS fab to sidebar
"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# 1. Find old page-arbitrage (first one) and check new one (second)
first = t.find('<!-- ===== 跨交易所聚合引擎 ===== -->')
second = t.find('<!-- ===== 智能套利引擎 ===== -->')
print(f'First arb: {first}')
print(f'Second arb: {second}')

# Remove first arb page
end_first = t.find('<div class="page" id="page-stratmarket"', first)
t = t[:first] + t[end_first:]
print(f'After removing first arb: {len(t)} chars')

# 2. Find second arb page - add flow viz + trade log sections
second_start = t.find('=== 智能套利引擎')
second_end = t.find('<!-- ===== 复制交易', second_start)
close_div = t.rfind('</div>', second_start, second_end)
print(f'Second arb: {second_start} to {second_end}, closes at {close_div}')

# Add flow + log before closing </div>
insertion = '''
        <!-- 搬砖流向可视化 -->
        <div class="card" style="padding:14px;margin-bottom:12px">
          <div style="font-weight:700;margin-bottom:10px">📊 <span data-i18n="arb_flow"></span></div>
          <div id="arb-flow-container" style="display:flex;flex-direction:column;gap:10px">
            <div class="arb-flow-row" style="display:flex;align-items:center;gap:10px;padding:10px;background:var(--card-bg);border:1px solid var(--border);border-radius:8px">
              <div style="flex:0 0 80px;text-align:center;font-weight:700;font-size:13px;color:var(--green)">Binance</div>
              <div style="flex:1;height:3px;background:var(--border);border-radius:2px;overflow:hidden">
                <div style="width:100%;height:3px;background:linear-gradient(90deg,var(--green),var(--blue));animation:arb-flow-bar 1.5s infinite"></div>
              </div>
              <div style="flex:0 0 80px;text-align:center;font-weight:700;font-size:13px;color:var(--blue)">OKX</div>
            </div>
          </div>
        </div>

        <!-- 交易日志 -->
        <div class="card" style="padding:14px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
            <div style="font-weight:700">📝 <span data-i18n="arb_log_title"></span></div>
            <div style="font-size:11px;color:var(--muted)" data-i18n="arb_log_auto_refresh"></div>
          </div>
          <div id="arb-trade-log" style="max-height:250px;overflow-y:auto;font-size:12px;font-family:monospace">
            <div style="padding:4px 0;color:var(--muted)" data-i18n="arb_history_empty"></div>
          </div>
        </div>

        <style>
          @keyframes arb-flow-bar {
            0% { transform: scaleX(0); opacity: 0; }
            50% { transform: scaleX(1); opacity: 1; }
            100% { transform: scaleX(0); opacity: 0; transform-origin: right; }
          }
        </style>'''

t = t[:close_div+7] + '\n' + insertion + t[close_div+7:]
print(f'Added flow + log. Length: {len(t)}')

# 3. Add i18n keys for arb_log/arb_flow/arb_bind
# Chinese block
zh_insert = "    arb_history:'套利执行历史', arb_history_empty:'暂无历史记录',"
zh_replace = zh_insert + "\n    arb_bind:'绑定交易所', arb_flow:'搬砖流向可视化', arb_log_title:'交易日志', arb_log_auto_refresh:'自动刷新中',"
if zh_insert in t:
    t = t.replace(zh_insert, zh_replace)
    print('Added ZH i18n keys')

# English block
en_insert = "    arb_history:'History', arb_history_empty:'No history',"
en_replace = en_insert + "\n    arb_bind:'Connect Exchange', arb_flow:'Arbitrage Flow', arb_log_title:'Execution Log', arb_log_auto_refresh:'Auto-refreshing',"
if en_insert in t:
    t = t.replace(en_insert, en_replace)
    print('Added EN i18n keys')

# 4. Add pageTitles entry for arbitrage
pagetitles_insert = "'square':" + "'QuantTalk'"
pagetitles_replace = "'arbitrage':" + "'跨交易所聚合引擎'" + ",'square':" + "'QuantTalk'"
if pagetitles_insert in t:
    t = t.replace(pagetitles_insert, pagetitles_replace)
    print('Added pageTitles arbitrage')

# 5. Add sim engine JS - insert before first arb variable declaration
anchor = 'let _arbInterval = null;'
pos = t.find(anchor)
if pos < 0:
    for m in ['let _arbRunning', '_arbHistory', '_arbInterval']:
        p = t.find(m, t.find('// Arb变量'))
        if p > 0: pos = p; break

print(f'Sim engine anchor at: {pos}')

sim_js = r'''
// ===== 跨交易所聚合引擎 - 模拟引擎 =====
const ARB_SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT'];
const EXCHANGE_ICONS = {'binance':'🟡','okx':'🔵','bybit':'🟣','kucoin':'🟠'};
const EXCHANGE_NAMES = {'binance':'Binance','okx':'OKX','bybit':'Bybit','kucoin':'KuCoin'};

function getSimPrices(symbol) {
  const basePrices = {'BTC/USDT': 67500, 'ETH/USDT': 3450, 'BNB/USDT': 610, 'SOL/USDT': 145, 'XRP/USDT': 0.62};
  const base = basePrices[symbol] || 50000;
  const v = [ -0.001, 0.0005, 0.002, -0.0015, 0.001, -0.0008 ];
  return {'binance': base*(1+v[0]+(Math.random()-0.5)*0.002), 'okx': base*(1+v[1]+(Math.random()-0.5)*0.002), 'bybit': base*(1+v[2]+(Math.random()-0.5)*0.002), 'kucoin': base*(1+v[3]+(Math.random()-0.5)*0.002)};
}
function getConnectedExchanges() { try{return JSON.parse(localStorage.getItem('arb_exchanges')||'{}')}catch(e){return {}} }
function renderConnectedExchanges() {
  const c = document.getElementById('arb-exchange-status'); if(!c) return;
  const exs = getConnectedExchanges();
  c.innerHTML = ['binance','okx','bybit','kucoin'].map(ex => {
    const s = exs[ex] ? 'on' : 'off';
    return '<div class="exchange-item '+s+'" data-ex="'+ex+'" style="cursor:pointer" onclick="addExchange(\''+ex+'\')"><div style="font-weight:600">'+(EXCHANGE_ICONS[ex]||'')+' '+(EXCHANGE_NAMES[ex]||ex)+'</div><div style="font-size:11px;color:var(--muted)">'+(s==='on'?'✅ 已连接':'❌ 未连接')+'</div><div style="font-size:12px;margin-top:2px" class="arb-balance">'+(s==='on'?'$'+(Math.random()*50000+1000).toFixed(2):'—')+'</div></div>';
  }).join('');
  return Object.keys(exs);
}
function syncExchangesToArbitrage() { 
  const s = localStorage.getItem('connected_exchanges');
  if(s) try{localStorage.setItem('arb_exchanges',s)}catch(e){}
  renderConnectedExchanges();
  try{toast('交易所已同步','success')}catch(e){}
}
function addExchange(n) { showPage('account'); try{toast('请先在【我的账户】中绑定交易所API','info')}catch(e){} }
function removeExchange(n) { const e=getConnectedExchanges(); delete e[n]; localStorage.setItem('arb_exchanges',JSON.stringify(e)); renderConnectedExchanges(); try{toast('已移除 '+n,'info')}catch(e){} }
function loadArbitragePrices() {
  const sym = document.getElementById('arb-symbol-select')?.value||'BTC/USDT';
  const prices = getSimPrices(sym);
  const grid = document.getElementById('arb-prices-grid');
  if(grid) {
    const vals = Object.values(prices); const max = Math.max(...vals); const min = Math.min(...vals);
    grid.innerHTML = Object.entries(prices).map(([ex,pr]) => {
      const isMax = pr===max; const isMin = pr===min;
      return '<div style="padding:10px;border:1px solid var(--border);border-radius:8px"><div style="font-weight:600;font-size:13px">'+(EXCHANGE_ICONS[ex]||'')+' '+(EXCHANGE_NAMES[ex]||ex)+'</div><div style="font-size:16px;font-weight:800;color:'+(isMax?'var(--green)':isMin?'var(--blue)':'var(--muted)')+';margin-top:4px">$'+pr.toFixed(2)+'</div><div style="font-size:11px;color:var(--muted);margin-top:2px">'+(isMax?'↑':isMin?'↓':'—')+'</div></div>';
    }).join('');
    if(vals.length>=2) {
      const spread = (max-min)/min*100;
      document.getElementById('arb-current-spread').textContent = spread.toFixed(3)+'%';
      document.getElementById('arb-spread-change').innerHTML = spread>0.1?'<span style="color:var(--green)">✓ 有机会</span>':'<span style="color:var(--muted)">- 无机会</span>';
      updateArbFlow(prices, sym);
    }
  }
  document.getElementById('arb-pairs-count').textContent = ARB_SYMBOLS.length;
}
function updateArbFlow(prices, sym) {
  const c = document.getElementById('arb-flow-container'); if(!c) return;
  const entries = Object.entries(prices); let bestBuy=null, bestSell=null, maxSpread=0;
  for(let i=0;i<entries.length;i++) for(let j=0;j<entries.length;j++) { if(i===j) continue;
    const sp = (entries[j][1]-entries[i][1])/entries[i][1]*100;
    if(sp>maxSpread){maxSpread=sp; bestBuy=entries[i]; bestSell=entries[j];}
  }
  if(maxSpread<0.01) { c.innerHTML='<div style="padding:20px;text-align:center;color:var(--muted);font-size:13px">暂无可用的套利价差</div>'; return; }
  const est = (1000*maxSpread/100).toFixed(2);
  c.innerHTML = '<div class="arb-flow-row" style="display:flex;align-items:center;gap:10px;padding:12px;background:rgba(34,197,94,0.05);border:1px solid rgba(34,197,94,0.2);border-radius:10px">'+
    '<div style="flex:0 0 100px;text-align:center"><div style="font-weight:700;font-size:14px;color:var(--green)">'+(EXCHANGE_ICONS[bestBuy[0]]||'')+' '+(EXCHANGE_NAMES[bestBuy[0]]||bestBuy[0])+'</div><div style="font-size:11px;color:var(--muted)">$'+bestBuy[1].toFixed(2)+'</div><div style="font-size:10px;color:var(--green);margin-top:2px">买入</div></div>'+
    '<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px"><div style="font-size:12px;font-weight:600;color:var(--text)">'+sym+'</div><div style="width:100%;height:3px;background:var(--border);border-radius:2px;overflow:hidden;position:relative"><div style="position:absolute;left:0;top:0;width:100%;height:3px;background:linear-gradient(90deg,var(--green),var(--blue));animation:arb-flow-bar 1.5s ease-in-out infinite"></div></div><div style="font-size:11px;color:var(--muted)"><span style="color:var(--green)">+'+maxSpread.toFixed(3)+'%</span> · 预估盈利 <span style="color:var(--green);font-weight:700">$'+est+'</span></div></div>'+
    '<div style="flex:0 0 100px;text-align:center"><div style="font-weight:700;font-size:14px;color:var(--blue)">'+(EXCHANGE_ICONS[bestSell[0]]||'')+' '+(EXCHANGE_NAMES[bestSell[0]]||bestSell[0])+'</div><div style="font-size:11px;color:var(--muted)">$'+bestSell[1].toFixed(2)+'</div><div style="font-size:10px;color:var(--blue);margin-top:2px">卖出</div></div></div>';
  const ms = parseFloat(document.getElementById('arb-min-spread')?.value||0.1);
  if(maxSpread>=ms) addArbTradeLog({symbol:sym,buy_exchange:bestBuy[0],sell_exchange:bestSell[0],buy_price:bestBuy[1],sell_price:bestSell[1],spread_percent:maxSpread,estimated_profit:parseFloat(est),time:new Date().toLocaleString()});
}
function addArbTradeLog(sig) {
  const log = document.getElementById('arb-trade-log'); if(!log) return;
  const em = log.querySelector('[data-i18n="arb_history_empty"]'); if(em) em.remove();
  const buy = EXCHANGE_NAMES[sig.buy_exchange]||sig.buy_exchange, sell = EXCHANGE_NAMES[sig.sell_exchange]||sig.sell_exchange;
  const e = document.createElement('div'); e.style.cssText = 'padding:6px 0;border-bottom:1px solid var(--border);font-size:12px;display:flex;gap:8px;align-items:center';
  e.innerHTML = '<span style="color:var(--muted);flex:0 0 70px">'+(sig.time.split(' ')[1]||sig.time)+'</span> <span style="color:var(--text);font-weight:600">'+sig.symbol+'</span> <span style="color:var(--green)">'+buy+'</span> <span style="color:var(--muted)">→</span> <span style="color:var(--blue)">'+sell+'</span> <span style="color:var(--green);font-weight:700;margin-left:auto">+'+sig.spread_percent.toFixed(3)+'%</span> <span style="color:var(--green);font-weight:700;flex:0 0 80px;text-align:right">$'+sig.estimated_profit.toFixed(2)+'</span>';
  log.insertBefore(e, log.firstChild);
  while(log.children.length>50) log.removeChild(log.lastChild);
  document.getElementById('arb-total-profit').textContent = '$'+(parseFloat(document.getElementById('arb-total-profit').textContent.replace('$','')||0)+sig.estimated_profit).toFixed(2);
  document.getElementById('arb-trade-count').textContent = parseInt(document.getElementById('arb-trade-count').textContent)+1;
}
function startArbitrageEngine() {
  _arbRunning=true; _arbAITrading=true;
  document.getElementById('arb-start-btn').style.display='none';
  document.getElementById('arb-stop-btn').style.display='';
  document.getElementById('arb-engine-status').innerHTML='🟢 <span data-i18n="arb_engine_running">运行中</span>';
  loadArbitragePrices();
  _arbInterval = setInterval(()=>{if(!_arbRunning)return;loadArbitragePrices()}, 5000);
  try{toast('AI 搬砖引擎已启动','success')}catch(e){}
  localStorage.setItem('arb_state',JSON.stringify({running:true}));
}
function stopArbitrageEngine() {
  _arbRunning=false; _arbAITrading=false;
  if(_arbInterval){clearInterval(_arbInterval);_arbInterval=null;}
  document.getElementById('arb-start-btn').style.display='';document.getElementById('arb-stop-btn').style.display='none';
  document.getElementById('arb-engine-status').innerHTML='⏸️ <span data-i18n="arb_engine_stopped">已停止</span>';
  try{toast('引擎已停止','info')}catch(e){}
  localStorage.setItem('arb_state',JSON.stringify({running:false}));
}
function scanArbitrage() { loadArbitragePrices(); try{toast('扫描完成','success')}catch(e){} }
function initArbitragePage() {
  syncExchangesToArbitrage();
  const isElite = _userPlan==='elite';
  const banner = document.getElementById('arb-lock-banner');
  if(banner) banner.style.display = isElite ? 'none' : 'flex';
  if(!isElite) { document.querySelectorAll('#page-arbitrage .card').forEach((c,i)=>{ if(i>=1&&i<=3){c.style.opacity='0.5';c.style.pointerEvents='none';}}); }
  loadArbitragePrices();
  renderConnectedExchanges();
  const s=localStorage.getItem('arb_state');
  if(s) try{const st=JSON.parse(s);if(st.running)startArbitrageEngine()}catch(e){}
}
function initExchangeUI() { renderConnectedExchanges(); }
function renderArbHistory() {}
function syncArbToConsole(sig) { const h=JSON.parse(localStorage.getItem('arb_history')||'[]'); h.unshift(sig); if(h.length>50)h.pop(); localStorage.setItem('arb_history',JSON.stringify(h)); }
'''

t = t[:pos] + '\n' + sim_js + '\n' + t[pos:]

# 6. Move CS from bottom-right to sidebar
fab_pos = t.find('id="cs-fab"')
if fab_pos > 0:
    div_start = t.rfind('<div', fab_pos-200, fab_pos)
    if div_start < 0: div_start = t.rfind('<', fab_pos-100, fab_pos)
    div_end = t.find('</div>', fab_pos) + 6
    before = t[:div_start].rstrip()
    after = t[div_end:].lstrip()
    t = before + '\n' + after
    print(f'Removed cs-fab ({div_start} to {div_end})')

# Find sidebar user card and add CS entry before </aside>
card = t.find('id="sidebar-user-card"')
if card > 0:
    aside_close = t.find('</aside>', card)
    cs_sidebar = '''
        <div onclick="toggleCS()" style="display:flex;align-items:center;gap:8px;padding:10px 16px;cursor:pointer;border-top:1px solid var(--border);margin-top:8px;transition:background 0.2s;border-radius:8px" onmouseover="this.style.background='var(--hover)'" onmouseout="this.style.background='transparent'">
          <span style="font-size:16px">💬</span>
          <span style="font-size:13px" data-i18n="cs_sidebar">官方客服</span>
        </div>'''
    t = t[:aside_close] + cs_sidebar + t[aside_close:]
    print(f'Added CS sidebar entry ({aside_close})')

# 7. Add cs_sidebar i18n
if 'cs_sidebar' not in t:
    zh = t.find("nav_dashboard:'仪表盘'")
    if zh > 0:
        le = t.find('\n', zh)
        t = t[:le+1] + "    cs_sidebar:'官方客服',\n" + t[le+1:]
    en = t.find("nav_dashboard:'Dashboard'")
    if en > 0:
        le = t.find('\n', en)
        t = t[:le+1] + "    cs_sidebar:'Customer Service',\n" + t[le+1:]

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Final verification
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')
print(f'\nFinal: {len(data)/1024:.1f} KB')
import re
funcs = set(m.group(1) for m in re.finditer(r'function (\w+)\(', text))
dupes = [f for f in funcs if text.count('function '+f+'(')>1]
print(f'Duplicate functions: {dupes}')
for k in ['arb-flow-container','arb-trade-log','cs_sidebar','toggleCS','getSimPrices','startArbitrageEngine']:
    print(f'{k}: {text.count(k)}')
