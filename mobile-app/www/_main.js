
// ===== 全局状态 =====
let currentPage = 'dashboard';
let orderDir = 'buy';
let klineChart = null;
let candleSeries = null;
let volumeSeries = null;
let btChart = null;
let btLineSeries = null;
let priceInterval = null;
let tickerInterval = null;

// ===== 市场数据 =====
const MARKET_DATA = [
  {sym:'BTC/USDT',fullKey:'sym_btc',cat:'crypto',icon:'₿',bg:'rgba(247,147,26,.15)',price:83420,chg:1.24,vol:'$2.1B'},
  {sym:'ETH/USDT',fullKey:'sym_eth',cat:'crypto',icon:'Ξ',bg:'rgba(98,126,234,.15)',price:3210,chg:-0.38,vol:'$980M'},
  {sym:'SOL/USDT',fullKey:'sym_sol',cat:'crypto',icon:'◎',bg:'rgba(20,241,149,.15)',price:152.4,chg:3.21,vol:'$640M'},
  {sym:'BNB/USDT',fullKey:'sym_bnb',cat:'crypto',icon:'B',bg:'rgba(243,186,47,.15)',price:598.2,chg:0.87,vol:'$320M'},
  {sym:'XRP/USDT',fullKey:'sym_xrp',cat:'crypto',icon:'✕',bg:'rgba(0,148,255,.15)',price:0.527,chg:-1.12,vol:'$280M'},
  {sym:'EUR/USD',fullKey:'sym_eurusd',cat:'forex',icon:'€',bg:'rgba(0,100,255,.15)',price:1.0842,chg:-0.12,vol:'$120B'},
  {sym:'GBP/USD',fullKey:'sym_gbpusd',cat:'forex',icon:'£',bg:'rgba(0,180,120,.15)',price:1.2634,chg:0.08,vol:'$80B'},
  {sym:'USD/JPY',fullKey:'sym_usdjpy',cat:'forex',icon:'¥',bg:'rgba(255,80,60,.15)',price:151.42,chg:0.34,vol:'$75B'},
  {sym:'USD/CHF',fullKey:'sym_usdchf',cat:'forex',icon:'₣',bg:'rgba(220,220,0,.15)',price:0.8934,chg:-0.06,vol:'$40B'},
  {sym:'AUD/USD',fullKey:'sym_audusd',cat:'forex',icon:'A$',bg:'rgba(0,180,200,.15)',price:0.6524,chg:0.22,vol:'$35B'},
  {sym:'XAU/USD',fullKey:'sym_gold',cat:'metals',icon:'🥇',bg:'rgba(255,184,0,.15)',price:2342.5,chg:0.68,vol:'$45B'},
  {sym:'XAG/USD',fullKey:'sym_silver',cat:'metals',icon:'🥈',bg:'rgba(180,180,180,.15)',price:28.42,chg:1.24,vol:'$8B'},
  {sym:'WTI/USD',fullKey:'sym_wti',cat:'energy',icon:'🛢',bg:'rgba(100,60,0,.15)',price:78.34,chg:-0.54,vol:'$20B'},
  {sym:'BRENT',fullKey:'sym_brent',cat:'energy',icon:'⛽',bg:'rgba(120,80,0,.15)',price:82.15,chg:-0.42,vol:'$18B'},
  {sym:'NAS100',fullKey:'sym_nas100',cat:'index',icon:'📊',bg:'rgba(59,130,246,.15)',price:18240,chg:0.92,vol:'$15B'},
  {sym:'SPX500',fullKey:'sym_spx500',cat:'index',icon:'🇺🇸',bg:'rgba(0,100,200,.15)',price:5142,chg:0.45,vol:'$12B'},
  {sym:'DOW',fullKey:'sym_dow',cat:'index',icon:'🏭',bg:'rgba(150,100,200,.15)',price:38420,chg:0.23,vol:'$10B'},
  {sym:'HSI',fullKey:'sym_hsi',cat:'index',icon:'🇭🇰',bg:'rgba(255,50,50,.15)',price:17820,chg:-0.84,vol:'$8B'},
];

// ===== 持仓数据 =====
let POSITIONS = [
  {sym:'BTC/USDT',dir:'long',size:0.05,entry:82100,curr:83420,lev:'5x',pnl:66,sl:80000,tp:88000,broker:'Binance'},
  {sym:'XAU/USD',dir:'long',size:1,entry:2320,curr:2342.5,lev:'10x',pnl:22.5,sl:2280,tp:2400,broker:'MT5'},
  {sym:'EUR/USD',dir:'short',size:10000,entry:1.0890,curr:1.0842,lev:'50x',pnl:48,sl:1.0950,tp:1.0750,broker:'MT5'},
  {sym:'ETH/USDT',dir:'long',size:0.5,entry:3180,curr:3210,lev:'3x',pnl:15,sl:3000,tp:3500,broker:'OKX'},
  {sym:'NAS100',dir:'short',size:1,entry:18400,curr:18240,lev:'20x',pnl:160,sl:18700,tp:17800,broker:'MT5'},
];

// ===== 策略数据 =====
let STRATEGIES = [
  {id:1,nameKey:'strat_name_1',sym:'BTC/USDT',broker:'Binance',typeKey:'strat_type_trend',status:'running',
   pnl:'+$1,240',pnl_pct:'+8.2%',winrate:'67%',trades:89,maxdd:'-5.2%',bars:[4,6,5,8,7,9,6,5,8,10,9,11,8,7,12]},
  {id:2,nameKey:'strat_name_2',sym:'XAU/USD',broker:'MT5',typeKey:'strat_type_grid',status:'running',
   pnl:'+$680',pnl_pct:'+4.5%',winrate:'72%',trades:156,maxdd:'-3.1%',bars:[3,5,4,6,5,7,6,4,5,6,7,8,6,5,7]},
  {id:3,nameKey:'strat_name_3',sym:'EUR/USD',broker:'MT5',typeKey:'strat_type_ema',status:'running',
   pnl:'+$320',pnl_pct:'+2.1%',winrate:'58%',trades:45,maxdd:'-7.4%',bars:[2,4,3,5,4,3,5,4,6,5,4,3,5,6,4]},
  {id:4,nameKey:'strat_name_4',sym:'NAS100',broker:'MT5',typeKey:'strat_type_mr',status:'paused',
   pnl:'-$124',pnl_pct:'-0.8%',winrate:'44%',trades:28,maxdd:'-12.1%',bars:[6,5,4,3,5,4,3,2,4,3,2,3,2,1,2]},
];

// ===== K线初始化 =====
function initKline(){
  const container = document.getElementById('kline-container');
  klineChart = LightweightCharts.createChart(container,{
    layout:{background:{type:'Solid',color:'#111F35'},textColor:'#6B8DB0'},
    grid:{vertLines:{color:'rgba(30,48,80,.5)'},horzLines:{color:'rgba(30,48,80,.5)'}},
    crosshair:{mode:LightweightCharts.CrosshairMode.Normal},
    rightPriceScale:{borderColor:'#1E3050'},
    timeScale:{borderColor:'#1E3050',timeVisible:true,secondsVisible:false},
    width:container.offsetWidth,
    height:container.offsetHeight
  });

  candleSeries = klineChart.addCandlestickSeries({
    upColor:'#00C896',downColor:'#FF4B6E',
    borderUpColor:'#00C896',borderDownColor:'#FF4B6E',
    wickUpColor:'#00C896',wickDownColor:'#FF4B6E'
  });

  volumeSeries = klineChart.addHistogramSeries({
    color:'rgba(0,200,150,.3)',priceFormat:{type:'volume'},
    priceScaleId:'',scaleMargins:{top:.8,bottom:0}
  });

  generateKlineData();

  window.addEventListener('resize',()=>{
    if(klineChart) klineChart.applyOptions({width:container.offsetWidth});
  });
}

function generateKlineData(){
  const data=[], volData=[];
  let price = 83000;
  const now = Math.floor(Date.now()/1000);
  for(let i=200;i>=0;i--){
    const t = now - i*60;
    const o = price;
    const change = (Math.random()-0.48)*800;
    const h = o + Math.abs(change)*1.2 + Math.random()*200;
    const l = o - Math.abs(change)*0.8 - Math.random()*200;
    const c = o + change;
    price = c;
    const isUp = c>=o;
    data.push({time:t,open:+o.toFixed(2),high:+h.toFixed(2),low:+l.toFixed(2),close:+c.toFixed(2)});
    volData.push({time:t,value:Math.random()*500+100,color:isUp?'rgba(0,200,150,.4)':'rgba(255,75,110,.4)'});
  }
  candleSeries.setData(data);
  volumeSeries.setData(volData);

  // 模拟实时更新
  if(priceInterval) clearInterval(priceInterval);
  priceInterval = setInterval(()=>{
    price += (Math.random()-0.48)*300;
    const t=Math.floor(Date.now()/1000);
    const c=+price.toFixed(2);
    candleSeries.update({time:t,open:price-100,high:price+200,low:price-200,close:c});
    volumeSeries.update({time:t,value:Math.random()*200+50,color:c>=price-100?'rgba(0,200,150,.4)':'rgba(255,75,110,.4)'});
    // 更新价格显示
    const chgPct = ((c-83000)/83000*100).toFixed(2);
    document.getElementById('chart-price').textContent='$'+Math.round(c).toLocaleString();
    const el=document.getElementById('chart-change');
    el.textContent=(chgPct>=0?'▲ +':'▼ ')+chgPct+'%';
    el.className='chart-change '+(chgPct>=0?'up':'down');
  },1500);
}

// ===== Ticker 跑马灯 =====
function initTicker(){
  const strip = document.getElementById('ticker-strip');
  const items = MARKET_DATA.slice(0,8);
  strip.innerHTML = items.map(d=>{
    const up = d.chg>=0;
    return `<div class="ticker-item">
      <span class="sym">${d.sym}</span>
      <span>${d.price.toLocaleString()}</span>
      <span class="chg ${up?'up-bg up':'down-bg down'}" style="padding:1px 6px;border-radius:4px;font-size:11px">${up?'▲+':'▼'}${Math.abs(d.chg)}%</span>
    </div>`;
  }).join('');

  // 模拟价格跳动
  if(tickerInterval) clearInterval(tickerInterval);
  tickerInterval = setInterval(()=>{
    MARKET_DATA.forEach(d=>{ d.price += d.price*(Math.random()-0.499)*0.001; });
    strip.innerHTML = MARKET_DATA.slice(0,8).map(d=>{
      const up=d.chg>=0;
      return `<div class="ticker-item">
        <span class="sym">${d.sym}</span>
        <span>${+d.price.toFixed(d.price>100?1:4)}</span>
        <span class="chg ${up?'up':'down'}" style="font-size:11px">${up?'▲+':'▼'}${Math.abs(d.chg).toFixed(2)}%</span>
      </div>`;
    }).join('');
  },2000);
}

// ===== 行情表格 =====
function renderMarket(filter){
  const data = filter==='all'?MARKET_DATA:MARKET_DATA.filter(d=>d.cat===filter);
  const tbody = document.getElementById('market-tbody');
  tbody.innerHTML = data.map(d=>{
    const up=d.chg>=0;
    const bars = Array.from({length:10},()=>Math.random()).map((v,i)=>`<div class="mb ${Math.random()>.5?'':'d'}" style="height:${Math.round(v*100)}%"></div>`).join('');
    const fullName = t(d.fullKey) || d.sym;
    return `<tr onclick="openSymbol('${d.sym}')">
      <td><div class="sym-cell">
        <div class="sym-icon" style="background:${d.bg}">${d.icon}</div>
        <div><div class="sym-name">${d.sym}</div><div class="sym-full">${fullName}</div></div>
      </div></td>
      <td style="font-weight:700;font-size:15px">${+d.price.toFixed(d.price>100?2:4)}</td>
      <td><span class="tag ${up?'tag-green':'tag-red'}">${up?'▲+':'▼'}${Math.abs(d.chg)}%</span></td>
      <td class="muted">${d.vol}</td>
      <td><div class="mini-bar">${bars}</div></td>
      <td><div style="display:flex;gap:6px">
        <button class="btn btn-primary" style="font-size:12px;padding:5px 12px" onclick="event.stopPropagation();quickBuy('${d.sym}')">${t('mkt_buy')||'Buy'}</button>
        <button class="btn btn-danger" style="font-size:12px;padding:5px 12px" onclick="event.stopPropagation();quickSell('${d.sym}')">${t('mkt_sell')||'Sell'}</button>
      </div></td>
    </tr>`;
  }).join('');
}

function filterMarket(cat,el){
  document.querySelectorAll('.mkt-tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  renderMarket(cat);
}

// ===== 持仓渲染 =====
function renderPositions(){
  // 更新持仓摘要栏
  const summary = document.getElementById('pos-summary');
  if(summary){
    const totalPnl = POSITIONS.reduce((s,p)=>s+p.pnl, 0);
    const pnlStr = (totalPnl>=0?'+':'')+'\$'+Math.abs(totalPnl).toFixed(2);
    const pnlCls = totalPnl>=0?'up':'down';
    summary.innerHTML = `${POSITIONS.length}<span style="margin-left:2px">${t('pos_active_count')}</span> · <span>${t('pos_float')}</span> <span class="${pnlCls}">${pnlStr}</span>`;
  }
  const list = document.getElementById('positions-list');
  list.innerHTML = POSITIONS.map((p,i)=>{
    const up = p.pnl>=0;
    const pnlPct = (p.pnl/((p.entry*p.size)||1)*100).toFixed(2);
    const fillW = Math.min(Math.abs(parseFloat(pnlPct)),20)*5;
    return `<div class="pos-card ${p.dir==='short'?'short':''}">
      <div class="pos-header">
        <div style="display:flex;align-items:center;gap:8px">
          <div class="pos-sym">${p.sym}</div>
          <span class="pos-dir-badge tag ${p.dir==='long'?'tag-green':'tag-red'}">${p.dir==='long'?t('card_long')+' LONG':t('card_short')+' SHORT'}</span>
          <span class="tag tag-blue" style="font-size:11px">${p.lev}</span>
          <span class="muted" style="font-size:12px">${p.broker}</span>
        </div>
        <div class="pos-pnl ${up?'':'neg'}">
          ${up?'+':''}\$${Math.abs(p.pnl).toFixed(2)}
          <div style="font-size:13px;font-weight:400">${up?'+':''}${pnlPct}%</div>
        </div>
      </div>
      <div class="pos-pnl-bar"><div class="pos-pnl-fill ${up?'':'neg'}" style="width:${fillW}%"></div></div>
      <div class="pos-grid">
        <div class="pos-item"><div class="lbl">${t('pos_open_lbl')||t('pos_open')}</div><div class="val">${p.entry.toLocaleString()}</div></div>
        <div class="pos-item"><div class="lbl">${t('pos_curr_lbl')||t('pos_current')}</div><div class="val ${up?'up':'down'}">${p.curr.toLocaleString()}</div></div>
        <div class="pos-item"><div class="lbl">${t('pos_sl_lbl')||'SL'}</div><div class="val down">${p.sl.toLocaleString()}</div></div>
        <div class="pos-item"><div class="lbl">${t('pos_tp_lbl')||'TP'}</div><div class="val up">${p.tp.toLocaleString()}</div></div>
      </div>
      <div class="pos-actions">
        <button class="btn btn-outline" style="font-size:12px;flex:1" onclick="aiAnalyze('${p.sym}')">🤖 ${t('pos_ai_analyze')||'AI'}</button>
        <button class="btn" style="font-size:12px;flex:1;background:rgba(255,184,0,.1);color:var(--yellow);border:1px solid rgba(255,184,0,.3)" onclick="editPosition(${i})">✏️ ${t('pos_edit_btn')||t('btn_edit')}</button>
        <button class="btn btn-danger" style="font-size:12px;flex:1" onclick="closePosition(${i})">✕ ${t('pos_close')}</button>
      </div>
    </div>`;
  }).join('');
}

// ===== 策略渲染 =====
function renderStrategies(){
  // 更新策略摘要栏
  const stratSum = document.getElementById('strat-summary');
  if(stratSum){
    const runCount = STRATEGIES.filter(s=>s.status==='running').length;
    const pauseCount = STRATEGIES.filter(s=>s.status==='paused').length;
    stratSum.innerHTML = `${runCount}<span style="margin-left:2px">${t('strat_running_count')}</span> · ${pauseCount}<span style="margin-left:2px">${t('strat_paused_count')}</span>`;
  }
  const grid = document.getElementById('strategy-grid');
  grid.innerHTML = STRATEGIES.map(s=>{
    const running = s.status==='running';
    const up = s.pnl.startsWith('+');
    const bars = s.bars.map((v,i)=>{
      const prev = i>0?s.bars[i-1]:v;
      return `<div class="ps-bar ${v<prev?'d':''}" style="height:${Math.round(v/12*100)}%"></div>`;
    }).join('');
    const stratName = t(s.nameKey) || s.nameKey;
    const stratType = t(s.typeKey) || s.typeKey;
    return `<div class="strat-card">
      <div class="strat-top">
        <div>
          <div class="strat-name">${stratName}</div>
          <div style="font-size:12px;color:var(--muted);margin-top:3px">${s.sym} · ${s.broker} · ${stratType}</div>
        </div>
        <div class="strat-status ${running?'up':'muted'}">
          <span style="width:6px;height:6px;border-radius:50%;background:${running?'var(--green)':'var(--muted)'};display:inline-block"></span>
          ${running?t('strat_running'):t('strat_paused')}
        </div>
      </div>
      <div class="perf-sparkline">${bars}</div>
      <div class="strat-metrics">
        <div class="sm-item"><div class="lbl">${t('strat_cum_pnl')||'P&L'}</div><div class="val ${up?'up':'down'}">${s.pnl}</div></div>
        <div class="sm-item"><div class="lbl">${t('bt_win_rate')}</div><div class="val">${s.winrate}</div></div>
        <div class="sm-item"><div class="lbl">${t('bt_max_dd')}</div><div class="val down">${s.maxdd}</div></div>
      </div>
      <div class="strat-footer">
        <div class="strat-tags">
          <span class="tag tag-blue" style="font-size:11px">${stratType}</span>
          <span class="tag ${up?'tag-green':'tag-red'}" style="font-size:11px">${s.pnl_pct}</span>
        </div>
        <div class="strat-controls">
          <button class="ctrl-btn ${running?'ctrl-pause':'ctrl-run'}" title="${running?t('strat_pause'):t('strat_start')}" onclick="toggleStrat(${s.id})">${running?'⏸':'▶'}</button>
          <button class="ctrl-btn ctrl-del" title="${t('strat_stop')||'Del'}" onclick="deleteStrat(${s.id})">🗑</button>
        </div>
      </div>
    </div>`;
  }).join('');
}

// ===== 账户交易日志 =====
const TLOG_PAIRS = ['BTC/USDT','XAU/USD','EUR/USD','ETH/USDT','NAS100','GBP/USD','AUD/USD','SOL/USDT','WTI/USD','BNB/USDT'];
let _tlogData = [];

function genTlogData(){
  _tlogData = Array.from({length:40},(_,i)=>{
    const buy = Math.random() > .45;
    const pnl = parseFloat(((Math.random()-.42)*480).toFixed(2));
    const pair = TLOG_PAIRS[Math.floor(Math.random()*TLOG_PAIRS.length)];
    const holdH = parseFloat((Math.random()*72+0.5).toFixed(1));
    const basePrice = pair.includes('BTC')?83200:pair.includes('ETH')?3200:pair.includes('XAU')?2340:pair.includes('NAS')?17800:pair.includes('SOL')?145:pair.includes('BNB')?580:1.08;
    const openP = (basePrice*(1+( Math.random()-.5)*.015)).toFixed(pair.includes('USD')&&!pair.includes('BTC')&&!pair.includes('ETH')&&!pair.includes('NAS')&&!pair.includes('SOL')&&!pair.includes('BNB')&&!pair.includes('XAU')? 4:2);
    const closeP = (parseFloat(openP)*(1+(pnl>0?1:-1)*Math.random()*.008)).toFixed(openP.indexOf('.')>=0?openP.split('.')[1].length:2);
    const lots = (Math.random()*0.9+0.1).toFixed(2);
    const d = new Date(Date.now()-i*86400000*2.3 - Math.random()*86400000);
    return {id:i, pair, buy, pnl, openP, closeP, lots, holdH, date:d};
  });
}

function renderTlog(filter='all'){
  const body = document.getElementById('tlog-body');
  if(!body) return;
  if(!_tlogData.length) genTlogData();
  let rows = _tlogData;
  if(filter==='buy')  rows = rows.filter(r=>r.buy);
  if(filter==='sell') rows = rows.filter(r=>!r.buy);
  if(filter==='win')  rows = rows.filter(r=>r.pnl>0);
  if(filter==='loss') rows = rows.filter(r=>r.pnl<=0);

  // 更新汇总
  const total = rows.length;
  const wins  = rows.filter(r=>r.pnl>0).length;
  const netPnl= rows.reduce((s,r)=>s+r.pnl,0).toFixed(2);
  const avgH  = total ? (rows.reduce((s,r)=>s+r.holdH,0)/total).toFixed(1) : 0;
  const best  = total ? Math.max(...rows.map(r=>r.pnl)).toFixed(2) : 0;
  const worst = total ? Math.min(...rows.map(r=>r.pnl)).toFixed(2) : 0;
  const setEl = (id,v)=>{ const el=document.getElementById(id); if(el) el.textContent=v; };
  setEl('tls-total', total);
  setEl('tls-wr',    total ? (wins/total*100).toFixed(1)+'%' : '—');
  const pnlEl = document.getElementById('tls-pnl');
  if(pnlEl){ pnlEl.textContent=(netPnl>0?'+':'')+`$${netPnl}`; pnlEl.className='tls-val '+(netPnl>=0?'up':'down'); }
  setEl('tls-hold',  avgH+'h');
  setEl('tls-best',  '+$'+best);
  setEl('tls-worst', '$'+worst);

  body.innerHTML = rows.map(r=>{
    const buyDir = r.buy ? t('tlog_dir_long') : t('tlog_dir_short');
    const pnlStr = (r.pnl>=0?'+':'')+`$${r.pnl.toFixed(2)}`;
    const pnlCls = r.pnl>=0 ? 'tlog-pnl-up' : 'tlog-pnl-down';
    const dirCls = r.buy ? 'tlog-dir-buy' : 'tlog-dir-sell';
    return `<div class="tlog-row">
      <span class="tlog-muted">${r.date.toISOString().slice(0,16).replace('T',' ')}</span>
      <span style="font-weight:600">${r.pair}</span>
      <span class="${dirCls}">${buyDir}</span>
      <span class="tlog-muted">${r.openP}</span>
      <span class="tlog-muted">${r.closeP}</span>
      <span class="tlog-muted">${r.lots}</span>
      <span class="${pnlCls}">${pnlStr}</span>
      <span class="tlog-muted">${r.holdH}h</span>
    </div>`;
  }).join('') || `<div style="padding:24px;text-align:center;color:var(--muted)" data-i18n="tlog_empty">${t('tlog_empty')}</div>`;
}

function filterTlog(f, btn){
  document.querySelectorAll('.tlog-filter-btn').forEach(b=>b.classList.remove('active'));
  if(btn) btn.classList.add('active');
  renderTlog(f);
}

function runBacktest(){
  const btn = document.getElementById('bt-btn');
  btn.disabled=true; btn.innerHTML='<div class="spinner" style="display:inline-block;vertical-align:middle"></div> '+t('bt_running');
  setTimeout(()=>{
    btn.disabled=false; btn.innerHTML='▶ '+t('bt_run');
    const result = document.getElementById('bt-result');
    result.classList.add('show');
    // 随机化结果
    document.getElementById('bt-return').textContent = '+'+(80+Math.random()*80).toFixed(1)+'%';
    document.getElementById('bt-annual').textContent = '+'+(50+Math.random()*60).toFixed(1)+'%';
    document.getElementById('bt-dd').textContent = '-'+(8+Math.random()*20).toFixed(1)+'%';
    document.getElementById('bt-sharpe').textContent = (1.2+Math.random()*1.5).toFixed(2);
    document.getElementById('bt-wr').textContent = (50+Math.random()*20).toFixed(1)+'%';
    document.getElementById('bt-trades').textContent = Math.floor(100+Math.random()*400);
    renderBtChart();
    renderBtLog();
  },2200);
}

function renderBtChart(){
  const container = document.getElementById('bt-chart');
  if(btChart){btChart.remove();btChart=null;}
  btChart = LightweightCharts.createChart(container,{
    layout:{background:{type:'Solid',color:'#111F35'},textColor:'#6B8DB0'},
    grid:{vertLines:{color:'rgba(30,48,80,.4)'},horzLines:{color:'rgba(30,48,80,.4)'}},
    rightPriceScale:{borderColor:'#1E3050'},
    timeScale:{borderColor:'#1E3050'},
    width:container.offsetWidth,height:300
  });
  btLineSeries = btChart.addAreaSeries({
    lineColor:'#00C896',topColor:'rgba(0,200,150,.3)',bottomColor:'rgba(0,200,150,.02)',lineWidth:2
  });
  const d=[];let val=10000;
  const now=Math.floor(Date.now()/1000);
  for(let i=365;i>=0;i--){
    val+=val*(Math.random()-.44)*.02;
    d.push({time:now-i*86400,value:+val.toFixed(2)});
  }
  btLineSeries.setData(d);
}

function renderBtLog(){
  const pairs=['BTC/USDT','XAU/USD','EUR/USD','ETH/USDT','NAS100'];
  const body=document.getElementById('bt-log-body');
  body.innerHTML=Array.from({length:15},(_,i)=>{
    const buy=Math.random()>.5;
    const pnl=((Math.random()-.4)*200).toFixed(2);
    const up=pnl>0;
    const pair=pairs[Math.floor(Math.random()*pairs.length)];
    const d=new Date(Date.now()-i*86400000*3);
    return `<div class="trade-log-row ${buy?'buy':'sell'}">
      <div class="dir">${buy?'BUY':'SELL'}</div>
      <div class="trade-col val">${pair}</div>
      <div class="trade-col">${d.toISOString().slice(0,10)}</div>
      <div class="trade-col pnl ${up?'up':'down'}">${up?'+':''}$${pnl}</div>
      <div class="trade-col muted">${(Math.random()*24+1).toFixed(1)}h</div>
    </div>`;
  }).join('');
}

// ===== AI 客服 - 调用真实AI =====
async function sendChat(){
  const input=document.getElementById('chat-input');
  const msg=input.value.trim();
  if(!msg) return;
  input.value='';
  addMsg(msg,'user');
  document.getElementById('chat-sugg').style.display='none';
  
  // 打字中动画
  const typingId='typing-'+Date.now();
  addMsg('<div class="typing"><span></span><span></span><span></span></div>','ai',typingId);
  
  try {
    // 调用后端AI API
    const response = await fetch('/api/ai/chat', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({
        message: msg,
        symbol: detectSymbol(msg)  // 尝试检测交易品种
      })
    });
    
    const data = await response.json();
    const el=document.getElementById(typingId);
    if(el) {
      el.querySelector('.bubble').innerHTML = formatAIResponse(data.message || data.analysis || '收到你的消息了！');
    }
  } catch(e) {
    // API调用失败，尝试关键词回复
    const el=document.getElementById(typingId);
    if(el) {
      el.querySelector('.bubble').innerHTML = getKeywordResponse(msg);
    }
  }
  scrollChat();
}

// 检测消息中的交易品种
function detectSymbol(msg) {
  const m = msg.toLowerCase();
  if(m.includes('btc')||m.includes('比特币')) return 'BTC';
  if(m.includes('eth')||m.includes('以太坊')) return 'ETH';
  if(m.includes('黄金')||m.includes('gold')||m.includes('xau')) return 'XAU';
  if(m.includes('原油')||m.includes('oil')||m.includes('wti')) return 'WTI';
  if(m.includes('欧元')||m.includes('eur')) return 'EUR';
  return null;
}

// 格式化AI响应
function formatAIResponse(text) {
  return text
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/📊/g, '<span style="color:#00c896">📊</span>')
    .replace(/🎯/g, '<span style="color:#ffc107">🎯</span>')
    .replace(/💰/g, '<span style="color:#ff9800">💰</span>')
    .replace(/⚡/g, '<span style="color:#2196f3">⚡</span>')
    .replace(/🛡️/g, '<span style="color:#e91e63">🛡️</span>');
}

// 关键词快速回复（API失败时备用）
function getKeywordResponse(msg) {
  const m = msg.toLowerCase();
  if(m.includes('btc')||m.includes('比特币')||m.includes('bitcoin')) return t('ai_resp_btc');
  if(m.includes('黄金')||m.includes('gold')||m.includes('xau')) return t('ai_resp_gold');
  if(m.includes('仓位')||m.includes('分配')||m.includes('position')) return t('ai_resp_position');
  if(m.includes('策略')||m.includes('推荐')||m.includes('strategy')) return t('ai_resp_strategy');
  return t('ai_resp_default');
}

function sendSugg(el){
  document.getElementById('chat-input').value=el.textContent;
  sendChat();
}

function chatKeydown(e){ if(e.key==='Enter') sendChat(); }

function addMsg(content,role,id){
  const isAI=role==='ai';
  const div=document.createElement('div');
  div.className='msg-row'+(isAI?'':' user');
  if(id) div.id=id;
  div.innerHTML=`<div class="msg-av ${isAI?'ai-av':'usr-av'}">${isAI?'🤖':'👤'}</div>
    <div class="bubble ${isAI?'ai-bubble':'user-bubble'}">${content}</div>`;
  document.getElementById('chat-messages').appendChild(div);
  scrollChat();
}
function scrollChat(){
  const c=document.getElementById('chat-messages');
  c.scrollTop=c.scrollHeight;
}

// ===== 页面切换 =====
const pageTitles={dashboard:'仪表盘',market:'行情',ai:'AI 客服',positions:'我的持仓',strategies:'策略管理',backtest:'策略回测',account:'我的账户',copy:'排行榜·跟单',autoopen:'自动建仓',square:'交易广场',stratmarket:'策略市场',signals:'信号广播'};

function showPage(name, navEl){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  const el=document.getElementById('page-'+name);
  if(el) el.classList.add('active');
  currentPage=name;
  window._currentPage = name;

  // 更新侧边栏高亮
  document.querySelectorAll('#sidebar .nav-item').forEach(n=>{
    n.classList.toggle('active', n.dataset.page===name);
  });
  // 标题：优先用 i18n，降级用 pageTitles中文映射，绝不显示裸name字符串
  const titleKey = 'page_' + name;
  let titleText = pageTitles[name] || name; // 默认中文fallback
  if(typeof t === 'function'){
    const translated = t(titleKey);
    if(translated && translated !== titleKey){
      titleText = translated; // i18n 有值，用翻译
    } else {
      // t()失败时：用zh字典兜底，再用pageTitles，绝不暴露name
      titleText = (I18N && I18N.zh && I18N.zh[titleKey]) || pageTitles[name] || name;
    }
  }
  const pageTitleEl = document.getElementById('page-title');
  if(pageTitleEl){
    pageTitleEl.textContent = titleText;
    pageTitleEl.setAttribute('data-i18n', titleKey); // 同步更新，切语言时能正确翻译
  }

  // 按需初始化
  if(name==='market') renderMarket('all');
  if(name==='positions') renderPositions();
  if(name==='strategies') renderStrategies();
  if(name==='account') renderTlog('all');
  if(name==='copy') initLbPage();
  if(name==='autoopen') initAutoOpen();
  if(name==='square') renderSquare('all');
  if(name==='stratmarket') renderStratMarket('all');
  if(name==='signals') renderSignalsPage();

  closeSidebar();
}

function setMobNav(el){
  document.querySelectorAll('.mob-nav-item').forEach(n=>n.classList.remove('active'));
  el.classList.add('active');
}

// ===== 下单 =====
function setDir(d){
  orderDir=d;
  document.getElementById('dir-buy').classList.toggle('sel',d==='buy');
  document.getElementById('dir-sell').classList.toggle('sel',d==='sell');
}

function placeOrder(){
  const sym=document.getElementById('order-symbol').value;
  const amt=document.getElementById('order-amount').value;
  const dir=orderDir==='buy'?t('dir_long'):t('dir_short');
  toast(`✅ ${dir} ${sym} $${amt} `+(t('toast_order_ok')||'Order placed!'),'success');
}

function showOrderModal(){ document.getElementById('order-modal').classList.add('show'); }
function submitOrder(){
  const sym=document.getElementById('m-symbol').value;
  const dir=document.getElementById('m-dir').value;
  const amt=document.getElementById('m-amount').value;
  closeModal('order-modal');
  const dirText=dir==='buy'?t('dir_long'):t('dir_short');
  toast(`✅ ${dirText} ${sym} \$${amt} `+(t('toast_submitted')||'Submitted!'),'success');
}

function quickBuy(sym){ document.getElementById('m-symbol').value=sym; document.getElementById('m-dir').value='buy'; showOrderModal(); }
function quickSell(sym){ document.getElementById('m-symbol').value=sym; document.getElementById('m-dir').value='sell'; showOrderModal(); }

// ===== 持仓操作 =====
function closePosition(i){
  const p=POSITIONS[i];
  if(confirm(`${t('confirm_close_pos')||'Close'} ${p.sym}? P&L ${p.pnl>=0?'+':''}$${p.pnl}`)){
    POSITIONS.splice(i,1);
    renderPositions();
    toast(`✅ ${p.sym} `+(t('toast_pos_closed')||'Closed'),'success');
  }
}
function editPosition(i){ toast('✏️ '+(t('toast_coming_soon')||'Coming soon'),''); }
function aiAnalyze(sym){ showPage('ai',null); setTimeout(()=>{ document.getElementById('chat-input').value=sym+(t('ai_analyze_suffix')||' analysis?'); sendChat(); },300); }
function closeAllConfirm(){ if(confirm(t('confirm_close_all')||'Close all positions?')){ POSITIONS=[]; renderPositions(); toast('⚡ '+(t('toast_all_closed')||'All positions closed'),'success'); } }

// ===== 策略操作 =====
function toggleStrat(id){
  const s=STRATEGIES.find(x=>x.id===id);
  if(s){ s.status=s.status==='running'?'paused':'running'; renderStrategies();
    const sName=t(s.nameKey)||s.nameKey;
    toast(s.status==='running'?`▶ "${sName}" `+(t('toast_strat_started')||'started'):`⏸ "${sName}" `+(t('toast_strat_paused')||'paused'),''); }
}
function deleteStrat(id){
  const s=STRATEGIES.find(x=>x.id===id);
  const sName=t(s&&s.nameKey)||'Strategy';
  if(s&&confirm(`${t('confirm_del_strat')||'Delete strategy'} "${sName}"?`)){ STRATEGIES=STRATEGIES.filter(x=>x.id!==id); renderStrategies(); toast(`🗑 `+(t('toast_strat_deleted')||'Deleted'),''); }
}
function showAddStrategy(){ toast('➕ '+(t('toast_coming_soon')||'Coming soon'),''); }

// ===== 券商 =====
function showBrokerModal(){ document.getElementById('broker-modal').classList.add('show'); }
function selectBroker(el,name){
  document.querySelectorAll('#broker-modal .broker-card').forEach(c=>c.style.borderColor='var(--border)');
  el.style.borderColor='var(--green)';
}
function connectBroker(){ closeModal('broker-modal'); toast('✅ '+(t('toast_broker_connected')||'Broker connected! API verified'),'success'); }

// ===== 工具函数 =====
function openSymbol(sym){ showPage('dashboard',null); document.querySelector('.chart-symbol').textContent=sym; }
function setInterval_(iv,el){ document.querySelectorAll('.iv-btn').forEach(b=>b.classList.remove('active')); el.classList.add('active'); generateKlineData(); }
function closeModal(id){ document.getElementById(id).classList.remove('show'); }
function toggleSidebar(){ document.getElementById('sidebar').classList.toggle('open'); document.getElementById('overlay').classList.toggle('show'); }
function closeSidebar(){ document.getElementById('sidebar').classList.remove('open'); document.getElementById('overlay').classList.remove('show'); }
// ===== 多语言翻译系统 =====
const I18N = {
  zh: {
    // 侧边栏导航
    nav_dashboard: '仪表盘', nav_market: '行情', nav_ai: 'AI 客服',
    nav_positions: '我的持仓', nav_strategies: '策略管理', nav_backtest: '策略回测', nav_account: '我的账户',
    // 顶部标题
    page_dashboard: '仪表盘', page_market: '行情', page_ai: 'AI 客服',
    page_positions: '我的持仓', page_strategies: '策略管理', page_backtest: '策略回测', page_account: '我的账户',
    page_copy: '跟单交易', page_autoopen: '自动建仓',
    // 仪表盘卡片标题
    total_asset: '总资产', daily_pnl: '今日盈亏', win_rate: '胜率', active_strategies: '活跃策略', pos_count: '持仓数量',
    // 仪表盘卡片副文字
    card_today: '今日', card_month: '本月', card_paused: '个暂停', card_running: '个运行中',
    card_long: '多', card_short: '空',
    // 快速下单按钮
    quick_order: '+ 快速下单',
    // 图表
    chart_update: '分钟更新',
    // 行情页
    market_title: '实时行情', search_placeholder: '搜索品种...',
    mkt_all: '全部', mkt_crypto: '加密货币', mkt_forex: '外汇', mkt_metals: '贵金属', mkt_energy: '能源', mkt_index: '指数',
    tbl_symbol: '品种', tbl_price: '最新价', tbl_change: '涨跌幅', tbl_volume: '成交量', tbl_trend: '7日走势', tbl_action: '操作',
    // AI客服
    ai_title: 'AI 量化助手', ai_placeholder: '输入你的交易指令或问题...',
    ai_welcome: '你好！我是 QuantAI 智能助手 🤖\n\n我可以帮你：\n• 查询实时行情和K线分析\n• 管理持仓和下单交易\n• 解读策略绩效\n• 风控建议和仓位管理\n\n请问有什么可以帮您的？',
    ai_feat1: '分析市场行情并给出策略建议', ai_feat2: '执行自动化交易下单',
    ai_feat3: '计算仓位、止损止盈点位', ai_feat4: '回测你的策略历史表现',
    ai_sugg1: 'BTC 现在可以买入吗？', ai_sugg2: '帮我做一个黄金网格策略',
    ai_sugg3: '我有$1000，怎么分配仓位？', ai_sugg4: 'EUR/USD 趋势分析', ai_sugg5: '查看我的持仓情况',
    quick_order_title: '快速下单', dir_long: '做多 Long', dir_short: '做空 Short',
    order_symbol: '交易品种', order_amount: '投入金额 (USD)', order_sltp: '止损 / 止盈 (%)', order_confirm: '确认下单',
    sentiment_title: '市场情绪', sent_bull: '多头', sent_bear: '空头', sent_fg: '恐贪指数', sent_greed: '贪婪', sent_flow: '大单净流入', sent_rate: '资金费率',
    // 持仓
    pos_title: '我的持仓', pos_symbol: '品种', pos_size: '手数', pos_open: '开仓价', pos_current: '当前价', pos_pnl: '浮盈/亏', pos_action: '操作',
    pos_close: '平仓', pos_empty: '暂无持仓',
    pos_my_title: '我的持仓', pos_active_count: '个活跃持仓', pos_float: '浮盈', close_all: '一键全平',
    pos_open_lbl: '开仓价', pos_curr_lbl: '当前价', pos_sl_lbl: '止损价', pos_tp_lbl: '止盈价',
    pos_ai_analyze: 'AI分析', pos_edit_btn: '修改',
    mkt_buy: '买入', mkt_sell: '卖出',
    strat_cum_pnl: '累计盈亏',
    // 策略
    strat_title: '策略管理', strat_new: '新建策略',
    strat_running: '运行中', strat_paused: '已暂停', strat_stopped: '已停止',
    strat_start: '启动', strat_pause: '暂停', strat_stop: '停止', strat_edit: '编辑',
    strat_my_title: '我的策略', strat_running_count: '个运行中', strat_paused_count: '个已暂停', strat_add: '添加策略',
    // 回测
    bt_title: '策略回测', bt_symbol: '交易品种', bt_strat_type: '策略类型',
    bt_start_date: '开始日期', bt_end_date: '结束日期', bt_capital: '初始资金 (USD)', bt_pos_size: '每笔仓位 (%)',
    bt_run: '开始回测', bt_total_return: '总收益率', bt_annual_return: '年化收益', bt_max_dd: '最大回撤',
    bt_sharpe: '夏普比率', bt_win_rate: '胜率', bt_trades: '总交易次数', bt_log_title: '交易记录（最近20笔）',
    strat_macd: 'MACD 趋势追踪', strat_ema: 'EMA 均线交叉', strat_rsi: 'RSI 超买超卖', strat_grid: '网格交易', strat_bb: '布林带突破',
    // 账户
    acc_title: '我的账户', acc_plan: '当前方案', acc_upgrade: '升级订阅',
    acc_broker: '券商账户', acc_connect: '连接券商',
    acc_member_free: '免费版', acc_member_pro: 'Pro 会员', acc_member_elite: '精英会员',
    acc_valid_until: '有效期至', acc_reg_date: '注册时间', acc_total_pnl: '总盈利',
    acc_brokers_count: '已连接券商', acc_running_strats: '运行策略', acc_account: '账户',
    acc_broker_section: '已连接券商', acc_subscription: '我的订阅',
    broker_connected: '已连接', broker_api_ok: 'API正常', broker_not_connected: '未连接', broker_pending: '待配置', broker_add_new: '添加新券商',
    btn_manage: '管理', btn_disconnect: '断开', btn_connect: '连接', btn_edit: '修改',
    plan_current: '当前', per_month: '/月', plan_view_all: '查看全部方案 →',
    plan_basic_f1: '全品种行情查看', plan_basic_f2: 'AI客服问答', plan_basic_f3: '2个策略', plan_basic_f4: '自动交易',
    plan_pro_f1: '无限策略', plan_pro_f2: 'AI自动交易', plan_pro_f3: '高级回测', plan_pro_f4: '多券商',
    plan_elite_f1: '自动建仓（策略/定投/跟单）', plan_elite_f2: '复制交易无限跟单', plan_elite_f3: '专属VIP客服', plan_elite_f4: '优先执行通道',
    plan_pro_f1: '无限策略', plan_pro_f2: 'AI自动交易', plan_pro_f3: '高级回测', plan_pro_f4: '多券商',
    risk_title: '风控设置', risk_max_loss: '单日最大亏损', risk_max_loss_desc: '超过后自动停止所有策略',
    risk_max_pos: '最大持仓比例', risk_max_pos_desc: '单品种不超过总资产百分比',
    risk_auto_order: 'AI 自动下单', risk_auto_order_desc: '允许AI在策略触发时自动执行',
    risk_notify: '下单前推送通知', risk_notify_desc: '每次下单前发送确认',
    risk_night: '夜间保护模式', risk_night_desc: '22:00-07:00 暂停自动交易',
    // 通用
    confirm: '确认', cancel: '取消', save: '保存', close: '关闭',
    loading: '加载中...', success: '操作成功', error: '操作失败',
    lang_switched: '🌐 已切换为中文',
    // 交易日志
    tlog_title:'交易日志', tlog_all:'全部', tlog_buy:'做多', tlog_sell:'做空', tlog_win:'盈利', tlog_loss:'亏损',
    tlog_total_trades:'总笔数', tlog_win_rate:'胜率', tlog_net_pnl:'净盈亏', tlog_avg_hold:'平均持仓', tlog_best:'最佳单笔', tlog_worst:'最差单笔',
    tlog_col_time:'时间', tlog_col_symbol:'品种', tlog_col_dir:'方向', tlog_col_open:'开仓价', tlog_col_close:'平仓价', tlog_col_size:'手数', tlog_col_pnl:'盈亏', tlog_col_hold:'持仓时长',
    tlog_dir_long:'做多', tlog_dir_short:'做空', tlog_empty:'暂无交易记录',
    // 复制交易
    nav_copy:'复制交易', copy_title:'复制交易', copy_subtitle:'一键跟随顶级交易者，信号实时同步',
    copy_goto_auto:'自动建仓设置', copy_my_follows:'我的跟单', copy_leaderboard:'信号源排行',
    copy_filter_all:'全部', copy_filter_crypto:'加密', copy_filter_forex:'外汇', copy_filter_stable:'低回撤',
    copy_followers:'人跟随', copy_monthly:'月收益', copy_winrate:'胜率', copy_maxdd:'最大回撤', copy_30pnl:'近30天盈利',
    copy_follow_btn:'跟单', copy_following:'✓ 已跟随', copy_unfollow:'取消跟随', copy_detail_btn:'详情',
    copy_pnl:'浮盈', copy_since:'跟随自', copy_follow_title:'跟单设置', copy_confirm_follow:'确认跟单',
    copy_toast_follow:'已开始跟单', copy_toast_unfollow:'已取消跟随',
    ct_tag_ct1:'BTC/ETH 专家 · 3年', ct_tag_ct2:'黄金/外汇 · 5年', ct_tag_ct3:'低回撤稳健型 · 4年',
    ct_tag_ct4:'夜盘剥头皮 · 2年', ct_tag_ct5:'宏观多品种 · 6年', ct_tag_ct6:'定投+趋势 · 7年',
    // 自动建仓
    nav_autoopen:'自动建仓', ao_title:'自动建仓', ao_subtitle:'三种智能建仓模式，全自动执行',
    ao_lock_title:'自动建仓为 Elite 专属功能', ao_lock_desc:'升级到 Elite 计划，解锁全自动交易建仓能力',
    ao_lock_btn:'立即升级 $199/月',
    ao_mode_signal:'策略触发', ao_mode_signal_desc:'RSI/MACD/EMA 等技术指标触发时自动建仓',
    ao_mode_dca:'定时定投', ao_mode_dca_desc:'按设定周期自动分批建仓，平均成本',
    ao_mode_copy:'跟单同步', ao_mode_copy_desc:'绑定信号源，自动同步其每笔开仓操作',
    ao_running:'运行中',
    ao_signal_cfg:'策略触发配置', ao_signal_ind:'触发指标', ao_signal_pair:'交易品种',
    ao_dca_cfg:'定时定投配置', ao_dca_pair:'定投品种', ao_dca_freq:'定投频率',
    ao_dca_hourly:'每小时', ao_dca_daily:'每天', ao_dca_weekly:'每周', ao_dca_monthly:'每月',
    ao_dca_amount:'每次金额 (USD)', ao_dca_total:'总投入上限 (USD)', ao_dca_price_drop:'下跌加倍 (%)', ao_dca_exit:'止盈退出 (%)',
    ao_dca_invested:'已投入',
    ao_copy_cfg:'跟单同步配置', ao_copy_source:'绑定信号源', ao_copy_select:'选择信号源',
    ao_copy_ratio:'跟单倍数', ao_copy_max:'单笔最大 (USD)', ao_copy_daily_loss:'日亏损保护 (USD)',
    ao_copy_filter:'只跟方向', ao_copy_all:'多空均跟', ao_copy_long_only:'只跟做多', ao_copy_short_only:'只跟做空',
    ao_copy_pairs:'限制品种', ao_copy_pairs_ph:'BTC,ETH（空=不限）', ao_not_following:'未跟随',
    ao_pos_size:'每笔仓位 (USD)', ao_sl:'止损 (%)', ao_tp:'止盈 (%)', ao_max_pos:'最大同时持仓',

    // 排行榜升级
    lb_tab_roi:'月收益排行', lb_tab_wr:'胜率排行', lb_tab_stable:'最稳排行', lb_tab_new:'新秀榜',
    // 交易广场
    nav_square:'交易广场', sq_title:'交易广场', sq_subtitle:'分享观点，发现市场情绪，与全球交易者同频',
    sq_post_ph:'分享你的市场观点、交易逻辑、仓位分析...', sq_post_btn:'发布观点',
    sq_filter_all:'全部', sq_filter_bull:'看多', sq_filter_bear:'看空', sq_filter_hot:'热门',
    sq_pair_label:'交易对', sq_sentiment_label:'情绪',
    // 策略市场
    nav_stratmarket:'策略市场', sm_title:'策略市场', sm_subtitle:'发现、分享、一键复用顶级量化策略',
    sm_upload_title:'发布我的策略', sm_upload_btn:'上传策略', sm_filter_all:'全部',
    sm_filter_trend:'趋势跟踪', sm_filter_grid:'网格', sm_filter_quant:'量化', sm_filter_arb:'套利',
    sm_name_label:'策略名称', sm_asset_label:'适用品种', sm_price_label:'定价(USD/月,0=免费)',
    sm_code_label:'策略代码 (Pine Script/伪代码)', sm_submit_btn:'提交审核', sm_backtest:'回测',
    sm_copy:'复制', sm_subscribe:'订阅',
    // 信号广播
    nav_signals:'信号广播', sig_title:'信号广播', sig_subtitle:'实时交易信号，一键订阅推送，接入自动建仓',
    sig_publish_title:'发布交易信号', sig_tab_live:'实时信号', sig_tab_sources:'信号源', sig_tab_history:'历史记录',
    sig_pair:'交易对', sig_dir:'方向', sig_dir_buy:'做多', sig_dir_sell:'做空',
    sig_entry:'入场价', sig_sl:'止损', sig_tp1:'TP1', sig_tp2:'TP2',
    sig_desc:'信号说明', sig_publish_btn:'广播信号',
    sig_follow:'跟单信号', sig_share:'分享', sig_subscribe_bc:'订阅信号源',
    ao_start:'启动自动建仓', ao_stop:'停止运行', ao_status_off:'● 未启动', ao_status_on:'🟢 运行中',
    ao_started:'已启动', ao_stopped:'已停止',
    ao_exec_log:'执行日志', ao_clear_log:'清空', ao_log_empty:'暂无执行记录',
    toast_elite_unlocked:'已解锁 Elite！自动建仓功能已开启',
    // Dashboard 简报 & 快捷操作
    dash_brief_title: 'AI 今日简报', dash_brief_time: '08:00 更新',
    dash_brief_content: '黄金今日偏多，美联储鸽派信号支撑，目标位 $2,380。BTC 在 $84,000 面临压力，短期建议观望。纳指受科技股财报带动，整体偏强。外汇方面 EUR/USD 弱势震荡，美元指数 104.2 支撑。',
    dash_signal_gold: '黄金 ▲ 多', dash_signal_btc: 'BTC ⚠ 观望', dash_signal_eur: 'EUR/USD ▼ 弱', dash_signal_nas: '纳指 ▲ 强',
    dash_quick_ops: '快捷操作', dash_btn_order: 'AI 下单', dash_btn_backtest: '快速回测', dash_btn_positions: '查看持仓',
    // AI欢迎消息
    ai_welcome_greet: '你好！我是 QuantAI 智能助手 🧠', ai_welcome_intro: '你可以告诉我你的交易想法，我会帮你：',
    // 模态框标签
    modal_symbol: '品种', modal_dir: '方向', modal_amount: '金额 (USD)', modal_leverage: '杠杆倍数',
    modal_sl: '止损 (%)', modal_tp: '止盈 (%)', modal_margin: '预计保证金', modal_max_profit: '最大收益', modal_max_loss: '最大亏损',
    // 券商模态框
    broker_modal_title: '连接新券商', broker_connect_btn: '验证并连接',
    cat_crypto: '加密货币', cat_forex_metals: '外汇/贵金属', cat_all_cfd: '全品种CFD',
    // 市场品种名
    sym_btc:'比特币',sym_eth:'以太坊',sym_sol:'Solana',sym_bnb:'币安币',sym_xrp:'瑞波币',
    sym_eurusd:'欧元/美元',sym_gbpusd:'英镑/美元',sym_usdjpy:'美元/日元',sym_usdchf:'美元/瑞郎',sym_audusd:'澳元/美元',
    sym_gold:'黄金现货',sym_silver:'白银现货',sym_wti:'WTI原油',sym_brent:'布伦特原油',
    sym_nas100:'纳斯达克100',sym_spx500:'标普500',sym_dow:'道琼斯',sym_hsi:'恒生指数',
    // 策略名称和类型
    strat_name_1:'BTC MACD趋势策略',strat_name_2:'黄金网格套利',strat_name_3:'EUR/USD 均线策略',strat_name_4:'纳指超短线',
    strat_type_trend:'趋势跟踪',strat_type_grid:'网格交易',strat_type_ema:'均线交叉',strat_type_mr:'均值回归',
    // Toast消息
    toast_order_ok:'下单成功！', toast_submitted:'已提交！', toast_pos_closed:'已平仓', toast_all_closed:'所有持仓已全部平仓',
    toast_strat_started:'已启动', toast_strat_paused:'已暂停', toast_strat_deleted:'策略已删除',
    toast_broker_connected:'券商连接成功！API 验证通过', toast_coming_soon:'功能即将上线，敬请期待',
    toast_upgrading:'即将跳转到', toast_view_plans:'查看完整订阅方案',
    // 确认对话框
    confirm_close_pos:'确认平仓', confirm_close_all:'确认一键全平所有持仓？此操作不可撤销！', confirm_del_strat:'确认删除策略',
    // 回测运行中
    bt_running:'回测中...',
    // AI分析后缀
    ai_analyze_suffix:' 当前持仓怎么看？',
    ai_placeholder:'输入你的交易指令或问题…',
    ai_resp_btc:'📊 BTC/USDT 当前分析：\n\n价格在 $83,400 附近，近期面临 $84,000 压力位。MACD 指标出现金叉信号，RSI(14) 在 58，偏多但未超买。\n\n建议：可在 $82,800 支撑附近小仓试多，止损 $81,000，目标 $86,000。风险收益比约 1:2.2。',
    ai_resp_gold:'🥇 黄金(XAU/USD)分析：\n\n金价维持强势，当前 $2,342。美联储降息预期支撑，美元指数偏弱。近期目标 $2,380，关键支撑 $2,310。\n\n建议：可持有多单，移动止损至 $2,320 锁住利润。',
    ai_resp_position:'📐 仓位管理建议（$1,000 资金）：\n\n• BTC/USDT: 30% ($300) — 主仓，5倍杠杆\n• XAU/USD: 25% ($250) — 对冲，10倍杠杆\n• EUR/USD: 20% ($200) — 外汇对冲\n• 现金储备: 25% ($250) — 等待机会\n\n单笔最大亏损控制在 3%。',
    ai_resp_strategy:'⚡ 为您推荐3个适合当前行情的策略：\n\n1. **BTC MACD趋势** — 胜率67%，回测年化+89%\n2. **黄金网格** — 适合震荡行情，月收益3-5%\n3. **EUR/USD均线** — 低风险，适合新手\n\n是否要我帮您开启某个策略？',
    ai_resp_default:'我理解了您的需求。根据当前市场情况，让我为您分析一下...\n\n📊 市场整体偏多，但需注意美联储政策风险。建议保持仓位在50%以下，并设置好止损。\n\n有什么具体的交易品种或策略想深入了解吗？',
  },
  en: {
    nav_dashboard: 'Dashboard', nav_market: 'Market', nav_ai: 'AI Chat',
    nav_positions: 'Positions', nav_strategies: 'Strategies', nav_backtest: 'Backtest', nav_account: 'Account',
    page_dashboard: 'Dashboard', page_market: 'Market', page_ai: 'AI Assistant',
    page_positions: 'My Positions', page_strategies: 'Strategy Manager', page_backtest: 'Backtest', page_account: 'My Account',
    page_copy: 'Copy Trading', page_autoopen: 'Auto Open',
    total_asset: 'Total Assets', daily_pnl: "Today's P&L", win_rate: 'Win Rate', active_strategies: 'Active Strategies', pos_count: 'Open Positions',
    card_today: 'Today', card_month: 'This Month', card_paused: ' Paused', card_running: ' Running',
    card_long: 'Long', card_short: 'Short',
    quick_order: '+ Quick Order',
    chart_update: 'min update',
    market_title: 'Live Market', search_placeholder: 'Search symbol...',
    mkt_all: 'All', mkt_crypto: 'Crypto', mkt_forex: 'Forex', mkt_metals: 'Metals', mkt_energy: 'Energy', mkt_index: 'Index',
    tbl_symbol: 'Symbol', tbl_price: 'Price', tbl_change: 'Change', tbl_volume: 'Volume', tbl_trend: '7D Trend', tbl_action: 'Action',
    ai_title: 'AI Trading Assistant', ai_placeholder: 'Type a message...',
    ai_welcome: 'Hello! I\'m QuantAI Assistant 🤖\n\nI can help you:\n• Real-time market data & chart analysis\n• Manage positions & place orders\n• Strategy performance review\n• Risk management & position sizing\n\nHow can I assist you today?',
    ai_feat1: 'Analyze market trends & suggest strategies', ai_feat2: 'Execute automated trade orders',
    ai_feat3: 'Calculate position sizing & stop levels', ai_feat4: 'Backtest your strategy performance',
    ai_sugg1: 'Should I buy BTC now?', ai_sugg2: 'Create a gold grid strategy',
    ai_sugg3: 'I have $1000, how to allocate?', ai_sugg4: 'EUR/USD trend analysis', ai_sugg5: 'Show my positions',
    quick_order_title: 'Quick Order', dir_long: 'Long Buy', dir_short: 'Short Sell',
    order_symbol: 'Symbol', order_amount: 'Amount (USD)', order_sltp: 'Stop Loss / Take Profit (%)', order_confirm: 'Place Order',
    sentiment_title: 'Market Sentiment', sent_bull: 'Bull', sent_bear: 'Bear', sent_fg: 'Fear & Greed', sent_greed: 'Greed', sent_flow: 'Net Large Inflow', sent_rate: 'Funding Rate',
    pos_title: 'My Positions', pos_symbol: 'Symbol', pos_size: 'Size', pos_open: 'Open Price', pos_current: 'Current', pos_pnl: 'P&L', pos_action: 'Action',
    pos_close: 'Close', pos_empty: 'No open positions',
    pos_my_title: 'My Positions', pos_active_count: ' Active Positions', pos_float: 'Floating P&L', close_all: 'Close All',
    pos_open_lbl: 'Open Price', pos_curr_lbl: 'Current', pos_sl_lbl: 'Stop Loss', pos_tp_lbl: 'Take Profit',
    pos_ai_analyze: 'AI Analysis', pos_edit_btn: 'Edit',
    mkt_buy: 'Buy', mkt_sell: 'Sell',
    strat_cum_pnl: 'Total P&L',
    strat_title: 'Strategy Manager', strat_new: 'New Strategy',
    strat_running: 'Running', strat_paused: 'Paused', strat_stopped: 'Stopped',
    strat_start: 'Start', strat_pause: 'Pause', strat_stop: 'Stop', strat_edit: 'Edit',
    strat_my_title: 'My Strategies', strat_running_count: ' Running', strat_paused_count: ' Paused', strat_add: 'Add Strategy',
    bt_title: 'Backtest', bt_symbol: 'Symbol', bt_strat_type: 'Strategy Type',
    bt_start_date: 'Start Date', bt_end_date: 'End Date', bt_capital: 'Initial Capital (USD)', bt_pos_size: 'Position Size (%)',
    bt_run: 'Run Backtest', bt_total_return: 'Total Return', bt_annual_return: 'Annual Return', bt_max_dd: 'Max Drawdown',
    bt_sharpe: 'Sharpe Ratio', bt_win_rate: 'Win Rate', bt_trades: 'Total Trades', bt_log_title: 'Trade Log (Last 20)',
    strat_macd: 'MACD Trend Following', strat_ema: 'EMA Crossover', strat_rsi: 'RSI Overbought/Oversold', strat_grid: 'Grid Trading', strat_bb: 'Bollinger Breakout',
    acc_title: 'My Account', acc_plan: 'Current Plan', acc_upgrade: 'Upgrade',
    acc_broker: 'Broker Account', acc_connect: 'Connect Broker',
    acc_member_free: 'Free', acc_member_pro: 'Pro Member', acc_member_elite: 'Elite Member',
    acc_valid_until: 'Valid Until', acc_reg_date: 'Registered', acc_total_pnl: 'Total P&L',
    acc_brokers_count: 'Brokers', acc_running_strats: 'Active Strategies', acc_account: 'Account',
    acc_broker_section: 'Connected Brokers', acc_subscription: 'My Subscription',
    broker_connected: 'Connected', broker_api_ok: 'API OK', broker_not_connected: 'Not Connected', broker_pending: 'Pending', broker_add_new: 'Add Broker',
    btn_manage: 'Manage', btn_disconnect: 'Disconnect', btn_connect: 'Connect', btn_edit: 'Edit',
    plan_current: 'Current', per_month: '/mo', plan_view_all: 'View All Plans →',
    plan_basic_f1: 'All market data', plan_basic_f2: 'AI Q&A', plan_basic_f3: '2 strategies', plan_basic_f4: 'Auto trading',
    plan_pro_f1: 'Unlimited strategies', plan_pro_f2: 'AI auto trading', plan_pro_f3: 'Advanced backtest', plan_pro_f4: 'Multi-broker',
    plan_elite_f1: 'Auto Open (Signal/DCA/Copy)', plan_elite_f2: 'Unlimited copy trading', plan_elite_f3: 'VIP support', plan_elite_f4: 'Priority execution',
    plan_pro_f1: 'Unlimited strategies', plan_pro_f2: 'AI auto trading', plan_pro_f3: 'Advanced backtest', plan_pro_f4: 'Multi-broker',
    risk_title: 'Risk Controls', risk_max_loss: 'Daily Max Loss', risk_max_loss_desc: 'Auto-stop all strategies if exceeded',
    risk_max_pos: 'Max Position Size', risk_max_pos_desc: 'Per symbol, % of total assets',
    risk_auto_order: 'AI Auto Order', risk_auto_order_desc: 'Allow AI to execute when strategy triggers',
    risk_notify: 'Pre-order Notification', risk_notify_desc: 'Send confirmation before each trade',
    risk_night: 'Night Protection', risk_night_desc: '22:00-07:00 suspend auto trading',
    confirm: 'Confirm', cancel: 'Cancel', save: 'Save', close: 'Close',
    loading: 'Loading...', success: 'Success', error: 'Error',
    lang_switched: '🌐 Switched to English',
    // Trade Log
    tlog_title:'Trade Log', tlog_all:'All', tlog_buy:'Long', tlog_sell:'Short', tlog_win:'Profit', tlog_loss:'Loss',
    tlog_total_trades:'Trades', tlog_win_rate:'Win Rate', tlog_net_pnl:'Net P&L', tlog_avg_hold:'Avg Hold', tlog_best:'Best Trade', tlog_worst:'Worst Trade',
    tlog_col_time:'Time', tlog_col_symbol:'Symbol', tlog_col_dir:'Dir', tlog_col_open:'Open', tlog_col_close:'Close', tlog_col_size:'Lots', tlog_col_pnl:'P&L', tlog_col_hold:'Hold Time',
    tlog_dir_long:'Long', tlog_dir_short:'Short', tlog_empty:'No trade records',
    nav_copy:'Copy Trading', copy_title:'Copy Trading', copy_subtitle:'Follow top traders, sync signals in real time',
    copy_goto_auto:'Auto Open Settings', copy_my_follows:'My Follows', copy_leaderboard:'Signal Leaderboard',
    copy_filter_all:'All', copy_filter_crypto:'Crypto', copy_filter_forex:'Forex', copy_filter_stable:'Low DD',
    copy_followers:'followers', copy_monthly:'Monthly', copy_winrate:'Win Rate', copy_maxdd:'Max DD', copy_30pnl:'30D P&L',
    copy_follow_btn:'Follow', copy_following:'✓ Following', copy_unfollow:'Unfollow', copy_detail_btn:'Details',
    copy_pnl:'Float P&L', copy_since:'Since', copy_follow_title:'Follow Settings', copy_confirm_follow:'Confirm Follow',
    copy_toast_follow:'Now following', copy_toast_unfollow:'Unfollowed',
    ct_tag_ct1:'BTC/ETH Expert · 3yr', ct_tag_ct2:'Gold/Forex · 5yr', ct_tag_ct3:'Low-DD Stable · 4yr',
    ct_tag_ct4:'Night Scalper · 2yr', ct_tag_ct5:'Macro Multi · 6yr', ct_tag_ct6:'DCA+Trend · 7yr',
    nav_autoopen:'Auto Open', ao_title:'Auto Open', ao_subtitle:'3 intelligent auto-entry modes',
    ao_lock_title:'Auto Open is Elite-only', ao_lock_desc:'Upgrade to Elite to unlock fully automated position opening',
    ao_lock_btn:'Upgrade $199/mo',
    ao_mode_signal:'Signal Trigger', ao_mode_signal_desc:'Auto open when RSI/MACD/EMA conditions are met',
    ao_mode_dca:'Recurring DCA', ao_mode_dca_desc:'Auto buy at set intervals to average cost',
    ao_mode_copy:'Copy Sync', ao_mode_copy_desc:'Mirror every entry from your followed signal source',
    ao_running:'Running',
    ao_signal_cfg:'Signal Trigger Config', ao_signal_ind:'Indicator', ao_signal_pair:'Symbol',
    ao_dca_cfg:'DCA Config', ao_dca_pair:'DCA Symbol', ao_dca_freq:'Frequency',
    ao_dca_hourly:'Hourly', ao_dca_daily:'Daily', ao_dca_weekly:'Weekly', ao_dca_monthly:'Monthly',
    ao_dca_amount:'Amount per Entry (USD)', ao_dca_total:'Total Cap (USD)', ao_dca_price_drop:'Double on Dip (%)', ao_dca_exit:'Take Profit (%)',
    ao_dca_invested:'Invested',
    ao_copy_cfg:'Copy Sync Config', ao_copy_source:'Signal Source', ao_copy_select:'Select source',
    ao_copy_ratio:'Copy Ratio', ao_copy_max:'Max per Trade (USD)', ao_copy_daily_loss:'Daily Loss Guard (USD)',
    ao_copy_filter:'Direction Filter', ao_copy_all:'Long & Short', ao_copy_long_only:'Long Only', ao_copy_short_only:'Short Only',
    ao_copy_pairs:'Limit Symbols', ao_copy_pairs_ph:'BTC,ETH (empty=all)', ao_not_following:'Not Following',
    ao_pos_size:'Position Size (USD)', ao_sl:'Stop Loss (%)', ao_tp:'Take Profit (%)', ao_max_pos:'Max Open Positions',

    // Leaderboard upgrade
    lb_tab_roi:'Monthly ROI', lb_tab_wr:'Win Rate', lb_tab_stable:'Most Stable', lb_tab_new:'Rising Stars',
    // Trading Square
    nav_square:'Trading Square', sq_title:'Trading Square', sq_subtitle:'Share views, discover sentiment, sync with global traders',
    sq_post_ph:'Share your market view, trade logic, position analysis...', sq_post_btn:'Post',
    sq_filter_all:'All', sq_filter_bull:'Bullish', sq_filter_bear:'Bearish', sq_filter_hot:'Hot',
    sq_pair_label:'Pair', sq_sentiment_label:'Sentiment',
    // Strategy Market
    nav_stratmarket:'Strategy Market', sm_title:'Strategy Market', sm_subtitle:'Discover, share, and copy top quant strategies',
    sm_upload_title:'Publish My Strategy', sm_upload_btn:'Upload Strategy', sm_filter_all:'All',
    sm_filter_trend:'Trend', sm_filter_grid:'Grid', sm_filter_quant:'Quant', sm_filter_arb:'Arb',
    sm_name_label:'Strategy Name', sm_asset_label:'Asset', sm_price_label:'Price (USD/mo, 0=Free)',
    sm_code_label:'Strategy Code (Pine Script/Pseudocode)', sm_submit_btn:'Submit for Review', sm_backtest:'Backtest',
    sm_copy:'Copy', sm_subscribe:'Subscribe',
    // Signal Broadcast
    nav_signals:'Signal Broadcast', sig_title:'Signal Broadcast', sig_subtitle:'Live signals, one-click subscribe, connect to Auto Open',
    sig_publish_title:'Publish Trade Signal', sig_tab_live:'Live Signals', sig_tab_sources:'Signal Sources', sig_tab_history:'History',
    sig_pair:'Pair', sig_dir:'Direction', sig_dir_buy:'Buy', sig_dir_sell:'Sell',
    sig_entry:'Entry', sig_sl:'Stop Loss', sig_tp1:'TP1', sig_tp2:'TP2',
    sig_desc:'Signal Note', sig_publish_btn:'Broadcast Signal',
    sig_follow:'Follow Signal', sig_share:'Share', sig_subscribe_bc:'Subscribe Source',
    ao_start:'Start Auto Open', ao_stop:'Stop', ao_status_off:'● Stopped', ao_status_on:'🟢 Running',
    ao_started:'Started', ao_stopped:'Stopped',
    ao_exec_log:'Execution Log', ao_clear_log:'Clear', ao_log_empty:'No execution records',
    toast_elite_unlocked:'Elite unlocked! Auto Open is now available',
    // Dashboard brief & quick ops
    dash_brief_title: 'AI Daily Brief', dash_brief_time: 'Updated 08:00',
    dash_brief_content: 'Gold bullish today, supported by Fed dovish signals, target $2,380. BTC faces resistance at $84,000, short-term cautious. Nasdaq driven by tech earnings, generally strong. EUR/USD weak oscillation, USD index 104.2 support.',
    dash_signal_gold: 'Gold ▲ Bull', dash_signal_btc: 'BTC ⚠ Watch', dash_signal_eur: 'EUR/USD ▼ Weak', dash_signal_nas: 'Nasdaq ▲ Strong',
    dash_quick_ops: 'Quick Actions', dash_btn_order: 'AI Order', dash_btn_backtest: 'Quick Backtest', dash_btn_positions: 'View Positions',
    // AI welcome message
    ai_welcome_greet: 'Hello! I\'m QuantAI Assistant 🧠', ai_welcome_intro: 'Tell me your trading ideas and I\'ll help you:',
    // Modal labels
    modal_symbol: 'Symbol', modal_dir: 'Direction', modal_amount: 'Amount (USD)', modal_leverage: 'Leverage',
    modal_sl: 'Stop Loss (%)', modal_tp: 'Take Profit (%)', modal_margin: 'Est. Margin', modal_max_profit: 'Max Profit', modal_max_loss: 'Max Loss',
    // Broker modal
    broker_modal_title: 'Connect Broker', broker_connect_btn: 'Verify & Connect',
    cat_crypto: 'Crypto', cat_forex_metals: 'Forex / Metals', cat_all_cfd: 'All CFDs',
    // Symbol names
    sym_btc:'Bitcoin',sym_eth:'Ethereum',sym_sol:'Solana',sym_bnb:'BNB',sym_xrp:'Ripple',
    sym_eurusd:'EUR/USD',sym_gbpusd:'GBP/USD',sym_usdjpy:'USD/JPY',sym_usdchf:'USD/CHF',sym_audusd:'AUD/USD',
    sym_gold:'Spot Gold',sym_silver:'Spot Silver',sym_wti:'WTI Crude',sym_brent:'Brent Crude',
    sym_nas100:'Nasdaq 100',sym_spx500:'S&P 500',sym_dow:'Dow Jones',sym_hsi:'Hang Seng',
    // Strategy names & types
    strat_name_1:'BTC MACD Trend',strat_name_2:'Gold Grid Arb',strat_name_3:'EUR/USD EMA Strategy',strat_name_4:'Nasdaq Scalping',
    strat_type_trend:'Trend Following',strat_type_grid:'Grid Trading',strat_type_ema:'EMA Crossover',strat_type_mr:'Mean Reversion',
    // Toast messages
    toast_order_ok:'Order placed!', toast_submitted:'Submitted!', toast_pos_closed:'Position closed', toast_all_closed:'All positions closed',
    toast_strat_started:'started', toast_strat_paused:'paused', toast_strat_deleted:'Strategy deleted',
    toast_broker_connected:'Broker connected! API verified', toast_coming_soon:'Coming soon, stay tuned',
    toast_upgrading:'Redirecting to', toast_view_plans:'View all subscription plans',
    // Confirm dialogs
    confirm_close_pos:'Confirm close', confirm_close_all:'Close all positions? This cannot be undone!', confirm_del_strat:'Delete strategy',
    // Backtest running
    bt_running:'Running...',
    // AI analyze suffix
    ai_analyze_suffix:' how does my position look?',
    ai_placeholder:'Enter your trading instruction or question…',
    ai_resp_btc:'📊 BTC/USDT Analysis:\n\nPrice near $83,400, facing resistance at $84,000. MACD golden cross, RSI(14) at 58 — bullish but not overbought.\n\nSuggestion: Try a small long near $82,800 support, stop at $81,000, target $86,000. R/R ≈ 1:2.2.',
    ai_resp_gold:'🥇 Gold (XAU/USD) Analysis:\n\nGold stays strong at $2,342. Fed dovish signals and weak USD provide support. Near-term target $2,380, key support $2,310.\n\nSuggestion: Hold longs, move stop to $2,320 to lock in profits.',
    ai_resp_position:'📐 Position Sizing ($1,000 capital):\n\n• BTC/USDT: 30% ($300) — Main, 5x leverage\n• XAU/USD: 25% ($250) — Hedge, 10x leverage\n• EUR/USD: 20% ($200) — FX hedge\n• Cash: 25% ($250) — Await opportunity\n\nMax single-trade loss: 3%.',
    ai_resp_strategy:'⚡ 3 Strategies for Current Market:\n\n1. **BTC MACD Trend** — 67% win rate, +89% annual backtest\n2. **Gold Grid** — Best for ranging markets, 3-5%/month\n3. **EUR/USD EMA** — Low risk, great for beginners\n\nShall I activate one for you?',
    ai_resp_default:'I understand your needs. Let me analyze the current market conditions...\n\n📊 Overall market is bullish, but watch Fed policy risks. Keep position below 50% and always set stop-losses.\n\nAny specific symbol or strategy you\'d like to explore?',
  },
  ja: {
    nav_dashboard: 'ダッシュボード', nav_market: '相場', nav_ai: 'AIアシスト',
    nav_positions: 'ポジション', nav_strategies: 'ストラテジー', nav_backtest: 'バックテスト', nav_account: 'アカウント',
    page_dashboard: 'ダッシュボード', page_market: '相場', page_ai: 'AIアシスタント',
    page_positions: 'ポジション', page_strategies: 'ストラテジー管理', page_backtest: 'バックテスト', page_account: 'アカウント',
    page_copy: 'コピートレード', page_autoopen: '自動建玉',
    total_asset: '総資産', daily_pnl: '本日損益', win_rate: '勝率', active_strategies: '稼働中戦略', pos_count: '保有ポジション',
    card_today: '本日', card_month: '今月', card_paused: '停止中', card_running: '稼働中',
    card_long: 'ロング', card_short: 'ショート',
    quick_order: '＋ 注文する',
    chart_update: '分更新',
    market_title: 'リアルタイム相場', search_placeholder: '銘柄を検索...',
    mkt_all: 'すべて', mkt_crypto: '暗号通貨', mkt_forex: 'FX', mkt_metals: '貴金属', mkt_energy: 'エネルギー', mkt_index: '指数',
    tbl_symbol: '銘柄', tbl_price: '最新価格', tbl_change: '変動率', tbl_volume: '出来高', tbl_trend: '7日間推移', tbl_action: '操作',
    ai_title: 'AIトレーディングアシスタント', ai_placeholder: 'メッセージを入力...',
    ai_welcome: 'こんにちは！QuantAIアシスタントです 🤖\n\nお手伝いできること：\n• リアルタイム相場・チャート分析\n• ポジション管理・注文\n• 戦略パフォーマンス分析\n• リスク管理・ポジションサイジング\n\nご質問はありますか？',
    ai_feat1: '市場トレンドを分析して戦略提案', ai_feat2: '自動売買注文を実行',
    ai_feat3: 'ポジションサイズとストップを計算', ai_feat4: '戦略のバックテストを実行',
    ai_sugg1: 'BTCを今買うべきですか？', ai_sugg2: 'ゴールドグリッド戦略を作成',
    ai_sugg3: '$1000の資金配分は？', ai_sugg4: 'EUR/USD トレンド分析', ai_sugg5: 'ポジションを確認',
    quick_order_title: '＋ 注文する', dir_long: 'ロング（買い）', dir_short: 'ショート（売り）',
    order_symbol: '銘柄', order_amount: '投資額 (USD)', order_sltp: 'SL / TP (%)', order_confirm: '注文確定',
    sentiment_title: '市場センチメント', sent_bull: '強気', sent_bear: '弱気', sent_fg: '恐怖&欲望', sent_greed: '欲張り', sent_flow: '大口ネット流入', sent_rate: '資金調達率',
    pos_title: 'ポジション', pos_symbol: '銘柄', pos_size: '数量', pos_open: '建値', pos_current: '現在値', pos_pnl: '損益', pos_action: '操作',
    pos_close: '決済', pos_empty: 'ポジションなし',
    pos_my_title: '保有ポジション', pos_active_count: '件のポジション', pos_float: '含み損益', close_all: '一括決済',
    pos_open_lbl: '建値', pos_curr_lbl: '現在値', pos_sl_lbl: 'SL', pos_tp_lbl: 'TP',
    pos_ai_analyze: 'AI分析', pos_edit_btn: '修正',
    mkt_buy: '買い', mkt_sell: '売り',
    strat_cum_pnl: '累積損益',
    strat_title: 'ストラテジー管理', strat_new: '新規作成',
    strat_running: '稼働中', strat_paused: '一時停止', strat_stopped: '停止',
    strat_start: '開始', strat_pause: '停止', strat_stop: '中断', strat_edit: '編集',
    strat_my_title: 'マイ戦略', strat_running_count: '件稼働中', strat_paused_count: '件一時停止', strat_add: '戦略を追加',
    bt_title: 'バックテスト', bt_symbol: '銘柄', bt_strat_type: '戦略タイプ',
    bt_start_date: '開始日', bt_end_date: '終了日', bt_capital: '初期資金 (USD)', bt_pos_size: 'ポジションサイズ (%)',
    bt_run: 'バックテスト実行', bt_total_return: '総収益率', bt_annual_return: '年間収益', bt_max_dd: '最大下落率',
    bt_sharpe: 'シャープレシオ', bt_win_rate: '勝率', bt_trades: '総取引数', bt_log_title: '取引記録（直近20件）',
    strat_macd: 'MACDトレンドフォロー', strat_ema: 'EMAクロスオーバー', strat_rsi: 'RSI過買過売', strat_grid: 'グリッドトレード', strat_bb: 'ボリンジャーブレイクアウト',
    acc_title: 'アカウント', acc_plan: '現在のプラン', acc_upgrade: 'アップグレード',
    acc_broker: 'ブローカー口座', acc_connect: '接続',
    acc_member_free: '無料版', acc_member_pro: 'Proメンバー', acc_member_elite: 'エリートメンバー',
    acc_valid_until: '有効期限', acc_reg_date: '登録日', acc_total_pnl: '総損益',
    acc_brokers_count: '接続ブローカー', acc_running_strats: '稼働中戦略', acc_account: 'アカウント',
    acc_broker_section: '接続済みブローカー', acc_subscription: 'サブスクリプション',
    broker_connected: '接続済み', broker_api_ok: 'API正常', broker_not_connected: '未接続', broker_pending: '設定待ち', broker_add_new: 'ブローカーを追加',
    btn_manage: '管理', btn_disconnect: '切断', btn_connect: '接続', btn_edit: '編集',
    plan_current: '現在', per_month: '/月', plan_view_all: 'すべてのプランを見る →',
    plan_basic_f1: '全銘柄相場閲覧', plan_basic_f2: 'AI Q&A', plan_basic_f3: '戦略2つ', plan_basic_f4: '自動売買',
    plan_pro_f1: '無制限戦略', plan_pro_f2: 'AI自動売買', plan_pro_f3: '高度バックテスト', plan_pro_f4: 'マルチブローカー',
    risk_title: 'リスク管理設定', risk_max_loss: '日次最大損失', risk_max_loss_desc: '超過時に全戦略を自動停止',
    risk_max_pos: '最大ポジション比率', risk_max_pos_desc: '銘柄あたり総資産の上限%',
    risk_auto_order: 'AI自動注文', risk_auto_order_desc: '戦略トリガー時にAIが自動実行',
    risk_notify: '注文前通知', risk_notify_desc: '各注文前に確認を送信',
    risk_night: '夜間保護モード', risk_night_desc: '22:00-07:00は自動売買停止',
    confirm: '確認', cancel: 'キャンセル', save: '保存', close: '閉じる',
    loading: '読み込み中...', success: '成功', error: 'エラー',
    lang_switched: '🌐 日本語に切り替えました',
    tlog_title:'取引ログ', tlog_all:'すべて', tlog_buy:'ロング', tlog_sell:'ショート', tlog_win:'利益', tlog_loss:'損失',
    tlog_total_trades:'総取引数', tlog_win_rate:'勝率', tlog_net_pnl:'純損益', tlog_avg_hold:'平均保有', tlog_best:'最良取引', tlog_worst:'最悪取引',
    tlog_col_time:'時間', tlog_col_symbol:'銘柄', tlog_col_dir:'方向', tlog_col_open:'建値', tlog_col_close:'決済値', tlog_col_size:'数量', tlog_col_pnl:'損益', tlog_col_hold:'保有期間',
    tlog_dir_long:'ロング', tlog_dir_short:'ショート', tlog_empty:'取引記録なし',
    nav_copy:'コピートレード', copy_title:'コピートレード', copy_subtitle:'トップトレーダーをフォロー、リアルタイム同期',
    copy_goto_auto:'自動建玉設定', copy_my_follows:'フォロー中', copy_leaderboard:'シグナルランキング',
    copy_filter_all:'全て', copy_filter_crypto:'仮想通貨', copy_filter_forex:'FX', copy_filter_stable:'低DD',
    copy_followers:'フォロワー', copy_monthly:'月利', copy_winrate:'勝率', copy_maxdd:'最大DD', copy_30pnl:'30日損益',
    copy_follow_btn:'フォロー', copy_following:'✓ フォロー中', copy_unfollow:'解除', copy_detail_btn:'詳細',
    copy_pnl:'含み損益', copy_since:'開始', copy_follow_title:'フォロー設定', copy_confirm_follow:'フォロー確認',
    copy_toast_follow:'フォロー開始', copy_toast_unfollow:'フォロー解除',
    ct_tag_ct1:'BTC/ETH専門家 · 3年', ct_tag_ct2:'ゴールド/FX · 5年', ct_tag_ct3:'低DD安定型 · 4年',
    ct_tag_ct4:'夜間スキャルプ · 2年', ct_tag_ct5:'マクロ複合 · 6年', ct_tag_ct6:'DCA+トレンド · 7年',
    nav_autoopen:'自動建玉', ao_title:'自動建玉', ao_subtitle:'3種類の自動エントリーモード',
    ao_lock_title:'Elite限定機能', ao_lock_desc:'Eliteにアップグレードして自動建玉を解放',
    ao_lock_btn:'アップグレード $199/月',
    ao_mode_signal:'シグナル', ao_mode_signal_desc:'RSI/MACD/EMA条件で自動エントリー',
    ao_mode_dca:'積立投資', ao_mode_dca_desc:'定期的に自動分割購入',
    ao_mode_copy:'コピー同期', ao_mode_copy_desc:'シグナル源の全エントリーをミラー',
    ao_running:'実行中',
    ao_signal_cfg:'シグナル設定', ao_signal_ind:'指標', ao_signal_pair:'銘柄',
    ao_dca_cfg:'積立設定', ao_dca_pair:'銘柄', ao_dca_freq:'頻度',
    ao_dca_hourly:'毎時', ao_dca_daily:'毎日', ao_dca_weekly:'毎週', ao_dca_monthly:'毎月',
    ao_dca_amount:'1回金額(USD)', ao_dca_total:'上限(USD)', ao_dca_price_drop:'下落倍増(%)', ao_dca_exit:'利確(%)',
    ao_dca_invested:'投資済み',
    ao_copy_cfg:'コピー同期設定', ao_copy_source:'シグナル源', ao_copy_select:'選択',
    ao_copy_ratio:'倍率', ao_copy_max:'1取引最大(USD)', ao_copy_daily_loss:'日次損失制限(USD)',
    ao_copy_filter:'方向', ao_copy_all:'両方向', ao_copy_long_only:'ロングのみ', ao_copy_short_only:'ショートのみ',
    ao_copy_pairs:'銘柄制限', ao_copy_pairs_ph:'BTC,ETH（空=制限なし）', ao_not_following:'未フォロー',
    ao_pos_size:'ポジションサイズ(USD)', ao_sl:'SL(%)', ao_tp:'TP(%)', ao_max_pos:'最大同時ポジション',

    // リーダーボード
    lb_tab_roi:'月利ランク', lb_tab_wr:'勝率ランク', lb_tab_stable:'安定ランク', lb_tab_new:'新星',
    // トレード広場
    nav_square:'トレード広場', sq_title:'トレード広場', sq_subtitle:'見解を共有し、世界のトレーダーとつながる',
    sq_post_ph:'相場見解・ポジション分析を共有...', sq_post_btn:'投稿',
    sq_filter_all:'すべて', sq_filter_bull:'強気', sq_filter_bear:'弱気', sq_filter_hot:'ホット',
    sq_pair_label:'銘柄', sq_sentiment_label:'センチメント',
    // ストラテジーマーケット
    nav_stratmarket:'ストラテジー市場', sm_title:'ストラテジー市場', sm_subtitle:'トップ戦略を発見・共有・コピー',
    sm_upload_title:'戦略を公開', sm_upload_btn:'戦略アップロード', sm_filter_all:'すべて',
    sm_filter_trend:'トレンド', sm_filter_grid:'グリッド', sm_filter_quant:'クオンツ', sm_filter_arb:'アーブ',
    sm_name_label:'戦略名', sm_asset_label:'銘柄', sm_price_label:'価格(USD/月, 0=無料)',
    sm_code_label:'戦略コード', sm_submit_btn:'審査に提出', sm_backtest:'バックテスト',
    sm_copy:'コピー', sm_subscribe:'購読',
    // シグナル放送
    nav_signals:'シグナル放送', sig_title:'シグナル放送', sig_subtitle:'リアルタイム信号・購読・自動建玉連携',
    sig_publish_title:'シグナル配信', sig_tab_live:'ライブ', sig_tab_sources:'配信元', sig_tab_history:'履歴',
    sig_pair:'銘柄', sig_dir:'方向', sig_dir_buy:'ロング', sig_dir_sell:'ショート',
    sig_entry:'エントリー', sig_sl:'SL', sig_tp1:'TP1', sig_tp2:'TP2',
    sig_desc:'メモ', sig_publish_btn:'シグナル配信',
    sig_follow:'シグナルフォロー', sig_share:'共有', sig_subscribe_bc:'配信元を購読',
    ao_start:'自動建玉開始', ao_stop:'停止', ao_status_off:'● 停止中', ao_status_on:'🟢 実行中',
    ao_started:'開始', ao_stopped:'停止',
    ao_exec_log:'実行ログ', ao_clear_log:'クリア', ao_log_empty:'実行記録なし',
    toast_elite_unlocked:'Eliteに解放！自動建玉が利用可能です',
    dash_brief_title: 'AIデイリーブリーフ', dash_brief_time: '08:00更新',
    dash_brief_content: '金は本日強気、FRBのハト派シグナルに支えられ目標$2,380。BTCは$84,000に抵抗、短期は様子見。ナスダックはテック決算主導で全体的に強い。EUR/USDは弱いレンジ相場、ドル指数104.2サポート。',
    dash_signal_gold: '金 ▲ 強気', dash_signal_btc: 'BTC ⚠ 様子見', dash_signal_eur: 'EUR/USD ▼ 弱', dash_signal_nas: 'ナスダック ▲ 強',
    dash_quick_ops: 'クイック操作', dash_btn_order: 'AI 注文', dash_btn_backtest: 'クイックBT', dash_btn_positions: 'ポジション確認',
    ai_welcome_greet: 'こんにちは！QuantAIアシスタントです 🧠', ai_welcome_intro: '取引のご相談をどうぞ：',
    modal_symbol: '銘柄', modal_dir: '方向', modal_amount: '金額 (USD)', modal_leverage: 'レバレッジ',
    modal_sl: 'SL (%)', modal_tp: 'TP (%)', modal_margin: '証拠金', modal_max_profit: '最大利益', modal_max_loss: '最大損失',
    broker_modal_title: 'ブローカー接続', broker_connect_btn: '認証して接続',
    cat_crypto: '暗号通貨', cat_forex_metals: 'FX/貴金属', cat_all_cfd: 'CFD全般',
    sym_btc:'ビットコイン',sym_eth:'イーサリアム',sym_sol:'ソラナ',sym_bnb:'BNB',sym_xrp:'リップル',
    sym_eurusd:'ユーロドル',sym_gbpusd:'ポンドドル',sym_usdjpy:'ドル円',sym_usdchf:'ドルスイス',sym_audusd:'豪ドルドル',
    sym_gold:'金スポット',sym_silver:'銀スポット',sym_wti:'WTI原油',sym_brent:'ブレント原油',
    sym_nas100:'ナスダック100',sym_spx500:'S&P 500',sym_dow:'ダウ平均',sym_hsi:'ハンセン指数',
    strat_name_1:'BTC MACDトレンド',strat_name_2:'ゴールドグリッド',strat_name_3:'EUR/USD EMA戦略',strat_name_4:'ナスダックスキャルプ',
    strat_type_trend:'トレンドフォロー',strat_type_grid:'グリッドトレード',strat_type_ema:'EMAクロス',strat_type_mr:'平均回帰',
    toast_order_ok:'注文完了！', toast_submitted:'送信済！', toast_pos_closed:'ポジション決済', toast_all_closed:'全ポジション決済',
    toast_strat_started:'開始', toast_strat_paused:'停止', toast_strat_deleted:'戦略削除',
    toast_broker_connected:'ブローカー接続成功', toast_coming_soon:'近日公開予定',
    toast_upgrading:'リダイレクト中', toast_view_plans:'全プランを見る',
    confirm_close_pos:'決済確認', confirm_close_all:'全ポジションを決済しますか？元に戻せません！', confirm_del_strat:'戦略を削除',
    bt_running:'実行中...', ai_analyze_suffix:' のポジションはどうでしょう？',
    ai_placeholder:'取引指示や質問を入力してください…',
    ai_resp_btc:'📊 BTC/USDT 分析：\n\n価格は $83,400 付近、$84,000 の抵抗線に直面。MACD ゴールデンクロス、RSI(14) は 58 — 強気だが過買いではない。\n\n提案：$82,800 サポート付近で小ロング、損切り $81,000、目標 $86,000。R/R ≈ 1:2.2。',
    ai_resp_gold:'🥇 ゴールド(XAU/USD) 分析：\n\n金価格は $2,342 で強勢維持。FED ハト派シグナルと弱いドルが支援。近期目標 $2,380、サポート $2,310。\n\n提案：ロングを保持し、損切りを $2,320 に移動して利益確定。',
    ai_resp_position:'📐 ポジションサイジング（$1,000 資金）：\n\n• BTC/USDT: 30% ($300) — メイン、5倍レバレッジ\n• XAU/USD: 25% ($250) — ヘッジ、10倍\n• EUR/USD: 20% ($200) — FX ヘッジ\n• 現金: 25% ($250) — 待機\n\n1トレード最大損失：3%。',
    ai_resp_strategy:'⚡ 現在の相場に合う3つの戦略：\n\n1. **BTC MACD トレンド** — 勝率67%、年化+89%\n2. **ゴールド グリッド** — レンジ相場向き、月3-5%\n3. **EUR/USD EMA** — 低リスク、初心者向け\n\nどれかを有効にしますか？',
    ai_resp_default:'ご要望を理解しました。現在の市場状況を分析します...\n\n📊 全体的に強気ですが、FED 政策リスクに注意。ポジションを50%以下に保ち、損切りを必ず設定してください。\n\n特定の銘柄や戦略について詳しく知りたい場合は教えてください。',
  },
  ko: {
    nav_dashboard: '대시보드', nav_market: '시장', nav_ai: 'AI 채팅',
    nav_positions: '포지션', nav_strategies: '전략', nav_backtest: '백테스트', nav_account: '계정',
    page_dashboard: '대시보드', page_market: '시장', page_ai: 'AI 어시스턴트',
    page_positions: '내 포지션', page_strategies: '전략 관리', page_backtest: '백테스트', page_account: '내 계정',
    page_copy: '카피 트레이딩', page_autoopen: '자동 진입',
    total_asset: '총 자산', daily_pnl: '오늘 손익', win_rate: '승률', active_strategies: '활성 전략', pos_count: '포지션 수',
    card_today: '오늘', card_month: '이번달', card_paused: '일시정지', card_running: '실행중',
    card_long: '롱', card_short: '숏',
    quick_order: '+ 빠른 주문',
    chart_update: '분 업데이트',
    market_title: '실시간 시장', search_placeholder: '종목 검색...',
    ai_title: 'AI 트레이딩 어시스턴트', ai_placeholder: '메시지 입력...',
    ai_welcome: '안녕하세요! QuantAI 어시스턴트입니다 🤖\n\n도움을 드릴 수 있는 것:\n• 실시간 시장 데이터 & 차트 분석\n• 포지션 관리 & 주문\n• 전략 성과 분석\n• 리스크 관리 & 포지션 사이징\n\n무엇을 도와드릴까요?',
    pos_title: '내 포지션', pos_symbol: '종목', pos_size: '규모', pos_open: '시작가', pos_current: '현재가', pos_pnl: '손익', pos_action: '작업',
    pos_close: '청산', pos_empty: '포지션 없음',
    strat_title: '전략 관리', strat_new: '새 전략',
    strat_running: '실행중', strat_paused: '일시정지', strat_stopped: '중지됨',
    strat_start: '시작', strat_pause: '일시정지', strat_stop: '중지', strat_edit: '편집',
    acc_title: '내 계정', acc_plan: '현재 플랜', acc_upgrade: '업그레이드',
    acc_broker: '브로커 계정', acc_connect: '브로커 연결',
    acc_member_free: '무료', acc_member_pro: 'Pro 회원', acc_member_elite: '엘리트 회원',
    acc_valid_until: '유효기간', acc_reg_date: '가입일', acc_total_pnl: '총 손익',
    acc_brokers_count: '연결 브로커', acc_running_strats: '운영 전략', acc_account: '계정',
    acc_broker_section: '연결된 브로커', acc_subscription: '내 구독',
    broker_connected: '연결됨', broker_api_ok: 'API 정상', broker_not_connected: '미연결', broker_pending: '설정 필요', broker_add_new: '브로커 추가',
    btn_manage: '관리', btn_disconnect: '연결해제', btn_connect: '연결', btn_edit: '수정',
    plan_current: '현재', per_month: '/월', plan_view_all: '모든 플랜 보기 →',
    plan_basic_f1: '전체 시장 데이터', plan_basic_f2: 'AI Q&A', plan_basic_f3: '전략 2개', plan_basic_f4: '자동 거래',
    plan_pro_f1: '무제한 전략', plan_pro_f2: 'AI 자동 거래', plan_pro_f3: '고급 백테스트', plan_pro_f4: '멀티 브로커',
    risk_title: '리스크 설정', risk_max_loss: '일일 최대 손실', risk_max_loss_desc: '초과 시 모든 전략 자동 중지',
    risk_max_pos: '최대 포지션 비율', risk_max_pos_desc: '종목당 총 자산의 상한 %',
    risk_auto_order: 'AI 자동 주문', risk_auto_order_desc: '전략 트리거 시 AI가 자동 실행',
    risk_notify: '주문 전 알림', risk_notify_desc: '매 주문 전 확인 발송',
    risk_night: '야간 보호 모드', risk_night_desc: '22:00-07:00 자동 거래 중지',
    mkt_all: '전체', mkt_crypto: '암호화폐', mkt_forex: '외환', mkt_metals: '귀금속', mkt_energy: '에너지', mkt_index: '지수',
    tbl_symbol: '종목', tbl_price: '현재가', tbl_change: '등락률', tbl_volume: '거래량', tbl_trend: '7일 추세', tbl_action: '작업',
    ai_feat1: '시장 트렌드 분석 및 전략 제안', ai_feat2: '자동화 거래 주문 실행',
    ai_feat3: '포지션 크기 및 스탑 계산', ai_feat4: '전략 백테스트 실행',
    ai_sugg1: 'BTC 지금 매수해도 될까요?', ai_sugg2: '금 그리드 전략 만들기',
    ai_sugg3: '$1000 자금 배분 방법', ai_sugg4: 'EUR/USD 추세 분석', ai_sugg5: '내 포지션 확인',
    quick_order_title: '빠른 주문', dir_long: '롱 매수', dir_short: '숏 매도',
    order_symbol: '종목', order_amount: '금액 (USD)', order_sltp: '손절/익절 (%)', order_confirm: '주문하기',
    sentiment_title: '시장 심리', sent_bull: '강세', sent_bear: '약세', sent_fg: '공포&탐욕', sent_greed: '탐욕', sent_flow: '대형 순유입', sent_rate: '자금 조달률',
    pos_my_title: '내 포지션', pos_active_count: '개 활성 포지션', pos_float: '평가손익', close_all: '전체 청산',
    pos_open_lbl: '시작가', pos_curr_lbl: '현재가', pos_sl_lbl: '손절', pos_tp_lbl: '익절',
    pos_ai_analyze: 'AI 분석', pos_edit_btn: '수정',
    mkt_buy: '매수', mkt_sell: '매도',
    strat_cum_pnl: '누적 손익',
    strat_my_title: '내 전략', strat_running_count: '개 실행중', strat_paused_count: '개 일시정지', strat_add: '전략 추가',
    bt_title: '백테스트', bt_symbol: '종목', bt_strat_type: '전략 유형',
    bt_start_date: '시작일', bt_end_date: '종료일', bt_capital: '초기 자본 (USD)', bt_pos_size: '포지션 크기 (%)',
    bt_run: '백테스트 실행', bt_total_return: '총 수익률', bt_annual_return: '연간 수익', bt_max_dd: '최대 낙폭',
    bt_sharpe: '샤프 비율', bt_win_rate: '승률', bt_trades: '총 거래 수', bt_log_title: '거래 기록 (최근 20건)',
    strat_macd: 'MACD 추세 추종', strat_ema: 'EMA 크로스오버', strat_rsi: 'RSI 과매수/과매도', strat_grid: '그리드 거래', strat_bb: '볼린저 돌파',
    confirm: '확인', cancel: '취소', save: '저장', close: '닫기',
    loading: '로딩중...', success: '성공', error: '오류',
    lang_switched: '🌐 한국어로 전환되었습니다',
    tlog_title:'거래 로그', tlog_all:'전체', tlog_buy:'롱', tlog_sell:'숏', tlog_win:'수익', tlog_loss:'손실',
    tlog_total_trades:'총 거래', tlog_win_rate:'승률', tlog_net_pnl:'순 손익', tlog_avg_hold:'평균 보유', tlog_best:'최고 거래', tlog_worst:'최저 거래',
    tlog_col_time:'시간', tlog_col_symbol:'종목', tlog_col_dir:'방향', tlog_col_open:'시작가', tlog_col_close:'청산가', tlog_col_size:'수량', tlog_col_pnl:'손익', tlog_col_hold:'보유 기간',
    tlog_dir_long:'롱', tlog_dir_short:'숏', tlog_empty:'거래 기록 없음',
    nav_copy:'카피 트레이딩', copy_title:'카피 트레이딩', copy_subtitle:'상위 트레이더를 팔로우, 실시간 신호 동기화',
    copy_goto_auto:'자동 진입 설정', copy_my_follows:'팔로잉', copy_leaderboard:'신호 랭킹',
    copy_filter_all:'전체', copy_filter_crypto:'암호화폐', copy_filter_forex:'외환', copy_filter_stable:'저 DD',
    copy_followers:'팔로워', copy_monthly:'월 수익', copy_winrate:'승률', copy_maxdd:'최대 DD', copy_30pnl:'30일 손익',
    copy_follow_btn:'팔로우', copy_following:'✓ 팔로잉', copy_unfollow:'언팔로우', copy_detail_btn:'상세',
    copy_pnl:'미실현 손익', copy_since:'시작', copy_follow_title:'팔로우 설정', copy_confirm_follow:'팔로우 확인',
    copy_toast_follow:'팔로우 시작', copy_toast_unfollow:'팔로우 취소',
    ct_tag_ct1:'BTC/ETH 전문가 · 3년', ct_tag_ct2:'골드/외환 · 5년', ct_tag_ct3:'저DD 안정형 · 4년',
    ct_tag_ct4:'야간 스캘퍼 · 2년', ct_tag_ct5:'매크로 멀티 · 6년', ct_tag_ct6:'DCA+트렌드 · 7년',
    nav_autoopen:'자동 진입', ao_title:'자동 진입', ao_subtitle:'3가지 스마트 자동 진입 모드',
    ao_lock_title:'Elite 전용 기능', ao_lock_desc:'Elite 요금제로 업그레이드하여 자동 진입 잠금 해제',
    ao_lock_btn:'업그레이드 $199/월',
    ao_mode_signal:'신호 트리거', ao_mode_signal_desc:'RSI/MACD/EMA 조건 충족 시 자동 진입',
    ao_mode_dca:'정기 적립', ao_mode_dca_desc:'설정 주기로 자동 분할 매수',
    ao_mode_copy:'카피 동기화', ao_mode_copy_desc:'신호 소스의 모든 진입을 자동 복제',
    ao_running:'실행 중',
    ao_signal_cfg:'신호 설정', ao_signal_ind:'지표', ao_signal_pair:'종목',
    ao_dca_cfg:'적립 설정', ao_dca_pair:'종목', ao_dca_freq:'빈도',
    ao_dca_hourly:'매시간', ao_dca_daily:'매일', ao_dca_weekly:'매주', ao_dca_monthly:'매월',
    ao_dca_amount:'1회 금액(USD)', ao_dca_total:'총 한도(USD)', ao_dca_price_drop:'하락 배수(%)', ao_dca_exit:'익절(%)',
    ao_dca_invested:'투자됨',
    ao_copy_cfg:'카피 설정', ao_copy_source:'신호 소스', ao_copy_select:'선택',
    ao_copy_ratio:'배율', ao_copy_max:'거래당 최대(USD)', ao_copy_daily_loss:'일일 손실 한도(USD)',
    ao_copy_filter:'방향', ao_copy_all:'롱&숏', ao_copy_long_only:'롱만', ao_copy_short_only:'숏만',
    ao_copy_pairs:'종목 제한', ao_copy_pairs_ph:'BTC,ETH（비어있으면=무제한）', ao_not_following:'미팔로우',
    ao_pos_size:'포지션 크기(USD)', ao_sl:'손절(%)', ao_tp:'익절(%)', ao_max_pos:'최대 동시 포지션',

    // 리더보드
    lb_tab_roi:'월 수익 순위', lb_tab_wr:'승률 순위', lb_tab_stable:'안정 순위', lb_tab_new:'신진',
    // 트레이딩 스퀘어
    nav_square:'트레이딩 스퀘어', sq_title:'트레이딩 스퀘어', sq_subtitle:'시각 공유, 감성 발견, 글로벌 트레이더와 연결',
    sq_post_ph:'시장 전망·포지션 분석을 공유하세요...', sq_post_btn:'게시',
    sq_filter_all:'전체', sq_filter_bull:'강세', sq_filter_bear:'약세', sq_filter_hot:'인기',
    sq_pair_label:'페어', sq_sentiment_label:'감성',
    // 전략 시장
    nav_stratmarket:'전략 시장', sm_title:'전략 시장', sm_subtitle:'최고 퀀트 전략 발견·공유·복사',
    sm_upload_title:'내 전략 공개', sm_upload_btn:'전략 업로드', sm_filter_all:'전체',
    sm_filter_trend:'트렌드', sm_filter_grid:'그리드', sm_filter_quant:'퀀트', sm_filter_arb:'차익',
    sm_name_label:'전략명', sm_asset_label:'종목', sm_price_label:'가격(USD/월, 0=무료)',
    sm_code_label:'전략 코드', sm_submit_btn:'심사 제출', sm_backtest:'백테스트',
    sm_copy:'복사', sm_subscribe:'구독',
    // 신호 방송
    nav_signals:'신호 방송', sig_title:'신호 방송', sig_subtitle:'실시간 신호·구독·자동 진입 연결',
    sig_publish_title:'신호 발행', sig_tab_live:'실시간', sig_tab_sources:'신호원', sig_tab_history:'히스토리',
    sig_pair:'페어', sig_dir:'방향', sig_dir_buy:'롱', sig_dir_sell:'숏',
    sig_entry:'진입', sig_sl:'손절', sig_tp1:'TP1', sig_tp2:'TP2',
    sig_desc:'메모', sig_publish_btn:'신호 방송',
    sig_follow:'신호 팔로우', sig_share:'공유', sig_subscribe_bc:'신호원 구독',
    ao_start:'자동 진입 시작', ao_stop:'정지', ao_status_off:'● 정지됨', ao_status_on:'🟢 실행 중',
    ao_started:'시작됨', ao_stopped:'정지됨',
    ao_exec_log:'실행 로그', ao_clear_log:'초기화', ao_log_empty:'실행 기록 없음',
    toast_elite_unlocked:'Elite 잠금 해제! 자동 진입 기능 사용 가능',
    dash_brief_title: 'AI 일일 브리핑', dash_brief_time: '08:00 업데이트',
    dash_brief_content: '금 오늘 강세, 연준 비둘기파 신호 지지, 목표 $2,380. BTC $84,000 저항, 단기 관망. 나스닥 실적 주도로 전반 강세. EUR/USD 약세 횡보, 달러 인덱스 104.2 지지.',
    dash_signal_gold: '금 ▲ 강세', dash_signal_btc: 'BTC ⚠ 관망', dash_signal_eur: 'EUR/USD ▼ 약세', dash_signal_nas: '나스닥 ▲ 강세',
    dash_quick_ops: '빠른 작업', dash_btn_order: 'AI 주문', dash_btn_backtest: '빠른 백테스트', dash_btn_positions: '포지션 보기',
    ai_welcome_greet: '안녕하세요! QuantAI 어시스턴트입니다 🧠', ai_welcome_intro: '거래 아이디어를 알려주세요:',
    modal_symbol: '종목', modal_dir: '방향', modal_amount: '금액 (USD)', modal_leverage: '레버리지',
    modal_sl: '손절 (%)', modal_tp: '익절 (%)', modal_margin: '예상 증거금', modal_max_profit: '최대 수익', modal_max_loss: '최대 손실',
    broker_modal_title: '브로커 연결', broker_connect_btn: '확인 및 연결',
    cat_crypto: '암호화폐', cat_forex_metals: '외환/귀금속', cat_all_cfd: 'CFD 전체',
    sym_btc:'비트코인',sym_eth:'이더리움',sym_sol:'솔라나',sym_bnb:'BNB',sym_xrp:'리플',
    sym_eurusd:'유로달러',sym_gbpusd:'파운드달러',sym_usdjpy:'달러엔',sym_usdchf:'달러스위스',sym_audusd:'호주달러',
    sym_gold:'현물금',sym_silver:'현물은',sym_wti:'WTI원유',sym_brent:'브렌트원유',
    sym_nas100:'나스닥100',sym_spx500:'S&P 500',sym_dow:'다우존스',sym_hsi:'항셍지수',
    strat_name_1:'BTC MACD 추세',strat_name_2:'금 그리드 차익',strat_name_3:'EUR/USD EMA 전략',strat_name_4:'나스닥 초단타',
    strat_type_trend:'추세 추종',strat_type_grid:'그리드 거래',strat_type_ema:'EMA 크로스',strat_type_mr:'평균 회귀',
    toast_order_ok:'주문 완료!', toast_submitted:'제출됨!', toast_pos_closed:'포지션 청산', toast_all_closed:'전체 포지션 청산',
    toast_strat_started:'시작', toast_strat_paused:'일시정지', toast_strat_deleted:'전략 삭제됨',
    toast_broker_connected:'브로커 연결 성공', toast_coming_soon:'곧 출시 예정',
    toast_upgrading:'이동 중', toast_view_plans:'전체 플랜 보기',
    confirm_close_pos:'청산 확인', confirm_close_all:'모든 포지션을 청산할까요? 되돌릴 수 없습니다!', confirm_del_strat:'전략 삭제',
    bt_running:'실행중...', ai_analyze_suffix:' 포지션 어떻게 볼까요?',
    ai_placeholder:'거래 지시 또는 질문을 입력하세요…',
    ai_resp_btc:'📊 BTC/USDT 분석：\n\n가격 $83,400 근처, $84,000 저항선 직면. MACD 골든크로스, RSI(14) 58 — 강세지만 과매수 아님.\n\n제안: $82,800 지지 근처 소규모 롱, 손절 $81,000, 목표 $86,000. R/R ≈ 1:2.2.',
    ai_resp_gold:'🥇 금(XAU/USD) 분석：\n\n금값 $2,342 강세 유지. Fed 비둘기파 신호와 약달러 지지. 근기 목표 $2,380, 핵심 지지 $2,310.\n\n제안: 롱 유지, 손절을 $2,320으로 이동하여 이익 확정.',
    ai_resp_position:'📐 포지션 사이징 ($1,000 자금)：\n\n• BTC/USDT: 30% ($300) — 메인, 5배 레버리지\n• XAU/USD: 25% ($250) — 헤지, 10배\n• EUR/USD: 20% ($200) — FX 헤지\n• 현금: 25% ($250) — 기회 대기\n\n1회 최대 손실: 3%.',
    ai_resp_strategy:'⚡ 현재 시장에 맞는 3가지 전략：\n\n1. **BTC MACD 트렌드** — 승률 67%, 연화 +89%\n2. **금 그리드** — 박스권 시장용, 월 3-5%\n3. **EUR/USD EMA** — 저위험, 초보자 적합\n\n전략을 활성화할까요?',
    ai_resp_default:'요구사항을 이해했습니다. 현재 시장 상황을 분석합니다...\n\n📊 전반적으로 강세지만 Fed 정책 리스크 주의. 포지션을 50% 이하로 유지하고 손절을 설정하세요.\n\n특정 종목이나 전략에 대해 더 알고 싶으신가요?',
  },
  ru: {
    nav_dashboard: 'Панель', nav_market: 'Рынок', nav_ai: 'AI Чат',
    nav_positions: 'Позиции', nav_strategies: 'Стратегии', nav_backtest: 'Бэктест', nav_account: 'Аккаунт',
    page_dashboard: 'Панель управления', page_market: 'Рынок', page_ai: 'AI Ассистент',
    page_positions: 'Мои позиции', page_strategies: 'Управление стратегиями', page_backtest: 'Бэктест', page_account: 'Мой аккаунт',
    page_copy: 'Копи-трейдинг', page_autoopen: 'Авто-открытие',
    total_asset: 'Общие активы', daily_pnl: 'П&У сегодня', win_rate: 'Винрейт', active_strategies: 'Активные стратегии', pos_count: 'Позиций',
    card_today: 'Сегодня', card_month: 'Месяц', card_paused: 'Пауза', card_running: 'Работает',
    card_long: 'Лонг', card_short: 'Шорт',
    quick_order: '+ Быстрый ордер',
    chart_update: 'мин обновление',
    market_title: 'Рынок в реальном времени', search_placeholder: 'Поиск инструмента...',
    ai_title: 'AI Торговый Ассистент', ai_placeholder: 'Введите сообщение...',
    ai_welcome: 'Привет! Я QuantAI Ассистент 🤖\n\nЯ могу помочь:\n• Данные рынка в реальном времени\n• Управление позициями\n• Анализ стратегий\n• Риск-менеджмент\n\nКак я могу вам помочь?',
    pos_title: 'Мои позиции', pos_symbol: 'Инструмент', pos_size: 'Объём', pos_open: 'Цена входа', pos_current: 'Текущая', pos_pnl: 'П&У', pos_action: 'Действие',
    pos_close: 'Закрыть', pos_empty: 'Нет позиций',
    strat_title: 'Управление стратегиями', strat_new: 'Новая стратегия',
    strat_running: 'Работает', strat_paused: 'Пауза', strat_stopped: 'Остановлена',
    strat_start: 'Запуск', strat_pause: 'Пауза', strat_stop: 'Стоп', strat_edit: 'Ред.',
    acc_title: 'Мой аккаунт', acc_plan: 'Текущий план', acc_upgrade: 'Обновить',
    acc_broker: 'Счёт брокера', acc_connect: 'Подключить брокера',
    acc_member_free: 'Бесплатно', acc_member_pro: 'Pro Участник', acc_member_elite: 'Элита',
    acc_valid_until: 'Действует до', acc_reg_date: 'Дата регистрации', acc_total_pnl: 'Общий П&У',
    acc_brokers_count: 'Брокеры', acc_running_strats: 'Активных стратегий', acc_account: 'Счёт',
    acc_broker_section: 'Подключённые брокеры', acc_subscription: 'Моя подписка',
    broker_connected: 'Подключён', broker_api_ok: 'API ОК', broker_not_connected: 'Не подключён', broker_pending: 'Ожидает', broker_add_new: 'Добавить брокера',
    btn_manage: 'Управлять', btn_disconnect: 'Отключить', btn_connect: 'Подключить', btn_edit: 'Изменить',
    plan_current: 'Текущий', per_month: '/мес', plan_view_all: 'Все тарифы →',
    plan_basic_f1: 'Все рыночные данные', plan_basic_f2: 'AI Q&A', plan_basic_f3: '2 стратегии', plan_basic_f4: 'Автоторговля',
    plan_pro_f1: 'Неограниченные стратегии', plan_pro_f2: 'AI автоторговля', plan_pro_f3: 'Продвинутый бэктест', plan_pro_f4: 'Мультиброкер',
    risk_title: 'Риск-менеджмент', risk_max_loss: 'Дневной макс. убыток', risk_max_loss_desc: 'Автостоп при превышении',
    risk_max_pos: 'Макс. размер позиции', risk_max_pos_desc: 'На инструмент, % от активов',
    risk_auto_order: 'AI автозаявки', risk_auto_order_desc: 'AI исполняет при триггере стратегии',
    risk_notify: 'Уведомление перед сделкой', risk_notify_desc: 'Отправлять подтверждение',
    risk_night: 'Ночная защита', risk_night_desc: '22:00-07:00 приостановить автоторговлю',
    mkt_all: 'Все', mkt_crypto: 'Крипто', mkt_forex: 'Форекс', mkt_metals: 'Металлы', mkt_energy: 'Энергия', mkt_index: 'Индексы',
    tbl_symbol: 'Инструмент', tbl_price: 'Цена', tbl_change: 'Изменение', tbl_volume: 'Объём', tbl_trend: '7д тренд', tbl_action: 'Действие',
    ai_feat1: 'Анализ рынка и стратегии', ai_feat2: 'Автоматические торговые ордера',
    ai_feat3: 'Расчёт позиции и стопов', ai_feat4: 'Бэктест вашей стратегии',
    ai_sugg1: 'Покупать BTC сейчас?', ai_sugg2: 'Создать сетчатую стратегию на золото',
    ai_sugg3: 'Как распределить $1000?', ai_sugg4: 'Анализ EUR/USD', ai_sugg5: 'Мои позиции',
    quick_order_title: 'Быстрый ордер', dir_long: 'Лонг (Покупка)', dir_short: 'Шорт (Продажа)',
    order_symbol: 'Инструмент', order_amount: 'Сумма (USD)', order_sltp: 'SL / TP (%)', order_confirm: 'Разместить ордер',
    sentiment_title: 'Рыночный сентимент', sent_bull: 'Быки', sent_bear: 'Медведи', sent_fg: 'Страх&Жадность', sent_greed: 'Жадность', sent_flow: 'Чистый крупный приток', sent_rate: 'Ставка финансирования',
    pos_my_title: 'Мои позиции', pos_active_count: ' активных позиций', pos_float: 'Плавающий П&У', close_all: 'Закрыть всё',
    pos_open_lbl: 'Цена входа', pos_curr_lbl: 'Текущая', pos_sl_lbl: 'Стоп', pos_tp_lbl: 'Тейк',
    pos_ai_analyze: 'AI Анализ', pos_edit_btn: 'Изменить',
    mkt_buy: 'Купить', mkt_sell: 'Продать',
    strat_cum_pnl: 'Общий П&У',
    strat_my_title: 'Мои стратегии', strat_running_count: ' работает', strat_paused_count: ' пауза', strat_add: 'Добавить стратегию',
    bt_title: 'Бэктест', bt_symbol: 'Инструмент', bt_strat_type: 'Тип стратегии',
    bt_start_date: 'Дата начала', bt_end_date: 'Дата окончания', bt_capital: 'Начальный капитал (USD)', bt_pos_size: 'Размер позиции (%)',
    bt_run: 'Запустить', bt_total_return: 'Общая доходность', bt_annual_return: 'Годовая доходность', bt_max_dd: 'Макс. просадка',
    bt_sharpe: 'Коэф. Шарпа', bt_win_rate: 'Процент выигрышей', bt_trades: 'Всего сделок', bt_log_title: 'Журнал сделок (20 последних)',
    strat_macd: 'MACD трендовая', strat_ema: 'EMA кроссовер', strat_rsi: 'RSI перекупленность', strat_grid: 'Сеточная торговля', strat_bb: 'Прорыв Боллинджера',
    confirm: 'ОК', cancel: 'Отмена', save: 'Сохранить', close: 'Закрыть',
    loading: 'Загрузка...', success: 'Успешно', error: 'Ошибка',
    lang_switched: '🌐 Переключено на русский',
    tlog_title:'Журнал сделок', tlog_all:'Все', tlog_buy:'Лонг', tlog_sell:'Шорт', tlog_win:'Прибыль', tlog_loss:'Убыток',
    tlog_total_trades:'Сделок', tlog_win_rate:'Винрейт', tlog_net_pnl:'Чист. П&У', tlog_avg_hold:'Ср. удержание', tlog_best:'Лучшая', tlog_worst:'Худшая',
    tlog_col_time:'Время', tlog_col_symbol:'Символ', tlog_col_dir:'Направление', tlog_col_open:'Цена откр.', tlog_col_close:'Цена закр.', tlog_col_size:'Лоты', tlog_col_pnl:'П&У', tlog_col_hold:'Время удержания',
    tlog_dir_long:'Лонг', tlog_dir_short:'Шорт', tlog_empty:'Нет записей о сделках',
    nav_copy:'Копи-трейдинг', copy_title:'Копи-трейдинг', copy_subtitle:'Следуй за топ-трейдерами, синхронизация сигналов',
    copy_goto_auto:'Авто-открытие позиций', copy_my_follows:'Мои подписки', copy_leaderboard:'Рейтинг сигналов',
    copy_filter_all:'Все', copy_filter_crypto:'Крипто', copy_filter_forex:'Форекс', copy_filter_stable:'Низ. DD',
    copy_followers:'подписчиков', copy_monthly:'Месяц', copy_winrate:'Винрейт', copy_maxdd:'Макс. DD', copy_30pnl:'30д П&У',
    copy_follow_btn:'Следить', copy_following:'✓ Подписан', copy_unfollow:'Отписаться', copy_detail_btn:'Детали',
    copy_pnl:'Плав. П&У', copy_since:'С', copy_follow_title:'Настройки подписки', copy_confirm_follow:'Подтвердить',
    copy_toast_follow:'Подписка активна', copy_toast_unfollow:'Подписка отменена',
    ct_tag_ct1:'BTC/ETH Эксперт · 3г', ct_tag_ct2:'Золото/Форекс · 5л', ct_tag_ct3:'Низк.DD · 4г',
    ct_tag_ct4:'Ночной Скальпер · 2г', ct_tag_ct5:'Макро Мульти · 6л', ct_tag_ct6:'DCA+Тренд · 7л',
    nav_autoopen:'Авто-открытие', ao_title:'Авто-открытие', ao_subtitle:'3 режима умного авто-входа',
    ao_lock_title:'Только для Elite', ao_lock_desc:'Обновитесь до Elite для авто-открытия позиций',
    ao_lock_btn:'Обновить $199/мес',
    ao_mode_signal:'Сигнал', ao_mode_signal_desc:'Авто-вход при срабатывании RSI/MACD/EMA',
    ao_mode_dca:'DCA', ao_mode_dca_desc:'Автоматические регулярные покупки',
    ao_mode_copy:'Копи-синхрон', ao_mode_copy_desc:'Зеркалирование каждой сделки сигнал-провайдера',
    ao_running:'Работает',
    ao_signal_cfg:'Настройки сигнала', ao_signal_ind:'Индикатор', ao_signal_pair:'Инструмент',
    ao_dca_cfg:'Настройки DCA', ao_dca_pair:'Инструмент', ao_dca_freq:'Частота',
    ao_dca_hourly:'Каждый час', ao_dca_daily:'Ежедневно', ao_dca_weekly:'Еженедельно', ao_dca_monthly:'Ежемесячно',
    ao_dca_amount:'Сумма за вход(USD)', ao_dca_total:'Лимит(USD)', ao_dca_price_drop:'Удвоение при падении(%)', ao_dca_exit:'Тейк(%)',
    ao_dca_invested:'Инвестировано',
    ao_copy_cfg:'Настройки копи', ao_copy_source:'Источник сигналов', ao_copy_select:'Выбрать',
    ao_copy_ratio:'Коэффициент', ao_copy_max:'Макс. за сделку(USD)', ao_copy_daily_loss:'Дневной лимит убытков(USD)',
    ao_copy_filter:'Направление', ao_copy_all:'Лонг и Шорт', ao_copy_long_only:'Только лонг', ao_copy_short_only:'Только шорт',
    ao_copy_pairs:'Лимит инструментов', ao_copy_pairs_ph:'BTC,ETH (пусто=без ограничений)', ao_not_following:'Не подписан',
    ao_pos_size:'Размер позиции(USD)', ao_sl:'Стоп(%)', ao_tp:'Тейк(%)', ao_max_pos:'Макс. позиций',
    ao_start:'Запустить', ao_stop:'Остановить', ao_status_off:'● Остановлен', ao_status_on:'🟢 Работает',
    ao_started:'Запущен', ao_stopped:'Остановлен',
    ao_exec_log:'Журнал сделок', ao_clear_log:'Очистить', ao_log_empty:'Нет записей',
    toast_elite_unlocked:'Elite разблокирован! Авто-открытие доступно',
    dash_brief_title: 'AI Дневной брифинг', dash_brief_time: 'Обновлено 08:00',
    dash_brief_content: 'Золото сегодня бычье, поддержанное сигналами ФРС. BTC сопротивление на $84,000. Nasdaq сильный на отчётах. EUR/USD слабый.',
    dash_signal_gold: 'Золото ▲ Бычье', dash_signal_btc: 'BTC ⚠ Нейтрально', dash_signal_eur: 'EUR/USD ▼ Слабо', dash_signal_nas: 'Nasdaq ▲ Сильный',
    dash_quick_ops: 'Быстрые действия', dash_btn_order: 'AI Ордер', dash_btn_backtest: 'Быстрый Бэктест', dash_btn_positions: 'Позиции',
    ai_welcome_greet: 'Привет! Я QuantAI Ассистент 🧠', ai_welcome_intro: 'Расскажите о ваших торговых идеях:',
    modal_symbol: 'Инструмент', modal_dir: 'Направление', modal_amount: 'Сумма (USD)', modal_leverage: 'Плечо',
    modal_sl: 'Стоп (%)', modal_tp: 'Тейк (%)', modal_margin: 'Маржа', modal_max_profit: 'Макс. прибыль', modal_max_loss: 'Макс. убыток',
    broker_modal_title: 'Подключить брокера', broker_connect_btn: 'Проверить и подключить',
    cat_crypto: 'Крипто', cat_forex_metals: 'Форекс/Металлы', cat_all_cfd: 'Все CFD',
    sym_btc:'Биткоин',sym_eth:'Эфириум',sym_sol:'Солана',sym_bnb:'BNB',sym_xrp:'Риппл',
    sym_eurusd:'EUR/USD',sym_gbpusd:'GBP/USD',sym_usdjpy:'USD/JPY',sym_usdchf:'USD/CHF',sym_audusd:'AUD/USD',
    sym_gold:'Спот золото',sym_silver:'Спот серебро',sym_wti:'Нефть WTI',sym_brent:'Нефть Brent',
    sym_nas100:'Nasdaq 100',sym_spx500:'S&P 500',sym_dow:'Dow Jones',sym_hsi:'Hang Seng',
    strat_name_1:'BTC MACD Тренд',strat_name_2:'Сетка Золото',strat_name_3:'EUR/USD EMA Стратегия',strat_name_4:'Nasdaq Скальпинг',
    strat_type_trend:'Тренд',strat_type_grid:'Сетка',strat_type_ema:'EMA Крест',strat_type_mr:'Возврат к среднему',
    toast_order_ok:'Ордер размещён!', toast_submitted:'Отправлено!', toast_pos_closed:'Позиция закрыта', toast_all_closed:'Все позиции закрыты',
    toast_strat_started:'запущена', toast_strat_paused:'остановлена', toast_strat_deleted:'Стратегия удалена',
    toast_broker_connected:'Брокер подключён', toast_coming_soon:'Скоро появится',
    toast_upgrading:'Переход к', toast_view_plans:'Все тарифы',
    confirm_close_pos:'Закрыть позицию', confirm_close_all:'Закрыть все позиции? Нельзя отменить!', confirm_del_strat:'Удалить стратегию',
    bt_running:'Выполняется...', ai_analyze_suffix:' как выглядит моя позиция?',
    ai_placeholder:'Введите торговую инструкцию или вопрос…',
    ai_resp_btc:'📊 Анализ BTC/USDT:\n\nЦена около $83 400, сопротивление на $84 000. MACD золотой крест, RSI(14) = 58 — бычий, но не перекуплен.\n\nРекомендация: небольшой лонг от $82 800, стоп $81 000, цель $86 000. R/R ≈ 1:2,2.',
    ai_resp_gold:'🥇 Анализ Gold (XAU/USD):\n\nЗолото сильное на $2 342. Поддержка от голубиного ФРС и слабого доллара. Цель $2 380, поддержка $2 310.\n\nРекомендация: держать лонг, передвинуть стоп на $2 320 для фиксации прибыли.',
    ai_resp_position:'📐 Управление позицией ($1 000 капитал):\n\n• BTC/USDT: 30% ($300) — основная, плечо 5х\n• XAU/USD: 25% ($250) — хедж, плечо 10х\n• EUR/USD: 20% ($200) — валютный хедж\n• Наличные: 25% ($250) — ожидание\n\nМакс. убыток на сделку: 3%.',
    ai_resp_strategy:'⚡ 3 стратегии для текущего рынка:\n\n1. **BTC MACD Тренд** — 67% побед, +89% в год\n2. **Золотая сетка** — для диапазонного рынка, 3-5%/мес\n3. **EUR/USD EMA** — низкий риск, для новичков\n\nАктивировать одну из них?',
    ai_resp_default:'Я понял ваш запрос. Позвольте проанализировать текущий рынок...\n\n📊 Рынок в целом бычий, но следите за рисками ФРС. Держите позиции ниже 50% и устанавливайте стоп-лоссы.\n\nЕсть ли конкретный инструмент или стратегия для детального изучения?',
  },
  ar: {
    nav_dashboard: 'لوحة القيادة', nav_market: 'السوق', nav_ai: 'دردشة AI',
    nav_positions: 'المراكز', nav_strategies: 'الاستراتيجيات', nav_backtest: 'الاختبار', nav_account: 'الحساب',
    page_dashboard: 'لوحة القيادة', page_market: 'السوق', page_ai: 'مساعد AI',
    page_positions: 'مراكزي', page_strategies: 'إدارة الاستراتيجيات', page_backtest: 'الاختبار العكسي', page_account: 'حسابي',
    page_copy: 'تداول النسخ', page_autoopen: 'الفتح التلقائي',
    total_asset: 'إجمالي الأصول', daily_pnl: 'أرباح اليوم', win_rate: 'معدل الفوز', active_strategies: 'الاستراتيجيات النشطة', pos_count: 'عدد المراكز',
    card_today: 'اليوم', card_month: 'هذا الشهر', card_paused: 'متوقف', card_running: 'يعمل',
    card_long: 'شراء', card_short: 'بيع',
    quick_order: '+ أمر سريع', chart_update: 'دقيقة تحديث',
    market_title: 'السوق المباشر', search_placeholder: 'ابحث عن رمز...',
    ai_title: 'مساعد التداول AI', ai_placeholder: 'اكتب رسالة...',
    ai_welcome: 'مرحباً! أنا مساعد QuantAI 🤖',
    mkt_all: 'الكل', mkt_crypto: 'كريبتو', mkt_forex: 'فوركس', mkt_metals: 'معادن', mkt_energy: 'طاقة', mkt_index: 'مؤشرات',
    tbl_symbol: 'الرمز', tbl_price: 'السعر', tbl_change: 'التغيير', tbl_volume: 'الحجم', tbl_trend: 'اتجاه 7 أيام', tbl_action: 'إجراء',
    ai_feat1: 'تحليل الأسواق واقتراح الاستراتيجيات', ai_feat2: 'تنفيذ أوامر تلقائية',
    ai_feat3: 'حساب حجم المركز والوقف', ai_feat4: 'اختبار أداء الاستراتيجية',
    ai_sugg1: 'هل أشتري BTC الآن؟', ai_sugg2: 'إنشاء استراتيجية شبكة ذهب',
    ai_sugg3: 'كيف أوزع 1000$؟', ai_sugg4: 'تحليل EUR/USD', ai_sugg5: 'عرض مراكزي',
    quick_order_title: 'أمر سريع', dir_long: 'شراء', dir_short: 'بيع',
    order_symbol: 'الرمز', order_amount: 'المبلغ (USD)', order_sltp: 'وقف / جني (%)', order_confirm: 'تأكيد الأمر',
    sentiment_title: 'معنويات السوق', sent_bull: 'صاعد', sent_bear: 'هابط', sent_fg: 'خوف وطمع', sent_greed: 'طمع', sent_flow: 'صافي التدفق الكبير', sent_rate: 'معدل التمويل',
    pos_title: 'مراكزي', pos_symbol: 'الرمز', pos_size: 'الحجم', pos_open: 'سعر الفتح', pos_current: 'الحالي', pos_pnl: 'الربح/الخسارة', pos_action: 'إجراء',
    pos_close: 'إغلاق', pos_empty: 'لا توجد مراكز',
    pos_my_title: 'مراكزي', pos_active_count: ' مراكز نشطة', pos_float: 'أرباح عائمة', close_all: 'إغلاق الكل',
    pos_open_lbl: 'سعر الفتح', pos_curr_lbl: 'الحالي', pos_sl_lbl: 'وقف', pos_tp_lbl: 'جني',
    pos_ai_analyze: 'تحليل AI', pos_edit_btn: 'تعديل',
    mkt_buy: 'شراء', mkt_sell: 'بيع',
    strat_cum_pnl: 'إجمالي الربح',
    strat_title: 'إدارة الاستراتيجيات', strat_new: 'استراتيجية جديدة',
    strat_running: 'يعمل', strat_paused: 'متوقف', strat_stopped: 'محطوط',
    strat_start: 'بدء', strat_pause: 'إيقاف مؤقت', strat_stop: 'إيقاف', strat_edit: 'تعديل',
    strat_my_title: 'استراتيجياتي', strat_running_count: ' تعمل', strat_paused_count: ' متوقفة', strat_add: 'إضافة استراتيجية',
    bt_title: 'الاختبار العكسي', bt_symbol: 'الرمز', bt_strat_type: 'نوع الاستراتيجية',
    bt_start_date: 'تاريخ البدء', bt_end_date: 'تاريخ الانتهاء', bt_capital: 'رأس المال الأولي (USD)', bt_pos_size: 'حجم الصفقة (%)',
    bt_run: 'تشغيل الاختبار', bt_total_return: 'إجمالي العائد', bt_annual_return: 'العائد السنوي', bt_max_dd: 'أقصى تراجع',
    bt_sharpe: 'نسبة شارب', bt_win_rate: 'معدل الفوز', bt_trades: 'إجمالي الصفقات', bt_log_title: 'سجل الصفقات (آخر 20)',
    strat_macd: 'MACD اتجاهي', strat_ema: 'EMA تقاطع', strat_rsi: 'RSI تشبع', strat_grid: 'تداول شبكي', strat_bb: 'اختراق بولينجر',
    acc_title: 'حسابي', acc_plan: 'الخطة الحالية', acc_upgrade: 'ترقية',
    acc_broker: 'حساب الوسيط', acc_connect: 'ربط الوسيط',
    acc_member_free: 'مجاني', acc_member_pro: 'عضو Pro', acc_member_elite: 'عضو نخبة',
    acc_valid_until: 'صالح حتى', acc_reg_date: 'تاريخ التسجيل', acc_total_pnl: 'إجمالي الربح',
    acc_brokers_count: 'الوسطاء', acc_running_strats: 'استراتيجيات نشطة', acc_account: 'حساب',
    acc_broker_section: 'الوسطاء المتصلون', acc_subscription: 'اشتراكي',
    broker_connected: 'متصل', broker_api_ok: 'API سليم', broker_not_connected: 'غير متصل', broker_pending: 'في الانتظار', broker_add_new: 'إضافة وسيط',
    btn_manage: 'إدارة', btn_disconnect: 'قطع', btn_connect: 'توصيل', btn_edit: 'تعديل',
    plan_current: 'الحالي', per_month: '/شهر', plan_view_all: 'عرض كل الخطط →',
    plan_basic_f1: 'بيانات السوق الكاملة', plan_basic_f2: 'AI Q&A', plan_basic_f3: '2 استراتيجيات', plan_basic_f4: 'تداول آلي',
    plan_pro_f1: 'استراتيجيات غير محدودة', plan_pro_f2: 'AI تداول آلي', plan_pro_f3: 'اختبار متقدم', plan_pro_f4: 'متعدد الوسطاء',
    risk_title: 'ضوابط المخاطر', risk_max_loss: 'الحد الأقصى للخسارة اليومية', risk_max_loss_desc: 'إيقاف الاستراتيجيات عند التجاوز',
    risk_max_pos: 'الحجم الأقصى للمركز', risk_max_pos_desc: '% من الأصول الإجمالية للرمز',
    risk_auto_order: 'أوامر AI التلقائية', risk_auto_order_desc: 'تنفيذ AI عند تشغيل الاستراتيجية',
    risk_notify: 'إشعار قبل التداول', risk_notify_desc: 'إرسال تأكيد قبل كل صفقة',
    risk_night: 'وضع الحماية الليلية', risk_night_desc: '22:00-07:00 تعليق التداول الآلي',
    confirm: 'تأكيد', cancel: 'إلغاء', save: 'حفظ', close: 'إغلاق',
    loading: 'جار التحميل...', success: 'نجاح', error: 'خطأ',
    lang_switched: '🌐 تم التبديل إلى العربية',
    tlog_title:'سجل الصفقات', tlog_all:'الكل', tlog_buy:'شراء', tlog_sell:'بيع', tlog_win:'ربح', tlog_loss:'خسارة',
    tlog_total_trades:'الصفقات', tlog_win_rate:'معدل الفوز', tlog_net_pnl:'صافي الربح', tlog_avg_hold:'متوسط الاحتفاظ', tlog_best:'أفضل صفقة', tlog_worst:'أسوأ صفقة',
    tlog_col_time:'الوقت', tlog_col_symbol:'الرمز', tlog_col_dir:'الاتجاه', tlog_col_open:'سعر الدخول', tlog_col_close:'سعر الخروج', tlog_col_size:'الحجم', tlog_col_pnl:'الربح/الخسارة', tlog_col_hold:'مدة الاحتفاظ',
    tlog_dir_long:'شراء', tlog_dir_short:'بيع', tlog_empty:'لا توجد سجلات صفقات',
    nav_copy:'نسخ التداول', copy_title:'نسخ التداول', copy_subtitle:'تابع كبار المتداولين، مزامنة الإشارات',
    copy_goto_auto:'إعدادات الفتح التلقائي', copy_my_follows:'متابعتي', copy_leaderboard:'ترتيب المصادر',
    copy_filter_all:'الكل', copy_filter_crypto:'كريبتو', copy_filter_forex:'فوركس', copy_filter_stable:'انخفاض DD',
    copy_followers:'متابع', copy_monthly:'الشهر', copy_winrate:'معدل الفوز', copy_maxdd:'أقصى DD', copy_30pnl:'30 يوم',
    copy_follow_btn:'متابعة', copy_following:'✓ متابَع', copy_unfollow:'إلغاء', copy_detail_btn:'التفاصيل',
    copy_pnl:'الأرباح', copy_since:'منذ', copy_follow_title:'إعدادات المتابعة', copy_confirm_follow:'تأكيد',
    copy_toast_follow:'بدأت المتابعة', copy_toast_unfollow:'تم إلغاء المتابعة',
    ct_tag_ct1:'خبير BTC/ETH · 3 سنوات', ct_tag_ct2:'ذهب/فوركس · 5 سنوات', ct_tag_ct3:'استقرار DD منخفض · 4 سنوات',
    ct_tag_ct4:'مضارب ليلي · سنتان', ct_tag_ct5:'متعدد الأصول · 6 سنوات', ct_tag_ct6:'DCA+اتجاه · 7 سنوات',
    nav_autoopen:'الفتح التلقائي', ao_title:'الفتح التلقائي', ao_subtitle:'3 أوضاع ذكية للدخول التلقائي',
    ao_lock_title:'ميزة Elite حصرية', ao_lock_desc:'ترقية إلى Elite لفتح إمكانية الدخول التلقائي',
    ao_lock_btn:'ترقية $199/شهر',
    ao_mode_signal:'إشارة', ao_mode_signal_desc:'دخول تلقائي عند تحقق شروط RSI/MACD/EMA',
    ao_mode_dca:'DCA دوري', ao_mode_dca_desc:'شراء دوري تلقائي بسعر متوسط',
    ao_mode_copy:'مزامنة النسخ', ao_mode_copy_desc:'نسخ كل دخول من مصدر الإشارات',
    ao_running:'يعمل',
    ao_signal_cfg:'إعداد الإشارة', ao_signal_ind:'المؤشر', ao_signal_pair:'الرمز',
    ao_dca_cfg:'إعداد DCA', ao_dca_pair:'الرمز', ao_dca_freq:'التكرار',
    ao_dca_hourly:'كل ساعة', ao_dca_daily:'يومياً', ao_dca_weekly:'أسبوعياً', ao_dca_monthly:'شهرياً',
    ao_dca_amount:'مبلغ الدخول(USD)', ao_dca_total:'الحد الأقصى(USD)', ao_dca_price_drop:'مضاعفة عند الهبوط(%)', ao_dca_exit:'جني الأرباح(%)',
    ao_dca_invested:'تم الاستثمار',
    ao_copy_cfg:'إعداد النسخ', ao_copy_source:'مصدر الإشارات', ao_copy_select:'اختر',
    ao_copy_ratio:'المعامل', ao_copy_max:'الحد الأقصى(USD)', ao_copy_daily_loss:'حد الخسارة اليومية(USD)',
    ao_copy_filter:'الاتجاه', ao_copy_all:'شراء وبيع', ao_copy_long_only:'شراء فقط', ao_copy_short_only:'بيع فقط',
    ao_copy_pairs:'تقييد الرموز', ao_copy_pairs_ph:'BTC,ETH (فارغ=بدون قيود)', ao_not_following:'غير متابع',
    ao_pos_size:'حجم الصفقة(USD)', ao_sl:'وقف الخسارة(%)', ao_tp:'جني الأرباح(%)', ao_max_pos:'الحد الأقصى للمراكز',
    ao_start:'بدء الفتح التلقائي', ao_stop:'إيقاف', ao_status_off:'● متوقف', ao_status_on:'🟢 يعمل',
    ao_started:'بدأ', ao_stopped:'متوقف',
    ao_exec_log:'سجل التنفيذ', ao_clear_log:'مسح', ao_log_empty:'لا توجد سجلات',
    toast_elite_unlocked:'تم فتح Elite! الفتح التلقائي متاح الآن',
    dash_brief_title: 'النشرة اليومية AI', dash_brief_time: 'تحديث 08:00',
    dash_brief_content: 'الذهب صاعد اليوم بدعم من FED. BTC مقاومة $84,000. ناسداك قوي. EUR/USD ضعيف.',
    dash_signal_gold: 'ذهب ▲ صاعد', dash_signal_btc: 'BTC ⚠ مراقبة', dash_signal_eur: 'EUR/USD ▼ ضعيف', dash_signal_nas: 'ناسداك ▲ قوي',
    dash_quick_ops: 'إجراءات سريعة', dash_btn_order: 'أمر AI', dash_btn_backtest: 'اختبار سريع', dash_btn_positions: 'عرض المراكز',
    ai_welcome_greet: 'مرحباً! أنا مساعد QuantAI 🧠', ai_welcome_intro: 'أخبرني بأفكارك التجارية:',
    modal_symbol: 'الرمز', modal_dir: 'الاتجاه', modal_amount: 'المبلغ (USD)', modal_leverage: 'الرافعة',
    modal_sl: 'وقف خسارة (%)', modal_tp: 'جني أرباح (%)', modal_margin: 'الهامش', modal_max_profit: 'أقصى ربح', modal_max_loss: 'أقصى خسارة',
    broker_modal_title: 'ربط وسيط', broker_connect_btn: 'تحقق وربط',
    cat_crypto: 'تشفير', cat_forex_metals: 'فوركس/معادن', cat_all_cfd: 'كل CFD',
    sym_btc:'بيتكوين',sym_eth:'إيثيريوم',sym_sol:'سولانا',sym_bnb:'BNB',sym_xrp:'ريبل',
    sym_eurusd:'يورو/دولار',sym_gbpusd:'جنيه/دولار',sym_usdjpy:'دولار/ين',sym_usdchf:'دولار/فرنك',sym_audusd:'أوسي/دولار',
    sym_gold:'ذهب فوري',sym_silver:'فضة فورية',sym_wti:'نفط WTI',sym_brent:'نفط برنت',
    sym_nas100:'ناسداك 100',sym_spx500:'S&P 500',sym_dow:'داو جونز',sym_hsi:'هانغ سنغ',
    strat_name_1:'BTC MACD اتجاه',strat_name_2:'شبكة ذهب',strat_name_3:'EUR/USD EMA',strat_name_4:'ناسداك سكالب',
    strat_type_trend:'اتجاهي',strat_type_grid:'شبكي',strat_type_ema:'EMA تقاطع',strat_type_mr:'ارتداد وسطي',
    toast_order_ok:'تم الأمر!', toast_submitted:'تم الإرسال!', toast_pos_closed:'تم إغلاق المركز', toast_all_closed:'تم إغلاق جميع المراكز',
    toast_strat_started:'بدأت', toast_strat_paused:'متوقفة', toast_strat_deleted:'تم حذف الاستراتيجية',
    toast_broker_connected:'تم ربط الوسيط', toast_coming_soon:'قريباً',
    toast_upgrading:'جار التحويل', toast_view_plans:'كل الخطط',
    confirm_close_pos:'تأكيد إغلاق', confirm_close_all:'إغلاق كل المراكز؟ لا يمكن التراجع!', confirm_del_strat:'حذف الاستراتيجية',
    bt_running:'جارٍ...', ai_analyze_suffix:' كيف ترى مركزي؟',
    ai_placeholder:'أدخل تعليمات التداول أو سؤالك…',
    ai_resp_btc:'📊 تحليل BTC/USDT:\n\nالسعر قرب $83,400، مواجهة مقاومة $84,000. تقاطع MACD الذهبي، RSI(14) = 58 — صاعد لكن غير مشبع.\n\nالتوصية: لونج صغير من $82,800، وقف $81,000، هدف $86,000. R/R ≈ 1:2.2.',
    ai_resp_gold:'🥇 تحليل الذهب (XAU/USD):\n\nالذهب قوي عند $2,342. دعم من FED الحمامي والدولار الضعيف. هدف $2,380، دعم $2,310.\n\nالتوصية: الاحتفاظ بالشراء، تحريك الوقف إلى $2,320 لتأمين الأرباح.',
    ai_resp_position:'📐 إدارة المركز ($1,000 رأس مال):\n\n• BTC/USDT: 30% ($300) — رئيسي، 5x رافعة\n• XAU/USD: 25% ($250) — تحوط، 10x\n• EUR/USD: 20% ($200) — تحوط عملات\n• نقدي: 25% ($250) — انتظار\n\nأقصى خسارة: 3% للصفقة.',
    ai_resp_strategy:'⚡ 3 استراتيجيات مناسبة للسوق الحالي:\n\n1. **BTC MACD اتجاهي** — 67% فوز، +89% سنوياً\n2. **شبكة الذهب** — للسوق الجانبي، 3-5%/شهر\n3. **EUR/USD EMA** — مخاطرة منخفضة، مناسب للمبتدئين\n\nهل تريد تفعيل إحداها؟',
    ai_resp_default:'فهمت طلبك. دعني أحلل أوضاع السوق الحالية...\n\n📊 السوق صاعد بشكل عام، لكن احذر مخاطر سياسة FED. أبقِ المراكز أقل من 50% وضع وقف الخسارة دائماً.\n\nهل تريد استكشاف رمز أو استراتيجية معينة؟',
  },

  // ===== 12种新语言翻译 (Quantpeak 18语言计划) =====
  // 繁体中文
  'zh-tw': {
    nav_dashboard:'儀表盤',nav_market:'行情',nav_ai:'AI 客服',
    nav_positions:'我的持倉',nav_strategies:'策略管理',nav_backtest:'策略回測',nav_account:'我的帳戶',
    page_dashboard:'儀表盤',page_market:'行情',page_ai:'AI 客服',
    page_positions:'我的持倉',page_strategies:'策略管理',page_backtest:'策略回測',page_account:'我的帳戶',
    page_copy:'跟單交易',page_autoopen:'自動建倉',
    total_asset:'總資產',daily_pnl:'今日損益',win_rate:'勝率',active_strategies:'活躍策略',pos_count:'持倉數量',
    card_today:'今日',card_month:'本月',card_paused:'個暫停',card_running:'個運行中',
    card_long:'多',card_short:'空',
    quick_order:'+ 快速下單',
    chart_update:'分鐘更新',
    market_title:'即時行情',search_placeholder:'搜尋品種...',
    mkt_all:'全部',mkt_crypto:'加密貨幣',mkt_forex:'外匯',mkt_metals:'貴金屬',mkt_energy:'能源',mkt_index:'指數',
    tbl_symbol:'品種',tbl_price:'最新價',tbl_change:'漲跌幅',tbl_volume:'成交量',tbl_trend:'7日走勢',tbl_action:'操作',
    ai_title:'AI 量化助手',ai_placeholder:'輸入你的交易指令或問題...',
    ai_welcome:'你好！我是 QuantAI 智能助手 🤖\n\n我可以幫你：\n• 查詢即時行情和K線分析\n• 管理持倉和下單交易\n• 解讀策略績效\n• 風控建議和倉位管理\n\n請問有什麼可以幫您的？',
    ai_feat1:'分析市場行情並給出策略建議',ai_feat2:'執行自動化交易下單',
    ai_feat3:'計算倉位、止損止盈點位',ai_feat4:'回測你的策略歷史表現',
    ai_sugg1:'BTC 現在可以買入嗎？',ai_sugg2:'幫我做一個黃金網格策略',
    ai_sugg3:'我有$1000，怎麼分配倉位？',ai_sugg4:'EUR/USD 趨勢分析',ai_sugg5:'查看我的持倉情況',
    quick_order_title:'快速下單',dir_long:'做多 Long',dir_short:'做空 Short',
    order_symbol:'交易品種',order_amount:'投入金額 (USD)',order_sltp:'止損 / 止盈 (%)',order_confirm:'確認下單',
    sentiment_title:'市場情緒',sent_bull:'多頭',sent_bear:'空頭',sent_fg:'恐貪指數',sent_greed:'貪婪',sent_flow:'大單淨流入',sent_rate:'資金費率',
    pos_title:'我的持倉',pos_symbol:'品種',pos_size:'手數',pos_open:'開倉價',pos_current:'當前價',pos_pnl:'浮盈/虧',pos_action:'操作',
    pos_close:'平倉',pos_empty:'暫無持倉',
    pos_my_title:'我的持倉',pos_active_count:'個活躍持倉',pos_float:'浮盈',close_all:'一鍵全平',
    pos_open_lbl:'開倉價',pos_curr_lbl:'當前價',pos_sl_lbl:'止損價',pos_tp_lbl:'止盈價',
    pos_ai_analyze:'AI分析',pos_edit_btn:'修改',
    mkt_buy:'買入',mkt_sell:'賣出',
    strat_cum_pnl:'累計損益',
    strat_title:'策略管理',strat_new:'新建策略',
    strat_running:'運行中',strat_paused:'已暫停',strat_stopped:'已停止',
    strat_start:'啟動',strat_pause:'暫停',strat_stop:'停止',strat_edit:'編輯',
    strat_my_title:'我的策略',strat_running_count:'個運行中',strat_paused_count:'個已暫停',strat_add:'添加策略',
    bt_title:'策略回測',bt_symbol:'交易品種',bt_strat_type:'策略類型',
    bt_start_date:'開始日期',bt_end_date:'結束日期',bt_capital:'初始資金 (USD)',bt_pos_size:'每筆倉位 (%)',
    bt_run:'開始回測',bt_total_return:'總收益率',bt_annual_return:'年化收益',bt_max_dd:'最大回撤',
    bt_sharpe:'夏普比率',bt_win_rate:'勝率',bt_trades:'總交易次數',bt_log_title:'交易記錄（最近20筆）',
    strat_macd:'MACD 趨勢追蹤',strat_ema:'EMA 均線交叉',strat_rsi:'RSI 超買超賣',strat_grid:'網格交易',strat_bb:'布林帶突破',
    acc_title:'我的帳戶',acc_plan:'當前方案',acc_upgrade:'升級訂閱',
    acc_broker:'券商帳戶',acc_connect:'連接券商',
    acc_member_free:'免費版',acc_member_pro:'Pro 會員',acc_member_elite:'精英會員',
    acc_valid_until:'有效期至',acc_reg_date:'註冊時間',acc_total_pnl:'總盈利',
    acc_brokers_count:'已連接券商',acc_running_strats:'運行策略',acc_account:'帳戶',
    acc_broker_section:'已連接券商',acc_subscription:'我的訂閱',
    broker_connected:'已連接',broker_api_ok:'API正常',broker_not_connected:'未連接',broker_pending:'待配置',broker_add_new:'添加新券商',
    btn_manage:'管理',btn_disconnect:'斷開',btn_connect:'連接',btn_edit:'修改',
    plan_current:'當前',per_month:'/月',plan_view_all:'查看全部方案 →',
    plan_basic_f1:'全品種行情查看',plan_basic_f2:'AI客服問答',plan_basic_f3:'2個策略',plan_basic_f4:'自動交易',
    plan_pro_f1:'無限策略',plan_pro_f2:'AI自動交易',plan_pro_f3:'高級回測',plan_pro_f4:'多券商',
    plan_elite_f1:'自動建倉（策略/定投/跟單）',plan_elite_f2:'複製交易無限跟單',plan_elite_f3:'專屬VIP客服',plan_elite_f4:'優先執行通道',
    risk_title:'風控設置',risk_max_loss:'單日最大虧損',risk_max_loss_desc:'超過後自動停止所有策略',
    risk_max_pos:'最大持倉比例',risk_max_pos_desc:'單品種不超過總資產百分比',
    risk_auto_order:'AI 自動下單',risk_auto_order_desc:'允許AI在策略觸發時自動執行',
    risk_notify:'下單前推送通知',risk_notify_desc:'每次下單前發送確認',
    risk_night:'夜間保護模式',risk_night_desc:'22:00-07:00 暫停自動交易',
    confirm:'確認',cancel:'取消',save:'儲存',close:'關閉',
    loading:'載入中...',success:'操作成功',error:'操作失敗',
    lang_switched:'🌐 已切換為繁體中文',
    tlog_title:'交易日誌',tlog_all:'全部',tlog_buy:'做多',tlog_sell:'做空',tlog_win:'盈利',tlog_loss:'虧損',
    tlog_total_trades:'總筆數',tlog_win_rate:'勝率',tlog_net_pnl:'淨損益',tlog_avg_hold:'平均持倉',tlog_best:'最佳單筆',tlog_worst:'最差單筆',
    tlog_col_time:'時間',tlog_col_symbol:'品種',tlog_col_dir:'方向',tlog_col_open:'開倉價',tlog_col_close:'平倉價',tlog_col_size:'手數',tlog_col_pnl:'損益',tlog_col_hold:'持倉時長',
    tlog_dir_long:'做多',tlog_dir_short:'做空',tlog_empty:'暫無交易記錄',
    nav_copy:'複製交易',copy_title:'複製交易',copy_subtitle:'一鍵跟隨頂級交易者，信號即時同步',
    copy_goto_auto:'自動建倉設置',copy_my_follows:'我的跟單',copy_leaderboard:'信號源排行',
    copy_filter_all:'全部',copy_filter_crypto:'加密',copy_filter_forex:'外匯',copy_filter_stable:'低回撤',
    copy_followers:'人跟隨',copy_monthly:'月收益',copy_winrate:'勝率',copy_maxdd:'最大回撤',copy_30pnl:'近30天盈利',
    copy_follow_btn:'跟單',copy_following:'✓ 已跟隨',copy_unfollow:'取消跟隨',copy_detail_btn:'詳情',
    copy_pnl:'浮盈',copy_since:'跟隨自',copy_follow_title:'跟單設置',copy_confirm_follow:'確認跟單',
    copy_toast_follow:'已開始跟單',copy_toast_unfollow:'已取消跟隨',
    ct_tag_ct1:'BTC/ETH 專家 · 3年',ct_tag_ct2:'黃金/外匯 · 5年',ct_tag_ct3:'低回撤穩健型 · 4年',
    ct_tag_ct4:'夜盤剝头皮 · 2年',ct_tag_ct5:'宏觀多品種 · 6年',ct_tag_ct6:'定投+趨勢 · 7年',
    nav_autoopen:'自動建倉',ao_title:'自動建倉',ao_subtitle:'三種智能建倉模式，全自動執行',
    ao_lock_title:'自動建倉為 Elite 專屬功能',ao_lock_desc:'升級到 Elite 計劃，解鎖全自動化交易建倉能力',
    ao_lock_btn:'立即升級 $199/月',
    ao_mode_signal:'策略觸發',ao_mode_signal_desc:'RSI/MACD/EMA 等技術指標觸發時自動建倉',
    ao_mode_dca:'定時定投',ao_mode_dca_desc:'按設定週期自動分批建倉，平均成本',
    ao_mode_copy:'跟單同步',ao_mode_copy_desc:'綁定信號源，自動同步其每筆開倉操作',
    ao_running:'運行中',
    ao_signal_cfg:'策略觸發配置',ao_signal_ind:'觸發指標',ao_signal_pair:'交易品種',
    ao_dca_cfg:'定時定投配置',ao_dca_pair:'定投品種',ao_dca_freq:'定投頻率',
    ao_dca_hourly:'每小時',ao_dca_daily:'每天',ao_dca_weekly:'每週',ao_dca_monthly:'每月',
    ao_dca_amount:'每次金額 (USD)',ao_dca_total:'總投入上限 (USD)',ao_dca_price_drop:'下跌加倍 (%)',ao_dca_exit:'止盈退出 (%)',
    ao_dca_invested:'已投入',
    ao_copy_cfg:'跟單同步配置',ao_copy_source:'綁定信號源',ao_copy_select:'選擇信號源',
    ao_copy_ratio:'跟單倍數',ao_copy_max:'單筆最大 (USD)',ao_copy_daily_loss:'日虧損保護 (USD)',
    ao_copy_filter:'只跟方向',ao_copy_all:'多空均跟',ao_copy_long_only:'只跟做多',ao_copy_short_only:'只跟做空',
    ao_copy_pairs:'限制品種',ao_copy_pairs_ph:'BTC,ETH（空=不限）',ao_not_following:'未跟隨',
    ao_pos_size:'每筆倉位 (USD)',ao_sl:'止損 (%)',ao_tp:'止盈 (%)',ao_max_pos:'最大同時持倉',
    lb_tab_roi:'月收益排行',lb_tab_wr:'勝率排行',lb_tab_stable:'最穩排行',lb_tab_new:'新秀榜',
    nav_square:'交易廣場',sq_title:'交易廣場',sq_subtitle:'分享觀點，發現市場情緒，與全球交易者同頻',
    sq_post_ph:'分享你的市場觀點、交易邏輯、倉位分析...',sq_post_btn:'發布觀點',
    sq_filter_all:'全部',sq_filter_bull:'看多',sq_filter_bear:'看空',sq_filter_hot:'熱門',
    sq_pair_label:'交易對',sq_sentiment_label:'情緒',
    nav_stratmarket:'策略市場',sm_title:'策略市場',sm_subtitle:'發現、分享、一鍵復用頂級量化策略',
    sm_upload_title:'發布我的策略',sm_upload_btn:'上傳策略',sm_filter_all:'全部',
    sm_filter_trend:'趨勢追蹤',sm_filter_grid:'網格',sm_filter_quant:'量化',sm_filter_arb:'套利',
    sm_name_label:'策略名稱',sm_asset_label:'適用品種',sm_price_label:'定價(USD/月,0=免費)',
    sm_code_label:'策略代碼',sm_submit_btn:'提交審核',sm_backtest:'回測',
    sm_copy:'複製',sm_subscribe:'訂閱',
    nav_signals:'信號廣播',sig_title:'信號廣播',sig_subtitle:'即時交易信號，一鍵訂閱推送，接入自動建倉',
    sig_publish_title:'發布交易信號',sig_tab_live:'即時信號',sig_tab_sources:'信號源',sig_tab_history:'歷史記錄',
    sig_pair:'交易對',sig_dir:'方向',sig_dir_buy:'做多',sig_dir_sell:'做空',
    sig_entry:'入埸價',sig_sl:'止損',sig_tp1:'TP1',sig_tp2:'TP2',
    sig_desc:'信號說明',sig_publish_btn:'廣播信號',
    sig_follow:'跟單信號',sig_share:'分享',sig_subscribe_bc:'訂閱信號源',
    ao_start:'啟動自動建倉',ao_stop:'停止運行',ao_status_off:'● 未啟動',ao_status_on:'🟢 運行中',
    ao_started:'已啟動',ao_stopped:'已停止',
    ao_exec_log:'執行日誌',ao_clear_log:'清空',ao_log_empty:'暫無執行記錄',
    toast_elite_unlocked:'已解鎖 Elite！自動建倉功能已開啟',
    dash_brief_title:'AI 今日簡報',dash_brief_time:'08:00 更新',
    dash_brief_content:'黃金今日偏多，美聯儲鴿派信號支撐，目標位 $2,380。BTC 在 $84,000 面臨壓力，短期建議觀望。納指受科技股財報帶動，整體偏強。外匯方面 EUR/USD 弱勢震盪，美元指數 104.2 支撐。',
    dash_signal_gold:'黃金 ▲ 多',dash_signal_btc:'BTC ⚠ 觀望',dash_signal_eur:'EUR/USD ▼ 弱',dash_signal_nas:'納指 ▲ 強',
    dash_quick_ops:'快捷操作',dash_btn_order:'AI 下單',dash_btn_backtest:'快速回測',dash_btn_positions:'查看持倉',
    ai_welcome_greet:'你好！我是 QuantAI 智能助手 🧠',ai_welcome_intro:'你可以告訴我你的交易想法，我會幫你：',
    modal_symbol:'品種',modal_dir:'方向',modal_amount:'金額 (USD)',modal_leverage:'槓桿倍數',
    modal_sl:'止損 (%)',modal_tp:'止盈 (%)',modal_margin:'預計保證金',modal_max_profit:'最大收益',modal_max_loss:'最大虧損',
    broker_modal_title:'連接新券商',broker_connect_btn:'驗證並連接',
    cat_crypto:'加密貨幣',cat_forex_metals:'外匯/貴金屬',cat_all_cfd:'全品種CFD',
    sym_btc:'比特幣',sym_eth:'以太坊',sym_sol:'Solana',sym_bnb:'幣安幣',sym_xrp:'瑞波幣',
    sym_eurusd:'歐元/美元',sym_gbpusd:'英鎊/美元',sym_usdjpy:'美元/日元',sym_usdchf:'美元/瑞郎',sym_audusd:'澳元/美元',
    sym_gold:'黃金現貨',sym_silver:'白銀現貨',sym_wti:'WTI原油',sym_brent:'布倫特原油',
    sym_nas100:'納斯達克100',sym_spx500:'標普500',sym_dow:'道琼斯',sym_hsi:'恆生指數',
    strat_name_1:'BTC MACD趨勢策略',strat_name_2:'黃金網格套利',strat_name_3:'EUR/USD 均線策略',strat_name_4:'納指超短線',
    strat_type_trend:'趨勢追蹤',strat_type_grid:'網格交易',strat_type_ema:'均線交叉',strat_type_mr:'均值回歸',
    toast_order_ok:'下單成功！',toast_submitted:'已提交！',toast_pos_closed:'已平倉',toast_all_closed:'所有持倉已全部平倉',
    toast_strat_started:'已啟動',toast_strat_paused:'已暫停',toast_strat_deleted:'策略已刪除',
    toast_broker_connected:'券商連接成功！API 驗證通過',toast_coming_soon:'功能即將上線，敬請期待',
    toast_upgrading:'即將跳轉到',toast_view_plans:'查看完整訂閱方案',
    confirm_close_pos:'確認平倉',confirm_close_all:'確認一鍵全平所有持倉？此操作不可撤銷！',confirm_del_strat:'確認刪除策略',
    bt_running:'回測中...',
    ai_analyze_suffix:' 當前持倉怎麼看？',
    ai_placeholder:'輸入你的交易指令或問題…',
    ai_resp_btc:'📊 BTC/USDT 當前分析：\n\n價格在 $83,400 附近，近期面臨 $84,000 壓力位。MACD 指標出現金叉信號，RSI(14) 在 58，偏多但未超買。\n\n建議：可在 $82,800 支撐附近小倉試多，止損 $81,000，目標 $86,000。風險收益比約 1:2.2。',
    ai_resp_gold:'🥇 黃金(XAU/USD)分析：\n\n金價維持強勢，當前 $2,342。美聯儲降息預期支撐，美元指數偏弱。近期目標 $2,380，關鍵支撐 $2,310。\n\n建議：可持有多單，移動止損至 $2,320 鎖住利潤。',
    ai_resp_position:'📐 倉位管理建議（$1,000 資金）：\n\n• BTC/USDT: 30% ($300) — 主倉，5倍槓桿\n• XAU/USD: 25% ($250) — 對沖，10倍槓桿\n• EUR/USD: 20% ($200) — 外匯對沖\n• 現金儲備: 25% ($250) — 等待機會\n\n單筆最大虧損控制在 3%。',
    ai_resp_strategy:'⚡ 為您推薦3個適合當前行情的策略：\n\n1. **BTC MACD趨勢** — 勝率67%，回測年化+89%\n2. **黃金網格** — 適合震盪行情，月收益3-5%\n3. **EUR/USD均線** — 低風險，適合新手\n\n是否要我幫您開啟某個策略？',
    ai_resp_default:'我理解了您的需求。根據當前市場情況，讓我為您分析一下...\n\n📊 市場整體偏多，但需注意美聯儲政策風險。建議保持倉位在50%以下，並設置好止損。\n\n有什麼具體的交易品種或策略想深入了解嗎？',
  },

  // 粤语
  yue: {
    nav_dashboard:'儀表板',nav_market:'行情',nav_ai:'AI 客服',
    nav_positions:'我嘅持倉',nav_strategies:'策略管理',nav_backtest:'策略回測',nav_account:'我嘅戶口',
    page_dashboard:'儀表板',page_market:'行情',page_ai:'AI 助手',
    page_positions:'我嘅持倉',page_strategies:'策略管理',page_backtest:'策略回測',page_account:'我嘅戶口',
    page_copy:'跟單交易',page_autoopen:'自動開倉',
    total_asset:'總資產',daily_pnl:'今日盈虧',win_rate:'勝率',active_strategies:'活躍策略',pos_count:'持倉數量',
    card_today:'今日',card_month:'今個月',card_paused:'個暫停',card_running:'個運作中',
    card_long:'好',card_short:'淡',
    quick_order:'+ 快速落單',
    chart_update:'分鐘更新',
    market_title:'實時行情',search_placeholder:'搜尋品種...',
    mkt_all:'全部',mkt_crypto:'加密貨幣',mkt_forex:'外匯',mkt_metals:'貴金屬',mkt_energy:'能源',mkt_index:'指數',
    tbl_symbol:'品種',tbl_price:'最新價',tbl_change:'升跌幅',tbl_volume:'成交量',tbl_trend:'7日趨勢',tbl_action:'操作',
    ai_title:'AI 量化助手',ai_placeholder:'輸入你嘅交易指令或問題...',
    ai_welcome:'你好！我是 QuantAI 智能助手 🤖\n\n我可以幫你：\n• 查詢實時行情同K線分析\n• 管理持倉同落單交易\n• 解讀策略表現\n• 風控建議同倉位管理\n\n請問有咩可以幫到你？',
    ai_feat1:'分析市場行情並給出策略建議',ai_feat2:'執行自動化交易落單',
    ai_feat3:'計算倉位、止蝕止賺點位',ai_feat4:'回測你嘅策略歷史表現',
    ai_sugg1:'BTC 現在可以買入嗎？',ai_sugg2:'幫我做一個黃金網格策略',
    ai_sugg3:'我有$1000，點樣分配倉位？',ai_sugg4:'EUR/USD 趨勢分析',ai_sugg5:'睇下我嘅持倉情況',
    quick_order_title:'快速落單',dir_long:'做好 Long',dir_short:'做淡 Short',
    order_symbol:'交易品種',order_amount:'投入金額 (USD)',order_sltp:'止蝕 / 止賺 (%)',order_confirm:'確認落單',
    sentiment_title:'市場情緒',sent_bull:'好友',sent_bear:'淡友',sent_fg:'恐貪指數',sent_greed:'貪心',sent_flow:'大單淨流入',sent_rate:'資金費率',
    pos_title:'我嘅持倉',pos_symbol:'品種',pos_size:'手數',pos_open:'開倉價',pos_current:'現價',pos_pnl:'浮盈/虧',pos_action:'操作',
    pos_close:'平倉',pos_empty:'暫無持倉',
    pos_my_title:'我嘅持倉',pos_active_count:'個活躍持倉',pos_float:'浮盈',close_all:'一鍵全平',
    pos_open_lbl:'開倉價',pos_curr_lbl:'現價',pos_sl_lbl:'止蝕價',pos_tp_lbl:'止賺價',
    pos_ai_analyze:'AI分析',pos_edit_btn:'修改',
    mkt_buy:'買入',mkt_sell:'賣出',
    strat_cum_pnl:'累計盈虧',
    strat_title:'策略管理',strat_new:'新建策略',
    strat_running:'運作中',strat_paused:'已暫停',strat_stopped:'已停止',
    strat_start:'啟動',strat_pause:'暫停',strat_stop:'停止',strat_edit:'編輯',
    strat_my_title:'我嘅策略',strat_running_count:'個運作中',strat_paused_count:'個已暫停',strat_add:'添加策略',
    bt_title:'策略回測',bt_symbol:'交易品種',bt_strat_type:'策略類型',
    bt_start_date:'開始日期',bt_end_date:'結束日期',bt_capital:'初始資金 (USD)',bt_pos_size:'每筆倉位 (%)',
    bt_run:'開始回測',bt_total_return:'總回報率',bt_annual_return:'年度回報',bt_max_dd:'最大回撤',
    bt_sharpe:'夏普比率',bt_win_rate:'勝率',bt_trades:'總交易次數',bt_log_title:'交易記錄（最近20筆）',
    strat_macd:'MACD 趨勢追蹤',strat_ema:'EMA 均線交叉',strat_rsi:'RSI 超買超賣',strat_grid:'網格交易',strat_bb:'布林帶突破',
    acc_title:'我嘅戶口',acc_plan:'當前方案',acc_upgrade:'升級訂閱',
    acc_broker:'券商戶口',acc_connect:'連接券商',
    acc_member_free:'免費版',acc_member_pro:'Pro 會員',acc_member_elite:'精英會員',
    acc_valid_until:'有效期至',acc_reg_date:'註冊時間',acc_total_pnl:'總盈利',
    acc_brokers_count:'已連接券商',acc_running_strats:'運作策略',acc_account:'戶口',
    acc_broker_section:'已連接券商',acc_subscription:'我嘅訂閱',
    broker_connected:'已連接',broker_api_ok:'API正常',broker_not_connected:'未連接',broker_pending:'待配置',broker_add_new:'添加新券商',
    btn_manage:'管理',btn_disconnect:'斷開',btn_connect:'連接',btn_edit:'修改',
    plan_current:'當前',per_month:'/月',plan_view_all:'查看全部方案 →',
    plan_basic_f1:'全品種行情查看',plan_basic_f2:'AI客服問答',plan_basic_f3:'2個策略',plan_basic_f4:'自動交易',
    plan_pro_f1:'無限策略',plan_pro_f2:'AI自動交易',plan_pro_f3:'高級回測',plan_pro_f4:'多券商',
    plan_elite_f1:'自動開倉（策略/定投/跟單）',plan_elite_f2:'複製交易無限跟單',plan_elite_f3:'專屬VIP客服',plan_elite_f4:'優先執行通道',
    risk_title:'風控設置',risk_max_loss:'單日最大虧損',risk_max_loss_desc:'超過後自動停止所有策略',
    risk_max_pos:'最大持倉比例',risk_max_pos_desc:'單品種不超過總資產百分比',
    risk_auto_order:'AI 自動落單',risk_auto_order_desc:'允許AI喺策略觸發時自動執行',
    risk_notify:'落單前推送通知',risk_notify_desc:'每次落單前發送確認',
    risk_night:'夜間保護模式',risk_night_desc:'22:00-07:00 暫停自動交易',
    confirm:'確認',cancel:'取消',save:'儲存',close:'關閉',
    loading:'載入中...',success:'操作成功',error:'操作失敗',
    lang_switched:'🌐 已切換為粵語',
    tlog_title:'交易記錄',tlog_all:'全部',tlog_buy:'做好',tlog_sell:'做淡',tlog_win:'盈利',tlog_loss:'虧損',
    tlog_total_trades:'總筆數',tlog_win_rate:'勝率',tlog_net_pnl:'淨盈虧',tlog_avg_hold:'平均持倉',tlog_best:'最佳單筆',tlog_worst:'最差單筆',
    tlog_col_time:'時間',tlog_col_symbol:'品種',tlog_col_dir:'方向',tlog_col_open:'開倉價',tlog_col_close:'平倉價',tlog_col_size:'手數',tlog_col_pnl:'盈虧',tlog_col_hold:'持倉時長',
    tlog_dir_long:'做好',tlog_dir_short:'做淡',tlog_empty:'暫無交易記錄',
    nav_copy:'複製交易',copy_title:'複製交易',copy_subtitle:'一鍵跟隨頂級交易者，信號實時同步',
    copy_goto_auto:'自動開倉設置',copy_my_follows:'我嘅跟單',copy_leaderboard:'信號源排行',
    copy_filter_all:'全部',copy_filter_crypto:'加密',copy_filter_forex:'外匯',copy_filter_stable:'低回撤',
    copy_followers:'人跟隨',copy_monthly:'月收益',copy_winrate:'勝率',copy_maxdd:'最大回撤',copy_30pnl:'近30天盈利',
    copy_follow_btn:'跟單',copy_following:'✓ 已跟隨',copy_unfollow:'取消跟隨',copy_detail_btn:'詳情',
    copy_pnl:'浮盈',copy_since:'跟隨自',copy_follow_title:'跟單設置',copy_confirm_follow:'確認跟單',
    copy_toast_follow:'已開始跟單',copy_toast_unfollow:'已取消跟隨',
    ct_tag_ct1:'BTC/ETH 專家 · 3年',ct_tag_ct2:'黃金/外匯 · 5年',ct_tag_ct3:'低回撤穩健型 · 4年',
    ct_tag_ct4:'夜盤剝头皮 · 2年',ct_tag_ct5:'宏觀多品種 · 6年',ct_tag_ct6:'定投+趨勢 · 7年',
    nav_autoopen:'自動開倉',ao_title:'自動開倉',ao_subtitle:'三種智能開倉模式，全自動執行',
    ao_lock_title:'自動開倉為 Elite 專屬功能',ao_lock_desc:'升級到 Elite 計劃，解鎖全自動化交易開倉能力',
    ao_lock_btn:'立即升級 $199/月',
    ao_mode_signal:'策略觸發',ao_mode_signal_desc:'RSI/MACD/EMA 等技術指標觸發時自動開倉',
    ao_mode_dca:'定時定投',ao_mode_dca_desc:'按設定週期自動分批開倉，平均成本',
    ao_mode_copy:'跟單同步',ao_mode_copy_desc:'綁定信號源，自動同步其每筆開倉操作',
    ao_running:'運作中',
    ao_signal_cfg:'策略觸發配置',ao_signal_ind:'觸發指標',ao_signal_pair:'交易品種',
    ao_dca_cfg:'定時定投配置',ao_dca_pair:'定投品種',ao_dca_freq:'定投頻率',
    ao_dca_hourly:'每小時',ao_dca_daily:'每日',ao_dca_weekly:'每週',ao_dca_monthly:'每月',
    ao_dca_amount:'每次金額 (USD)',ao_dca_total:'總投入上限 (USD)',ao_dca_price_drop:'下跌加倍 (%)',ao_dca_exit:'止賺退出 (%)',
    ao_dca_invested:'已投入',
    ao_copy_cfg:'跟單同步配置',ao_copy_source:'綁定信號源',ao_copy_select:'選擇信號源',
    ao_copy_ratio:'跟單倍數',ao_copy_max:'單筆最大 (USD)',ao_copy_daily_loss:'日虧損保護 (USD)',
    ao_copy_filter:'只跟方向',ao_copy_all:'多淡均跟',ao_copy_long_only:'只跟做好',ao_copy_short_only:'只跟做淡',
    ao_copy_pairs:'限制品種',ao_copy_pairs_ph:'BTC,ETH（空=不限）',ao_not_following:'未跟隨',
    ao_pos_size:'每筆倉位 (USD)',ao_sl:'止蝕 (%)',ao_tp:'止賺 (%)',ao_max_pos:'最大同時持倉',
    lb_tab_roi:'月收益排行',lb_tab_wr:'勝率排行',lb_tab_stable:'最穩排行',lb_tab_new:'新秀榜',
    nav_square:'交易廣場',sq_title:'交易廣場',sq_subtitle:'分享觀點，發現市場情緒，與全球交易者同頻',
    sq_post_ph:'分享你嘅市場觀點、交易邏輯、倉位分析...',sq_post_btn:'發布觀點',
    sq_filter_all:'全部',sq_filter_bull:'睇好',sq_filter_bear:'睇淡',sq_filter_hot:'熱門',
    sq_pair_label:'交易對',sq_sentiment_label:'情緒',
    nav_stratmarket:'策略市場',sm_title:'策略市場',sm_subtitle:'發現、分享、一鍵復用頂級量化策略',
    sm_upload_title:'發布我嘅策略',sm_upload_btn:'上傳策略',sm_filter_all:'全部',
    sm_filter_trend:'趨勢追蹤',sm_filter_grid:'網格',sm_filter_quant:'量化',sm_filter_arb:'套利',
    sm_name_label:'策略名稱',sm_asset_label:'適用品種',sm_price_label:'定價(USD/月,0=免費)',
    sm_code_label:'策略代碼',sm_submit_btn:'提交審核',sm_backtest:'回測',
    sm_copy:'複製',sm_subscribe:'訂閱',
    nav_signals:'信號廣播',sig_title:'信號廣播',sig_subtitle:'實時交易信號，一鍵訂閱推送，接入自動開倉',
    sig_publish_title:'發布交易信號',sig_tab_live:'實時信號',sig_tab_sources:'信號源',sig_tab_history:'歷史記錄',
    sig_pair:'交易對',sig_dir:'方向',sig_dir_buy:'做好',sig_dir_sell:'做淡',
    sig_entry:'入埸價',sig_sl:'止蝕',sig_tp1:'TP1',sig_tp2:'TP2',
    sig_desc:'信號說明',sig_publish_btn:'廣播信號',
    sig_follow:'跟單信號',sig_share:'分享',sig_subscribe_bc:'訂閱信號源',
    ao_start:'啟動自動開倉',ao_stop:'停止運作',ao_status_off:'● 未啟動',ao_status_on:'🟢 運作中',
    ao_started:'已啟動',ao_stopped:'已停止',
    ao_exec_log:'執行日誌',ao_clear_log:'清空',ao_log_empty:'暫無執行記錄',
    toast_elite_unlocked:'已解鎖 Elite！自動開倉功能已開啟',
    dash_brief_title:'AI 今日簡報',dash_brief_time:'08:00 更新',
    dash_brief_content:'黃金今日偏多，美聯儲鴿派信號支撐，目標位 $2,380。BTC 在 $84,000 面臨壓力，短期建議觀望。納指受科技股財報帶動，整體偏強。外匯方面 EUR/USD 弱勢震盪，美元指數 104.2 支撐。',
    dash_signal_gold:'黃金 ▲ 多',dash_signal_btc:'BTC ⚠ 觀望',dash_signal_eur:'EUR/USD ▼ 弱',dash_signal_nas:'納指 ▲ 強',
    dash_quick_ops:'快捷操作',dash_btn_order:'AI 落單',dash_btn_backtest:'快速回測',dash_btn_positions:'查看持倉',
    ai_welcome_greet:'你好！我是 QuantAI 智能助手 🧠',ai_welcome_intro:'你可以話俾我聽你嘅交易想法，我會幫你：',
    modal_symbol:'品種',modal_dir:'方向',modal_amount:'金額 (USD)',modal_leverage:'槓桿倍數',
    modal_sl:'止蝕 (%)',modal_tp:'止賺 (%)',modal_margin:'預計保證金',modal_max_profit:'最大收益',modal_max_loss:'最大虧損',
    broker_modal_title:'連接新券商',broker_connect_btn:'驗證並連接',
    cat_crypto:'加密貨幣',cat_forex_metals:'外匯/貴金屬',cat_all_cfd:'全品種CFD',
    sym_btc:'比特幣',sym_eth:'以太坊',sym_sol:'Solana',sym_bnb:'幣安幣',sym_xrp:'瑞波幣',
    sym_eurusd:'歐元/美元',sym_gbpusd:'英鎊/美元',sym_usdjpy:'美元/日元',sym_usdchf:'美元/瑞郎',sym_audusd:'澳元/美元',
    sym_gold:'黃金現貨',sym_silver:'白銀現貨',sym_wti:'WTI原油',sym_brent:'布倫特原油',
    sym_nas100:'納斯達克100',sym_spx500:'標普500',sym_dow:'道琼斯',sym_hsi:'恆生指數',
    strat_name_1:'BTC MACD趨勢策略',strat_name_2:'黃金網格套利',strat_name_3:'EUR/USD 均線策略',strat_name_4:'納指超短線',
    strat_type_trend:'趨勢追蹤',strat_type_grid:'網格交易',strat_type_ema:'均線交叉',strat_type_mr:'均值回歸',
    toast_order_ok:'落單成功！',toast_submitted:'已提交！',toast_pos_closed:'已平倉',toast_all_closed:'所有持倉已全部平倉',
    toast_strat_started:'已啟動',toast_strat_paused:'已暫停',toast_strat_deleted:'策略已刪除',
    toast_broker_connected:'券商連接成功！API 驗證通過',toast_coming_soon:'功能即將上線，敬請期待',
    toast_upgrading:'即將跳轉到',toast_view_plans:'查看完整訂閱方案',
    confirm_close_pos:'確認平倉',confirm_close_all:'確認一鍵全平所有持倉？此操作不可撤銷！',confirm_del_strat:'確認刪除策略',
    bt_running:'回測中...',
    ai_analyze_suffix:' 當前持倉點睇？',
    ai_placeholder:'輸入你嘅交易指令或問題…',
    ai_resp_btc:'📊 BTC/USDT 當前分析：\n\n價格在 $83,400 附近，近期面臨 $84,000 壓力位。MACD 指標出現金叉信號，RSI(14) 在 58，偏多但未超買。\n\n建議：可在 $82,800 支撐附近小倉試好，止蝕 $81,000，目標 $86,000。風險收益比約 1:2.2。',
    ai_resp_gold:'🥇 黃金(XAU/USD)分析：\n\n金價維持強勢，當前 $2,342。美聯儲降息預期支撐，美元指數偏弱。近期目標 $2,380，關鍵支撐 $2,310。\n\n建議：可持有多單，移動止蝕至 $2,320 鎖住利潤。',
    ai_resp_position:'📐 倉位管理建議（$1,000 資金）：\n\n• BTC/USDT: 30% ($300) — 主倉，5倍槓桿\n• XAU/USD: 25% ($250) — 對沖，10倍槓桿\n• EUR/USD: 20% ($200) — 外匯對沖\n• 現金儲備: 25% ($250) — 等待機會\n\n單筆最大虧損控制在 3%。',
    ai_resp_strategy:'⚡ 為您推薦3個適合當前行情的策略：\n\n1. **BTC MACD趨勢** — 勝率67%，回測年化+89%\n2. **黃金網格** — 適合震盪行情，月收益3-5%\n3. **EUR/USD均線** — 低風險，適合新手\n\n是否要我幫您開啟某個策略？',
    ai_resp_default:'我理解了您的需求。根據當前市場情況，讓我為您分析一下...\n\n📊 市場整體偏多，但需注意美聯儲政策風險。建議保持倉位在50%以下，並設置好止蝕。\n\n有什麼具體的交易品種或策略想深入了解嗎？',
  },

  // 德语
  de: {
    nav_dashboard:'Dashboard',nav_market:'Markt',nav_ai:'AI Chat',
    nav_positions:'Positionen',nav_strategies:'Strategien',nav_backtest:'Backtest',nav_account:'Konto',
    page_dashboard:'Dashboard',page_market:'Markt',page_ai:'AI Assistent',
    page_positions:'Meine Positionen',page_strategies:'Strategieverwaltung',page_backtest:'Backtest',page_account:'Mein Konto',
    page_copy:'Copy Trading',page_autoopen:'Auto-Eröffnung',
    total_asset:'Gesamtvermögen',daily_pnl:'Heutige P&L',win_rate:'Gewinnrate',active_strategies:'Aktive Strategien',pos_count:'Offene Positionen',
    card_today:'Heute',card_month:'Diesen Monat',card_paused:' Pausiert',card_running:' Läuft',
    card_long:'Long',card_short:'Short',
    quick_order:'+ Schnellorder',
    chart_update:'Min Update',
    market_title:'Live-Markt',search_placeholder:'Symbol suchen...',
    mkt_all:'Alle',mkt_crypto:'Krypto',mkt_forex:'Forex',mkt_metals:'Metalle',mkt_energy:'Energie',mkt_index:'Indizes',
    tbl_symbol:'Symbol',tbl_price:'Preis',tbl_change:'Änderung',tbl_volume:'Volumen',tbl_trend:'7T Trend',tbl_action:'Aktion',
    ai_title:'AI Trading Assistent',ai_placeholder:'Nachricht eingeben...',
    ai_welcome:'Hallo! Ich bin QuantAI Assistent 🤖\n\nIch kann dir helfen:\n• Echtzeit-Marktdaten & Chartanalyse\n• Positionen & Orders verwalten\n• Strategie-Performance analysieren\n• Risikomanagement & Positionsgröße\n\nWie kann ich dir helfen?',
    ai_feat1:'Markttrends analysieren & Strategien vorschlagen',ai_feat2:'Automatische Trades ausführen',
    ai_feat3:'Positionsgröße & Stops berechnen',ai_feat4:'Strategie-Backtest durchführen',
    ai_sugg1:'Sollte ich BTC jetzt kaufen?',ai_sugg2:'Gold Grid Strategie erstellen',
    ai_sugg3:'Wie $1000 aufteilen?',ai_sugg4:'EUR/USD Trendanalayse',ai_sugg5:'Meine Positionen anzeigen',
    quick_order_title:'Schnellorder',dir_long:'Long Kauf',dir_short:'Short Verkauf',
    order_symbol:'Symbol',order_amount:'Betrag (USD)',order_sltp:'SL / TP (%)',order_confirm:'Order platzieren',
    sentiment_title:'Marktstimmung',sent_bull:'Bullisch',sent_bear:'Bearisch',sent_fg:'Angst & Gier',sent_greed:'Gier',sent_flow:'Großorder Nettozufluss',sent_rate:'Funding Rate',
    pos_title:'Meine Positionen',pos_symbol:'Symbol',pos_size:'Größe',pos_open:'Eröffnung',pos_current:'Aktuell',pos_pnl:'P&L',pos_action:'Aktion',
    pos_close:'Schließen',pos_empty:'Keine Positionen',
    pos_my_title:'Meine Positionen',pos_active_count:' Aktive',pos_float:'Floating P&L',close_all:'Alle schließen',
    pos_open_lbl:'Eröffnung',pos_curr_lbl:'Aktuell',pos_sl_lbl:'Stop Loss',pos_tp_lbl:'Take Profit',
    pos_ai_analyze:'KI-Analyse',pos_edit_btn:'Bearbeiten',
    mkt_buy:'Kaufen',mkt_sell:'Verkaufen',
    strat_cum_pnl:'Gesamt P&L',
    strat_title:'Strategieverwaltung',strat_new:'Neue Strategie',
    strat_running:'Läuft',strat_paused:'Pausiert',strat_stopped:'Gestoppt',
    strat_start:'Start',strat_pause:'Pause',strat_stop:'Stop',strat_edit:'Bearbeiten',
    strat_my_title:'Meine Strategien',strat_running_count:' Läuft',strat_paused_count:' Pausiert',strat_add:'Strategie hinzufügen',
    bt_title:'Backtest',bt_symbol:'Symbol',bt_strat_type:'Strategietyp',
    bt_start_date:'Startdatum',bt_end_date:'Enddatum',bt_capital:'Startkapital (USD)',bt_pos_size:'Positionsgröße (%)',
    bt_run:'Backtest starten',bt_total_return:'Gesamtrendite',bt_annual_return:'Jährliche Rendite',bt_max_dd:'Max Drawdown',
    bt_sharpe:'Sharpe Ratio',bt_win_rate:'Gewinnrate',bt_trades:'Gesamte Trades',bt_log_title:'Handelsprotokoll (Letzte 20)',
    strat_macd:'MACD Trendfolge',strat_ema:'EMA Crossover',strat_rsi:'RSI Überkauft/Überverkauft',strat_grid:'Grid Trading',strat_bb:'Bollinger Ausbruch',
    acc_title:'Mein Konto',acc_plan:'Aktueller Plan',acc_upgrade:'Upgrade',
    acc_broker:'Broker-Konto',acc_connect:'Broker verbinden',
    acc_member_free:'Kostenlos',acc_member_pro:'Pro Member',acc_member_elite:'Elite Member',
    acc_valid_until:'Gültig bis',acc_reg_date:'Registriert',acc_total_pnl:'Gesamt P&L',
    acc_brokers_count:'Broker',acc_running_strats:'Aktive Strategien',acc_account:'Konto',
    acc_broker_section:'Verbundene Broker',acc_subscription:'Mein Abo',
    broker_connected:'Verbunden',broker_api_ok:'API OK',broker_not_connected:'Nicht verbunden',broker_pending:'Ausstehend',broker_add_new:'Broker hinzufügen',
    btn_manage:'Verwalten',btn_disconnect:'Trennen',btn_connect:'Verbinden',btn_edit:'Bearbeiten',
    plan_current:'Aktuell',per_month:'/Mo',plan_view_all:'Alle Pläne →',
    plan_basic_f1:'Alle Marktdaten',plan_basic_f2:'AI Q&A',plan_basic_f3:'2 Strategien',plan_basic_f4:'Auto Trading',
    plan_pro_f1:'Unbegrenzte Strategien',plan_pro_f2:'AI Auto Trading',plan_pro_f3:'Erweiterter Backtest',plan_pro_f4:'Multi-Broker',
    plan_elite_f1:'Auto-Eröffnung (Signal/DCA/Copy)',plan_elite_f2:'Unbegrenztes Copy Trading',plan_elite_f3:'VIP Support',plan_elite_f4:'Prioritätsausführung',
    risk_title:'Risikokontrollen',risk_max_loss:'Tagesmaximum Verlust',risk_max_loss_desc:'Auto-Stop bei Überschreitung',
    risk_max_pos:'Max Positionsgröße',risk_max_pos_desc:'Pro Symbol, % der Gesamtmittel',
    risk_auto_order:'AI Auto Order',risk_auto_order_desc:'KI darf bei Strategie-Trigger ausführen',
    risk_notify:'Vor-Order Benachrichtigung',risk_notify_desc:'Bestätigung vor jedem Trade',
    risk_night:'Nachtschutz',risk_night_desc:'22:00-07:00 Auto Trading pausieren',
    confirm:'Bestätigen',cancel:'Abbrechen',save:'Speichern',close:'Schließen',
    loading:'Laden...',success:'Erfolg',error:'Fehler',
    lang_switched:'🌐 Zu Deutsch gewechselt',
    tlog_title:'Handelsprotokoll',tlog_all:'Alle',tlog_buy:'Long',tlog_sell:'Short',tlog_win:'Gewinn',tlog_loss:'Verlust',
    tlog_total_trades:'Trades',tlog_win_rate:'Gewinnrate',tlog_net_pnl:'Netto P&L',tlog_avg_hold:'Durchschn. Haltezeit',tlog_best:'Bester Trade',tlog_worst:'Schlechtester Trade',
    tlog_col_time:'Zeit',tlog_col_symbol:'Symbol',tlog_col_dir:'Richtung',tlog_col_open:'Eröffnung',tlog_col_close:'Schließen',tlog_col_size:'Lots',tlog_col_pnl:'P&L',tlog_col_hold:'Haltezeit',
    tlog_dir_long:'Long',tlog_dir_short:'Short',tlog_empty:'Keine Handelsaufzeichnungen',
    nav_copy:'Copy Trading',copy_title:'Copy Trading',copy_subtitle:'Top Trader folgen, Signale in Echtzeit synchron',
    copy_goto_auto:'Auto-Einstellungen',copy_my_follows:'Meine Follows',copy_leaderboard:'Signal Rangliste',
    copy_filter_all:'Alle',copy_filter_crypto:'Krypto',copy_filter_forex:'Forex',copy_filter_stable:'Niedrig DD',
    copy_followers:'Follower',copy_monthly:'Monatlich',copy_winrate:'Gewinnrate',copy_maxdd:'Max DD',copy_30pnl:'30T P&L',
    copy_follow_btn:'Folgen',copy_following:'✓ Folgend',copy_unfollow:'Unfollow',copy_detail_btn:'Details',
    copy_pnl:'Float P&L',copy_since:'Seit',copy_follow_title:'Follow Einstellungen',copy_confirm_follow:'Bestätigen',
    copy_toast_follow:'Folge jetzt',copy_toast_unfollow:'Unfollowed',
    ct_tag_ct1:'BTC/ETH Experte · 3Jahre',ct_tag_ct2:'Gold/Forex · 5Jahre',ct_tag_ct3:'Niedrig-DD Stabil · 4Jahre',
    ct_tag_ct4:'Nacht Scalper · 2Jahre',ct_tag_ct5:'Makro Multi · 6Jahre',ct_tag_ct6:'DCA+Trend · 7Jahre',
    nav_autoopen:'Auto-Eröffnung',ao_title:'Auto-Eröffnung',ao_subtitle:'3 intelligente Auto-Einstiegsmodi',
    ao_lock_title:'Auto-Eröffnung ist Elite-exklusiv',ao_lock_desc:'Auf Elite upgraden um Auto-Eröffnung freizuschalten',
    ao_lock_btn:'Upgraden $199/Monat',
    ao_mode_signal:'Signal Trigger',ao_mode_signal_desc:'Auto-Einstieg bei RSI/MACD/EMA Bedingungen',
    ao_mode_dca:'Wiederkehrende DCA',ao_mode_dca_desc:'Automatischer regelmäßiger Kauf zum Durchschnittspreis',
    ao_mode_copy:'Copy Sync',ao_mode_copy_desc:'Jeden Einstieg vom Signalquelle spiegeln',
    ao_running:'Läuft',
    ao_signal_cfg:'Signal Konfiguration',ao_signal_ind:'Indikator',ao_signal_pair:'Symbol',
    ao_dca_cfg:'DCA Konfiguration',ao_dca_pair:'Symbol',ao_dca_freq:'Häufigkeit',
    ao_dca_hourly:'Stündlich',ao_dca_daily:'Täglich',ao_dca_weekly:'Wöchentlich',ao_dca_monthly:'Monatlich',
    ao_dca_amount:'Betrag pro Einstieg (USD)',ao_dca_total:'Gesamtlimit (USD)',ao_dca_price_drop:'Verdoppeln bei Kurssturz (%)',ao_dca_exit:'Take Profit (%)',
    ao_dca_invested:'Investiert',
    ao_copy_cfg:'Copy Konfiguration',ao_copy_source:'Signalquelle',ao_copy_select:'Auswählen',
    ao_copy_ratio:'Verhältnis',ao_copy_max:'Max pro Trade (USD)',ao_copy_daily_loss:'Tagesverlust-Grenze (USD)',
    ao_copy_filter:'Richtungsfilter',ao_copy_all:'Long & Short',ao_copy_long_only:'Nur Long',ao_copy_short_only:'Nur Short',
    ao_copy_pairs:'Limit Symbole',ao_copy_pairs_ph:'BTC,ETH (leer=alle)',ao_not_following:'Nicht folgen',
    ao_pos_size:'Positionsgröße (USD)',ao_sl:'Stop Loss (%)',ao_tp:'Take Profit (%)',ao_max_pos:'Max offene Positionen',
    lb_tab_roi:'Monatliche ROI',lb_tab_wr:'Gewinnrate',lb_tab_stable:'Am stabilsten',lb_tab_new:'Aufsteiger',
    nav_square:'Trading Platz',sq_title:'Trading Platz',sq_subtitle:'Teile deine Sicht, entdecke Sentiment, sync mit globalen Tradern',
    sq_post_ph:'Teile deine Marktsicht, Tradingslogik, Positionsanalyse...',sq_post_btn:'Posten',
    sq_filter_all:'Alle',sq_filter_bull:'Bullisch',sq_filter_bear:'Bearisch',sq_filter_hot:'Heiß',
    sq_pair_label:'Paar',sq_sentiment_label:'Sentiment',
    nav_stratmarket:'Strategiemarkt',sm_title:'Strategiemarkt',sm_subtitle:'Entdecke, teile und kopiere Top-Quant-Strategien',
    sm_upload_title:'Meine Strategie veröffentlichen',sm_upload_btn:'Strategie hochladen',sm_filter_all:'Alle',
    sm_filter_trend:'Trend',sm_filter_grid:'Grid',sm_filter_quant:'Quant',sm_filter_arb:'Arb',
    sm_name_label:'Strategiename',sm_asset_label:'Symbol',sm_price_label:'Preis (USD/Monat, 0=Gratis)',
    sm_code_label:'Strategiecode',sm_submit_btn:'Zur Prüfung einreichen',sm_backtest:'Backtest',
    sm_copy:'Kopieren',sm_subscribe:'Abonnieren',
    nav_signals:'Signal广播',sig_title:'Signal广播',sig_subtitle:'Live-Signale, Ein-Klick-Abonnement, verbinde mit Auto-Eröffnung',
    sig_publish_title:'Handelssignal veröffentlichen',sig_tab_live:'Live Signale',sig_tab_sources:'Signalquellen',sig_tab_history:'Verlauf',
    sig_pair:'Paar',sig_dir:'Richtung',sig_dir_buy:'Kauf',sig_dir_sell:'Verkauf',
    sig_entry:'Einstieg',sig_sl:'Stop Loss',sig_tp1:'TP1',sig_tp2:'TP2',
    sig_desc:'Signalnotiz',sig_publish_btn:'Signal senden',
    sig_follow:'Signal folgen',sig_share:'Teilen',sig_subscribe_bc:'Quelle abonnieren',
    ao_start:'Auto-Eröffnung starten',ao_stop:'Stopp',ao_status_off:'● Gestoppt',ao_status_on:'🟢 Läuft',
    ao_started:'Gestartet',ao_stopped:'Gestoppt',
    ao_exec_log:'Ausführungsprotokoll',ao_clear_log:'Löschen',ao_log_empty:'Keine Ausführungsaufzeichnungen',
    toast_elite_unlocked:'Elite freigeschaltet! Auto-Eröffnung ist jetzt verfügbar',
    dash_brief_title:'AI Tagesbriefing',dash_brief_time:'Update 08:00',
    dash_brief_content:'Gold heute bullisch, unterstützt von Fed Dovish-Signalen, Ziel $2,380. BTC hat Widerstand bei $84,000, kurzfristig vorsichtig. Nasdaq von Tech-Ergebnissen getrieben, generell stark. EUR/USD schwache Oszillation, USD-Index 104.2 Unterstützung.',
    dash_signal_gold:'Gold ▲ Bullisch',dash_signal_btc:'BTC ⚠ Beobachten',dash_signal_eur:'EUR/USD ▼ Schwach',dash_signal_nas:'Nasdaq ▲ Stark',
    dash_quick_ops:'Schnelle Aktionen',dash_btn_order:'AI Order',dash_btn_backtest:'Schneller Backtest',dash_btn_positions:'Positionen anzeigen',
    ai_welcome_greet:'Hallo! Ich bin QuantAI Assistent 🧠',ai_welcome_intro:'Erzähl mir deine Tradingideen und ich helfe dir:',
    modal_symbol:'Symbol',modal_dir:'Richtung',modal_amount:'Betrag (USD)',modal_leverage:'Hebel',
    modal_sl:'Stop Loss (%)',modal_tp:'Take Profit (%)',modal_margin:'Geschätzte Marge',modal_max_profit:'Max Gewinn',modal_max_loss:'Max Verlust',
    broker_modal_title:'Broker verbinden',broker_connect_btn:'Verifizieren & Verbinden',
    cat_crypto:'Krypto',cat_forex_metals:'Forex / Metalle',cat_all_cfd:'Alle CFDs',
    sym_btc:'Bitcoin',sym_eth:'Ethereum',sym_sol:'Solana',sym_bnb:'BNB',sym_xrp:'Ripple',
    sym_eurusd:'EUR/USD',sym_gbpusd:'GBP/USD',sym_usdjpy:'USD/JPY',sym_usdchf:'USD/CHF',sym_audusd:'AUD/USD',
    sym_gold:'Spot Gold',sym_silver:'Spot Silber',sym_wti:'WTI Rohöl',sym_brent:'Brent Rohöl',
    sym_nas100:'Nasdaq 100',sym_spx500:'S&P 500',sym_dow:'Dow Jones',sym_hsi:'Hang Seng',
    strat_name_1:'BTC MACD Trend',strat_name_2:'Gold Grid Arb',strat_name_3:'EUR/USD EMA Strategie',strat_name_4:'Nasdaq Scalping',
    strat_type_trend:'Trendfolge',strat_type_grid:'Grid Trading',strat_type_ema:'EMA Crossover',strat_type_mr:'Mean Reversion',
    toast_order_ok:'Order platziert!',toast_submitted:'Gesendet!',toast_pos_closed:'Position geschlossen',toast_all_closed:'Alle Positionen geschlossen',
    toast_strat_started:'gestartet',toast_strat_paused:'pausiert',toast_strat_deleted:'Strategie gelöscht',
    toast_broker_connected:'Broker verbunden! API verifiziert',toast_coming_soon:'Demnächst',
    toast_upgrading:'Weiterleitung zu',toast_view_plans:'Alle Pläne anzeigen',
    confirm_close_pos:'Schließen bestätigen',confirm_close_all:'Alle Positionen schließen? Dies kann nicht rückgängig gemacht werden!',confirm_del_strat:'Strategie löschen',
    bt_running:'Läuft...',
    ai_analyze_suffix:' wie sieht meine Position aus?',
    ai_placeholder:'Nachricht eingeben…',
    ai_resp_btc:'📊 BTC/USDT Analyse:\n\nPreis nahe $83,400, Widerstand bei $84,000. MACD goldener Crossover, RSI(14) bei 58 — bullisch aber nicht überkauft.\n\nVorschlag: Kleiner Long nahe $82,800 Unterstützung, Stop bei $81,000, Ziel $86,000. R/R ≈ 1:2.2.',
    ai_resp_gold:'🥇 Gold (XAU/USD) Analyse:\n\nGold bleibt stark bei $2,342. Fed Dovish-Signale und schwacher USD bieten Unterstützung. Kurzfristiges Ziel $2,380, Schlüsselunterstützung $2,310.\n\nVorschlag: Longs halten, Stop auf $2,320 verschieben um Gewinne zu sichern.',
    ai_resp_position:'📐 Positionsgröße ($1.000 Kapital):\n\n• BTC/USDT: 30% ($300) — Hauptposition, 5x Hebel\n• XAU/USD: 25% ($250) — Absicherung, 10x\n• EUR/USD: 20% ($200) — FX Absicherung\n• Bargeld: 25% ($250) — Auf Gelegenheit warten\n\nMaximaler Verlust pro Trade: 3%.',
    ai_resp_strategy:'⚡ 3 Strategien für den aktuellen Markt:\n\n1. **BTC MACD Trend** — 67% Gewinnrate, +89% annualisiert\n2. **Gold Grid** — Am besten für Seitwärtsmärkte, 3-5%/Monat\n3. **EUR/USD EMA** — Niedriges Risiko, gut für Anfänger\n\nSoll ich eine für dich aktivieren?',
    ai_resp_default:'Ich verstehe deine Anfrage. Lass mich die aktuellen Marktbedingungen analysieren...\n\n📊 Der Markt ist generell bullisch, aber achte auf Fed-Policing-Risiken. Halte Positionen unter 50% und setze immer Stops.\n\nGibt es ein bestimmtes Symbol oder eine Strategie, die du erkunden möchtest?',
  },

  // 法语
  fr: {
    nav_dashboard:'Tableau de bord',nav_market:'Marché',nav_ai:'Chat IA',
    nav_positions:'Positions',nav_strategies:'Stratégies',nav_backtest:'Backtest',nav_account:'Compte',
    page_dashboard:'Tableau de bord',page_market:'Marché',page_ai:'Assistant IA',
    page_positions:'Mes Positions',page_strategies:'Gestionnaire de stratégies',page_backtest:'Backtest',page_account:'Mon Compte',
    page_copy:'Copy Trading',page_autoopen:'Ouverture Auto',
    total_asset:'Total Actifs',daily_pnl:'P&L du jour',win_rate:'Taux de réussite',active_strategies:'Stratégies actives',pos_count:'Positions ouvertes',
    card_today:"Aujourd'hui",card_month:'Ce mois',card_paused:' En pause',card_running:' En cours',
    card_long:'Long',card_short:'Short',
    quick_order:'+ Ordre rapide',
    chart_update:'min mise à jour',
    market_title:'Marché en direct',search_placeholder:'Rechercher symbole...',
    mkt_all:'Tous',mkt_crypto:'Crypto',mkt_forex:'Forex',mkt_metals:'Métaux',mkt_energy:'Énergie',mkt_index:'Indices',
    tbl_symbol:'Symbole',tbl_price:'Prix',tbl_change:'Variation',tbl_volume:'Volume',tbl_trend:'Tendance 7j',tbl_action:'Action',
    ai_title:'Assistant Trading IA',ai_placeholder:'Entrez un message...',
    ai_welcome:'Bonjour! Je suis l\'assistant QuantAI 🤖\n\nJe peux vous aider:\n• Données de marché en temps réel & analyse de graphiques\n• Gérer les positions & passer des ordres\n• Analyser les performances des stratégies\n• Gestion des risques & taille des positions\n\nComment puis-je vous aider?',
    ai_feat1:'Analyser les tendances du marché et suggérer des stratégies',ai_feat2:'Exécuter des ordres de trading automatisés',
    ai_feat3:'Calculer la taille de position et les stops',ai_feat4:'Backtester la performance de votre stratégie',
    ai_sugg1:'Devrais-je acheter du BTC maintenant?',ai_sugg2:'Créer une stratégie grid sur l\'or',
    ai_sugg3:'Comment allouer $1000?',ai_sugg4:'Analyse de tendance EUR/USD',ai_sugg5:'Afficher mes positions',
    quick_order_title:'Ordre rapide',dir_long:'Achat Long',dir_short:'Vente Short',
    order_symbol:'Symbole',order_amount:'Montant (USD)',order_sltp:'SL / TP (%)',order_confirm:'Passer l\'ordre',
    sentiment_title:'Sentiment du marché',sent_bull:'Haussier',sent_bear:'Baissier',sent_fg:'Peur & Avidité',sent_greed:'Avidité',sent_flow:'Flux net important',sent_rate:'Taux de financement',
    pos_title:'Mes Positions',pos_symbol:'Symbole',pos_size:'Taille',pos_open:'Prix d\'entrée',pos_current:'Actuel',pos_pnl:'P&L',pos_action:'Action',
    pos_close:'Fermer',pos_empty:'Aucune position',
    pos_my_title:'Mes Positions',pos_active_count:' Positions actives',pos_float:'P&L flottant',close_all:'Tout fermer',
    pos_open_lbl:'Entrée',pos_curr_lbl:'Actuel',pos_sl_lbl:'Stop Loss',pos_tp_lbl:'Take Profit',
    pos_ai_analyze:'Analyse IA',pos_edit_btn:'Modifier',
    mkt_buy:'Acheter',mkt_sell:'Vendre',
    strat_cum_pnl:'P&L total',
    strat_title:'Gestionnaire de stratégies',strat_new:'Nouvelle stratégie',
    strat_running:'En cours',strat_paused:'En pause',strat_stopped:'Arrêtée',
    strat_start:'Démarrer',strat_pause:'Pause',strat_stop:'Arrêter',strat_edit:'Modifier',
    strat_my_title:'Mes Stratégies',strat_running_count:' en cours',strat_paused_count:' en pause',strat_add:'Ajouter une stratégie',
    bt_title:'Backtest',bt_symbol:'Symbole',bt_strat_type:'Type de stratégie',
    bt_start_date:'Date de début',bt_end_date:'Date de fin',bt_capital:'Capital initial (USD)',bt_pos_size:'Taille de position (%)',
    bt_run:'Lancer le backtest',bt_total_return:'Rendement total',bt_annual_return:'Rendement annualisé',bt_max_dd:'Drawdown max',
    bt_sharpe:'Ratio de Sharpe',bt_win_rate:'Taux de réussite',bt_trades:'Total des trades',bt_log_title:'Journal des trades (20 derniers)',
    strat_macd:'MACD Suivi de tendance',strat_ema:'EMA Crossover',strat_rsi:'RSI Survente/Surachat',strat_grid:'Grid Trading',strat_bb:'Bollinger Breakout',
    acc_title:'Mon Compte',acc_plan:'Plan actuel',acc_upgrade:'Mettre à niveau',
    acc_broker:'Compte broker',acc_connect:'Connecter le broker',
    acc_member_free:'Gratuit',acc_member_pro:'Membre Pro',acc_member_elite:'Membre Elite',
    acc_valid_until:'Valide jusqu\'au',acc_reg_date:'Inscription',acc_total_pnl:'P&L total',
    acc_brokers_count:'Brokers',acc_running_strats:'Stratégies actives',acc_account:'Compte',
    acc_broker_section:'Brokers connectés',acc_subscription:'Mon abonnement',
    broker_connected:'Connecté',broker_api_ok:'API OK',broker_not_connected:'Non connecté',broker_pending:'En attente',broker_add_new:'Ajouter un broker',
    btn_manage:'Gérer',btn_disconnect:'Déconnecter',btn_connect:'Connecter',btn_edit:'Modifier',
    plan_current:'Actuel',per_month:'/mois',plan_view_all:'Voir tous les plans →',
    plan_basic_f1:'Toutes les données de marché',plan_basic_f2:'Q&R IA',plan_basic_f3:'2 stratégies',plan_basic_f4:'Trading auto',
    plan_pro_f1:'Stratégies illimitées',plan_pro_f2:'Trading auto IA',plan_pro_f3:'Backtest avancé',plan_pro_f4:'Multi-broker',
    plan_elite_f1:'Ouverture auto (Signal/DCA/Copy)',plan_elite_f2:'Copy trading illimité',plan_elite_f3:'Support VIP',plan_elite_f4:'Exécution prioritaire',
    risk_title:'Contrôles de risque',risk_max_loss:'Perte max quotidienne',risk_max_loss_desc:'Auto-stop si dépassé',
    risk_max_pos:'Taille max de position',risk_max_pos_desc:'Par symbole, % du total des actifs',
    risk_auto_order:'Ordre auto IA',risk_auto_order_desc:'L\'IA exécute quand la stratégie se déclenche',
    risk_notify:'Notification pré-ordre',risk_notify_desc:'Envoyer confirmation avant chaque trade',
    risk_night:'Protection nocturne',risk_night_desc:'22:00-07:00 suspendre le trading auto',
    confirm:'Confirmer',cancel:'Annuler',save:'Sauvegarder',close:'Fermer',
    loading:'Chargement...',success:'Succès',error:'Erreur',
    lang_switched:'🌐 Passé en français',
    tlog_title:'Journal des trades',tlog_all:'Tous',tlog_buy:'Long',tlog_sell:'Short',tlog_win:'Profit',tlog_loss:'Perte',
    tlog_total_trades:'Trades',tlog_win_rate:'Taux de réussite',tlog_net_pnl:'P&L net',tlog_avg_hold:'Moyenne tenue',tlog_best:'Meilleur trade',tlog_worst:'Pire trade',
    tlog_col_time:'Temps',tlog_col_symbol:'Symbole',tlog_col_dir:'Direction',tlog_col_open:'Entrée',tlog_col_close:'Sortie',tlog_col_size:'Lots',tlog_col_pnl:'P&L',tlog_col_hold:'Durée',
    tlog_dir_long:'Long',tlog_dir_short:'Short',tlog_empty:'Aucun enregistrement',
    nav_copy:'Copy Trading',copy_title:'Copy Trading',copy_subtitle:'Suivez les meilleurs traders, signaux en temps réel',
    copy_goto_auto:'Paramètres ouverture auto',copy_my_follows:'Mes abonnements',copy_leaderboard:'Classement des signaux',
    copy_filter_all:'Tous',copy_filter_crypto:'Crypto',copy_filter_forex:'Forex',copy_filter_stable:'Faible DD',
    copy_followers:'abonnés',copy_monthly:'Mensuel',copy_winrate:'Taux de réussite',copy_maxdd:'DD max',copy_30pnl:'P&L 30j',
    copy_follow_btn:'Suivre',copy_following:'✓ Suivi',copy_unfollow:'Ne plus suivre',copy_detail_btn:'Détails',
    copy_pnl:'P&L flottant',copy_since:'Depuis',copy_follow_title:'Paramètres de suivi',copy_confirm_follow:'Confirmer',
    copy_toast_follow:'Suivi commencé',copy_toast_unfollow:'Suivi annulé',
    ct_tag_ct1:'Expert BTC/ETH · 3ans',ct_tag_ct2:'Or/Forex · 5ans',ct_tag_ct3:'Stable DD faible · 4ans',
    ct_tag_ct4:'Scalper nocturne · 2ans',ct_tag_ct5:'Multi-macro · 6ans',ct_tag_ct6:'DCA+Tendance · 7ans',
    nav_autoopen:'Ouverture Auto',ao_title:'Ouverture Auto',ao_subtitle:'3 modes intelligents d\'entrée auto',
    ao_lock_title:'Ouverture Auto exclusive Elite',ao_lock_desc:'Passez à Elite pour débloquer l\'entrée automatique',
    ao_lock_btn:'Mettre à niveau $199/mois',
    ao_mode_signal:'Déclencheur de signal',ao_mode_signal_desc:'Entrée auto quand conditions RSI/MACD/EMA remplies',
    ao_mode_dca:'DCA récurrent',ao_mode_dca_desc:'Achats automatiques périodiques pour coût moyen',
    ao_mode_copy:'Sync copy',ao_mode_copy_desc:'Mirror chaque entrée de la source de signaux',
    ao_running:'En cours',
    ao_signal_cfg:'Config signal',ao_signal_ind:'Indicateur',ao_signal_pair:'Symbole',
    ao_dca_cfg:'Config DCA',ao_dca_pair:'Symbole',ao_dca_freq:'Fréquence',
    ao_dca_hourly:'Toutes les heures',ao_dca_daily:'Quotidien',ao_dca_weekly:'Hebdomadaire',ao_dca_monthly:'Mensuel',
    ao_dca_amount:'Montant par entrée (USD)',ao_dca_total:'Plafond total (USD)',ao_dca_price_drop:'Doubledip si baisse (%)',ao_dca_exit:'Take Profit (%)',
    ao_dca_invested:'Investi',
    ao_copy_cfg:'Config copy',ao_copy_source:'Source de signaux',ao_copy_select:'Sélectionner',
    ao_copy_ratio:'Ratio',ao_copy_max:'Max par trade (USD)',ao_copy_daily_loss:'Limite perte quotidienne (USD)',
    ao_copy_filter:'Filtre direction',ao_copy_all:'Long & Short',ao_copy_long_only:'Long seulement',ao_copy_short_only:'Short seulement',
    ao_copy_pairs:'Limiter symboles',ao_copy_pairs_ph:'BTC,ETH (vide=tous)',ao_not_following:'Non suivi',
    ao_pos_size:'Taille position (USD)',ao_sl:'Stop Loss (%)',ao_tp:'Take Profit (%)',ao_max_pos:'Max positions ouvertes',
    lb_tab_roi:'ROI mensuel',lb_tab_wr:'Taux de réussite',lb_tab_stable:'Le plus stable',lb_tab_new:'Nouveaux',
    nav_square:'Place de trading',sq_title:'Place de trading',sq_subtitle:'Partagez vos vues, découvrez le sentiment, synchronisez avec les traders globaux',
    sq_post_ph:'Partagez votre vue de marché, logique de trading, analyse de position...',sq_post_btn:'Publier',
    sq_filter_all:'Tous',sq_filter_bull:'Haussier',sq_filter_bear:'Baissier',sq_filter_hot:'Hot',
    sq_pair_label:'Paire',sq_sentiment_label:'Sentiment',
    nav_stratmarket:'Marché des stratégies',sm_title:'Marché des stratégies',sm_subtitle:'Découvrez, partagez et copiez les meilleures stratégies quant',
    sm_upload_title:'Publier ma stratégie',sm_upload_btn:'Uploader stratégie',sm_filter_all:'Tous',
    sm_filter_trend:'Tendance',sm_filter_grid:'Grid',sm_filter_quant:'Quant',sm_filter_arb:'Arb',
    sm_name_label:'Nom de la stratégie',sm_asset_label:'Symbole',sm_price_label:'Prix (USD/mois, 0=Gratuit)',
    sm_code_label:'Code de stratégie',sm_submit_btn:'Soumettre pour révision',sm_backtest:'Backtest',
    sm_copy:'Copier',sm_subscribe:'S\'abonner',
    nav_signals:'Diffusion de signaux',sig_title:'Diffusion de signaux',sig_subtitle:'Signaux en direct, abonnement en un clic, connexion à l\'ouverture auto',
    sig_publish_title:'Publier signal de trading',sig_tab_live:'Signaux en direct',sig_tab_sources:'Sources de signaux',sig_tab_history:'Historique',
    sig_pair:'Paire',sig_dir:'Direction',sig_dir_buy:'Achat',sig_dir_sell:'Vente',
    sig_entry:'Entrée',sig_sl:'Stop Loss',sig_tp1:'TP1',sig_tp2:'TP2',
    sig_desc:'Note du signal',sig_publish_btn:'Diffuser le signal',
    sig_follow:'Suivre le signal',sig_share:'Partager',sig_subscribe_bc:'S\'abonner à la source',
    ao_start:'Démarrer ouverture auto',ao_stop:'Arrêter',ao_status_off:'● Arrêté',ao_status_on:'🟢 En cours',
    ao_started:'Démarré',ao_stopped:'Arrêté',
    ao_exec_log:'Journal d\'exécution',ao_clear_log:'Effacer',ao_log_empty:'Aucun enregistrement',
    toast_elite_unlocked:'Elite débloqué! Ouverture auto maintenant disponible',
    dash_brief_title:'Briefing quotidien IA',dash_brief_time:'Mise à jour 08:00',
    dash_brief_content:'Or haussier aujourd\'hui, soutenu par signaux Fed dovish, objectif $2,380. BTC résistance à $84,000, court terme prudent. Nasdaq driven par résultats tech, généralement fort. EUR/USD oscillation faible, USD index 104.2 support.',
    dash_signal_gold:'Or ▲ Haussier',dash_signal_btc:'BTC ⚠ Surveiller',dash_signal_eur:'EUR/USD ▼ Faible',dash_signal_nas:'Nasdaq ▲ Fort',
    dash_quick_ops:'Actions rapides',dash_btn_order:'Ordre IA',dash_btn_backtest:'Backtest rapide',dash_btn_positions:'Voir les positions',
    ai_welcome_greet:'Bonjour! Je suis l\'assistant QuantAI 🧠',ai_welcome_intro:'Parlez-moi de vos idées de trading et je vous aiderai:',
    modal_symbol:'Symbole',modal_dir:'Direction',modal_amount:'Montant (USD)',modal_leverage:'Effet de levier',
    modal_sl:'Stop Loss (%)',modal_tp:'Take Profit (%)',modal_margin:'Marge estimée',modal_max_profit:'Profit max',modal_max_loss:'Perte max',
    broker_modal_title:'Connecter un broker',broker_connect_btn:'Vérifier et connecter',
    cat_crypto:'Crypto',cat_forex_metals:'Forex / Métaux',cat_all_cfd:'Tous les CFD',
    sym_btc:'Bitcoin',sym_eth:'Ethereum',sym_sol:'Solana',sym_bnb:'BNB',sym_xrp:'Ripple',
    sym_eurusd:'EUR/USD',sym_gbpusd:'GBP/USD',sym_usdjpy:'USD/JPY',sym_usdchf:'USD/CHF',sym_audusd:'AUD/USD',
    sym_gold:'Or au comptant',sym_silver:'Argent au comptant',sym_wti:'WTI Crude',sym_brent:'Brent Crude',
    sym_nas100:'Nasdaq 100',sym_spx500:'S&P 500',sym_dow:'Dow Jones',sym_hsi:'Hang Seng',
    strat_name_1:'BTC MACD Tendance',strat_name_2:'Grid Or',strat_name_3:'Stratégie EUR/USD EMA',strat_name_4:'Scalping Nasdaq',
    strat_type_trend:'Suivi de tendance',strat_type_grid:'Grid Trading',strat_type_ema:'EMA Crossover',strat_type_mr:'Retour à la moyenne',
    toast_order_ok:'Ordre passé!',toast_submitted:'Soumis!',toast_pos_closed:'Position fermée',toast_all_closed:'Toutes les positions fermées',
    toast_strat_started:'démarrée',toast_strat_paused:'en pause',toast_strat_deleted:'Stratégie supprimée',
    toast_broker_connected:'Broker connecté! API vérifié',toast_coming_soon:'Bientôt disponible',
    toast_upgrading:'Redirection vers',toast_view_plans:'Voir tous les plans',
    confirm_close_pos:'Confirmer fermeture',confirm_close_all:'Fermer toutes les positions? Irréversible!',confirm_del_strat:'Supprimer la stratégie',
    bt_running:'En cours...',
    ai_analyze_suffix:' comment est ma position?',
    ai_placeholder:'Entrez votre instruction de trading ou question…',
    ai_resp_btc:'📊 Analyse BTC/USDT:\n\nPrix près de $83,400, résistance à $84,000. MACD golden cross, RSI(14) à 58 — haussier mais pas suracheté.\n\nSuggestion: Petit long près du support $82,800, stop à $81,000, objectif $86,000. R/R ≈ 1:2.2.',
    ai_resp_gold:'🥇 Analyse Or (XAU/USD):\n\nL\'or reste fort à $2,342. Signaux Fed dovish et dollar faible offrent support. Objectif court terme $2,380, support clé $2,310.\n\nSuggestion: Garder les longs, déplacer le stop à $2,320 pour sécuriser les profits.',
    ai_resp_position:'📐 Gestion de position ($1.000 capital):\n\n• BTC/USDT: 30% ($300) — Position principale, levier 5x\n• XAU/USD: 25% ($250) — Couverture, 10x\n• EUR/USD: 20% ($200) — Couverture FX\n• Liquidités: 25% ($250) — Attendre les opportunités\n\nPerte max par trade: 3%.',
    ai_resp_strategy:'⚡ 3 stratégies pour le marché actuel:\n\n1. **BTC MACD Tendance** — 67% de réussite, +89% annualisé\n2. **Grid Or** — Pour marchés latéraux, 3-5%/mois\n3. **EUR/USD EMA** — Risque faible, idéal pour débutants\n\nVoulez-vous en activer une?',
    ai_resp_default:'J\'ai compris votre demande. Laissez-moi analyser les conditions actuelles du marché...\n\n📊 Le marché est généralement haussier, mais attention aux risques de politique Fed. Gardez les positions sous 50% et définissez toujours des stops.\n\nY a-t-il un symbole ou une stratégie spécifique que vous souhaitez explorer?',
  },

  // 西班牙语
  es: {
    nav_dashboard:'Panel',nav_market:'Mercado',nav_ai:'Chat IA',
    nav_positions:'Posiciones',nav_strategies:'Estrategias',nav_backtest:'Backtest',nav_account:'Cuenta',
    page_dashboard:'Panel',page_market:'Mercado',page_ai:'Asistente IA',
    page_positions:'Mis Posiciones',page_strategies:'Gestor de estrategias',page_backtest:'Backtest',page_account:'Mi Cuenta',
    page_copy:'Copy Trading',page_autoopen:'Apertura Auto',
    total_asset:'Activos totales',daily_pnl:'P&L de hoy',win_rate:'Tasa de acierto',active_strategies:'Estrategias activas',pos_count:'Posiciones abiertas',
    card_today:'Hoy',card_month:'Este mes',card_paused:' Pausadas',card_running:' En ejecución',
    card_long:'Long',card_short:'Short',
    quick_order:'+ Orden rápida',
    chart_update:'min actualización',
    market_title:'Mercado en vivo',search_placeholder:'Buscar símbolo...',
    mkt_all:'Todos',mkt_crypto:'Cripto',mkt_forex:'Forex',mkt_metals:'Metales',mkt_energy:'Energía',mkt_index:'Índices',
    tbl_symbol:'Símbolo',tbl_price:'Precio',tbl_change:'Cambio',tbl_volume:'Volumen',tbl_trend:'Tendencia 7d',tbl_action:'Acción',
    ai_title:'Asistente de Trading IA',ai_placeholder:'Escribe un mensaje...',
    ai_welcome:'¡Hola! Soy el asistente QuantAI 🤖\n\nPuedo ayudarte:\n• Datos de mercado en tiempo real y análisis de gráficos\n• Gestionar posiciones y colocar órdenes\n• Analizar rendimiento de estrategias\n• Gestión de riesgos y tamaño de posición\n\n¿Cómo puedo ayudarte?',
    ai_feat1:'Analizar tendencias del mercado y sugerir estrategias',ai_feat2:'Ejecutar órdenes de trading automatizadas',
    ai_feat3:'Calcular tamaño de posición y stops',ai_feat4:'Backtestear el rendimiento de tu estrategia',
    ai_sugg1:'¿Debería comprar BTC ahora?',ai_sugg2:'Crear estrategia grid en oro',
    ai_sugg3:'¿Cómo distribuir $1000?',ai_sugg4:'Análisis de tendencia EUR/USD',ai_sugg5:'Mostrar mis posiciones',
    quick_order_title:'Orden rápida',dir_long:'Compra Long',dir_short:'Venta Short',
    order_symbol:'Símbolo',order_amount:'Monto (USD)',order_sltp:'SL / TP (%)',order_confirm:'Colocar orden',
    sentiment_title:'Sentimiento del mercado',sent_bull:'Alcista',sent_bear:'Bajista',sent_fg:'Miedo y Codicia',sent_greed:'Codicia',sent_flow:'Flujo neto grande',sent_rate:'Tasa de financiación',
    pos_title:'Mis Posiciones',pos_symbol:'Símbolo',pos_size:'Tamaño',pos_open:'Precio entrada',pos_current:'Actual',pos_pnl:'P&L',pos_action:'Acción',
    pos_close:'Cerrar',pos_empty:'Sin posiciones',
    pos_my_title:'Mis Posiciones',pos_active_count:' Posiciones activas',pos_float:'P&L flotante',close_all:'Cerrar todo',
    pos_open_lbl:'Entrada',pos_curr_lbl:'Actual',pos_sl_lbl:'Stop Loss',pos_tp_lbl:'Take Profit',
    pos_ai_analyze:'Análisis IA',pos_edit_btn:'Editar',
    mkt_buy:'Comprar',mkt_sell:'Vender',
    strat_cum_pnl:'P&L total',
    strat_title:'Gestor de estrategias',strat_new:'Nueva estrategia',
    strat_running:'En ejecución',strat_paused:'Pausada',strat_stopped:'Detenida',
    strat_start:'Iniciar',strat_pause:'Pausar',strat_stop:'Detener',strat_edit:'Editar',
    strat_my_title:'Mis Estrategias',strat_running_count:' en ejecución',strat_paused_count:' pausadas',strat_add:'Añadir estrategia',
    bt_title:'Backtest',bt_symbol:'Símbolo',bt_strat_type:'Tipo de estrategia',
    bt_start_date:'Fecha inicio',bt_end_date:'Fecha fin',bt_capital:'Capital inicial (USD)',bt_pos_size:'Tamaño de posición (%)',
    bt_run:'Iniciar backtest',bt_total_return:'Retorno total',bt_annual_return:'Retorno anual',bt_max_dd:'Drawdown máx',
    bt_sharpe:'Ratio de Sharpe',bt_win_rate:'Tasa de acierto',bt_trades:'Total trades',bt_log_title:'Registro de trades (últimos 20)',
    strat_macd:'MACD Tendencia',strat_ema:'EMA Crossover',strat_rsi:'RSI Sobrecompra/sobrevta',strat_grid:'Grid Trading',strat_bb:'Rotura Bollinger',
    acc_title:'Mi Cuenta',acc_plan:'Plan actual',acc_upgrade:'Mejorar',
    acc_broker:'Cuenta de broker',acc_connect:'Conectar broker',
    acc_member_free:'Gratis',acc_member_pro:'Miembro Pro',acc_member_elite:'Miembro Elite',
    acc_valid_until:'Válido hasta',acc_reg_date:'Registrado',acc_total_pnl:'P&L total',
    acc_brokers_count:'Brokers',acc_running_strats:'Estrategias activas',acc_account:'Cuenta',
    acc_broker_section:'Brokers conectados',acc_subscription:'Mi suscripción',
    broker_connected:'Conectado',broker_api_ok:'API OK',broker_not_connected:'No conectado',broker_pending:'Pendiente',broker_add_new:'Añadir broker',
    btn_manage:'Gestionar',btn_disconnect:'Desconectar',btn_connect:'Conectar',btn_edit:'Editar',
    plan_current:'Actual',per_month:'/mes',plan_view_all:'Ver todos los planes →',
    plan_basic_f1:'Todos los datos de mercado',plan_basic_f2:'Q&R IA',plan_basic_f3:'2 estrategias',plan_basic_f4:'Trading auto',
    plan_pro_f1:'Estrategias ilimitadas',plan_pro_f2:'Trading auto IA',plan_pro_f3:'Backtest avanzado',plan_pro_f4:'Multi-broker',
    plan_elite_f1:'Apertura auto (Signal/DCA/Copy)',plan_elite_f2:'Copy trading ilimitado',plan_elite_f3:'Soporte VIP',plan_elite_f4:'Ejecución prioritaria',
    risk_title:'Controles de riesgo',risk_max_loss:'Pérdida máx diaria',risk_max_loss_desc:'Auto-stop si se supera',
    risk_max_pos:'Tamaño máx de posición',risk_max_pos_desc:'Por símbolo, % del total de activos',
    risk_auto_order:'Orden auto IA',risk_auto_order_desc:'IA ejecuta cuando la estrategia se activa',
    risk_notify:'Notificación pre-orden',risk_notify_desc:'Enviar confirmación antes de cada trade',
    risk_night:'Protección nocturna',risk_night_desc:'22:00-07:00 pausar trading auto',
    confirm:'Confirmar',cancel:'Cancelar',save:'Guardar',close:'Cerrar',
    loading:'Cargando...',success:'Éxito',error:'Error',
    lang_switched:'🌐 Cambiado a español',
    tlog_title:'Registro de trades',tlog_all:'Todos',tlog_buy:'Long',tlog_sell:'Short',tlog_win:'Ganancia',tlog_loss:'Pérdida',
    tlog_total_trades:'Trades',tlog_win_rate:'Tasa de acierto',tlog_net_pnl:'P&L neto',tlog_avg_hold:'Promedio retención',tlog_best:'Mejor trade',tlog_worst:'Peor trade',
    tlog_col_time:'Tiempo',tlog_col_symbol:'Símbolo',tlog_col_dir:'Dirección',tlog_col_open:'Entrada',tlog_col_close:'Salida',tlog_col_size:'Lotes',tlog_col_pnl:'P&L',tlog_col_hold:'Duración',
    tlog_dir_long:'Long',tlog_dir_short:'Short',tlog_empty:'Sin registros',
    nav_copy:'Copy Trading',copy_title:'Copy Trading',copy_subtitle:'Sigue a los mejores traders, señales en tiempo real',
    copy_goto_auto:'Configuración apertura auto',copy_my_follows:'Mis Seguimientos',copy_leaderboard:'Clasificación de señales',
    copy_filter_all:'Todos',copy_filter_crypto:'Cripto',copy_filter_forex:'Forex',copy_filter_stable:'DD bajo',
    copy_followers:'seguidores',copy_monthly:'Mensual',copy_winrate:'Tasa de acierto',copy_maxdd:'DD máx',copy_30pnl:'P&L 30d',
    copy_follow_btn:'Seguir',copy_following:'✓ Siguiendo',copy_unfollow:'Dejar de seguir',copy_detail_btn:'Detalles',
    copy_pnl:'P&L flotante',copy_since:'Desde',copy_follow_title:'Ajustes de seguimiento',copy_confirm_follow:'Confirmar',
    copy_toast_follow:'Seguimiento iniciado',copy_toast_unfollow:'Seguimiento cancelado',
    ct_tag_ct1:'Experto BTC/ETH · 3 años',ct_tag_ct2:'Oro/Forex · 5 años',ct_tag_ct3:'Bajo DD estable · 4 años',
    ct_tag_ct4:'Scalper nocturno · 2 años',ct_tag_ct5:'Multi-macro · 6 años',ct_tag_ct6:'DCA+Tendencia · 7 años',
    nav_autoopen:'Apertura Auto',ao_title:'Apertura Auto',ao_subtitle:'3 modos inteligentes de entrada auto',
    ao_lock_title:'Apertura Auto exclusiva de Elite',ao_lock_desc:'Mejora a Elite para desbloquear la entrada automática',
    ao_lock_btn:'Mejorar $199/mes',
    ao_mode_signal:'Disparador de señal',ao_mode_signal_desc:'Entrada auto cuando se cumplen condiciones RSI/MACD/EMA',
    ao_mode_dca:'DCA recurrente',ao_mode_dca_desc:'Compras automáticas periódicas para costo promedio',
    ao_mode_copy:'Sync copy',ao_mode_copy_desc:'Espejar cada entrada de la fuente de señales',
    ao_running:'En ejecución',
    ao_signal_cfg:'Config señal',ao_signal_ind:'Indicador',ao_signal_pair:'Símbolo',
    ao_dca_cfg:'Config DCA',ao_dca_pair:'Símbolo',ao_dca_freq:'Frecuencia',
    ao_dca_hourly:'Cada hora',ao_dca_daily:'Diario',ao_dca_weekly:'Semanal',ao_dca_monthly:'Mensual',
    ao_dca_amount:'Monto por entrada (USD)',ao_dca_total:'Límite total (USD)',ao_dca_price_drop:'Doble si baja (%)',ao_dca_exit:'Take Profit (%)',
    ao_dca_invested:'Invertido',
    ao_copy_cfg:'Config copy',ao_copy_source:'Fuente de señales',ao_copy_select:'Seleccionar',
    ao_copy_ratio:'Ratio',ao_copy_max:'Max por trade (USD)',ao_copy_daily_loss:'Límite pérdida diaria (USD)',
    ao_copy_filter:'Filtro dirección',ao_copy_all:'Long & Short',ao_copy_long_only:'Solo Long',ao_copy_short_only:'Solo Short',
    ao_copy_pairs:'Limitar símbolos',ao_copy_pairs_ph:'BTC,ETH (vacío=todos)',ao_not_following:'No siguiendo',
    ao_pos_size:'Tamaño posición (USD)',ao_sl:'Stop Loss (%)',ao_tp:'Take Profit (%)',ao_max_pos:'Máx posiciones abiertas',
    lb_tab_roi:'ROI mensual',lb_tab_wr:'Tasa de acierto',lb_tab_stable:'Más estable',lb_tab_new:'Nuevos',
    nav_square:'Plaza de trading',sq_title:'Plaza de trading',sq_subtitle:'Comparte tus opiniones, descubre el sentimiento, sincroniza con traders globales',
    sq_post_ph:'Comparte tu visión del mercado, lógica de trading, análisis de posición...',sq_post_btn:'Publicar',
    sq_filter_all:'Todos',sq_filter_bull:'Alcista',sq_filter_bear:'Bajista',sq_filter_hot:'Hot',
    sq_pair_label:'Pareja',sq_sentiment_label:'Sentimiento',
    nav_stratmarket:'Mercado de estrategias',sm_title:'Mercado de estrategias',sm_subtitle:'Descubre, comparte y copia las mejores estrategias cuant',
    sm_upload_title:'Publicar mi estrategia',sm_upload_btn:'Subir estrategia',sm_filter_all:'Todos',
    sm_filter_trend:'Tendencia',sm_filter_grid:'Grid',sm_filter_quant:'Quant',sm_filter_arb:'Arb',
    sm_name_label:'Nombre de estrategia',sm_asset_label:'Símbolo',sm_price_label:'Precio (USD/mes, 0=Gratis)',
    sm_code_label:'Código de estrategia',sm_submit_btn:'Enviar para revisión',sm_backtest:'Backtest',
    sm_copy:'Copiar',sm_subscribe:'Suscribirse',
    nav_signals:'Difusión de señales',sig_title:'Difusión de señales',sig_subtitle:'Señales en vivo, suscripción en un clic, conecta con apertura auto',
    sig_publish_title:'Publicar señal de trading',sig_tab_live:'Señales en vivo',sig_tab_sources:'Fuentes de señales',sig_tab_history:'Historial',
    sig_pair:'Pareja',sig_dir:'Dirección',sig_dir_buy:'Compra',sig_dir_sell:'Venta',
    sig_entry:'Entrada',sig_sl:'Stop Loss',sig_tp1:'TP1',sig_tp2:'TP2',
    sig_desc:'Nota de señal',sig_publish_btn:'Difundir señal',
    sig_follow:'Seguir señal',sig_share:'Compartir',sig_subscribe_bc:'Suscribirse a fuente',
    ao_start:'Iniciar apertura auto',ao_stop:'Detener',ao_status_off:'● Detenido',ao_status_on:'🟢 En ejecución',
    ao_started:'Iniciado',ao_stopped:'Detenido',
    ao_exec_log:'Log de ejecución',ao_clear_log:'Limpiar',ao_log_empty:'Sin registros',
    toast_elite_unlocked:'¡Elite desbloqueado! Apertura auto ahora disponible',
    dash_brief_title:'Briefing diario IA',dash_brief_time:'Actualización 08:00',
    dash_brief_content:'Oro alcista hoy, soutenu par signaux Fed dovish, objectif $2,380. BTC résistance à $84,000, court terme prudent. Nasdaq mené par résultats tech, généralement fort. EUR/USD oscillation faible, USD index 104.2 support.',
    dash_signal_gold:'Oro ▲ Alcista',dash_signal_btc:'BTC ⚠ Observar',dash_signal_eur:'EUR/USD ▼ Débil',dash_signal_nas:'Nasdaq ▲ Fuerte',
    dash_quick_ops:'Acciones rápidas',dash_btn_order:'Orden IA',dash_btn_backtest:'Backtest rápido',dash_btn_positions:'Ver posiciones',
    ai_welcome_greet:'¡Hola! Soy el asistente QuantAI 🧠',ai_welcome_intro:'Cuéntame tus ideas de trading y te ayudaré:',
    modal_symbol:'Símbolo',modal_dir:'Dirección',modal_amount:'Monto (USD)',modal_leverage:'Apalancamiento',
    modal_sl:'Stop Loss (%)',modal_tp:'Take Profit (%)',modal_margin:'Margen estimado',modal_max_profit:'Beneficio máx',modal_max_loss:'Pérdida máx',
    broker_modal_title:'Conectar broker',broker_connect_btn:'Verificar y conectar',
    cat_crypto:'Cripto',cat_forex_metals:'Forex / Metales',cat_all_cfd:'Todos los CFD',
    sym_btc:'Bitcoin',sym_eth:'Ethereum',sym_sol:'Solana',sym_bnb:'BNB',sym_xrp:'Ripple',
    sym_eurusd:'EUR/USD',sym_gbpusd:'GBP/USD',sym_usdjpy:'USD/JPY',sym_usdchf:'USD/CHF',sym_audusd:'AUD/USD',
    sym_gold:'Oro spot',sym_silver:'Plata spot',sym_wti:'WTI Crude',sym_brent:'Brent Crude',
    sym_nas100:'Nasdaq 100',sym_spx500:'S&P 500',sym_dow:'Dow Jones',sym_hsi:'Hang Seng',
    strat_name_1:'BTC MACD Tendencia',strat_name_2:'Grid Oro',strat_name_3:'Estrategia EUR/USD EMA',strat_name_4:'Scalping Nasdaq',
    strat_type_trend:'Seguimiento de tendencia',strat_type_grid:'Grid Trading',strat_type_ema:'EMA Crossover',strat_type_mr:'Reversión a la media',
    toast_order_ok:'¡Ordenplaced!',toast_submitted:'¡Enviado!',toast_pos_closed:'Posición cerrada',toast_all_closed:'Todas las posiciones cerradas',
    toast_strat_started:'iniciada',toast_strat_paused:'pausada',toast_strat_deleted:'Estrategia eliminada',
    toast_broker_connected:'¡Broker conectado! API verificada',toast_coming_soon:'Próximamente',
    toast_upgrading:'Redireccionando a',toast_view_plans:'Ver todos los planes',
    confirm_close_pos:'Confirmar cierre',confirm_close_all:'¿Cerrar todas las posiciones? ¡Irreversible!',confirm_del_strat:'Eliminar estrategia',
    bt_running:'Ejecutando...',
    ai_analyze_suffix:' ¿cómo está mi posición?',
    ai_placeholder:'Ingresa tu instrucción de trading o pregunta…',
    ai_resp_btc:'📊 Análisis BTC/USDT:\n\nPrecio cerca de $83,400, resistencia en $84,000. MACD golden cross, RSI(14) en 58 — alcista pero no sobrecomprado.\n\nSugerencia: Pequeño long cerca del soporte $82,800, stop en $81,000, objetivo $86,000. R/R ≈ 1:2.2.',
    ai_resp_gold:'🥇 Análisis Oro (XAU/USD):\n\nEl oro se mantiene fuerte en $2,342. Señales Fed dovish y dólar débil ofrecen soporte. Objetivo corto plazo $2,380, soporte clave $2,310.\n\nSugerencia: Mantener los longs, mover el stop a $2,320 para asegurar ganancias.',
    ai_resp_position:'📐 Gestión de posición ($1,000 capital):\n\n• BTC/USDT: 30% ($300) — Posición principal, apalancamiento 5x\n• XAU/USD: 25% ($250) — Cobertura, 10x\n• EUR/USD: 20% ($200) — Cobertura FX\n• Efectivo: 25% ($250) — Esperar oportunidades\n\nPérdida máx por trade: 3%.',
    ai_resp_strategy:'⚡ 3 estrategias para el mercado actual:\n\n1. **BTC MACD Tendencia** — 67% de acierto, +89% anualizado\n2. **Grid Oro** — Para mercados laterales, 3-5%/mes\n3. **EUR/USD EMA** — Bajo riesgo, ideal para principiantes\n\n¿Quiere activar una?',
    ai_resp_default:'He entendido tu solicitud. Déjame analizar las condiciones actuales del mercado...\n\n📊 El mercado es generalmente alcista, pero cuidado con los riesgos de política Fed. Mantén las posiciones bajo 50% y siempre establece stops.\n\n¿Hay algún símbolo o estrategia específica que quieras explorar?',
  },

  // 葡萄牙语
  pt: {
    nav_dashboard:'Painel',nav_market:'Mercado',nav_ai:'Chat IA',
    nav_positions:'Posições',nav_strategies:'Estratégias',nav_backtest:'Backtest',nav_account:'Conta',
    page_dashboard:'Painel',page_market:'Mercado',page_ai:'Assistente IA',
    page_positions:'Minhas Posições',page_strategies:'Gerenciador de Estratégias',page_backtest:'Backtest',page_account:'Minha Conta',
    page_copy:'Copy Trading',page_autoopen:'Abertura Auto',
    total_asset:'Ativos Totais',daily_pnl:'P&L do Dia',win_rate:'Taxa de Acerto',active_strategies:'Estratégias Ativas',pos_count:'Posições Abertas',
    card_today:'Hoje',card_month:'Este Mês',card_paused:' Pausadas',card_running:' Em Execução',
    card_long:'Long',card_short:'Short',
    quick_order:'+ Ordem Rápida',
    chart_update:'min atualização',
    market_title:'Mercado ao Vivo',search_placeholder:'Buscar símbolo...',
    mkt_all:'Todos',mkt_crypto:'Cripto',mkt_forex:'Forex',mkt_metals:'Metais',mkt_energy:'Energia',mkt_index:'Índices',
    tbl_symbol:'Símbolo',tbl_price:'Preço',tbl_change:'Variação',tbl_volume:'Volume',tbl_trend:'Tendência 7d',tbl_action:'Ação',
    ai_title:'Assistente de Trading IA',ai_placeholder:'Digite uma mensagem...',
    ai_welcome:'Olá! Sou o assistente QuantAI 🤖\n\nPosso ajudá-lo:\n• Dados de mercado em tempo real e análise de gráficos\n• Gerenciar posições e colocar ordens\n• Analisar desempenho de estratégias\n• Gerenciamento de risco e tamanho de posição\n\nComo posso ajudá-lo?',
    ai_feat1:'Analisar tendências do mercado e sugerir estratégias',ai_feat2:'Executar ordens de trading automatizadas',
    ai_feat3:'Calcular tamanho de posição e stops',ai_feat4:'Testar o desempenho da sua estratégia',
    ai_sugg1:'Devo comprar BTC agora?',ai_sugg2:'Criar estratégia grid no ouro',
    ai_sugg3:'Como alocar $1000?',ai_sugg4:'Análise de tendência EUR/USD',ai_sugg5:'Mostrar minhas posições',
    quick_order_title:'Ordem Rápida',dir_long:'Compra Long',dir_short:'Venda Short',
    order_symbol:'Símbolo',order_amount:'Valor (USD)',order_sltp:'SL / TP (%)',order_confirm:'Colocar ordem',
    sentiment_title:'Sentimento do Mercado',sent_bull:'Altista',sent_bear:'Baixista',sent_fg:'Medo e Ganância',sent_greed:'Ganância',sent_flow:'Fluxo líquido grande',sent_rate:'Taxa de financiamento',
    pos_title:'Minhas Posições',pos_symbol:'Símbolo',pos_size:'Tamanho',pos_open:'Preço entrada',pos_current:'Atual',pos_pnl:'P&L',pos_action:'Ação',
    pos_close:'Fechar',pos_empty:'Sem posições',
    pos_my_title:'Minhas Posições',pos_active_count:' Posições ativas',pos_float:'P&L flutuante',close_all:'Fechar tudo',
    pos_open_lbl:'Entrada',pos_curr_lbl:'Atual',pos_sl_lbl:'Stop Loss',pos_tp_lbl:'Take Profit',
    pos_ai_analyze:'Análise IA',pos_edit_btn:'Editar',
    mkt_buy:'Comprar',mkt_sell:'Vender',
    strat_cum_pnl:'P&L total',
    strat_title:'Gerenciador de Estratégias',strat_new:'Nova estratégia',
    strat_running:'Em Execução',strat_paused:'Pausada',strat_stopped:'Parada',
    strat_start:'Iniciar',strat_pause:'Pausar',strat_stop:'Parar',strat_edit:'Editar',
    strat_my_title:'Minhas Estratégias',strat_running_count:' em execução',strat_paused_count:' pausadas',strat_add:'Adicionar estratégia',
    bt_title:'Backtest',bt_symbol:'Símbolo',bt_strat_type:'Tipo de estratégia',
    bt_start_date:'Data início',bt_end_date:'Data fim',bt_capital:'Capital inicial (USD)',bt_pos_size:'Tamanho de posição (%)',
    bt_run:'Iniciar backtest',bt_total_return:'Retorno total',bt_annual_return:'Retorno anual',bt_max_dd:'Drawdown máx',
    bt_sharpe:'Ratio de Sharpe',bt_win_rate:'Taxa de acerto',bt_trades:'Total de trades',bt_log_title:'Registro de trades (últimos 20)',
    strat_macd:'MACD Tendência',strat_ema:'EMA Crossover',strat_rsi:'RSI Sobrecompra/sobrevenda',strat_grid:'Grid Trading',strat_bb:'Rompimento Bollinger',
    acc_title:'Minha Conta',acc_plan:'Plano atual',acc_upgrade:'Atualizar',
    acc_broker:'Conta do broker',acc_connect:'Conectar broker',
    acc_member_free:'Grátis',acc_member_pro:'Membro Pro',acc_member_elite:'Membro Elite',
    acc_valid_until:'Válido até',acc_reg_date:'Registrado',acc_total_pnl:'P&L total',
    acc_brokers_count:'Brokers',acc_running_strats:'Estratégias ativas',acc_account:'Conta',
    acc_broker_section:'Brokers conectados',acc_subscription:'Minha assinatura',
    broker_connected:'Conectado',broker_api_ok:'API OK',broker_not_connected:'Não conectado',broker_pending:'Pendente',broker_add_new:'Adicionar broker',
    btn_manage:'Gerenciar',btn_disconnect:'Desconectar',btn_connect:'Conectar',btn_edit:'Editar',
    plan_current:'Atual',per_month:'/mês',plan_view_all:'Ver todos os planos →',
    plan_basic_f1:'Todos os dados de mercado',plan_basic_f2:'Q&R IA',plan_basic_f3:'2 estratégias',plan_basic_f4:'Trading auto',
    plan_pro_f1:'Estratégias ilimitadas',plan_pro_f2:'Trading auto IA',plan_pro_f3:'Backtest avançado',plan_pro_f4:'Multi-broker',
    plan_elite_f1:'Abertura auto (Signal/DCA/Copy)',plan_elite_f2:'Copy trading ilimitado',plan_elite_f3:'Suporte VIP',plan_elite_f4:'Execução prioritária',
    risk_title:'Controles de risco',risk_max_loss:'Perda máx diária',risk_max_loss_desc:'Auto-stop se exceder',
    risk_max_pos:'Tamanho máx de posição',risk_max_pos_desc:'Por símbolo, % do total de ativos',
    risk_auto_order:'Ordem auto IA',risk_auto_order_desc:'IA executa quando a estratégia é ativada',
    risk_notify:'Notificação pré-ordem',risk_notify_desc:'Enviar confirmação antes de cada trade',
    risk_night:'Proteção noturna',risk_night_desc:'22:00-07:00 pausar trading auto',
    confirm:'Confirmar',cancel:'Cancelar',save:'Salvar',close:'Fechar',
    loading:'Carregando...',success:'Sucesso',error:'Erro',
    lang_switched:'🌐 Mudado para Português',
    tlog_title:'Registro de trades',tlog_all:'Todos',tlog_buy:'Long',tlog_sell:'Short',tlog_win:'Lucro',tlog_loss:'Perda',
    tlog_total_trades:'Trades',tlog_win_rate:'Taxa de acerto',tlog_net_pnl:'P&L líquido',tlog_avg_hold:'Média retenção',tlog_best:'Melhor trade',tlog_worst:'Pior trade',
    tlog_col_time:'Tempo',tlog_col_symbol:'Símbolo',tlog_col_dir:'Direção',tlog_col_open:'Entrada',tlog_col_close:'Saída',tlog_col_size:'Lotes',tlog_col_pnl:'P&L',tlog_col_hold:'Duração',
    tlog_dir_long:'Long',tlog_dir_short:'Short',tlog_empty:'Sem registros',
    nav_copy:'Copy Trading',copy_title:'Copy Trading',copy_subtitle:'Siga os melhores traders, sinais em tempo real',
    copy_goto_auto:'Configuração abertura auto',copy_my_follows:'Meus Seguidores',copy_leaderboard:'Classificação de sinais',
    copy_filter_all:'Todos',copy_filter_crypto:'Cripto',copy_filter_forex:'Forex',copy_filter_stable:'DD baixo',
    copy_followers:'seguidores',copy_monthly:'Mensal',copy_winrate:'Taxa de acerto',copy_maxdd:'DD máx',copy_30pnl:'P&L 30d',
    copy_follow_btn:'Seguir',copy_following:'✓ Seguindo',copy_unfollow:'Deixar de seguir',copy_detail_btn:'Detalhes',
    copy_pnl:'P&L flutuante',copy_since:'Desde',copy_follow_title:'Ajustes de acompanhamento',copy_confirm_follow:'Confirmar',
    copy_toast_follow:'Acompanhamento iniciado',copy_toast_unfollow:'Acompanhamento cancelado',
    ct_tag_ct1:'Especialista BTC/ETH · 3 anos',ct_tag_ct2:'Oro/Forex · 5 anos',ct_tag_ct3:'DD baixo estável · 4 anos',
    ct_tag_ct4:'Scalper noturno · 2 anos',ct_tag_ct5:'Multi-macro · 6 anos',ct_tag_ct6:'DCA+Tendência · 7 anos',
    nav_autoopen:'Abertura Auto',ao_title:'Abertura Auto',ao_subtitle:'3 modos inteligentes de entrada auto',
    ao_lock_title:'Abertura Auto exclusiva do Elite',ao_lock_desc:'Atualize para Elite para desbloquear a entrada automática',
    ao_lock_btn:'Atualizar $199/mês',
    ao_mode_signal:'Disparador de sinal',ao_mode_signal_desc:'Entrada auto quando condições RSI/MACD/EMA forem cumpridas',
    ao_mode_dca:'DCA recorrente',ao_mode_dca_desc:'Compras automáticas periódicas para custo médio',
    ao_mode_copy:'Sync copy',ao_mode_copy_desc:'Espelhar cada entrada da fonte de sinais',
    ao_running:'Em execução',
    ao_signal_cfg:'Config sinal',ao_signal_ind:'Indicador',ao_signal_pair:'Símbolo',
    ao_dca_cfg:'Config DCA',ao_dca_pair:'Símbolo',ao_dca_freq:'Frequência',
    ao_dca_hourly:'A cada hora',ao_dca_daily:'Diário',ao_dca_weekly:'Semanal',ao_dca_monthly:'Mensal',
    ao_dca_amount:'Valor por entrada (USD)',ao_dca_total:'Limite total (USD)',ao_dca_price_drop:'Dobrar se cair (%)',ao_dca_exit:'Take Profit (%)',
    ao_dca_invested:'Investido',
    ao_copy_cfg:'Config copy',ao_copy_source:'Fonte de sinais',ao_copy_select:'Selecionar',
    ao_copy_ratio:'Ratio',ao_copy_max:'Max por trade (USD)',ao_copy_daily_loss:'Limite perda diária (USD)',
    ao_copy_filter:'Filtro direção',ao_copy_all:'Long & Short',ao_copy_long_only:'Só Long',ao_copy_short_only:'Só Short',
    ao_copy_pairs:'Limitar símbolos',ao_copy_pairs_ph:'BTC,ETH (vazio=todos)',ao_not_following:'Não seguindo',
    ao_pos_size:'Tamanho posição (USD)',ao_sl:'Stop Loss (%)',ao_tp:'Take Profit (%)',ao_max_pos:'Máx posições abertas',
    lb_tab_roi:'ROI mensal',lb_tab_wr:'Taxa de acerto',lb_tab_stable:'Mais estável',lb_tab_new:'Novatos',
    nav_square:'Plaza de trading',sq_title:'Plaza de trading',sq_subtitle:'Compartilhe suas opiniões, descubra o sentimento, sincronize com traders globais',
    sq_post_ph:'Compartilhe sua visão do mercado, lógica de trading, análise de posição...',sq_post_btn:'Publicar',
    sq_filter_all:'Todos',sq_filter_bull:'Altista',sq_filter_bear:'Baixista',sq_filter_hot:'Quente',
    sq_pair_label:'Par',sq_sentiment_label:'Sentimento',
    nav_stratmarket:'Mercado de estratégias',sm_title:'Mercado de estratégias',sm_subtitle:'Descubra, compartilhe e copie as melhores estratégias quant',
    sm_upload_title:'Publicar minha estratégia',sm_upload_btn:'Enviar estratégia',sm_filter_all:'Todos',
    sm_filter_trend:'Tendência',sm_filter_grid:'Grid',sm_filter_quant:'Quant',sm_filter_arb:'Arb',
    sm_name_label:'Nome da estratégia',sm_asset_label:'Símbolo',sm_price_label:'Preço (USD/mês, 0=Grátis)',
    sm_code_label:'Código da estratégia',sm_submit_btn:'Enviar para revisão',sm_backtest:'Backtest',
    sm_copy:'Copiar',sm_subscribe:'Assinar',
    nav_signals:'Broadcast de sinais',sig_title:'Broadcast de sinais',sig_subtitle:'Sinais ao vivo, assinatura em um clique, conecte com abertura auto',
    sig_publish_title:'Publicar sinal de trading',sig_tab_live:'Sinais ao vivo',sig_tab_sources:'Fontes de sinais',sig_tab_history:'Histórico',
    sig_pair:'Par',sig_dir:'Direção',sig_dir_buy:'Compra',sig_dir_sell:'Venda',
    sig_entry:'Entrada',sig_sl:'Stop Loss',sig_tp1:'TP1',sig_tp2:'TP2',
    sig_desc:'Nota do sinal',sig_publish_btn:'Broadcast sinal',
    sig_follow:'Seguir sinal',sig_share:'Compartilhar',sig_subscribe_bc:'Assinar fonte',
    ao_start:'Iniciar abertura auto',ao_stop:'Parar',ao_status_off:'● Parado',ao_status_on:'🟢 Em execução',
    ao_started:'Iniciado',ao_stopped:'Parado',
    ao_exec_log:'Log de execução',ao_clear_log:'Limpar',ao_log_empty:'Sem registros',
    toast_elite_unlocked:'Elite desbloqueado! Abertura auto agora disponível',
    dash_brief_title:'Briefing diário IA',dash_brief_time:'Atualização 08:00',
    dash_brief_content:'Ouro altista hoje, apoiado por sinais Fed dovish, alvo $2,380. BTC resistência em $84,000, curto prazo cauteloso. Nasdaq impulsionado por resultados de tech, geralmente forte. EUR/USD oscilação fraca, USD índice 104.2 suporte.',
    dash_signal_gold:'Oro ▲ Altista',dash_signal_btc:'BTC ⚠ Observar',dash_signal_eur:'EUR/USD ▼ Fraco',dash_signal_nas:'Nasdaq ▲ Forte',
    dash_quick_ops:'Ações rápidas',dash_btn_order:'Ordem IA',dash_btn_backtest:'Backtest rápido',dash_btn_positions:'Ver posições',
    ai_welcome_greet:'Olá! Sou o assistente QuantAI 🧠',ai_welcome_intro:'Conte-me suas ideias de trading e eu ajudarei:',
    modal_symbol:'Símbolo',modal_dir:'Direção',modal_amount:'Valor (USD)',modal_leverage:'Alavancagem',
    modal_sl:'Stop Loss (%)',modal_tp:'Take Profit (%)',modal_margin:'Margem estimada',modal_max_profit:'Lucro máx',modal_max_loss:'Perda máx',
    broker_modal_title:'Conectar broker',broker_connect_btn:'Verificar e conectar',
    cat_crypto:'Cripto',cat_forex_metals:'Forex / Metais',cat_all_cfd:'Todos os CFD',
    sym_btc:'Bitcoin',sym_eth:'Ethereum',sym_sol:'Solana',sym_bnb:'BNB',sym_xrp:'Ripple',
    sym_eurusd:'EUR/USD',sym_gbpusd:'GBP/USD',sym_usdjpy:'USD/JPY',sym_usdchf:'USD/CHF',sym_audusd:'AUD/USD',
    sym_gold:'Ouro spot',sym_silver:'Prata spot',sym_wti:'WTI Crude',sym_brent:'Brent Crude',
    sym_nas100:'Nasdaq 100',sym_spx500:'S&P 500',sym_dow:'Dow Jones',sym_hsi:'Hang Seng',
    strat_name_1:'BTC MACD Tendência',strat_name_2:'Grid Ouro',strat_name_3:'Estratégia EUR/USD EMA',strat_name_4:'Scalping Nasdaq',
    strat_type_trend:'Seguimento de tendência',strat_type_grid:'Grid Trading',strat_type_ema:'EMA Crossover',strat_type_mr:'Reversão à média',
    toast_order_ok:'Ordem Placement!',toast_submitted:'Enviado!',toast_pos_closed:'Posição fechada',toast_all_closed:'Todas as posições fechadas',
    toast_strat_started:'iniciada',toast_strat_paused:'pausada',toast_strat_deleted:'Estratégia excluída',
    toast_broker_connected:'Broker conectado! API verificada',toast_coming_soon:'Em breve',
    toast_upgrading:'Redirecionando para',toast_view_plans:'Ver todos os planos',
    confirm_close_pos:'Confirmar fechamento',confirm_close_all:'Fechar todas as posições? Irreversível!',confirm_del_strat:'Excluir estratégia',
    bt_running:'Executando...',
    ai_analyze_suffix:' como está minha posição?',
    ai_placeholder:'Digite sua instrução de trading ou pergunta…',
    ai_resp_btc:'📊 Análise BTC/USDT:\n\nPreço próximo a $83,400, resistência em $84,000. MACD golden cross, RSI(14) em 58 — altista mas não sobrecomprado.\n\nSugestão: Pequeno long próximo ao suporte $82,800, stop em $81,000, alvo $86,000. R/R ≈ 1:2.2.',
    ai_resp_gold:'🥇 Análise Ouro (XAU/USD):\n\nO ouro se mantém forte em $2,342. Sinais Fed dovish e dólar fraco oferecem suporte. Alvo curto prazo $2,380, suporte chave $2,310.\n\nSugestão: Manter os longs, mover o stop para $2,320 para asegurar ganhos.',
    ai_resp_position:'📐 Gestão de posição ($1.000 capital):\n\n• BTC/USDT: 30% ($300) — Posição principal, alavancagem 5x\n• XAU/USD: 25% ($250) — Hedge, 10x\n• EUR/USD: 20% ($200) — Hedge FX\n• Dinheiro: 25% ($250) — Esperar oportunidades\n\nPerda máx por trade: 3%.',
    ai_resp_strategy:'⚡ 3 estratégias para o mercado atual:\n\n1. **BTC MACD Tendência** — 67% de acerto, +89% anualizado\n2. **Grid Ouro** — Para mercados laterais, 3-5%/mês\n3. **EUR/USD EMA** — Baixo risco, ideal para iniciantes\n\nQuer ativar uma?',
    ai_resp_default:'Entendi sua solicitação. Deixe-me analisar as condições atuais do mercado...\n\n📊 O mercado é geralmente altista, mas cuidado com riscos de política Fed. Mantenha as posições abaixo de 50% e sempre defina stops.\n\nHá algum símbolo ou estratégia específica que você quer explorar?',
  },

  // 印地语
  hi: {
    nav_dashboard:'डैशबोर्ड',nav_market:'बाज़ार',nav_ai:'चैट AI',
    nav_positions:'पोज़िशन',nav_strategies:'रणनीतियाँ',nav_backtest:'बैकटेस्ट',nav_account:'खाता',
    page_dashboard:'डैशबोर्ड',page_market:'बाज़ार',page_ai:'AI सहायक',
    page_positions:'मेरी पोज़िशन',page_strategies:'रणनीति प्रबंधक',page_backtest:'बैकटेस्ट',page_account:'मेरा खाता',
    page_copy:'कॉपी ट्रेडिंग',page_autoopen:'ऑटो ओपन',
    total_asset:'कुल संपत्ति',daily_pnl:'आज का P&L',win_rate:'जीत दर',active_strategies:'सक्रिय रणनीतियाँ',pos_count:'खुली पोज़िशन',
    card_today:'आज',card_month:'इस महीने',card_paused:' रुकी',card_running:' चल रही',
    card_long:'लॉन्ग',card_short:'शॉर्ट',
    quick_order:'+ त्वरित ऑर्डर',
    chart_update:'मिनट अपडेट',
    market_title:'लाइव बाज़ार',search_placeholder:'सिंबल खोजें...',
    mkt_all:'सभी',mkt_crypto:'क्रिप्टो',mkt_forex:'फॉरेक्स',mkt_metals:'धातुएँ',mkt_energy:'ऊर्जा',mkt_index:'इंडेक्स',
    tbl_symbol:'सिंबल',tbl_price:'कीमत',tbl_change:'बदलाव',tbl_volume:'वॉल्यूम',tbl_trend:'7D ट्रेंड',tbl_action:'कार्रवाई',
    ai_title:'AI ट्रेडिंग सहायक',ai_placeholder:'संदेश लिखें...',
    ai_welcome:'नमस्ते! मैं QuantAI सहायक हूँ 🤖\n\nमैं आपकी मदद कर सकता हूँ:\n• रियल-टाइम मार्केट डेटा और चार्ट विश्लेषण\n• पोज़िशन और ऑर्डर प्रबंधित करना\n• रणनीति प्रदर्शन का विश्लेषण\n• जोखिम प्रबंधन और पोज़िशन साइज़\n\nमैं आपकी कैसे मदद कर सकता हूँ?',
    ai_feat1:'मार्केट ट्रेंड विश्लेषण और रणनीति सुझाव',ai_feat2:'स्वचालित ट्रेड निष्पादन',
    ai_feat3:'पोज़िशन साइज़ और स्टॉप्स की गणना',ai_feat4:'आपकी रणनीति का बैकटेस्ट करना',
    ai_sugg1:'क्या मुझे BTC खरीदना चाहिए?',ai_sugg2:'गोल्ड ग्रिड रणनीति बनाएं',
    ai_sugg3:'$1000 कैसे आवंटित करें?',ai_sugg4:'EUR/USD ट्रेंड विश्लेषण',ai_sugg5:'मेरी पोज़िशन दिखाएं',
    quick_order_title:'त्वरित ऑर्डर',dir_long:'लॉन्ग खरीदें',dir_short:'शॉर्ट बेचें',
    order_symbol:'सिंबल',order_amount:'राशि (USD)',order_sltp:'SL / TP (%)',order_confirm:'ऑर्डर प्लेस करें',
    sentiment_title:'मार्केट सेंटिमेंट',sent_bull:'बुलिश',sent_bear:'बेयरिश',sent_fg:'डर और लालच',sent_greed:'लालच',sent_flow:'बड़ा नेट फ्लो',sent_rate:'फंडिंग दर',
    pos_title:'मेरी पोज़िशन',pos_symbol:'सिंबल',pos_size:'साइज़',pos_open:'एंट्री',pos_current:'वर्तमान',pos_pnl:'P&L',pos_action:'कार्रवाई',
    pos_close:'बंद करें',pos_empty:'कोई पोज़िशन नहीं',
    pos_my_title:'मेरी पोज़िशन',pos_active_count:' सक्रिय',pos_float:'फ्लोटिंग P&L',close_all:'सभी बंद करें',
    pos_open_lbl:'एंट्री',pos_curr_lbl:'वर्तमान',pos_sl_lbl:'स्टॉप लॉस',pos_tp_lbl:'टेक प्रॉफिट',
    pos_ai_analyze:'AI विश्लेषण',pos_edit_btn:'संपादित करें',
    mkt_buy:'खरीदें',mkt_sell:'बेचें',
    strat_cum_pnl:'कुल P&L',
    strat_title:'रणनीति प्रबंधक',strat_new:'नई रणनीति',
    strat_running:'चल रही',strat_paused:'रुकी',strat_stopped:'रुकी हुई',
    strat_start:'शुरू',strat_pause:'रोकें',strat_stop:'बंद',strat_edit:'संपादित करें',
    strat_my_title:'मेरी रणनीतियाँ',strat_running_count:' चल रही',strat_paused_count:' रुकी',strat_add:'रणनीति जोड़ें',
    bt_title:'बैकटेस्ट',bt_symbol:'सिंबल',bt_strat_type:'रणनीति प्रकार',
    bt_start_date:'प्रारंभ तिथि',bt_end_date:'समाप्ति तिथि',bt_capital:'प्रारंभिक पूँजी (USD)',bt_pos_size:'पोज़िशन साइज़ (%)',
    bt_run:'बैकटेस्ट शुरू करें',bt_total_return:'कुल रिटर्न',bt_annual_return:'वार्षिक रिटर्न',bt_max_dd:'अधिकतम ड्रॉडाउन',
    bt_sharpe:'शार्प अनुपात',bt_win_rate:'जीत दर',bt_trades:'कुल ट्रेड',bt_log_title:'ट्रेड लॉग (पिछले 20)',
    strat_macd:'MACD ट्रेंड फॉलो',strat_ema:'EMA क्रॉसओवर',strat_rsi:'RSI ओवरबॉट/ओवरसोल्ड',strat_grid:'ग्रिड ट्रेडिंग',strat_bb:'बोलिंगर ब्रेकआउट',
    acc_title:'मेरा खाता',acc_plan:'वर्तमान योजना',acc_upgrade:'अपग्रेड',
    acc_broker:'ब्रोकर खाता',acc_connect:'ब्रोकर कनेक्ट करें',
    acc_member_free:'मुफ्त',acc_member_pro:'प्रो सदस्य',acc_member_elite:'एलीट सदस्य',
    acc_valid_until:'तक वैध',acc_reg_date:'पंजीकृत',acc_total_pnl:'कुल P&L',
    acc_brokers_count:'ब्रोकर',acc_running_strats:'सक्रिय रणनीतियाँ',acc_account:'खाता',
    acc_broker_section:'कनेक्टेड ब्रोकर',acc_subscription:'मेरी सदस्यता',
    broker_connected:'कनेक्टेड',broker_api_ok:'API ठीक',broker_not_connected:'कनेक्ट नहीं',broker_pending:'लंबित',broker_add_new:'ब्रोकर जोड़ें',
    btn_manage:'प्रबंधित करें',btn_disconnect:'डिस्कनेक्ट',btn_connect:'कनेक्ट',btn_edit:'संपादित करें',
    plan_current:'वर्तमान',per_month:'/माह',plan_view_all:'सभी योजनाएँ देखें →',
    plan_basic_f1:'सभी मार्केट डेटा',plan_basic_f2:'AI Q&A',plan_basic_f3:'2 रणनीतियाँ',plan_basic_f4:'ऑटो ट्रेडिंग',
    plan_pro_f1:'असीमित रणनीतियाँ',plan_pro_f2:'AI ऑटो ट्रेडिंग',plan_pro_f3:'एडवांस्ड बैकटेस्ट',plan_pro_f4:'मल्टी-ब्रोकर',
    plan_elite_f1:'ऑटो ओपन (Signal/DCA/Copy)',plan_elite_f2:'असीमित कॉपी ट्रेडिंग',plan_elite_f3:'VIP सपोर्ट',plan_elite_f4:'प्राथमिकता निष्पादन',
    risk_title:'जोखिम नियंत्रण',risk_max_loss:'दैनिक अधिकतम हानि',risk_max_loss_desc:'सीमा पार करने पर ऑटो-स्टॉप',
    risk_max_pos:'अधिकतम पोज़िशन साइज़',risk_max_pos_desc:'प्रति सिंबल, कुल संपत्ति का %',
    risk_auto_order:'AI ऑटो ऑर्डर',risk_auto_order_desc:'रणनीति ट्रिगर होने पर AI निष्पादित करे',
    risk_notify:'पूर्व-ऑर्डर सूचना',risk_notify_desc:'प्रत्येक ट्रेड से पहले पुष्टि भेजें',
    risk_night:'रात्रि सुरक्षा',risk_night_desc:'22:00-07:00 ऑटो ट्रेडिंग रोकें',
    confirm:'पुष्टि करें',cancel:'रद्द करें',save:'सहेजें',close:'बंद करें',
    loading:'लोड हो रहा है...',success:'सफल',error:'त्रुटि',
    lang_switched:'🌐 हिंदी में बदल गया',
    tlog_title:'ट्रेड लॉग',tlog_all:'सभी',tlog_buy:'लॉन्ग',tlog_sell:'शॉर्ट',tlog_win:'लाभ',tlog_loss:'हानि',
    tlog_total_trades:'ट्रेड',tlog_win_rate:'जीत दर',tlog_net_pnl:'शुद्ध P&L',tlog_avg_hold:'औसत होल्ड',tlog_best:'सर्वश्रेष्ठ ट्रेड',tlog_worst:'सर्वाधिक खराब ट्रेड',
    tlog_col_time:'समय',tlog_col_symbol:'सिंबल',tlog_col_dir:'दिशा',tlog_col_open:'एंट्री',tlog_col_close:'एक्ज़िट',tlog_col_size:'लॉट',tlog_col_pnl:'P&L',tlog_col_hold:'अवधि',
    tlog_dir_long:'लॉन्ग',tlog_dir_short:'शॉर्ट',tlog_empty:'कोई ट्रेड रिकॉर्ड नहीं',
    nav_copy:'कॉपी ट्रेडिंग',copy_title:'कॉपी ट्रेडिंग',copy_subtitle:'शीर्ष व्यापारियों का अनुसरण, रियल-टाइम सिग्नल',
    copy_goto_auto:'ऑटो सेटिंग्स',copy_my_follows:'मेरे फॉलो',copy_leaderboard:'सिग्नल लीडरबोर्ड',
    copy_filter_all:'सभी',copy_filter_crypto:'क्रिप्टो',copy_filter_forex:'फॉरेक्स',copy_filter_stable:'कम DD',
    copy_followers:'फॉलोअर्स',copy_monthly:'मासिक',copy_winrate:'जीत दर',copy_maxdd:'अधिकतम DD',copy_30pnl:'30D P&L',
    copy_follow_btn:'फॉलो करें',copy_following:'✓ फॉलो कर रहे हैं',copy_unfollow:'अनफॉलो',copy_detail_btn:'विवरण',
    copy_pnl:'फ्लोटिंग P&L',copy_since:'से',copy_follow_title:'फॉलो सेटिंग्स',copy_confirm_follow:'पुष्टि करें',
    copy_toast_follow:'फॉलो शुरू',copy_toast_unfollow:'अनफॉलो',
    ct_tag_ct1:'BTC/ETH विशेषज्ञ · 3 वर्ष',ct_tag_ct2:'गोल्ड/फॉरेक्स · 5 वर्ष',ct_tag_ct3:'कम DD स्थिर · 4 वर्ष',
    ct_tag_ct4:'रात्रि स्कैल्पर · 2 वर्ष',ct_tag_ct5:'मैक्रो मल्टी · 6 वर्ष',ct_tag_ct6:'DCA+ट्रेंड · 7 वर्ष',
    nav_autoopen:'ऑटो ओपन',ao_title:'ऑटो ओपन',ao_subtitle:'3 इंटेलिजेंट ऑटो एंट्री मोड',
    ao_lock_title:'ऑटो ओपन एलीट एक्सक्लूसिव',ao_lock_desc:'ऑटो एंट्री अनलॉक करने के लिए एलीट में अपग्रेड करें',
    ao_lock_btn:'अपग्रेड $199/माह',
    ao_mode_signal:'सिग्नल ट्रिगर',ao_mode_signal_desc:'RSI/MACD/EMA शर्तें पूरी होने पर ऑटो एंट्री',
    ao_mode_dca:'आवर्ती DCA',ao_mode_dca_desc:'औसत लागत के लिए स्वचालित आवधिक खरीद',
    ao_mode_copy:'कॉपी सिंक',ao_mode_copy_desc:'सिग्नल स्रोत की प्रत्येक एंट्री मिरर करें',
    ao_running:'चल रही',
    ao_signal_cfg:'सिग्नल कॉन्फ़िग',ao_signal_ind:'इंडिकेटर',ao_signal_pair:'सिंबल',
    ao_dca_cfg:'DCA कॉन्फ़िग',ao_dca_pair:'सिंबल',ao_dca_freq:'आवृत्ति',
    ao_dca_hourly:'प्रति घंटा',ao_daily:'दैनिक',ao_dca_weekly:'साप्ताहिक',ao_dca_monthly:'मासिक',
    ao_dca_amount:'प्रति एंट्री राशि (USD)',ao_dca_total:'कुल सीमा (USD)',ao_dca_price_drop:'गिरने पर दोगुना (%)',ao_dca_exit:'टेक प्रॉफिट (%)',
    ao_dca_invested:'निवेशित',
    ao_copy_cfg:'कॉपी कॉन्फ़िग',ao_copy_source:'सिग्नल स्रोत',ao_copy_select:'चुनें',
    ao_copy_ratio:'अनुपात',ao_copy_max:'प्रति ट्रेड अधिकतम (USD)',ao_copy_daily_loss:'दैनिक हानि सीमा (USD)',
    ao_copy_filter:'दिशा फ़िल्टर',ao_copy_all:'लॉन्ग और शॉर्ट',ao_copy_long_only:'केवल लॉन्ग',ao_copy_short_only:'केवल शॉर्ट',
    ao_copy_pairs:'सीमित सिंबल',ao_copy_pairs_ph:'BTC,ETH (खाली=सभी)',ao_not_following:'अनुसरण नहीं कर रहे',
    ao_pos_size:'पोज़िशन साइज़ (USD)',ao_sl:'स्टॉप लॉस (%)',ao_tp:'टेक प्रॉफिट (%)',ao_max_pos:'अधिकतम खुली पोज़िशन',
    lb_tab_roi:'मासिक ROI',lb_tab_wr:'जीत दर',lb_tab_stable:'सबसे स्थिर',lb_tab_new:'नए',
    nav_square:'ट्रेडिंग स्क्वायर',sq_title:'ट्रेडिंग स्क्वायर',sq_subtitle:'अपनी राय साझा करें, सेंटिमेंट खोजें, वैश्विक व्यापारियों के साथ सिंक करें',
    sq_post_ph:'अपना मार्केट व्यू, ट्रेडिंग लॉजिक, पोज़िशन विश्लेषण साझा करें...',sq_post_btn:'पोस्ट करें',
    sq_filter_all:'सभी',sq_filter_bull:'बुलिश',sq_filter_bear:'बेयरिश',sq_filter_hot:'हॉट',
    sq_pair_label:'जोड़ी',sq_sentiment_label:'सेंटिमेंट',
    nav_stratmarket:'रणनीति बाज़ार',sm_title:'रणनीति बाज़ार',sm_subtitle:'शीर्ष क्वांट रणनीतियाँ खोजें, साझा करें, कॉपी करें',
    sm_upload_title:'मेरी रणनीति पब्लिश करें',sm_upload_btn:'रणनीति अपलोड करें',sm_filter_all:'सभी',
    sm_filter_trend:'ट्रेंड',sm_filter_grid:'ग्रिड',sm_filter_quant:'क्वांट',sm_filter_arb:'आर्ब',
    sm_name_label:'रणनीति का नाम',sm_asset_label:'सिंबल',sm_price_label:'मूल्य (USD/माह, 0=मुफ्त)',
    sm_code_label:'रणनीति कोड',sm_submit_btn:'समीक्षा के लिए सबमिट करें',sm_backtest:'बैकटेस्ट',
    sm_copy:'कॉपी',sm_subscribe:'सब्सक्राइब',
    nav_signals:'सिग्नल ब्रॉडकास्ट',sig_title:'सिग्नल ब्रॉडकास्ट',sig_subtitle:'लाइव सिग्नल, वन-क्लिक सब्सक्रिप्शन, ऑटो ओपन से कनेक्ट',
    sig_publish_title:'ट्रेडिंग सिग्नल पब्लिश करें',sig_tab_live:'लाइव सिग्नल',sig_tab_sources:'सिग्नल स्रोत',sig_tab_history:'इतिहास',
    sig_pair:'जोड़ी',sig_dir:'दिशा',sig_dir_buy:'खरीदें',sig_dir_sell:'बेचें',
    sig_entry:'एंट्री',sig_sl:'स्टॉप लॉस',sig_tp1:'TP1',sig_tp2:'TP2',
    sig_desc:'सिग्नल नोट',sig_publish_btn:'सिग्नल ब्रॉडकास्ट करें',
    sig_follow:'सिग्नल फॉलो करें',sig_share:'शेयर करें',sig_subscribe_bc:'स्रोत सब्सक्राइब करें',
    ao_start:'ऑटो ओपन शुरू करें',ao_stop:'रोकें',ao_status_off:'● रुका हुआ',ao_status_on:'🟢 चल रहा',
    ao_started:'शुरू हुआ',ao_stopped:'रुका',
    ao_exec_log:'निष्पादन लॉग',ao_clear_log:'साफ़ करें',ao_log_empty:'कोई रिकॉर्ड नहीं',
    toast_elite_unlocked:'एलीट अनलॉ! ऑटो ओपन अब उपलब्ध',
    dash_brief_title:'AI दैनिक ब्रीफिंग',dash_brief_time:'08:00 अपडेट',
    dash_brief_content:'आज गोल्ड बुलिश, Fed dovish सिग्नल से समर्थित, लक्ष्य $2,380। BTC $84,000 पर प्रतिरोध, अल्पकालिक सतर्क। Nasdaq tech परिणामों से प्रेरित, समग्र रूप से मजबूत। EUR/USD कमज़ोर दोलन, USD सूचकांक 104.2 समर्थन।',
    dash_signal_gold:'गोल्ड ▲ बुलिश',dash_signal_btc:'BTC ⚠ निरीक्षण',dash_signal_eur:'EUR/USD ▼ कमज़ोर',dash_signal_nas:'Nasdaq ▲ मजबूत',
    dash_quick_ops:'त्वरित कार्रवाई',dash_btn_order:'AI ऑर्डर',dash_btn_backtest:'त्वरित बैकटेस्ट',dash_btn_positions:'पोज़िशन देखें',
    ai_welcome_greet:'नमस्ते! मैं QuantAI सहायक हूँ 🧠',ai_welcome_intro:'मुझे अपने ट्रेडिंग विचार बताएं और मैं आपकी मदद करूँगा:',
    modal_symbol:'सिंबल',modal_dir:'दिशा',modal_amount:'राशि (USD)',modal_leverage:'लीवरेज',
    modal_sl:'स्टॉप लॉस (%)',modal_tp:'टेक प्रॉफिट (%)',modal_margin:'अनुमानित मार्जिन',modal_max_profit:'अधिकतम लाभ',modal_max_loss:'अधिकतम हानि',
    broker_modal_title:'ब्रोकर कनेक्ट करें',broker_connect_btn:'सत्यापित और कनेक्ट करें',
    cat_crypto:'क्रिप्टो',cat_forex_metals:'फॉरेक्स / धातुएँ',cat_all_cfd:'सभी CFD',
    sym_btc:'बिटकॉइन',sym_eth:'ईथीरियम',sym_sol:'सोलाना',sym_bnb:'BNB',sym_xrp:'रिपल',
    sym_eurusd:'EUR/USD',sym_gbpusd:'GBP/USD',sym_usdjpy:'USD/JPY',sym_usdchf:'USD/CHF',sym_audusd:'AUD/USD',
    sym_gold:'स्पॉट गोल्ड',sym_silver:'स्पॉट सिल्वर',sym_wti:'WTI क्रूड',sym_brent:'ब्रेंट क्रूड',
    sym_nas100:'Nasdaq 100',sym_spx500:'S&P 500',sym_dow:'डाउ जोन्स',sym_hsi:'हैंग सेंग',
    strat_name_1:'BTC MACD ट्रेंड',strat_name_2:'गोल्ड ग्रिड',strat_name_3:'EUR/USD EMA रणनीति',strat_name_4:'Nasdaq स्कैल्पिंग',
    strat_type_trend:'ट्रेंड फॉलो',strat_type_grid:'ग्रिड ट्रेडिंग',strat_type_ema:'EMA क्रॉसओवर',strat_type_mr:'मीन रिवर्जन',
    toast_order_ok:'ऑर्डर प्लेस!',toast_submitted:'सबमिट!',toast_pos_closed:'पोज़िशन बंद',toast_all_closed:'सभी पोज़िशन बंद',
    toast_strat_started:'शुरू',toast_strat_paused:'रुका',toast_strat_deleted:'रणनीति हटाई गई',
    toast_broker_connected:'ब्रोकर कनेक्टेड! API सत्यापित',toast_coming_soon:'जल्द आ रहा है',
    toast_upgrading:'रिडायरेक्ट हो रहा है',toast_view_plans:'सभी योजनाएँ देखें',
    confirm_close_pos:'बंद करने की पुष्टि करें',confirm_close_all:'सभी पोज़िशन बंद करें? यह अपरिवर्तनीय है!',confirm_del_strat:'रणनीति हटाएं',
    bt_running:'चल रहा है...',
    ai_analyze_suffix:' मेरी पोज़िशन कैसी है?',
    ai_placeholder:'अपना ट्रेडिंग निर्देश या प्रश्न लिखें…',
    ai_resp_btc:'📊 BTC/USDT विश्लेषण:\n\nकीमत $83,400 के आसपास, $84,000 पर प्रतिरोध। MACD गोल्डन क्रॉस, RSI(14) 58 पर — बुलिश लेकिन ओवरबॉट नहीं।\n\nसुझाव: $82,800 समर्थन के पास छोटा लॉन्ग, $81,000 पर स्टॉप, $86,000 लक्ष्य। R/R ≈ 1:2.2।',
    ai_resp_gold:'🥇 गोल्ड (XAU/USD) विश्लेषण:\n\nगोल्ड $2,342 पर मजबूत है। Fed dovish सिग्नल और कमज़ोर डॉलर समर्थन दे रहे हैं। अल्पकालिक लक्ष्य $2,380, मुख्य समर्थन $2,310।\n\nसुझाव: लॉन्ग रखें, $2,320 पर स्टॉप ले जाएं।',
    ai_resp_position:'📐 पोज़िशन प्रबंधन ($1,000 पूँजी):\n\n• BTC/USDT: 30% ($300) — मुख्य पोज़िशन, 5x लीवरेज\n• XAU/USD: 25% ($250) — हेज, 10x\n• EUR/USD: 20% ($200) — FX हेज\n• नकद: 25% ($250) — अवसर की प्रतीक्षा\n\nप्रति ट्रेड अधिकतम हानि: 3%।',
    ai_resp_strategy:'⚡ वर्तमान बाज़ार के लिए 3 रणनीतियाँ:\n\n1. **BTC MACD ट्रेंड** — 67% जीत दर, +89% वार्षिक\n2. **गोल्ड ग्रिड** — साइडवेज़ बाज़ार के लिए, 3-5%/माह\n3. **EUR/USD EMA** — कम जोखिम, शुरुआती के लिए उपयुक्त\n\nक्या आप कोई सक्रिय करना चाहते हैं?',
    ai_resp_default:'मैं आपकी अनुरोध समझ गया। वर्तमान बाज़ार स्थितियों का विश्लेषण करने दें...\n\n📊 बाज़ार सामान्य रूप से बुलिश है, लेकिन Fed नीति जोखिमों से सावधान रहें। पोज़िशन 50% से नीचे रखें और हमेशा स्टॉप सेट करें।\n\nक्या कोई विशेष सिंबल या रणनीति है जो आप खोजना चाहते हैं?',
  },

  // 马来语
  ms: {
    nav_dashboard:'Papan pemuka',nav_market:'Pasaran',nav_ai:'Chat AI',
    nav_positions:'Kedudukan',nav_strategies:'Strategi',nav_backtest:'Backtest',nav_account:'Akaun',
    page_dashboard:'Papan pemuka',page_market:'Pasaran',page_ai:'Pembantu AI',
    page_positions:'Kedudukan Saya',page_strategies:'Pengurus Strategi',page_backtest:'Backtest',page_account:'Akaun Saya',
    page_copy:'Copy Trading',page_autoopen:'Buka Auto',
    total_asset:'Jumlah Aset',daily_pnl:'P&L Hari Ini',win_rate:'Kadar Menang',active_strategies:'Strategi Aktif',pos_count:'Kedudukan Terbuka',
    card_today:'Hari Ini',card_month:'Bulan Ini',card_paused:' Berhenti',card_running:' Berjalan',
    card_long:'Long',card_short:'Short',
    quick_order:'+ Pesanan Pantas',
    chart_update:'min kemas kini',
    market_title:'Pasaran Langsung',search_placeholder:'Cari simbol...',
    mkt_all:'Semua',mkt_crypto:'Krypto',mkt_forex:'Forex',mkt_metals:'Logam',mkt_energy:'Tenaga',mkt_index:'Indeks',
    tbl_symbol:'Simbol',tbl_price:'Harga',tbl_change:'Perubahan',tbl_volume:'Volum',tbl_trend:'Trend 7H',tbl_action:'Tindakan',
    ai_title:'Pembantu Trading AI',ai_placeholder:'Mesej...',
    ai_welcome:'Hai! Saya pembantu QuantAI 🤖\n\nSaya boleh membantu:\n• Data pasaran masa nyata & analisis carta\n• Urus kedudukan & pesanan\n• Analisis prestasi strategi\n• Pengurusan risiko & saiz kedudukan\n\nBagaimana saya boleh membantu?',
    ai_feat1:'Analisis trend pasaran & cadangan strategi',ai_feat2:'Laksanakan trades automatik',
    ai_feat3:'Kirakan saiz kedudukan & stops',ai_feat4:'Backtest prestasi strategi anda',
    ai_sugg1:'Patutkah saya beli BTC sekarang?',ai_sugg2:'Cipta strategi grid emas',
    ai_sugg3:'Bagaimana nak agih $1000?',ai_sugg4:'Analisis trend EUR/USD',ai_sugg5:'Tunjuk kedudukan saya',
    quick_order_title:'Pesanan Pantas',dir_long:'Beli Long',dir_short:'Jual Short',
    order_symbol:'Simbol',order_amount:'Amaun (USD)',order_sltp:'SL / TP (%)',order_confirm:'Place pesanan',
    sentiment_title:'Sentimen Pasaran',sent_bull:'Bullish',sent_bear:'Bearish',sent_fg:'Takut & Tamak',sent_greed:'Tamak',sent_flow:'Aliran bersih besar',sent_rate:'Kadar pembiayaan',
    pos_title:'Kedudukan Saya',pos_symbol:'Simbol',pos_size:'Saiz',pos_open:'Entry',pos_current:'Semasa',pos_pnl:'P&L',pos_action:'Tindakan',
    pos_close:'Tutup',pos_empty:'Tiada kedudukan',
    pos_my_title:'Kedudukan Saya',pos_active_count:' Aktif',pos_float:'P&L Terapung',close_all:'Tutup semua',
    pos_open_lbl:'Entry',pos_curr_lbl:'Semasa',pos_sl_lbl:'Stop Loss',pos_tp_lbl:'Take Profit',
    pos_ai_analyze:'Analisis AI',pos_edit_btn:'Edit',
    mkt_buy:'Beli',mkt_sell:'Jual',
    strat_cum_pnl:'P&L Jumlah',
    strat_title:'Pengurus Strategi',strat_new:'Strategi Baru',
    strat_running:'Berjalan',strat_paused:'Berhenti',strat_stopped:'Dijentikan',
    strat_start:'Mula',strat_pause:'Jeda',strat_stop:'Stop',strat_edit:'Edit',
    strat_my_title:'Strategi Saya',strat_running_count:' berjalan',strat_paused_count:' berhenti',strat_add:'Tambah strategi',
    bt_title:'Backtest',bt_symbol:'Simbol',bt_strat_type:'Jenis strategi',
    bt_start_date:'Tarikh mula',bt_end_date:'Tarikh tamat',bt_capital:'Modal awal (USD)',bt_pos_size:'Saiz kedudukan (%)',
    bt_run:'Mula backtest',bt_total_return:'Pulangan jumlah',bt_annual_return:'Pulangan tahunan',bt_max_dd:'Max drawdown',
    bt_sharpe:'Nisbah Sharpe',bt_win_rate:'Kadar menang',bt_trades:'Jumlah trade',bt_log_title:'Log trade (20 terakhir)',
    strat_macd:'MACD Trend',strat_ema:'EMA Crossover',strat_rsi:'RSI Overbought/Oversold',strat_grid:'Grid Trading',strat_bb:'Bollinger Breakout',
    acc_title:'Akaun Saya',acc_plan:'Pelan semasa',acc_upgrade:'Tingkatkan',
    acc_broker:'Akaun broker',acc_connect:'Sambung broker',
    acc_member_free:'Percuma',acc_member_pro:'Ahli Pro',acc_member_elite:'Ahli Elite',
    acc_valid_until:'Valid sehingga',acc_reg_date:'Daftar',acc_total_pnl:'P&L Jumlah',
    acc_brokers_count:'Broker',acc_running_strats:'Strategi aktif',acc_account:'Akaun',
    acc_broker_section:'Broker disambung',acc_subscription:'Langganan saya',
    broker_connected:'Disambung',broker_api_ok:'API OK',broker_not_connected:'Tidak disambung',broker_pending:'Menunggu',broker_add_new:'Tambah broker',
    btn_manage:'Urus',btn_disconnect:'Putus',btn_connect:'Sambung',btn_edit:'Edit',
    plan_current:'Semasa',per_month:'/bln',plan_view_all:'Lihat semua pelan →',
    plan_basic_f1:'Semua data pasaran',plan_basic_f2:'Q&A AI',plan_basic_f3:'2 strategi',plan_basic_f4:'Trading auto',
    plan_pro_f1:'Strategi tidak terhad',plan_pro_f2:'Trading auto AI',plan_pro_f3:'Backtest lanjutan',plan_pro_f4:'Multi-broker',
    plan_elite_f1:'Buka auto (Signal/DCA/Copy)',plan_elite_f2:'Copy trading tidak terhad',plan_elite_f3:' sokongan VIP',plan_elite_f4:'Pelaksanaan keutamaan',
    risk_title:'Kawalan risiko',risk_max_loss:'Kerugian max harian',risk_max_loss_desc:'Auto-stop jika melebihi',
    risk_max_pos:'Saiz kedudukan max',risk_max_pos_desc:'Per simbol, % jumlah aset',
    risk_auto_order:'Pesanan auto AI',risk_auto_order_desc:'AI melaksanakan bila strategi diaktifkan',
    risk_notify:'Notifikasi pra-pesanan',risk_notify_desc:'Hantar pengesahan sebelum setiap trade',
    risk_night:'Perlindungan malam',risk_night_desc:'22:00-07:00 jeda trading auto',
    confirm:'Sahkan',cancel:'Batal',save:'Simpan',close:'Tutup',
    loading:'Memuat...',success:'Berjaya',error:'Ralat',
    lang_switched:'🌐 Bertukar ke Bahasa Melayu',
    tlog_title:'Log trade',tlog_all:'Semua',tlog_buy:'Long',tlog_sell:'Short',tlog_win:'Untung',tlog_loss:'Rugi',
    tlog_total_trades:'Trade',tlog_win_rate:'Kadar menang',tlog_net_pnl:'P&L bersih',tlog_avg_hold:'Purata pegang',tlog_best:'Trade terbaik',tlog_worst:'Trade terburuk',
    tlog_col_time:'Masa',tlog_col_symbol:'Simbol',tlog_col_dir:'Arah',tlog_col_open:'Entry',tlog_col_close:'Exit',tlog_col_size:'Lots',tlog_col_pnl:'P&L',tlog_col_hold:'Tempoh',
    tlog_dir_long:'Long',tlog_dir_short:'Short',tlog_empty:'Tiada rekod trade',
    nav_copy:'Copy Trading',copy_title:'Copy Trading',copy_subtitle:'Ikuti trader terbaik, isyarat masa nyata',
    copy_goto_auto:'Tetapan auto',copy_my_follows:'Pengikut saya',copy_leaderboard:'Papan pemuka isyarat',
    copy_filter_all:'Semua',copy_filter_crypto:'Krypto',copy_filter_forex:'Forex',copy_filter_stable:'DD rendah',
    copy_followers:'pengikut',copy_monthly:'Bulanan',copy_winrate:'Kadar menang',copy_maxdd:'DD max',copy_30pnl:'P&L 30h',
    copy_follow_btn:'Ikuti',copy_following:'✓ Mengikuti',copy_unfollow:'BerhentiFollow',copy_detail_btn:'Detail',
    copy_pnl:'P&L Terapung',copy_since:'Since',copy_follow_title:'Tetapan ikut',copy_confirm_follow:'Sahkan',
    copy_toast_follow:'Mula Follow',copy_toast_unfollow:'Berhenti Follow',
    ct_tag_ct1:'Pakar BTC/ETH · 3thn',ct_tag_ct2:'Emas/Forex · 5thn',ct_tag_ct3:'DD rendah stabil · 4thn',
    ct_tag_ct4:'Scalper malam · 2thn',ct_tag_ct5:'Multi-macro · 6thn',ct_tag_ct6:'DCA+Trend · 7thn',
    nav_autoopen:'Buka Auto',ao_title:'Buka Auto',ao_subtitle:'3 mod entry auto pintar',
    ao_lock_title:'Buka Auto eksklusif Elite',ao_lock_desc:'Tingkatkan ke Elite untuk buka kunci entry auto',
    ao_lock_btn:'Tingkatkan $199/bln',
    ao_mode_signal:'Pencetus isyarat',ao_mode_signal_desc:'Entry auto bila syarat RSI/MACD/EMA dipenuhi',
    ao_mode_dca:'DCA berulang',ao_mode_dca_desc:'Pembelian automatik berkala untuk kos purata',
    ao_mode_copy:'Sync copy',ao_mode_copy_desc:'Mirror setiap entry dari sumber isyarat',
    ao_running:'Berjalan',
    ao_signal_cfg:'Konfig isyarat',ao_signal_ind:'Indicator',ao_signal_pair:'Simbol',
    ao_dca_cfg:'Konfig DCA',ao_dca_pair:'Simbol',ao_dca_freq:'Frekuensi',
    ao_dca_hourly:'Setiap jam',ao_dca_daily:'Harian',ao_dca_weekly:'Mingguan',ao_dca_monthly:'Bulanan',
    ao_dca_amount:'Amaun per entry (USD)',ao_dca_total:'Limit jumlah (USD)',ao_dca_price_drop:'Double jika turun (%)',ao_dca_exit:'Take Profit (%)',
    ao_dca_invested:'Dilabur',
    ao_copy_cfg:'Konfig copy',ao_copy_source:'Sumber isyarat',ao_copy_select:'Pilih',
    ao_copy_ratio:'Ratio',ao_copy_max:'Max per trade (USD)',ao_copy_daily_loss:'Limit kerugian harian (USD)',
    ao_copy_filter:'Filter arah',ao_copy_all:'Long & Short',ao_copy_long_only:'Long saja',ao_copy_short_only:'Short saja',
    ao_copy_pairs:'Limit simbol',ao_copy_pairs_ph:'BTC,ETH (kosong=semua)',ao_not_following:'Tidak Follow',
    ao_pos_size:'Saiz kedudukan (USD)',ao_sl:'Stop Loss (%)',ao_tp:'Take Profit (%)',ao_max_pos:'Max kedudukan terbuka',
    lb_tab_roi:'ROI bulanan',lb_tab_wr:'Kadar menang',lb_tab_stable:'Paling stabil',lb_tab_new:'Baharu',
    nav_square:'Square Trading',sq_title:'Square Trading',sq_subtitle:'Kongsi pandangan, kesan sentiment, sepadan dengan trader global',
    sq_post_ph:'Kongsi pandangan pasaran, logik trading, analisis posisi...',sq_post_btn:'Pos',
    sq_filter_all:'Semua',sq_filter_bull:'Bullish',sq_filter_bear:'Bearish',sq_filter_hot:'Hot',
    sq_pair_label:'Pasangan',sq_sentiment_label:'Sentimen',
    nav_stratmarket:'Pasaran Strategi',sm_title:'Pasaran Strategi',sm_subtitle:'Temui, kongsi & salin strategi kuantitatif terbaik',
    sm_upload_title:'Publish strategi saya',sm_upload_btn:'Upload strategi',sm_filter_all:'Semua',
    sm_filter_trend:'Trend',sm_filter_grid:'Grid',sm_filter_quant:'Kuant',sm_filter_arb:'Arb',
    sm_name_label:'Nama strategi',sm_asset_label:'Simbol',sm_price_label:'Harga (USD/bln, 0= Percuma)',
    sm_code_label:'Kod strategi',sm_submit_btn:'Submit untuk semakan',sm_backtest:'Backtest',
    sm_copy:'Salin',sm_subscribe:'Langgan',
    nav_signals:'Broadcast Isyarat',sig_title:'Broadcast Isyarat',sig_subtitle:'Isyarat trading live, langganan 1 klik, sambung ke buka auto',
    sig_publish_title:'Publish isyarat trading',sig_tab_live:'Isyarat live',sig_tab_sources:'Sumber isyarat',sig_tab_history:'Sejarah',
    sig_pair:'Pasangan',sig_dir:'Arah',sig_dir_buy:'Beli',sig_dir_sell:'Jual',
    sig_entry:'Entry',sig_sl:'Stop Loss',sig_tp1:'TP1',sig_tp2:'TP2',
    sig_desc:'Nota isyarat',sig_publish_btn:'Broadcast isyarat',
    sig_follow:'Follow isyarat',sig_share:'Kongsi',sig_subscribe_bc:'Langgan sumber',
    ao_start:'Mula buka auto',ao_stop:'Stop',ao_status_off:'● Berhenti',ao_status_on:'🟢 Berjalan',
    ao_started:'Dimula',ao_stopped:'Dihentikan',
    ao_exec_log:'Log execution',ao_clear_log:'Clear',ao_log_empty:'Tiada rekod',
    toast_elite_unlocked:'Elite unlocked! Buka auto kini tersedia',
    dash_brief_title:'Briefing harian AI',dash_brief_time:'Update 08:00',
    dash_brief_content:'Emas bullish hari ini, disokong isyarat Fed dovish, sasaran $2,380. BTC menghadapi rintangan di $84,000, jangka pendek berhatihati. Nasdaq digerakkan oleh keputusan tech, secara amnya kuat. EUR/USD lemah, USD index 104.2 sokongan.',
    dash_signal_gold:'Emas ▲ Bullish',dash_signal_btc:'BTC ⚠ Pantau',dash_signal_eur:'EUR/USD ▼ Lemah',dash_signal_nas:'Nasdaq ▲ Kuat',
    dash_quick_ops:'Tindakan pantas',dash_btn_order:'Pesanan AI',dash_btn_backtest:'Backtest pantas',dash_btn_positions:'Lihat posisi',
    ai_welcome_greet:'Hai! Saya pembantu QuantAI 🧠',ai_welcome_intro:'Beritahu saya idea trading anda dan saya akan membantu:',
    modal_symbol:'Simbol',modal_dir:'Arah',modal_amount:'Amaun (USD)',modal_leverage:'Leverage',
    modal_sl:'Stop Loss (%)',modal_tp:'Take Profit (%)',modal_margin:'Margin dijangkakan',modal_max_profit:'Max untung',modal_max_loss:'Max rugi',
    broker_modal_title:'Sambungkan broker',broker_connect_btn:'Verify & sambung',
    cat_crypto:'Kripto',cat_forex_metals:'Forex / Logam',cat_all_cfd:'Semua CFD',
    sym_btc:'Bitcoin',sym_eth:'Ethereum',sym_sol:'Solana',sym_bnb:'BNB',sym_xrp:'Ripple',
    sym_eurusd:'EUR/USD',sym_gbpusd:'GBP/USD',sym_usdjpy:'USD/JPY',sym_usdchf:'USD/CHF',sym_audusd:'AUD/USD',
    sym_gold:'Emas spot',sym_silver:'Perak spot',sym_wti:'WTI Crude',sym_brent:'Brent Crude',
    sym_nas100:'Nasdaq 100',sym_spx500:'S&P 500',sym_dow:'Dow Jones',sym_hsi:'Hang Seng',
    strat_name_1:'BTC MACD Trend',strat_name_2:'Grid Emas',strat_name_3:'Strategi EUR/USD EMA',strat_name_4:'Scalping Nasdaq',
    strat_type_trend:'Trend following',strat_type_grid:'Grid Trading',strat_type_ema:'EMA Crossover',strat_type_mr:'Mean Reversion',
    toast_order_ok:'Pesanan placed!',toast_submitted:'Submitted!',toast_pos_closed:'Posisi ditutup',toast_all_closed:'Semua posisi ditutup',
    toast_strat_started:'dimula',toast_strat_paused:'dijeda',toast_strat_deleted:'strategi dipadam',
    toast_broker_connected:'Broker dishubung! API verified',toast_coming_soon:'Akan datang',
    toast_upgrading:'Redirecting to',toast_view_plans:'Lihat semua pelan',
    confirm_close_pos:'Sahkan menutup',confirm_close_all:'Tutup semua posisi? Tidak boleh undi!',confirm_del_strat:'Padam strategi',
    bt_running:'Berjalan...',
    ai_analyze_suffix:' bagaimana posisi saya?',
    ai_placeholder:'Masukkan arahan trading atau soalan…',
    ai_resp_btc:'📊 Analisis BTC/USDT:\n\nHarga cerca $83,400, rintangan di $84,000. MACD golden cross, RSI(14) pada 58 — bullish tetapi tidak overbought.\n\nCadangan: Long kecil près sokongan $82,800, stop pada $81,000, sasaran $86,000. R/R ≈ 1:2.2.',
    ai_resp_gold:'🥇 Analisis Emas (XAU/USD):\n\nEmas kekal kuat pada $2,342. Isyarat Fed dovish dan dollar lemah menawarkan sokongan. Sasaran jangka pendek $2,380, sokongan kunci $2,310.\n\nCadangan: Tahan long, move stop ke $2,320 untuk securing keuntungan.',
    ai_resp_position:'📐 Pengurusan posisi ($1,000 modal):\n\n• BTC/USDT: 30% ($300) — Posisi utama, leverage 5x\n• XAU/USD: 25% ($250) — Hedge, 10x\n• EUR/USD: 20% ($200) — Hedge FX\n• Tunai: 25% ($250) — Tunggu peluang\n\nMax rugi per trade: 3%.',
    ai_resp_strategy:'⚡ 3 strategi untuk pasaran semasa:\n\n1. **BTC MACD Trend** — 67% kadar menang, +89% tahunan\n2. **Grid Emas** — Untuk pasaran sideways, 3-5%/bln\n3. **EUR/USD EMA** — Risiko rendah, sesuai untuk pemula\n\nNak activate satu?',
    ai_resp_default:'Saya faham permintaan anda. Saya akan analisis keadaan pasaran semasa...\n\n📊 Pasaran secara amnya bullish, tapi perlu berhati-hati dengan risiko dasar Fed. Kekalkan posisi bawah 50% dan sentiasa tetapkan stops.\n\nAda simbol atau strategi spesifik yang anda nak explore?',
  },

  // 印尼语
  id: {
    nav_dashboard:'Dasbor',nav_market:'Pasar',nav_ai:'Chat AI',
    nav_positions:'Posisi',nav_strategies:'Strategi',nav_backtest:'Backtest',nav_account:'Akun',
    page_dashboard:'Dasbor',page_market:'Pasar',page_ai:'Asisten AI',
    page_positions:'Posisi Saya',page_strategies:'Manajer Strategi',page_backtest:'Backtest',page_account:'Akun Saya',
    page_copy:'Copy Trading',page_autoopen:'Buka Otomatis',
    total_asset:'Total Aset',daily_pnl:'P&L Hari Ini',win_rate:'Tingkat Menang',active_strategies:'Strategi Aktif',pos_count:'Posisi Terbuka',
    card_today:'Hari Ini',card_month:'Bulan Ini',card_paused:' Berhenti',card_running:' Berjalan',
    card_long:'Long',card_short:'Short',
    quick_order:'+ Pesanan Cepat',
    chart_update:'min pembaruan',
    market_title:'Pasar Langsung',search_placeholder:'Cari simbol...',
    mkt_all:'Semua',mkt_crypto:'Kripto',mkt_forex:'Forex',mkt_metals:'Logam',mkt_energy:'Energi',mkt_index:'Indeks',
    tbl_symbol:'Simbol',tbl_price:'Harga',tbl_change:'Perubahan',tbl_volume:'Volume',tbl_trend:'Trend 7H',tbl_action:'Tindakan',
    ai_title:'Asisten Trading AI',ai_placeholder:'Masukkan pesan...',
    ai_welcome:'Hai! Saya asisten QuantAI 🤖\n\nSaya bisa membantu:\n• Data pasar real-time & analisis grafik\n• Kelola posisi & pesanan\n• Analisis performa strategi\n• Manajemen risiko & ukuran posisi\n\nBagaimana saya bisa membantu?',
    ai_feat1:'Analisis tren pasar & saran strategi',ai_feat2:'Eksekusi trading otomatis',
    ai_feat3:'Hitung ukuran posisi & stops',ai_feat4:'Backtest performa strategi Anda',
    ai_sugg1:'Haruskah saya beli BTC sekarang?',ai_sugg2:'Buat strategi grid emas',
    ai_sugg3:'Bagaimana alokasikan $1000?',ai_sugg4:'Analisis tren EUR/USD',ai_sugg5:'Tampilkan posisi saya',
    quick_order_title:'Pesanan Cepat',dir_long:'Beli Long',dir_short:'Jual Short',
    order_symbol:'Simbol',order_amount:'Jumlah (USD)',order_sltp:'SL / TP (%)',order_confirm:'Pasang pesanan',
    sentiment_title:'Sentimen Pasar',sent_bull:'Bullish',sent_bear:'Bearish',sent_fg:'Takut & Serakah',sent_greed:'Serakah',sent_flow:'Aliran bersih besar',sent_rate:'Tingkat pendanaan',
    pos_title:'Posisi Saya',pos_symbol:'Simbol',pos_size:'Ukuran',pos_open:'Entry',pos_current:'Saat ini',pos_pnl:'P&L',pos_action:'Tindakan',
    pos_close:'Tutup',pos_empty:'Tidak ada posisi',
    pos_my_title:'Posisi Saya',pos_active_count:' Aktif',pos_float:'P&L Mengambang',close_all:'Tutup semua',
    pos_open_lbl:'Entry',pos_curr_lbl:'Saat ini',pos_sl_lbl:'Stop Loss',pos_tp_lbl:'Take Profit',
    pos_ai_analyze:'Analisis AI',pos_edit_btn:'Edit',
    mkt_buy:'Beli',mkt_sell:'Jual',
    strat_cum_pnl:'P&L Total',
    strat_title:'Manajer Strategi',strat_new:'Strategi Baru',
    strat_running:'Berjalan',strat_paused:'Berhenti',strat_stopped:'Berhenti',
    strat_start:'Mulai',strat_pause:'Jeda',strat_stop:'Stop',strat_edit:'Edit',
    strat_my_title:'Strategi Saya',strat_running_count:' berjalan',strat_paused_count:' berhenti',strat_add:'Tambah strategi',
    bt_title:'Backtest',bt_symbol:'Simbol',bt_strat_type:'Jenis strategi',
    bt_start_date:'Tanggal mulai',bt_end_date:'Tanggal akhir',bt_capital:'Modal awal (USD)',bt_pos_size:'Ukuran posisi (%)',
    bt_run:'Mulai backtest',bt_total_return:'Return total',bt_annual_return:'Return tahunan',bt_max_dd:'Max drawdown',
    bt_sharpe:'Rasio Sharpe',bt_win_rate:'Tingkat menang',bt_trades:'Total trade',bt_log_title:'Log trade (20 terakhir)',
    strat_macd:'MACD Tren',strat_ema:'EMA Crossover',strat_rsi:'RSI Overbought/Oversold',strat_grid:'Grid Trading',strat_bb:'Breakout Bollinger',
    acc_title:'Akun Saya',acc_plan:'Paket saat ini',acc_upgrade:'Upgrade',
    acc_broker:'Akun broker',acc_connect:'Sambungkan broker',
    acc_member_free:'Gratis',acc_member_pro:'anggota Pro',acc_member_elite:'anggota Elite',
    acc_valid_until:'Valid sampai',acc_reg_date:'Terdaftar',acc_total_pnl:'P&L Total',
    acc_brokers_count:'Broker',acc_running_strats:'Strategi aktif',acc_account:'Akun',
    acc_broker_section:'Broker terhubung',acc_subscription:'Langganan saya',
    broker_connected:'Terhubung',broker_api_ok:'API OK',broker_not_connected:'Tidak terhubung',broker_pending:'Menunggu',broker_add_new:'Tambah broker',
    btn_manage:'Kelola',btn_disconnect:'Putus',btn_connect:'Sambungkan',btn_edit:'Edit',
    plan_current:'Saat ini',per_month:'/bln',plan_view_all:'Lihat semua paket →',
    plan_basic_f1:'Semua data pasar',plan_basic_f2:'Q&A AI',plan_basic_f3:'2 strategi',plan_basic_f4:'Trading otomatis',
    plan_pro_f1:'Strategi tak terbatas',plan_pro_f2:'Trading otomatis AI',plan_pro_f3:'Backtest lanjutan',plan_pro_f4:'Multi-broker',
    plan_elite_f1:'Buka otomatis (Signal/DCA/Copy)',plan_elite_f2:'Copy trading tak terbatas',plan_elite_f3:'Dukungan VIP',plan_elite_f4:'Eksekusi prioritas',
    risk_title:'Kontrol risiko',risk_max_loss:'Kerugian max harian',risk_max_loss_desc:'Auto-stop jika melampaui',
    risk_max_pos:'Ukuran posisi max',risk_max_pos_desc:'Per simbol, % total aset',
    risk_auto_order:'Pesanan auto AI',risk_auto_order_desc:'AI eksekusi saat strategi terpicu',
    risk_notify:'Notifikasi pra-pesanan',risk_notify_desc:'Kirim konfirmasi sebelum setiap trade',
    risk_night:'Proteksi malam',risk_night_desc:'22:00-07:00 jeda trading otomatis',
    confirm:'Konfirmasi',cancel:'Batal',save:'Simpan',close:'Tutup',
    loading:'Memuat...',success:'Berhasil',error:'Error',
    lang_switched:'🌐 Berubah ke Bahasa Indonesia',
    tlog_title:'Log Trade',tlog_all:'Semua',tlog_buy:'Long',tlog_sell:'Short',tlog_win:'Profit',tlog_loss:'Kerugian',
    tlog_total_trades:'Trade',tlog_win_rate:'Tingkat menang',tlog_net_pnl:'P&L bersih',tlog_avg_hold:'Rata-rata menahan',tlog_best:'Trade terbaik',tlog_worst:'Trade terburuk',
    tlog_col_time:'Waktu',tlog_col_symbol:'Simbol',tlog_col_dir:'Arah',tlog_col_open:'Entry',tlog_col_close:'Exit',tlog_col_size:'Lot',tlog_col_pnl:'P&L',tlog_col_hold:'Durasi',
    tlog_dir_long:'Long',tlog_dir_short:'Short',tlog_empty:'Tidak ada rekam trade',
    nav_copy:'Copy Trading',copy_title:'Copy Trading',copy_subtitle:'Ikuti trader terbaik, sinyal real-time',
    copy_goto_auto:'Pengaturan auto',copy_my_follows:'Pengikut saya',copy_leaderboard:'Papan peringkat sinyal',
    copy_filter_all:'Semua',copy_filter_crypto:'Kripto',copy_filter_forex:'Forex',copy_filter_stable:'DD rendah',
    copy_followers:'pengikut',copy_monthly:'Bulanan',copy_winrate:'Tingkat menang',copy_maxdd:'DD max',copy_30pnl:'P&L 30h',
    copy_follow_btn:'Ikuti',copy_following:'✓ Mengikuti',copy_unfollow:'BerhentiFollow',copy_detail_btn:'Detail',
    copy_pnl:'P&L Mengambang',copy_since:'Desde',copy_follow_title:'Pengaturan mengikuti',copy_confirm_follow:'Konfirmasi',
    copy_toast_follow:'Mulai mengikuti',copy_toast_unfollow:'BerhentiFollow',
    ct_tag_ct1:'Ahli BTC/ETH · 3thn',ct_tag_ct2:'Emas/Forex · 5thn',ct_tag_ct3:'DD rendah stabil · 4thn',
    ct_tag_ct4:'Scalper malam · 2thn',ct_tag_ct5:'Multi-makro · 6thn',ct_tag_ct6:'DCA+Tren · 7thn',
    nav_autoopen:'Buka Otomatis',ao_title:'Buka Otomatis',ao_subtitle:'3 mode masuk otomatis cerdas',
    ao_lock_title:'Buka Otomatis eksklusif Elite',ao_lock_desc:'Upgrade ke Elite untuk membuka masuk otomatis',
    ao_lock_btn:'Upgrade $199/bln',
    ao_mode_signal:'Pemicu sinyal',ao_mode_signal_desc:'Masuk otomatis saat syarat RSI/MACD/EMA terpenuhi',
    ao_mode_dca:'DCA berulang',ao_mode_dca_desc:'Pembelian otomatis berkala untuk biaya rata-rata',
    ao_mode_copy:'Sync copy',ao_mode_copy_desc:'Cerminkan setiap masuk dari sumber sinyal',
    ao_running:'Berjalan',
    ao_signal_cfg:'Konfig sinyal',ao_signal_ind:'Indikator',ao_signal_pair:'Simbol',
    ao_dca_cfg:'Konfig DCA',ao_dca_pair:'Simbol',ao_dca_freq:'Frekuensi',
    ao_dca_hourly:'Setiap jam',ao_dca_daily:'Harian',ao_dca_weekly:'Mingguan',ao_dca_monthly:'Bulanan',
    ao_dca_amount:'Jumlah per masuk (USD)',ao_dca_total:'Batas total (USD)',ao_dca_price_drop:'Double jika turun (%)',ao_dca_exit:'Take Profit (%)',
    ao_dca_invested:'Diinvestasikan',
    ao_copy_cfg:'Konfig copy',ao_copy_source:'Sumber sinyal',ao_copy_select:'Pilih',
    ao_copy_ratio:'Rasio',ao_copy_max:'Max per trade (USD)',ao_copy_daily_loss:'Batas kerugian harian (USD)',
    ao_copy_filter:'Filter arah',ao_copy_all:'Long & Short',ao_copy_long_only:'Long saja',ao_copy_short_only:'Short saja',
    ao_copy_pairs:'Batasi simbol',ao_copy_pairs_ph:'BTC,ETH (kosong=semua)',ao_not_following:'TidakFollow',
    ao_pos_size:'Ukuran posisi (USD)',ao_sl:'Stop Loss (%)',ao_tp:'Take Profit (%)',ao_max_pos:'Max posisi terbuka',
    lb_tab_roi:'ROI bulanan',lb_tab_wr:'Tingkat menang',lb_tab_stable:'Paling stabil',lb_tab_new:'Baru',
    nav_square:'Pasar Trading',sq_title:'Pasar Trading',sq_subtitle:'Bagikan pandangan, temukan sentimen, sinkronkan dengan trader global',
    sq_post_ph:'Bagikan pandangan pasar, logika trading, analisis posisi...',sq_post_btn:'Posting',
    sq_filter_all:'Semua',sq_filter_bull:'Bullish',sq_filter_bear:'Bearish',sq_filter_hot:'Hot',
    sq_pair_label:'Pasangan',sq_sentiment_label:'Sentimen',
    nav_stratmarket:'Pasar Strategi',sm_title:'Pasar Strategi',sm_subtitle:'Temukan, bagikan & salin strategi kuantitatif terbaik',
    sm_upload_title:'Publikasi strategi saya',sm_upload_btn:'Unggah strategi',sm_filter_all:'Semua',
    sm_filter_trend:'Tren',sm_filter_grid:'Grid',sm_filter_quant:'Kuant',sm_filter_arb:'Arb',
    sm_name_label:'Nama strategi',sm_asset_label:'Simbol',sm_price_label:'Harga (USD/bln, 0=Gratis)',
    sm_code_label:'Kode strategi',sm_submit_btn:'Kirim untuk review',sm_backtest:'Backtest',
    sm_copy:'Salin',sm_subscribe:'Berlangganan',
    nav_signals:'Broadcast Sinyal',sig_title:'Broadcast Sinyal',sig_subtitle:'Sinyal trading live, langganan 1 klik, sambung ke buka otomatis',
    sig_publish_title:'Publikasi sinyal trading',sig_tab_live:'Sinyal live',sig_tab_sources:'Sumber sinyal',sig_tab_history:'Riwayat',
    sig_pair:'Pasangan',sig_dir:'Arah',sig_dir_buy:'Beli',sig_dir_sell:'Jual',
    sig_entry:'Entry',sig_sl:'Stop Loss',sig_tp1:'TP1',sig_tp2:'TP2',
    sig_desc:'Catatan sinyal',sig_publish_btn:'Broadcast sinyal',
    sig_follow:'Ikuti sinyal',sig_share:'Bagikan',sig_subscribe_bc:'Berlangganan sumber',
    ao_start:'Mulai buka otomatis',ao_stop:'Stop',ao_status_off:'● Berhenti',ao_status_on:'🟢 Berjalan',
    ao_started:'Dimulai',ao_stopped:'Dihentikan',
    ao_exec_log:'Log eksekusi',ao_clear_log:'Clear',ao_log_empty:'Tidak ada rekam',
    toast_elite_unlocked:'Elite terbuka! Buka otomatis sekarang tersedia',
    dash_brief_title:'Briefing harian AI',dash_brief_time:'Update 08:00',
    dash_brief_content:'Emas bullish hari ini, didukung sinyal Fed dovish, target $2,380. BTC menghadapi resistensi di $84,000, jangka pendek waspadai. Nasdaq didorong hasil tech, secara umum kuat. EUR/USD lemah berosilasi, USD index 104.2 support.',
    dash_signal_gold:'Emas ▲ Bullish',dash_signal_btc:'BTC ⚠ Pantau',dash_signal_eur:'EUR/USD ▼ Lemah',dash_signal_nas:'Nasdaq ▲ Kuat',
    dash_quick_ops:'Tindakan cepat',dash_btn_order:'Pesanan AI',dash_btn_backtest:'Backtest cepat',dash_btn_positions:'Lihat posisi',
    ai_welcome_greet:'Hai! Saya asisten QuantAI 🧠',ai_welcome_intro:'Ceritakan ide trading Anda dan saya akan membantu:',
    modal_symbol:'Simbol',modal_dir:'Arah',modal_amount:'Jumlah (USD)',modal_leverage:'Leverage',
    modal_sl:'Stop Loss (%)',modal_tp:'Take Profit (%)',modal_margin:'Margin estimasi',modal_max_profit:'Max profit',modal_max_loss:'Max kerugian',
    broker_modal_title:'Sambungkan broker',broker_connect_btn:'Verifikasi & sambungkan',
    cat_crypto:'Kripto',cat_forex_metals:'Forex / Logam',cat_all_cfd:'Semua CFD',
    sym_btc:'Bitcoin',sym_eth:'Ethereum',sym_sol:'Solana',sym_bnb:'BNB',sym_xrp:'Ripple',
    sym_eurusd:'EUR/USD',sym_gbpusd:'GBP/USD',sym_usdjpy:'USD/JPY',sym_usdchf:'USD/CHF',sym_audusd:'AUD/USD',
    sym_gold:'Emas spot',sym_silver:'Perak spot',sym_wti:'WTI Crude',sym_brent:'Brent Crude',
    sym_nas100:'Nasdaq 100',sym_spx500:'S&P 500',sym_dow:'Dow Jones',sym_hsi:'Hang Seng',
    strat_name_1:'BTC MACD Tren',strat_name_2:'Grid Emas',strat_name_3:'Strategi EUR/USD EMA',strat_name_4:'Scalping Nasdaq',
    strat_type_trend:'Tren following',strat_type_grid:'Grid Trading',strat_type_ema:'EMA Crossover',strat_type_mr:'Mean Reversion',
    toast_order_ok:'Pesanan placed!',toast_submitted:'Submitted!',toast_pos_closed:'Posisi ditutup',toast_all_closed:'Semua posisi ditutup',
    toast_strat_started:'dimulai',toast_strat_paused:'dijeda',toast_strat_deleted:'strategi dihapus',
    toast_broker_connected:'Broker terhubung! API terverifikasi',toast_coming_soon:'Segera hadir',
    toast_upgrading:'Mengalihkan ke',toast_view_plans:'Lihat semua paket',
    confirm_close_pos:'Konfirmasi tutup',confirm_close_all:'Tutup semua posisi? Tidak bisa dibatalkan!',confirm_del_strat:'Hapus strategi',
    bt_running:'Berjalan...',
    ai_analyze_suffix:' bagaimana posisi saya?',
    ai_placeholder:'Masukkan instruksi trading atau pertanyaan…',
    ai_resp_btc:'📊 Analisis BTC/USDT:\n\nHarga dekat $83,400, resistensi di $84,000. MACD golden cross, RSI(14) di 58 — bullish tapi tidak overbought.\n\nSaran: Long kecil dekat support $82,800, stop di $81,000, target $86,000. R/R ≈ 1:2.2.',
    ai_resp_gold:'🥇 Analisis Emas (XAU/USD):\n\nEmas tetap kuat di $2,342. Sinyal Fed dovish dan dollar lemah memberi support. Target jangka pendek $2,380, support kunci $2,310.\n\nSaran: Tahan long, pindahkan stop ke $2,320 untuk mengamankan profit.',
    ai_resp_position:'📐 Manajemen posisi ($1,000 modal):\n\n• BTC/USDT: 30% ($300) — Posisi utama, leverage 5x\n• XAU/USD: 25% ($250) — Hedge, 10x\n• EUR/USD: 20% ($200) — Hedge FX\n• Tunai: 25% ($250) — Tunggu peluang\n\nMax kerugian per trade: 3%.',
    ai_resp_strategy:'⚡ 3 strategi untuk pasar saat ini:\n\n1. **BTC MACD Tren** — 67% tingkat menang, +89% tahunan\n2. **Grid Emas** — Untuk pasar sideways, 3-5%/bln\n3. **EUR/USD EMA** — Risiko rendah, cocok untuk pemula\n\nMau aktivasi satu?',
    ai_resp_default:'Saya mengerti permintaan Anda. Mari saya analisis kondisi pasar saat ini...\n\n📊 Pasar secara umum bullish, tapi waspadai risiko kebijakan Fed. Jaga posisi di bawah 50% dan selalu pasang stops.\n\nAda simbol atau strategi spesifik yang ingin Anda eksplorasi?',
  },

  // 越南语
  vi: {
    nav_dashboard:'Bảng điều khiển',nav_market:'Thị trường',nav_ai:'Chat AI',
    nav_positions:'Vị thế',nav_strategies:'Chiến lược',nav_backtest:'Backtest',nav_account:'Tài khoản',
    page_dashboard:'Bảng điều khiển',page_market:'Thị trường',page_ai:'Trợ lý AI',
    page_positions:'Vị thế của tôi',page_strategies:'Quản lý chiến lược',page_backtest:'Backtest',page_account:'Tài khoản của tôi',
    page_copy:'Copy Trading',page_autoopen:'Mở Auto',
    total_asset:'Tổng tài sản',daily_pnl:'P&L hôm nay',win_rate:'Tỷ lệ thắng',active_strategies:'Chiến lược hoạt động',pos_count:'Vị thế mở',
    card_today:'Hôm nay',card_month:'Tháng này',card_paused:' Tạm dừng',card_running:' Đang chạy',
    card_long:'Long',card_short:'Short',
    quick_order:'+ Lệnh nhanh',
    chart_update:'phút cập nhật',
    market_title:'Thị trường trực tiếp',search_placeholder:'Tìm ký hiệu...',
    mkt_all:'Tất cả',mkt_crypto:'Crypto',mkt_forex:'Forex',mkt_metals:'Kim loại',mkt_energy:'Năng lượng',mkt_index:'Chỉ số',
    tbl_symbol:'Ký hiệu',tbl_price:'Giá',tbl_change:'Thay đổi',tbl_volume:'Khối lượng',tbl_trend:'Xu hướng 7 ngày',tbl_action:'Hành động',
    ai_title:'Trợ lý Trading AI',ai_placeholder:'Nhập tin nhắn...',
    ai_welcome:'Xin chào! Tôi là trợ lý QuantAI 🤖\n\nTôi có thể giúp bạn:\n• Dữ liệu thị trường thời gian thực & phân tích biểu đồ\n• Quản lý vị thế & đặt lệnh\n• Phân tích hiệu suất chiến lược\n• Quản lý rủi ro & kích thước vị thế\n\nTôi có thể giúp gì cho bạn?',
    ai_feat1:'Phân tích xu hướng thị trường & đề xuất chiến lược',ai_feat2:'Thực hiện giao dịch tự động',
    ai_feat3:'Tính toán kích thước vị thế & stops',ai_feat4:'Backtest hiệu suất chiến lược của bạn',
    ai_sugg1:'Tôi nên mua BTC bây giờ không?',ai_sugg2:'Tạo chiến lược grid vàng',
    ai_sugg3:'Làm sao phân bổ $1000?',ai_sugg4:'Phân tích xu hướng EUR/USD',ai_sugg5:'Hiển thị vị thế của tôi',
    quick_order_title:'Lệnh nhanh',dir_long:'Mua Long',dir_short:'Bán Short',
    order_symbol:'Ký hiệu',order_amount:'Số tiền (USD)',order_sltp:'SL / TP (%)',order_confirm:'Đặt lệnh',
    sentiment_title:'Cảm xúc thị trường',sent_bull:'Bullish',sent_bear:'Bearish',sent_fg:'Sợ hãi & Tham lam',sent_greed:'Tham lam',sent_flow:'Dòng chảy ròng lớn',sent_rate:'Tỷ lệ tài trợ',
    pos_title:'Vị thế của tôi',pos_symbol:'Ký hiệu',pos_size:'Kích thước',pos_open:'Entry',pos_current:'Hiện tại',pos_pnl:'P&L',pos_action:'Hành động',
    pos_close:'Đóng',pos_empty:'Không có vị thế',
    pos_my_title:'Vị thế của tôi',pos_active_count:' Hoạt động',pos_float:'P&L thả nổi',close_all:'Đóng tất cả',
    pos_open_lbl:'Entry',pos_curr_lbl:'Hiện tại',pos_sl_lbl:'Stop Loss',pos_tp_lbl:'Take Profit',
    pos_ai_analyze:'Phân tích AI',pos_edit_btn:'Chỉnh sửa',
    mkt_buy:'Mua',mkt_sell:'Bán',
    strat_cum_pnl:'P&L tổng',
    strat_title:'Quản lý chiến lược',strat_new:'Chiến lược mới',
    strat_running:'Đang chạy',strat_paused:'Tạm dừng',strat_stopped:'Dừng',
    strat_start:'Bắt đầu',strat_pause:'Tạm dừng',strat_stop:'Dừng',strat_edit:'Chỉnh sửa',
    strat_my_title:'Chiến lược của tôi',strat_running_count:' đang chạy',strat_paused_count:' tạm dừng',strat_add:'Thêm chiến lược',
    bt_title:'Backtest',bt_symbol:'Ký hiệu',bt_strat_type:'Loại chiến lược',
    bt_start_date:'Ngày bắt đầu',bt_end_date:'Ngày kết thúc',bt_capital:'Vốn ban đầu (USD)',bt_pos_size:'Kích thước vị thế (%)',
    bt_run:'Bắt đầu backtest',bt_total_return:'Tổng lợi nhuận',bt_annual_return:'Lợi nhuận hàng năm',bt_max_dd:'Drawdown tối đa',
    bt_sharpe:'Tỷ số Sharpe',bt_win_rate:'Tỷ lệ thắng',bt_trades:'Tổng giao dịch',bt_log_title:'Nhật ký giao dịch (20 gần nhất)',
    strat_macd:'MACD theo xu hướng',strat_ema:'EMA Crossover',strat_rsi:'RSI Quá mua/quá bán',strat_grid:'Grid Trading',strat_bb:'Bollinger Breakout',
    acc_title:'Tài khoản của tôi',acc_plan:'Gói hiện tại',acc_upgrade:'Nâng cấp',
    acc_broker:'Tài khoản broker',acc_connect:'Kết nối broker',
    acc_member_free:'Miễn phí',acc_member_pro:'Thành viên Pro',acc_member_elite:'Thành viên Elite',
    acc_valid_until:'Hạn đến',acc_reg_date:'Đăng ký',acc_total_pnl:'P&L tổng',
    acc_brokers_count:'Broker',acc_running_strats:'Chiến lược hoạt động',acc_account:'Tài khoản',
    acc_broker_section:'Broker đã kết nối',acc_subscription:'Đăng ký của tôi',
    broker_connected:'Đã kết nối',broker_api_ok:'API OK',broker_not_connected:'Chưa kết nối',broker_pending:'Đang chờ',broker_add_new:'Thêm broker',
    btn_manage:'Quản lý',btn_disconnect:'Ngắt kết nối',btn_connect:'Kết nối',btn_edit:'Chỉnh sửa',
    plan_current:'Hiện tại',per_month:'/tháng',plan_view_all:'Xem tất cả gói →',
    plan_basic_f1:'Tất cả dữ liệu thị trường',plan_basic_f2:'Q&A AI',plan_basic_f3:'2 chiến lược',plan_basic_f4:'Trading tự động',
    plan_pro_f1:'Chiến lược không giới hạn',plan_pro_f2:'Trading tự động AI',plan_pro_f3:'Backtest nâng cao',plan_pro_f4:'Multi-broker',
    plan_elite_f1:'Mở tự động (Signal/DCA/Copy)',plan_elite_f2:'Copy trading không giới hạn',plan_elite_f3:'Hỗ trợ VIP',plan_elite_f4:'Thực thi ưu tiên',
    risk_title:'Kiểm soát rủi ro',risk_max_loss:'Thua lỗ tối đa hàng ngày',risk_max_loss_desc:'Tự động dừng nếu vượt quá',
    risk_max_pos:'Kích thước vị thế tối đa',risk_max_pos_desc:'Mỗi ký hiệu, % tổng tài sản',
    risk_auto_order:'Lệnh auto AI',risk_auto_order_desc:'AI thực thi khi chiến lược được kích hoạt',
    risk_notify:'Thông báo trước lệnh',risk_notify_desc:'Gửi xác nhận trước mỗi giao dịch',
    risk_night:'Bảo vệ ban đêm',risk_night_desc:'22:00-07:00 tạm dừng trading tự động',
    confirm:'Xác nhận',cancel:'Hủy',save:'Lưu',close:'Đóng',
    loading:'Đang tải...',success:'Thành công',error:'Lỗi',
    lang_switched:'🌐 Đã chuyển sang Tiếng Việt',
    tlog_title:'Nhật ký giao dịch',tlog_all:'Tất cả',tlog_buy:'Long',tlog_sell:'Short',tlog_win:'Lời',tlog_loss:'Lỗ',
    tlog_total_trades:'Giao dịch',tlog_win_rate:'Tỷ lệ thắng',tlog_net_pnl:'P&L ròng',tlog_avg_hold:'Trung bình giữ',tlog_best:'Giao dịch tốt nhất',tlog_worst:'Giao dịch tệ nhất',
    tlog_col_time:'Thời gian',tlog_col_symbol:'Ký hiệu',tlog_col_dir:'Hướng',tlog_col_open:'Entry',tlog_col_close:'Exit',tlog_col_size:'Lô',tlog_col_pnl:'P&L',tlog_col_hold:'Thời gian',
    tlog_dir_long:'Long',tlog_dir_short:'Short',tlog_empty:'Không có bản ghi giao dịch',
    nav_copy:'Copy Trading',copy_title:'Copy Trading',copy_subtitle:'Theo dõi top trader, tín hiệu thời gian thực',
    copy_goto_auto:'Cài đặt auto',copy_my_follows:'Theo dõi của tôi',copy_leaderboard:'Bảng xếp hạng tín hiệu',
    copy_filter_all:'Tất cả',copy_filter_crypto:'Crypto',copy_filter_forex:'Forex',copy_filter_stable:'DD thấp',
    copy_followers:'người theo dõi',copy_monthly:'Hàng tháng',copy_winrate:'Tỷ lệ thắng',copy_maxdd:'DD max',copy_30pnl:'P&L 30 ngày',
    copy_follow_btn:'Theo dõi',copy_following:'✓ Đang theo dõi',copy_unfollow:'Bỏ theo dõi',copy_detail_btn:'Chi tiết',
    copy_pnl:'P&L thả nổi',copy_since:'Từ',copy_follow_title:'Cài đặt theo dõi',copy_confirm_follow:'Xác nhận',
    copy_toast_follow:'Bắt đầu theo dõi',copy_toast_unfollow:'Đã hủy theo dõi',
    ct_tag_ct1:'Chuyên gia BTC/ETH · 3 năm',ct_tag_ct2:'Vàng/Forex · 5 năm',ct_tag_ct3:'DD thấp ổn định · 4 năm',
    ct_tag_ct4:'Scalper đêm · 2 năm',ct_tag_ct5:'Đa vĩ mô · 6 năm',ct_tag_ct6:'DCA+xu hướng · 7 năm',
    nav_autoopen:'Mở Auto',ao_title:'Mở Auto',ao_subtitle:'3 chế độ vào tự động thông minh',
    ao_lock_title:'Mở Auto độc quyền Elite',ao_lock_desc:'Nâng cấp lên Elite để mở khóa vào tự động',
    ao_lock_btn:'Nâng cấp $199/tháng',
    ao_mode_signal:'Kích hoạt tín hiệu',ao_mode_signal_desc:'Vào tự động khi điều kiện RSI/MACD/EMA được đáp ứng',
    ao_mode_dca:'DCA định kỳ',ao_mode_dca_desc:'Mua tự động định kỳ để giá trung bình',
    ao_mode_copy:'Sync copy',ao_mode_copy_desc:'Mirror mỗi entry từ nguồn tín hiệu',
    ao_running:'Đang chạy',
    ao_signal_cfg:'Cấu hình tín hiệu',ao_signal_ind:'Chỉ báo',ao_signal_pair:'Ký hiệu',
    ao_dca_cfg:'Cấu hình DCA',ao_dca_pair:'Ký hiệu',ao_dca_freq:'Tần suất',
    ao_dca_hourly:'Mỗi giờ',ao_dca_daily:'Hàng ngày',ao_dca_weekly:'Hàng tuần',ao_dca_monthly:'Hàng tháng',
    ao_dca_amount:'Số tiền mỗi entry (USD)',ao_dca_total:'Giới hạn tổng (USD)',ao_dca_price_drop:'Gấp đôi nếu giảm (%)',ao_dca_exit:'Take Profit (%)',
    ao_dca_invested:'Đã đầu tư',
    ao_copy_cfg:'Cấu hình copy',ao_copy_source:'Nguồn tín hiệu',ao_copy_select:'Chọn',
    ao_copy_ratio:'Tỷ lệ',ao_copy_max:'Max mỗi giao dịch (USD)',ao_copy_daily_loss:'Giới hạn lỗ hàng ngày (USD)',
    ao_copy_filter:'Lọc hướng',ao_copy_all:'Long & Short',ao_copy_long_only:'Chỉ Long',ao_copy_short_only:'Chỉ Short',
    ao_copy_pairs:'Giới hạn ký hiệu',ao_copy_pairs_ph:'BTC,ETH (trống=tất cả)',ao_not_following:'Chưa theo dõi',
    ao_pos_size:'Kích thước vị thế (USD)',ao_sl:'Stop Loss (%)',ao_tp:'Take Profit (%)',ao_max_pos:'Max vị thế mở',
    lb_tab_roi:'ROI hàng tháng',lb_tab_wr:'Tỷ lệ thắng',lb_tab_stable:'Ổn định nhất',lb_tab_new:'Mới',
    nav_square:'Quảng trường Trading',sq_title:'Quảng trường Trading',sq_subtitle:'Chia sẻ quan điểm, khám phá cảm xúc, đồng bộ với traders toàn cầu',
    sq_post_ph:'Chia sẻ quan điểm thị trường, logic giao dịch, phân tích vị thế...',sq_post_btn:'Đăng',
    sq_filter_all:'Tất cả',sq_filter_bull:'Bullish',sq_filter_bear:'Bearish',sq_filter_hot:'Hot',
    sq_pair_label:'Cặp',sq_sentiment_label:'Cảm xúc',
    nav_stratmarket:'Thị trường chiến lược',sm_title:'Thị trường chiến lược',sm_subtitle:'Khám phá, chia sẻ & copy chiến lược quantitative tốt nhất',
    sm_upload_title:'Xuất bản chiến lược của tôi',sm_upload_btn:'Tải lên chiến lược',sm_filter_all:'Tất cả',
    sm_filter_trend:'Xu hướng',sm_filter_grid:'Grid',sm_filter_quant:'Quant',sm_filter_arb:'Arb',
    sm_name_label:'Tên chiến lược',sm_asset_label:'Ký hiệu',sm_price_label:'Giá (USD/tháng, 0=Miễn phí)',
    sm_code_label:'Mã chiến lược',sm_submit_btn:'Gửi để xem xét',sm_backtest:'Backtest',
    sm_copy:'Copy',sm_subscribe:'Đăng ký',
    nav_signals:'Phát tín hiệu',sig_title:'Phát tín hiệu',sig_subtitle:'Tín hiệu giao dịch live, đăng ký 1 click, kết nối với mở auto',
    sig_publish_title:'Xuất bản tín hiệu giao dịch',sig_tab_live:'Tín hiệu live',sig_tab_sources:'Nguồn tín hiệu',sig_tab_history:'Lịch sử',
    sig_pair:'Cặp',sig_dir:'Hướng',sig_dir_buy:'Mua',sig_dir_sell:'Bán',
    sig_entry:'Entry',sig_sl:'Stop Loss',sig_tp1:'TP1',sig_tp2:'TP2',
    sig_desc:'Ghi chú tín hiệu',sig_publish_btn:'Phát tín hiệu',
    sig_follow:'Theo dõi tín hiệu',sig_share:'Chia sẻ',sig_subscribe_bc:'Đăng ký nguồn',
    ao_start:'Bắt đầu mở auto',ao_stop:'Dừng',ao_status_off:'● Đã dừng',ao_status_on:'🟢 Đang chạy',
    ao_started:'Đã bắt đầu',ao_stopped:'Đã dừng',
    ao_exec_log:'Nhật ký thực thi',ao_clear_log:'Xóa',ao_log_empty:'Không có bản ghi',
    toast_elite_unlocked:'Elite đã mở khóa! Mở auto hiện có sẵn',
    dash_brief_title:'Báo cáo hàng ngày AI',dash_brief_time:'Cập nhật 08:00',
    dash_brief_content:'Vàng bullish hôm nay, được hỗ trợ bởi tín hiệu Fed dovish, mục tiêu $2,380. BTC gặp kháng cự tại $84,000, ngắn hạn thận trọng. Nasdaq được dẫn dắt bởi kết quả tech, nhìn chung mạnh. EUR/USD yếu dao động, chỉ số USD 104.2 hỗ trợ.',
    dash_signal_gold:'Vàng ▲ Bullish',dash_signal_btc:'BTC ⚠ Theo dõi',dash_signal_eur:'EUR/USD ▼ Yếu',dash_signal_nas:'Nasdaq ▲ Mạnh',
    dash_quick_ops:'Thao tác nhanh',dash_btn_order:'Lệnh AI',dash_btn_backtest:'Backtest nhanh',dash_btn_positions:'Xem vị thế',
    ai_welcome_greet:'Xin chào! Tôi là trợ lý QuantAI 🧠',ai_welcome_intro:'Hãy cho tôi biết ý tưởng giao dịch của bạn và tôi sẽ giúp:',
    modal_symbol:'Ký hiệu',modal_dir:'Hướng',modal_amount:'Số tiền (USD)',modal_leverage:'Đòn bẩy',
    modal_sl:'Stop Loss (%)',modal_tp:'Take Profit (%)',modal_margin:'Ký quỹ ước tính',modal_max_profit:'Lợi nhuận max',modal_max_loss:'Thua lỗ max',
    broker_modal_title:'Kết nối broker',broker_connect_btn:'Xác minh & kết nối',
    cat_crypto:'Crypto',cat_forex_metals:'Forex / Kim loại',cat_all_cfd:'Tất cả CFD',
    sym_btc:'Bitcoin',sym_eth:'Ethereum',sym_sol:'Solana',sym_bnb:'BNB',sym_xrp:'Ripple',
    sym_eurusd:'EUR/USD',sym_gbpusd:'GBP/USD',sym_usdjpy:'USD/JPY',sym_usdchf:'USD/CHF',sym_audusd:'AUD/USD',
    sym_gold:'Vàng spot',sym_silver:'Bạc spot',sym_wti:'WTI Crude',sym_brent:'Brent Crude',
    sym_nas100:'Nasdaq 100',sym_spx500:'S&P 500',sym_dow:'Dow Jones',sym_hsi:'Hang Seng',
    strat_name_1:'BTC MACD Xu hướng',strat_name_2:'Grid Vàng',strat_name_3:'Chiến lược EUR/USD EMA',strat_name_4:'Scalping Nasdaq',
    strat_type_trend:'Theo xu hướng',strat_type_grid:'Grid Trading',strat_type_ema:'EMA Crossover',strat_type_mr:'Trung bình ngược',
    toast_order_ok:'Lệnh đã đặt!',toast_submitted:'Đã gửi!',toast_pos_closed:'Vị thế đã đóng',toast_all_closed:'Tất cả vị thế đã đóng',
    toast_strat_started:'đã bắt đầu',toast_strat_paused:'đã tạm dừng',toast_strat_deleted:'chiến lược đã xóa',
    toast_broker_connected:'Broker đã kết nối! API đã xác minh',toast_coming_soon:'Sắp ra mắt',
    toast_upgrading:'Chuyển hướng đến',toast_view_plans:'Xem tất cả gói',
    confirm_close_pos:'Xác nhận đóng',confirm_close_all:'Đóng tất cả vị thế? Không thể hoàn tác!',confirm_del_strat:'Xóa chiến lược',
    bt_running:'Đang chạy...',
    ai_analyze_suffix:' vị thế của tôi như thế nào?',
    ai_placeholder:'Nhập hướng dẫn giao dịch hoặc câu hỏi…',
    ai_resp_btc:'📊 Phân tích BTC/USDT:\n\nGiá gần $83,400, kháng cự tại $84,000. MACD golden cross, RSI(14) ở 58 — bullish nhưng chưa quá mua.\n\nĐề xuất: Long nhỏ gần hỗ trợ $82,800, stop $81,000, mục tiêu $86,000. R/R ≈ 1:2.2.',
    ai_resp_gold:'🥇 Phân tích Vàng (XAU/USD):\n\nVàng vẫn mạnh tại $2,342. Tín hiệu Fed dovish và đô la yếu tạo hỗ trợ. Mục tiêu ngắn hạn $2,380, hỗ trợ quan trọng $2,310.\n\nĐề xuất: Giữ long, di chuyển stop đến $2,320 để khóa lợi nhuận.',
    ai_resp_position:'📐 Quản lý vị thế ($1,000 vốn):\n\n• BTC/USDT: 30% ($300) — Vị thế chính, đòn bẩy 5x\n• XAU/USD: 25% ($250) — Hedge, 10x\n• EUR/USD: 20% ($200) — Hedge FX\n• Tiền mặt: 25% ($250) — Chờ cơ hội\n\nThua lỗ max mỗi giao dịch: 3%.',
    ai_resp_strategy:'⚡ 3 chiến lược cho thị trường hiện tại:\n\n1. **BTC MACD Xu hướng** — 67% tỷ lệ thắng, +89%/năm\n2. **Grid Vàng** — Cho thị trường sideways, 3-5%/tháng\n3. **EUR/USD EMA** — Rủi ro thấp, phù hợp cho người mới\n\nBạn muốn kích hoạt một chiến lược?',
    ai_resp_default:'Tôi hiểu yêu cầu của bạn. Để tôi phân tích điều kiện thị trường hiện tại...\n\n📊 Thị trường nhìn chung bullish, nhưng cần cẩn thận với rủi ro chính sách Fed. Giữ vị thế dưới 50% và luôn đặt stops.\n\nCó ký hiệu hoặc chiến lược cụ thể nào bạn muốn khám phá?',
  },

  // 泰语
  th: {
    nav_dashboard:'แดชบอร์ด',nav_market:'ตลาด',nav_ai:'แชท AI',
    nav_positions:'สถานะ',nav_strategies:'กลยุทธ์',nav_backtest:'เทสต์ย้อนหลัง',nav_account:'บัญชี',
    page_dashboard:'แดชบอร์ด',page_market:'ตลาด',page_ai:'ผู้ช่วย AI',
    page_positions:'สถานะของฉัน',page_strategies:'จัดการกลยุทธ์',page_backtest:'เทสต์ย้อนหลัง',page_account:'บัญชีของฉัน',
    page_copy:'คัดลอกเทรด',page_autoopen:'เปิดอัตโนมัติ',
    total_asset:'สินทรัพย์รวม',daily_pnl:'P&L วันนี้',win_rate:'อัตราชนะ',active_strategies:'กลยุทธ์ที่ใช้งาน',pos_count:'สถานะเปิด',
    card_today:'วันนี้',card_month:'เดือนนี้',card_paused:' หยุด',card_running:' ทำงาน',
    card_long:'Long',card_short:'Short',
    quick_order:'+ คำสั่งเร็ว',
    chart_update:'นาทีอัปเดต',
    market_title:'ตลาดสด',search_placeholder:'ค้นหาสัญลักษณ์...',
    mkt_all:'ทั้งหมด',mkt_crypto:'คริปโต',mkt_forex:'ฟอเร็กซ์',mkt_metals:'โลหะ',mkt_energy:'พลังงาน',mkt_index:'ดัชนี',
    tbl_symbol:'สัญลักษณ์',tbl_price:'ราคา',tbl_change:'การเปลี่ยนแปลง',tbl_volume:'ปริมาณ',tbl_trend:'เทรนด์ 7 วัน',tbl_action:'การดำเนินการ',
    ai_title:'ผู้ช่วยเทรด AI',ai_placeholder:'พิมพ์ข้อความ...',
    ai_welcome:'สวัสดี! ฉันคือผู้ช่วย QuantAI 🤖\n\nฉันสามารถช่วยคุณได้:\n• ข้อมูลตลาดเรียลไทม์ & วิเคราะห์กราฟ\n• จัดการสถานะ & คำสั่ง\n• วิเคราะห์ประสิทธิภาพกลยุทธ์\n• จัดการความเสี่ยง & ขนาดสถานะ\n\nฉันจะช่วยคุณได้อย่างไร?',
    ai_feat1:'วิเคราะห์เทรนด์ตลาด & เสนอกลยุทธ์',ai_feat2:'ดำเนินการเทรดอัตโนมัติ',
    ai_feat3:'คำนวณขนาดสถานะ & stops',ai_feat4:'เทสต์ย้อนหลังประสิทธิภาพกลยุทธ์',
    ai_sugg1:'ควรซื้อ BTC ตอนนี้ไหม?',ai_sugg2:'สร้างกลยุทธ์ grid ทอง',
    ai_sugg3:'จัดสรร $1000 อย่างไร?',ai_sugg4:'วิเคราะห์เทรนด์ EUR/USD',ai_sugg5:'แสดงสถานะของฉัน',
    quick_order_title:'คำสั่งเร็ว',dir_long:'ซื้อ Long',dir_short:'ขาย Short',
    order_symbol:'สัญลักษณ์',order_amount:'จำนวน (USD)',order_sltp:'SL / TP (%)',order_confirm:'วางคำสั่ง',
    sentiment_title:'ความรู้สึกตลาด',sent_bull:'กระทิง',sent_bear:'หมี',sent_fg:'ความกลัว & ความโลภ',sent_greed:'ความโลภ',sent_flow:'กระแสเน็ตใหญ่',sent_rate:'อัตราการระดมทุน',
    pos_title:'สถานะของฉัน',pos_symbol:'สัญลักษณ์',pos_size:'ขนาด',pos_open:'เข้า',pos_current:'ปัจจุบัน',pos_pnl:'P&L',pos_action:'การดำเนินการ',
    pos_close:'ปิด',pos_empty:'ไม่มีสถานะ',
    pos_my_title:'สถานะของฉัน',pos_active_count:' ทำงาน',pos_float:'P&L ลอย',close_all:'ปิดทั้งหมด',
    pos_open_lbl:'เข้า',pos_curr_lbl:'ปัจจุบัน',pos_sl_lbl:'Stop Loss',pos_tp_lbl:'Take Profit',
    pos_ai_analyze:'วิเคราะห์ AI',pos_edit_btn:'แก้ไข',
    mkt_buy:'ซื้อ',mkt_sell:'ขาย',
    strat_cum_pnl:'P&L รวม',
    strat_title:'จัดการกลยุทธ์',strat_new:'กลยุทธ์ใหม่',
    strat_running:'ทำงาน',strat_paused:'หยุด',strat_stopped:'หยุดแล้ว',
    strat_start:'เริ่ม',strat_pause:'หยุด',strat_stop:'หยุด',strat_edit:'แก้ไข',
    strat_my_title:'กลยุทธ์ของฉัน',strat_running_count:' ทำงาน',strat_paused_count:' หยุด',strat_add:'เพิ่มกลยุทธ์',
    bt_title:'เทสต์ย้อนหลัง',bt_symbol:'สัญลักษณ์',bt_strat_type:'ประเภทกลยุทธ์',
    bt_start_date:'วันที่เริ่ม',bt_end_date:'วันที่สิ้นสุด',bt_capital:'ทุนเริ่มต้น (USD)',bt_pos_size:'ขนาดสถานะ (%)',
    bt_run:'เริ่มเทสต์ย้อนหลัง',bt_total_return:'ผลตอบแทนรวม',bt_annual_return:'ผลตอบแทนรายปี',bt_max_dd:'Drawdown สูงสุด',
    bt_sharpe:'อัตราส่วน Sharpe',bt_win_rate:'อัตราชนะ',bt_trades:'เทรดทั้งหมด',bt_log_title:'บันทึกเทรด (20 ล่าสุด)',
    strat_macd:'MACD ตามเทรนด์',strat_ema:'EMA Crossover',strat_rsi:'RSI overbought/oversold',strat_grid:'Grid Trading',strat_bb:'Bollinger Breakout',
    acc_title:'บัญชีของฉัน',acc_plan:'แผนปัจจุบัน',acc_upgrade:'อัปเกรด',
    acc_broker:'บัญชีโบรกเกอร์',acc_connect:'เชื่อมต่อโบรกเกอร์',
    acc_member_free:'ฟรี',acc_member_pro:'สมาชิก Pro',acc_member_elite:'สมาชิก Elite',
    acc_valid_until:'ใช้ได้ถึง',acc_reg_date:'ลงทะเบียน',acc_total_pnl:'P&L รวม',
    acc_brokers_count:'โบรกเกอร์',acc_running_strats:'กลยุทธ์ที่ใช้งาน',acc_account:'บัญชี',
    acc_broker_section:'โบรกเกอร์ที่เชื่อมต่อ',acc_subscription:'การสมัครของฉัน',
    broker_connected:'เชื่อมต่อแล้ว',broker_api_ok:'API OK',broker_not_connected:'ไม่ได้เชื่อมต่อ',broker_pending:'รอดำเนินการ',broker_add_new:'เพิ่มโบรกเกอร์',
    btn_manage:'จัดการ',btn_disconnect:'ตัดการเชื่อมต่อ',btn_connect:'เชื่อมต่อ',btn_edit:'แก้ไข',
    plan_current:'ปัจจุบัน',per_month:'/เดือน',plan_view_all:'ดูแผนทั้งหมด →',
    plan_basic_f1:'ข้อมูลตลาดทั้งหมด',plan_basic_f2:'Q&A AI',plan_basic_f3:'2 กลยุทธ์',plan_basic_f4:'เทรดอัตโนมัติ',
    plan_pro_f1:'กลยุทธ์ไม่จำกัด',plan_pro_f2:'เทรดอัตโนมัติ AI',plan_pro_f3:'เทสต์ย้อนหลังขั้นสูง',plan_pro_f4:'หลายโบรกเกอร์',
    plan_elite_f1:'เปิดอัตโนมัติ (Signal/DCA/Copy)',plan_elite_f2:'คัดลอกเทรดไม่จำกัด',plan_elite_f3:'สนับสนุน VIP',plan_elite_f4:'ดำเนินการเป็นลำดับ',
    risk_title:'การควบคุมความเสี่ยง',risk_max_loss:'ขาดทุนสูงสุดรายวัน',risk_max_loss_desc:'หยุดอัตโนมัติหากเกิน',
    risk_max_pos:'ขนาดสถานะสูงสุด',risk_max_pos_desc:'ต่อสัญลักษณ์, % ของสินทรัพย์ทั้งหมด',
    risk_auto_order:'คำสั่ง auto AI',risk_auto_order_desc:'AI ดำเนินการเมื่อกลยุทธ์ถูก Trigger',
    risk_notify:'แจ้งเตือนก่อนคำสั่ง',risk_notify_desc:'ส่งยืนยันก่อนทุกเทรด',
    risk_night:'โหมดป้องกันกลางคืน',risk_night_desc:'22:00-07:00 หยุดเทรดอัตโนมัติ',
    confirm:'ยืนยัน',cancel:'ยกเลิก',save:'บันทึก',close:'ปิด',
    loading:'กำลังโหลด...',success:'สำเร็จ',error:'ข้อผิดพลาด',
    lang_switched:'🌐 เปลี่ยนเป็นภาษาไทย',
    tlog_title:'บันทึกเทรด',tlog_all:'ทั้งหมด',tlog_buy:'Long',tlog_sell:'Short',tlog_win:'กำไร',tlog_loss:'ขาดทุน',
    tlog_total_trades:'เทรด',tlog_win_rate:'อัตราชนะ',tlog_net_pnl:'P&L สุทธิ',tlog_avg_hold:'ถือเฉลี่ย',tlog_best:'เทรดดีที่สุด',tlog_worst:'เทรดแย่ที่สุด',
    tlog_col_time:'เวลา',tlog_col_symbol:'สัญลักษณ์',tlog_col_dir:'ทิศทาง',tlog_col_open:'เข้า',tlog_col_close:'ออก',tlog_col_size:'ล็อต',tlog_col_pnl:'P&L',tlog_col_hold:'ระยะเวลา',
    tlog_dir_long:'Long',tlog_dir_short:'Short',tlog_empty:'ไม่มีบันทึกเทรด',
    nav_copy:'คัดลอกเทรด',copy_title:'คัดลอกเทรด',copy_subtitle:'ติดตามเทรดเดอร์ที่เก่ง, สัญญาณเรียลไทม์',
    copy_goto_auto:'ตั้งค่า auto',copy_my_follows:'การติดตามของฉัน',copy_leaderboard:'อันดับสัญญาณ',
    copy_filter_all:'ทั้งหมด',copy_filter_crypto:'คริปโต',copy_filter_forex:'ฟอเร็กซ์',copy_filter_stable:'DD ต่ำ',
    copy_followers:'ผู้ติดตาม',copy_monthly:'รายเดือน',copy_winrate:'อัตราชนะ',copy_maxdd:'DD สูงสุด',copy_30pnl:'P&L 30 วัน',
    copy_follow_btn:'ติดตาม',copy_following:'✓ กำลังติดตาม',copy_unfollow:'ยกเลิกติดตาม',copy_detail_btn:'รายละเอียด',
    copy_pnl:'P&L ลอย',copy_since:'ตั้งแต่',copy_follow_title:'ตั้งค่าติดตาม',copy_confirm_follow:'ยืนยัน',
    copy_toast_follow:'เริ่มติดตาม',copy_toast_unfollow:'ยกเลิกติดตาม',
    ct_tag_ct1:'ผู้เชี่ยว BTC/ETH · 3 ปี',ct_tag_ct2:'ทอง/ฟอเร็กซ์ · 5 ปี',ct_tag_ct3:'DD ต่ำเสถียร · 4 ปี',
    ct_tag_ct4:'Scalper กลางคืน · 2 ปี',ct_tag_ct5:'Multi-macro · 6 ปี',ct_tag_ct6:'DCA+เทรนด์ · 7 ปี',
    nav_autoopen:'เปิดอัตโนมัติ',ao_title:'เปิดอัตโนมัติ',ao_subtitle:'3 โหมดเข้าอัตโนมัติอัจฉริยะ',
    ao_lock_title:'เปิดอัตโนมัติสำหรับ Elite เท่านั้น',ao_lock_desc:'อัปเกรดเป็น Elite เพื่อปลดล็อกการเข้าอัตโนมัติ',
    ao_lock_btn:'อัปเกรด $199/เดือน',
    ao_mode_signal:'Trigger สัญญาณ',ao_mode_signal_desc:'เข้าอัตโนมัติเมื่อเงื่อนไข RSI/MACD/EMA ครบ',
    ao_mode_dca:'DCA ซ้ำ',ao_mode_dca_desc:'ซื้ออัตโนมัติเป็นระยะเพื่อต้นทุนเฉลี่ย',
    ao_mode_copy:'Sync copy',ao_mode_copy_desc:'สะท้อนทุกการเข้าจากแหล่งสัญญาณ',
    ao_running:'ทำงาน',
    ao_signal_cfg:'การตั้งค่าสัญญาณ',ao_signal_ind:'ตัวบ่งชี้',ao_signal_pair:'สัญลักษณ์',
    ao_dca_cfg:'การตั้งค่า DCA',ao_dca_pair:'สัญลักษณ์',ao_dca_freq:'ความถี่',
    ao_dca_hourly:'ทุกชั่วโมง',ao_dca_daily:'รายวัน',ao_dca_weekly:'รายสัปดาห์',ao_dca_monthly:'รายเดือน',
    ao_dca_amount:'จำนวนต่อการเข้า (USD)',ao_dca_total:'ขีดจำกัดรวม (USD)',ao_dca_price_drop:'double หากลง (%)',ao_dca_exit:'Take Profit (%)',
    ao_dca_invested:'ลงทุนแล้ว',
    ao_copy_cfg:'การตั้งค่าคัดลอก',ao_copy_source:'แหล่งสัญญาณ',ao_copy_select:'เลือก',
    ao_copy_ratio:'อัตราส่วน',ao_copy_max:'สูงสุดต่อเทรด (USD)',ao_copy_daily_loss:'ขีดจำกัดขาดทุนรายวัน (USD)',
    ao_copy_filter:'ตัวกรองทิศทาง',ao_copy_all:'Long & Short',ao_copy_long_only:'Long เท่านั้น',ao_copy_short_only:'Short เท่านั้น',
    ao_copy_pairs:'จำกัดสัญลักษณ์',ao_copy_pairs_ph:'BTC,ETH (ว่าง=ทั้งหมด)',ao_not_following:'ไม่ได้ติดตาม',
    ao_pos_size:'ขนาดสถานะ (USD)',ao_sl:'Stop Loss (%)',ao_tp:'Take Profit (%)',ao_max_pos:'สถานะเปิดสูงสุด',
    lb_tab_roi:'ROI รายเดือน',lb_tab_wr:'อัตราชนะ',lb_tab_stable:'เสถียรที่สุด',lb_tab_new:'มาใหม่',
    nav_square:'สแควร์เทรด',sq_title:'สแควร์เทรด',sq_subtitle:'แบ่งปันมุมมอง, ค้นหาความรู้สึก, ซิงค์กับเทรดเดอร์ทั่วโลก',
    sq_post_ph:'แบ่งปันมุมมองตลาด, ตรรกะเทรด, วิเคราะห์สถานะ...',sq_post_btn:'โพสต์',
    sq_filter_all:'ทั้งหมด',sq_filter_bull:'กระทิง',sq_filter_bear:'หมี',sq_filter_hot:'ฮอต',
    sq_pair_label:'คู่',sq_sentiment_label:'ความรู้สึก',
    nav_stratmarket:'ตลาดกลยุทธ์',sm_title:'ตลาดกลยุทธ์',sm_subtitle:'ค้นหา, แบ่งปัน & คัดลอกกลยุทธ์ Quant ที่ดีที่สุด',
    sm_upload_title:'เผยแพร่กลยุทธ์ของฉัน',sm_upload_btn:'อัปโหลดกลยุทธ์',sm_filter_all:'ทั้งหมด',
    sm_filter_trend:'เทรนด์',sm_filter_grid:'Grid',sm_filter_quant:'Quant',sm_filter_arb:'Arb',
    sm_name_label:'ชื่อกลยุทธ์',sm_asset_label:'สัญลักษณ์',sm_price_label:'ราคา (USD/เดือน, 0=ฟรี)',
    sm_code_label:'รหัสกลยุทธ์',sm_submit_btn:'ส่งเพื่อตรวจสอบ',sm_backtest:'เทสต์ย้อนหลัง',
    sm_copy:'คัดลอก',sm_subscribe:'สมัคร',
    nav_signals:'สัญญาณ Broadcast',sig_title:'สัญญาณ Broadcast',sig_subtitle:'สัญญาณเทรดสด, สมัคร 1 คลิก, เชื่อมต่อเปิดอัตโนมัติ',
    sig_publish_title:'เผยแพร่สัญญาณเทรด',sig_tab_live:'สัญญาณสด',sig_tab_sources:'แหล่งสัญญาณ',sig_tab_history:'ประวัติ',
    sig_pair:'คู่',sig_dir:'ทิศทาง',sig_dir_buy:'ซื้อ',sig_dir_sell:'ขาย',
    sig_entry:'เข้า',sig_sl:'Stop Loss',sig_tp1:'TP1',sig_tp2:'TP2',
    sig_desc:'หมายเหตุสัญญาณ',sig_publish_btn:'Broadcast สัญญาณ',
    sig_follow:'ติดตามสัญญาณ',sig_share:'แบ่งปัน',sig_subscribe_bc:'สมัครแหล่งสัญญาณ',
    ao_start:'เริ่มเปิดอัตโนมัติ',ao_stop:'หยุด',ao_status_off:'● หยุด',ao_status_on:'🟢 ทำงาน',
    ao_started:'เริ่มแล้ว',ao_stopped:'หยุดแล้ว',
    ao_exec_log:'บันทึกการดำเนินการ',ao_clear_log:'ล้าง',ao_log_empty:'ไม่มีบันทึก',
    toast_elite_unlocked:'Elite ปลดล็อก! เปิดอัตโนมัติพร้อมใช้งาน',
    dash_brief_title:'รายงาน AI รายวัน',dash_brief_time:'อัปเดต 08:00',
    dash_brief_content:'ทอง bullish วันนี้, ได้รับการสนับสนุนจากสัญญาณ Fed dovish, เป้าหมาย $2,380. BTC เผชิญแนวต้านที่ $84,000, ระยะสั้นระมัดระวัง Nasdaq ขับเคลื่อนด้วยผลลัพธ์ tech, โดยรวมแข็งแกร่ง EUR/USD อ่อนแอแกว่ง, ดัชนี USD 104.2 แนวรับ',
    dash_signal_gold:'ทอง ▲ Bullish',dash_signal_btc:'BTC ⚠ เฝ้าระวัง',dash_signal_eur:'EUR/USD ▼ อ่อนแอ',dash_signal_nas:'Nasdaq ▲ แข็งแกร่ง',
    dash_quick_ops:'การดำเนินการรวดเร็ว',dash_btn_order:'คำสั่ง AI',dash_btn_backtest:'เทสต์ย้อนหลังเร็ว',dash_btn_positions:'ดูสถานะ',
    ai_welcome_greet:'สวัสดี! ฉันคือผู้ช่วย QuantAI 🧠',ai_welcome_intro:'บอกฉันเกี่ยวกับไอเดียเทรดของคุณและฉันจะช่วย:',
    modal_symbol:'สัญลักษณ์',modal_dir:'ทิศทาง',modal_amount:'จำนวน (USD)',modal_leverage:'Leverage',
    modal_sl:'Stop Loss (%)',modal_tp:'Take Profit (%)',modal_margin:'Margin โดยประมาณ',modal_max_profit:'กำไรสูงสุด',modal_max_loss:'ขาดทุนสูงสุด',
    broker_modal_title:'เชื่อมต่อโบรกเกอร์',broker_connect_btn:'ยืนยัน & เชื่อมต่อ',
    cat_crypto:'คริปโต',cat_forex_metals:'Forex / โลหะ',cat_all_cfd:'CFD ทั้งหมด',
    sym_btc:'Bitcoin',sym_eth:'Ethereum',sym_sol:'Solana',sym_bnb:'BNB',sym_xrp:'Ripple',
    sym_eurusd:'EUR/USD',sym_gbpusd:'GBP/USD',sym_usdjpy:'USD/JPY',sym_usdchf:'USD/CHF',sym_audusd:'AUD/USD',
    sym_gold:'ทอง Spot',sym_silver:'เงิน Spot',sym_wti:'WTI Crude',sym_brent:'Brent Crude',
    sym_nas100:'Nasdaq 100',sym_spx500:'S&P 500',sym_dow:'Dow Jones',sym_hsi:'Hang Seng',
    strat_name_1:'BTC MACD เทรนด์',strat_name_2:'Grid ทอง',strat_name_3:'กลยุทธ์ EUR/USD EMA',strat_name_4:'Scalping Nasdaq',
    strat_type_trend:'ตามเทรนด์',strat_type_grid:'Grid Trading',strat_type_ema:'EMA Crossover',strat_type_mr:'Mean Reversion',
    toast_order_ok:'วางคำสั่งแล้ว!',toast_submitted:'ส่งแล้ว!',toast_pos_closed:'ปิดสถานะ',toast_all_closed:'ปิดสถานะทั้งหมด',
    toast_strat_started:'เริ่มแล้ว',toast_strat_paused:'หยุดแล้ว',toast_strat_deleted:'ลบกลยุทธ์แล้ว',
    toast_broker_connected:'เชื่อมต่อโบรกเกอร์แล้ว! API ยืนยัน',toast_coming_soon:'เร็วๆ นี้',
    toast_upgrading:'กำลังนำไปยัง',toast_view_plans:'ดูแผนทั้งหมด',
    confirm_close_pos:'ยืนยันการปิด',confirm_close_all:'ปิดสถานะทั้งหมด? ไม่สามารถยกเลิกได้!',confirm_del_strat:'ลบกลยุทธ์',
    bt_running:'กำลังทำงาน...',
    ai_analyze_suffix:' สถานะของฉันเป็นอย่างไร?',
    ai_placeholder:'ใส่คำสั่งเทรดหรือคำถาม…',
    ai_resp_btc:'📊 วิเคราะห์ BTC/USDT:\n\nราคาใกล้ $83,400, แนวต้านที่ $84,000. MACD golden cross, RSI(14) ที่ 58 — bullish แต่ยังไม่ overbought.\n\nข้อเสนอ: Long เล็กใกล้แนวรับ $82,800, stop ที่ $81,000, เป้าหมาย $86,000. R/R ≈ 1:2.2.',
    ai_resp_gold:'🥇 วิเคราะห์ทอง (XAU/USD):\n\nทองยังแข็งแกร่งที่ $2,342. สัญญาณ Fed dovish และดอลลาร์อ่อนให้การสนับสนุน เป้าหมายระยะสั้น $2,380, แนวรับสำคัญ $2,310.\n\nข้อเสนอ: ถือ long, ย้าย stop ไป $2,320 เพื่อล็อกกำไร.',
    ai_resp_position:'📐 การจัดการสถานะ ($1,000 ทุน):\n\n• BTC/USDT: 30% ($300) — สถานะหลัก, leverage 5x\n• XAU/USD: 25% ($250) — Hedge, 10x\n• EUR/USD: 20% ($200) — Hedge FX\n• เงินสด: 25% ($250) — รอโอกาส\n\nขาดทุนสูงสุดต่อเทรด: 3%.',
    ai_resp_strategy:'⚡ 3 กลยุทธ์สำหรับตลาดปัจจุบัน:\n\n1. **BTC MACD เทรนด์** — 67% อัตราชนะ, +89% ต่อปี\n2. **Grid ทอง** — สำหรับตลาด sideways, 3-5%/เดือน\n3. **EUR/USD EMA** — ความเสี่ยงต่ำ, เหมาะสำหรับมือใหม่\n\nต้องการเปิดใช้งานกลยุทธ์ไหม?',
    ai_resp_default:'ฉันเข้าใจคำขอของคุณ ให้ฉันวิเคราะห์สภาพตลาดปัจจุบัน...\n\n📊 ตลาดโดยรวม bullish แต่ต้องระวังความเสี่ยงจากนโยบาย Fed รักษาสถานะต่ำกว่า 50% และตั้ง stops เสมอ\n\nมีสัญลักษณ์หรือกลยุทธ์เฉพาะที่ต้องการสำรวจไหม?',
  },

  // 土耳其语
  tr: {
    nav_dashboard:'Pano',nav_market:'Piyasa',nav_ai:'AI Sohbet',
    nav_positions:'Pozisyonlar',nav_strategies:'Stratejiler',nav_backtest:'Geri Test',nav_account:'Hesap',
    page_dashboard:'Pano',page_market:'Piyasa',page_ai:'AI Asistanı',
    page_positions:'Pozisyonlarım',page_strategies:'Strateji Yöneticisi',page_backtest:'Geri Test',page_account:'Hesabım',
    page_copy:'Kopyalama Ticareti',page_autoopen:'Otomatik Aç',
    total_asset:'Toplam Varlık',daily_pnl:'Günlük P&L',win_rate:'Kazanma Oranı',active_strategies:'Aktif Stratejiler',pos_count:'Açık Pozisyon',
    card_today:'Bugün',card_month:'Bu Ay',card_paused:' Durdu',card_running:' Çalışıyor',
    card_long:'Long',card_short:'Short',
    quick_order:'+ Hızlı Emir',
    chart_update:'dk güncelleme',
    market_title:'Canlı Piyasa',search_placeholder:'Sembol ara...',
    mkt_all:'Tümü',mkt_crypto:'Kripto',mkt_forex:'Forex',mkt_metals:'Metaller',mkt_energy:'Enerji',mkt_index:'Endeksler',
    tbl_symbol:'Sembol',tbl_price:'Fiyat',tbl_change:'Değişim',tbl_volume:'Hacim',tbl_trend:'7G Trend',tbl_action:'Eylem',
    ai_title:'AI Ticaret Asistanı',ai_placeholder:'Mesaj yazın...',
    ai_welcome:'Merhaba! Ben QuantAI asistanıyım 🤖\n\nSize yardımcı olabilirim:\n• Gerçek zamanlı piyasa verileri & grafik analizi\n• Pozisyon & emir yönetimi\n• Strateji performansı analizi\n• Risk yönetimi & pozisyon büyüklüğü\n\nSize nasıl yardımcı olabilirim?',
    ai_feat1:'Piyasa trendlerini analiz et & strateji öner',ai_feat2:'Otomatik ticaret işlemleri gerçekleştir',
    ai_feat3:'Pozisyon büyüklüğü & stops hesapla',ai_feat4:'Stratejinin performansını geri test et',
    ai_sugg1:'Şimdi BTC almalı mıyım?',ai_sugg2:'Altın grid stratejisi oluştur',
    ai_sugg3:'$1000 nasıl dağıtılır?',ai_sugg4:'EUR/USD trend analizi',ai_sugg5:'Pozisyonlarımı göster',
    quick_order_title:'Hızlı Emir',dir_long:'Long Al',dir_short:'Short Sat',
    order_symbol:'Sembol',order_amount:'Tutar (USD)',order_sltp:'SL / TP (%)',order_confirm:'Emir ver',
    sentiment_title:'Piyasa Duygusu',sent_bull:'Boğa',sent_bear:'Ayı',sent_fg:'Korku & Açgözlülük',sent_greed:'Açgözlülük',sent_flow:'Büyük net akış',sent_rate:'Finansman oranı',
    pos_title:'Pozisyonlarım',pos_symbol:'Sembol',pos_size:'Büyüklük',pos_open:'Giriş',pos_current:'Güncel',pos_pnl:'P&L',pos_action:'Eylem',
    pos_close:'Kapat',pos_empty:'Pozisyon yok',
    pos_my_title:'Pozisyonlarım',pos_active_count:' Aktif',pos_float:'P&L Yüzen',close_all:'Tümünü kapat',
    pos_open_lbl:'Giriş',pos_curr_lbl:'Güncel',pos_sl_lbl:'Stop Loss',pos_tp_lbl:'Take Profit',
    pos_ai_analyze:'AI Analiz',pos_edit_btn:'Düzenle',
    mkt_buy:'Al',mkt_sell:'Sat',
    strat_cum_pnl:'Toplam P&L',
    strat_title:'Strateji Yöneticisi',strat_new:'Yeni Strateji',
    strat_running:'Çalışıyor',strat_paused:'Durdu',strat_stopped:'Durduruldu',
    strat_start:'Başlat',strat_pause:'Dur',strat_stop:'Durdur',strat_edit:'Düzenle',
    strat_my_title:'Stratejilerim',strat_running_count:' çalışıyor',strat_paused_count:' durdu',strat_add:'Strateji ekle',
    bt_title:'Geri Test',bt_symbol:'Sembol',bt_strat_type:'Strateji türü',
    bt_start_date:'Başlangıç tarihi',bt_end_date:'Bitiş tarihi',bt_capital:'Başlangıç sermayesi (USD)',bt_pos_size:'Pozisyon büyüklüğü (%)',
    bt_run:'Geri test başlat',bt_total_return:'Toplam getiri',bt_annual_return:'Yıllık getiri',bt_max_dd:'Maksimum drawdown',
    bt_sharpe:'Sharpe oranı',bt_win_rate:'Kazanma oranı',bt_trades:'Toplam işlem',bt_log_title:'İşlem günlüğü (son 20)',
    strar_macd:'MACD Trend takibi',strat_ema:'EMA Crossover',strat_rsi:'RSI Aşırı alım/aşırı satım',strat_grid:'Grid Ticareti',strat_bb:'Bollinger Kırılması',
    acc_title:'Hesabım',acc_plan:'Mevcut plan',acc_upgrade:'Yükselt',
    acc_broker:'Broker hesabı',acc_connect:'Broker bağla',
    acc_member_free:'Ücretsiz',acc_member_pro:'Pro Üye',acc_member_elite:'Elite Üye',
    acc_valid_until:'Geçerlilik',acc_reg_date:'Kayıt',acc_total_pnl:'Toplam P&L',
    acc_brokers_count:'Broker',acc_running_strats:'Aktif stratejiler',acc_account:'Hesap',
    acc_broker_section:'Bağlı brokerler',acc_subscription:'Aboneliğim',
    broker_connected:'Bağlı',broker_api_ok:'API OK',broker_not_connected:'Bağlı değil',broker_pending:'Beklemede',broker_add_new:'Broker ekle',
    btn_manage:'Yönet',btn_disconnect:'Bağlantıyı kes',btn_connect:'Bağla',btn_edit:'Düzenle',
    plan_current:'Mevcut',per_month:'/ay',plan_view_all:'Tüm planları gör →',
    plan_basic_f1:'Tüm piyasa verileri',plan_basic_f2:'AI Soru-Cevap',plan_basic_f3:'2 strateji',plan_basic_f4:'Otomatik ticaret',
    plan_pro_f1:'Sınırsız strateji',plan_pro_f2:'AI Otomatik ticaret',plan_pro_f3:'Gelişmiş geri test',plan_pro_f4:'Çoklu broker',
    plan_elite_f1:'Otomatik aç (Signal/DCA/Copy)',plan_elite_f2:'Sınırsız kopyalama ticareti',plan_elite_f3:'VIP desteği',plan_elite_f4:'Öncelikli işlem',
    risk_title:'Risk kontrolleri',risk_max_loss:'Günlük maksimum kayıp',risk_max_loss_desc:'Aşılırsa otomatik dur',
    risk_max_pos:'Maksimum pozisyon büyüklüğü',risk_max_pos_desc:'Sembol başına, toplam varlık %',
    risk_auto_order:'AI otomatik emir',risk_auto_order_desc:'Strateji tetiklendiğinde AI işlem yapar',
    risk_notify:'Ön emir bildirimi',risk_notify_desc:'Her işlemden önce onay gönder',
    risk_night:'Gece koruma modu',risk_night_desc:'22:00-07:00 otomatik ticareti durdur',
    confirm:'Onayla',cancel:'İptal',save:'Kaydet',close:'Kapat',
    loading:'Yükleniyor...',success:'Başarılı',error:'Hata',
    lang_switched:'🌐 Türkçe\'ye geçildi',
    tlog_title:'İşlem günlüğü',tlog_all:'Tümü',tlog_buy:'Long',tlog_sell:'Short',tlog_win:'Kar',tlog_loss:'Zarar',
    tlog_total_trades:'İşlemler',tlog_win_rate:'Kazanma oranı',tlog_net_pnl:'Net P&L',tlog_avg_hold:'Ortalama tutma',tlog_best:'En iyi işlem',tlog_worst:'En kötü işlem',
    tlog_col_time:'Zaman',tlog_col_symbol:'Sembol',tlog_col_dir:'Yön',tlog_col_open:'Giriş',tlog_col_close:'Çıkış',tlog_col_size:'Lot',tlog_col_pnl:'P&L',tlog_col_hold:'Süre',
    tlog_dir_long:'Long',tlog_dir_short:'Short',tlog_empty:'İşlem kaydı yok',
    nav_copy:'Kopyalama Ticareti',copy_title:'Kopyalama Ticareti',copy_subtitle:'En iyi tacirleri takip et, gerçek zamanlı sinyaller',
    copy_goto_auto:'Otomatik ayarlar',copy_my_follows:'Takiplerim',copy_leaderboard:'Sinyal lider tablosu',
    copy_filter_all:'Tümü',copy_filter_crypto:'Kripto',copy_filter_forex:'Forex',copy_filter_stable:'DD düşük',
    copy_followers:'takipçi',copy_monthly:'Aylık',copy_winrate:'Kazanma oranı',copy_maxdd:'Maks DD',copy_30pnl:'30G P&L',
    copy_follow_btn:'Takip et',copy_following:'✓ Takip ediliyor',copy_unfollow:'Takibi bırak',copy_detail_btn:'Detay',
    copy_pnl:'Yüzen P&L',copy_since:'Beriberi',copy_follow_title:'Takip ayarları',copy_confirm_follow:'Onayla',
    copy_toast_follow:'Takip başladı',copy_toast_unfollow:'Takip bırakıldı',
    ct_tag_ct1:'BTC/ETH uzmanı · 3 yıl',ct_tag_ct2:'Altın/Forex · 5 yıl',ct_tag_ct3:'Düşük DD stabil · 4 yıl',
    ct_tag_ct4:'Gece scalper · 2 yıl',ct_tag_ct5:'Çoklu makro · 6 yıl',ct_tag_ct6:'DCA+Trend · 7 yıl',
    nav_autoopen:'Otomatik Aç',ao_title:'Otomatik Aç',ao_subtitle:'3 akıllı otomatik giriş modu',
    ao_lock_title:'Otomatik Aç Elite\'ye özel',ao_lock_desc:'Otomatik girişi açmak için Elite\'ye yükselt',
    ao_lock_btn:'Yükselt $199/ay',
    ao_mode_signal:'Sinyal tetikleyici',ao_mode_signal_desc:'RSI/MACD/EMA koşulları karşılandığında otomatik giriş',
    ao_mode_dca:'Tekrarlayan DCA',ao_mode_dca_desc:'Ortalama maliyet için periyodik otomatik alım',
    ao_mode_copy:'Kopyalama senkron',ao_mode_copy_desc:'Sinyal kaynağının her girişini yansıt',
    ao_running:'Çalışıyor',
    ao_signal_cfg:'Sinyal yapılandırması',ao_signal_ind:'Indicator',ao_signal_pair:'Sembol',
    ao_dca_cfg:'DCA yapılandırması',ao_dca_pair:'Sembol',ao_dca_freq:'Frekans',
    ao_dca_hourly:'Her saat',ao_dca_daily:'Günlük',ao_dca_weekly:'Haftalık',ao_dca_monthly:'Aylık',
    ao_dca_amount:'Giriş başına tutar (USD)',ao_dca_total:'Toplam limit (USD)',ao_dca_price_drop:'Düşerse ikiye katla (%)',ao_dca_exit:'Take Profit (%)',
    ao_dca_invested:'Yatırıldı',
    ao_copy_cfg:'Kopyalama yapılandırması',ao_copy_source:'Sinyal kaynağı',ao_copy_select:'Seç',
    ao_copy_ratio:'Oran',ao_copy_max:'İşlem başına maks (USD)',ao_copy_daily_loss:'Günlük kayıp limiti (USD)',
    ao_copy_filter:'Yön filtresi',ao_copy_all:'Long & Short',ao_copy_long_only:'Sadece Long',ao_copy_short_only:'Sadece Short',
    ao_copy_pairs:'Sembol sınırla',ao_copy_pairs_ph:'BTC,ETH (boş=hepsi)',ao_not_following:'Takip etmiyor',
    ao_pos_size:'Pozisyon büyüklüğü (USD)',ao_sl:'Stop Loss (%)',ao_tp:'Take Profit (%)',ao_max_pos:'Maks açık pozisyon',
    lb_tab_roi:'Aylık ROI',lb_tab_wr:'Kazanma oranı',lb_tab_stable:'En stabil',lb_tab_new:'Yeni',
    nav_square:'Ticaret Alanı',sq_title:'Ticaret Alanı',sq_subtitle:'Görüşlerini paylaş, duyguları keşfet, global tüccarlarla senkronize et',
    sq_post_ph:'Piyasa görüşün, ticaret mantığı, pozisyon analizi paylaş...',sq_post_btn:'Paylaş',
    sq_filter_all:'Tümü',sq_filter_bull:'Boğa',sq_filter_bear:'Ayı',sq_filter_hot:'Popüler',
    sq_pair_label:'Çift',sq_sentiment_label:'Duygu',
    nav_stratmarket:'Strateji Pazarı',sm_title:'Strateji Pazarı',sm_subtitle:'En iyi quantitative stratejileri keşfet, paylaş & kopya et',
    sm_upload_title:'Stratejimi yayınla',sm_upload_btn:'Strateji yükle',sm_filter_all:'Tümü',
    sm_filter_trend:'Trend',sm_filter_grid:'Grid',sm_filter_quant:'Quant',sm_filter_arb:'Arb',
    sm_name_label:'Strateji adı',sm_asset_label:'Sembol',sm_price_label:'Fiyat (USD/ay, 0=Ücretsiz)',
    sm_code_label:'Strateji kodu',sm_submit_btn:'İnceleme için gönder',sm_backtest:'Geri test',
    sm_copy:'Kopya',sm_subscribe:'Abone ol',
    nav_signals:'Sinyal Yayını',sig_title:'Sinyal Yayını',sig_subtitle:'Canlı ticaret sinyalleri, 1 tıkla abonelik, otomatik aç\'a bağlan',
    sig_publish_title:'Ticaret sinyali yayınla',sig_tab_live:'Canlı sinyaller',sig_tab_sources:'Sinyal kaynakları',sig_tab_history:'Geçmiş',
    sig_pair:'Çift',sig_dir:'Yön',sig_dir_buy:'Al',sig_dir_sell:'Sat',
    sig_entry:'Giriş',sig_sl:'Stop Loss',sig_tp1:'TP1',sig_tp2:'TP2',
    sig_desc:'Sinyal notu',sig_publish_btn:'Sinyal yayınla',
    sig_follow:'Sinyali takip et',sig_share:'Paylaş',sig_subscribe_bc:'Kaynağa abone ol',
    ao_start:'Otomatik aç başlat',ao_stop:'Dur',ao_status_off:'● Durdu',ao_status_on:'🟢 Çalışıyor',
    ao_started:'Başlatıldı',ao_stopped:'Durduruldu',
    ao_exec_log:'İşlem günlüğü',ao_clear_log:'Temizle',ao_log_empty:'Kayıt yok',
    toast_elite_unlocked:'Elite açıldı! Otomatik aç artık mevcut',
    dash_brief_title:'AI Günlük Brifing',dash_brief_time:'08:00 güncelleme',
    dash_brief_content:'Altın bugün boğa, Fed güvercin sinyalleri destekliyor, hedef $2,380. BTC $84,000\'de dirençle karşılaşıyor, kısa vade dikkatli. Nasdaq tech sonuçlarıyla yönlendiriliyor, genel olarak güçlü. EUR/USD zayıf salınım, USD endeksi 104.2 destek.',
    dash_signal_gold:'Altın ▲ Boğa',dash_signal_btc:'BTC ⚠ İzle',dash_signal_eur:'EUR/USD ▼ Zayıf',dash_signal_nas:'Nasdaq ▲ Güçlü',
    dash_quick_ops:'Hızlı işlemler',dash_btn_order:'AI Emir',dash_btn_backtest:'Hızlı geri test',dash_btn_positions:'Pozisyonları gör',
    ai_welcome_greet:'Merhaba! Ben QuantAI asistanıyım 🧠',ai_welcome_intro:'Ticaret fikirlerini bana anlat ve yardımcı olayım:',
    modal_symbol:'Sembol',modal_dir:'Yön',modal_amount:'Tutar (USD)',modal_leverage:'Kaldıraç',
    modal_sl:'Stop Loss (%)',modal_tp:'Take Profit (%)',modal_margin:'Tahmini marj',modal_max_profit:'Maks kar',modal_max_loss:'Maks zarar',
    broker_modal_title:'Broker bağla',broker_connect_btn:'Doğrula & bağla',
    cat_crypto:'Kripto',cat_forex_metals:'Forex / Metaller',cat_all_cfd:'Tüm CFD\'ler',
    sym_btc:'Bitcoin',sym_eth:'Ethereum',sym_sol:'Solana',sym_bnb:'BNB',sym_xrp:'Ripple',
    sym_eurusd:'EUR/USD',sym_gbpusd:'GBP/USD',sym_usdjpy:'USD/JPY',sym_usdchf:'USD/CHF',sym_audusd:'AUD/USD',
    sym_gold:'Spot Altın',sym_silver:'Spot Gümüş',sym_wti:'WTI Ham',sym_brent:'Brent Ham',
    sym_nas100:'Nasdaq 100',sym_spx500:'S&P 500',sym_dow:'Dow Jones',sym_hsi:'Hang Seng',
    strat_name_1:'BTC MACD Trend',strat_name_2:'Altın Grid',strat_name_3:'EUR/USD EMA Stratejisi',strat_name_4:'Nasdaq Scalping',
    strat_type_trend:'Trend takibi',strat_type_grid:'Grid Ticareti',strat_type_ema:'EMA Crossover',strat_type_mr:'Ortalama dönüşü',
    toast_order_ok:'Emir verildi!',toast_submitted:'Gönderildi!',toast_pos_closed:'Pozisyon kapatıldı',toast_all_closed:'Tüm pozisyonlar kapatıldı',
    toast_strat_started:'başlatıldı',toast_strat_paused:'durdu',toast_strat_deleted:'strateji silindi',
    toast_broker_connected:'Broker bağlandı! API doğrulandı',toast_coming_soon:'Çok yakında',
    toast_upgrading:'Yönlendiriliyor',toast_view_plans:'Tüm planları gör',
    confirm_close_pos:'Kapatmayı onayla',confirm_close_all:'Tüm pozisyonları kapat? Geri alınamaz!',confirm_del_strat:'Strateji sil',
    bt_running:'Çalışıyor...',
    ai_analyze_suffix:' pozisyonum nasıl?',
    ai_placeholder:'Ticaret talimatınızı veya sorunuzu girin…',
    ai_resp_btc:'📊 BTC/USDT Analizi:\n\nFiyat $83,400 civarında, $84,000\'de direnç. MACD golden cross, RSI(14) 58\'de — boğa ama aşırı alınmamış.\n\nÖneri: $82,800 destek yakın küçük long, $81,000\'de stop, $86,000 hedef. R/R ≈ 1:2.2.',
    ai_resp_gold:'🥇 Altın (XAU/USD) Analizi:\n\nAltın $2,342\'de güçlü kalmaya devam ediyor. Fed güvercin sinyalleri ve zayıf dolar destek sağlıyor. Kısa vade hedef $2,380, kritik destek $2,310.\n\nÖneri: Longları tut, kârı kilitlemek için stop\'u $2,320\'ye taşı.',
    ai_resp_position:'📐 Pozisyon yönetimi ($1,000 sermaye):\n\n• BTC/USDT: 30% ($300) — Ana pozisyon, 5x kaldıraç\n• XAU/USD: 25% ($250) — Koruma, 10x\n• EUR/USD: 20% ($200) — FX koruması\n• Nakit: 25% ($250) — Fırsat bekle\n\nİşlem başına maks zarar: 3%.',
    ai_resp_strategy:'⚡ Mevcut piyasa için 3 strateji:\n\n1. **BTC MACD Trend** — 67% kazanma oranı, +89% yıllık\n2. **Altın Grid** — Yatay piyasalar için, 3-5%/ay\n3. **EUR/USD EMA** — Düşük risk, yeni başlayanlar için uygun\n\nBiri aktif etmemi ister misiniz?',
    ai_resp_default:'Talebinizi anladım. Mevcut piyasa koşullarını analiz edeyim...\n\n📊 Piyasa genel olarak boğa ama Fed politika risklerine dikkat. Pozisyonları %50\'nin altında tutun ve her zaman stop koyun.\n\nKeşfetmek istediğiniz belirli bir sembol veya strateji var mı?',
  },
};

// 当前语言
let _currentLang = localStorage.getItem('qlang') || 'zh';

// 获取翻译文本
function t(key){ return (I18N[_currentLang] || I18N.zh)[key] || key; }

// 应用翻译到页面
function applyLang(lang){
  _currentLang = lang;
  // 先恢复导航图标（防止被旧逻辑污染）
  document.querySelectorAll('.ni[data-nav-icon]').forEach(el => {
    el.textContent = el.getAttribute('data-nav-icon');
  });
  // 带 data-i18n 属性的元素自动替换
  // 注意：只替换「本身是叶节点」或「INPUT/TEXTAREA」，避免覆盖子元素
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const val = t(key);
    // 找不到翻译时t()会返回key本身，此时跳过，防止key字符串被渲染到页面
    if(!val || val === key) return;
    if(el.tagName === 'INPUT' || el.tagName === 'TEXTAREA'){
      el.placeholder = val;
    } else if(el.tagName === 'OPTION'){
      el.textContent = val;
    } else {
      // 只有没有子元素节点时才直接 textContent，否则只替换 Text 子节点
      const hasChildElements = Array.from(el.childNodes).some(n => n.nodeType === 1);
      if(!hasChildElements){
        el.textContent = val;
      } else {
        // 有子元素：只替换直接文本节点（不影响子 span）
        Array.from(el.childNodes).forEach(node => {
          if(node.nodeType === 3 && node.textContent.trim()){
            // 跳过：含子元素的容器保持原样，由各子span自己的data-i18n处理
          }
        });
        // 如果此元素自身没有子span负责翻译，强制更新文本节点
        const childSpans = el.querySelectorAll('[data-i18n]');
        if(childSpans.length === 0) el.textContent = val;
      }
    }
  });
  // 搜索框 placeholder 单独处理
  const searchInput = document.querySelector('.search-input');
  if(searchInput) searchInput.placeholder = t('search_placeholder');
  // html lang 属性
  document.documentElement.lang = lang;
  document.documentElement.dir = (lang === 'ar') ? 'rtl' : 'ltr';
  // 重渲染动态内容（持仓卡片、策略卡片、行情表格已用t()，需重新生成HTML）
  if(typeof renderPositions === 'function') renderPositions();
  if(typeof renderStrategies === 'function') renderStrategies();
  if(typeof renderCopyPage === 'function') renderCopyPage(); // renderCopyPage内部会调用updateCopySourceSelect
  if(typeof updateCopySourceSelect === 'function') updateCopySourceSelect(); // 额外确保autoopen下拉框也更新
  if(typeof initAutoOpen === 'function') initAutoOpen(); // 无条件重渲染autoopen（确保placeholder和下拉框始终更新）
  if(typeof renderMarket === 'function'){
    // 更健壮的 cat 获取方式
    let cat = 'all';
    const activeTab = document.querySelector('.mkt-tab.active');
    if(activeTab){
      const onclickStr = activeTab.getAttribute('onclick') || '';
      const m = onclickStr.match(/filterMarket\(['"](\w+)['"]/);
      if(m) cat = m[1];
    }
    renderMarket(cat);
  }
  // 同步 AI 欢迎语
  const welcomeBubble = document.getElementById('ai-welcome-bubble');
  if(welcomeBubble && document.getElementById('ai-welcome-msg')){
    welcomeBubble.innerHTML =
      `<span>${t('ai_welcome_greet')}</span><br>`+
      `<span>${t('ai_welcome_intro')}</span>`+
      `<ul style="margin-top:8px;padding-left:16px;display:flex;flex-direction:column;gap:4px;font-size:13px;color:var(--muted)">`+
      `<li>${t('ai_feat1')}</li><li>${t('ai_feat2')}</li><li>${t('ai_feat3')}</li><li>${t('ai_feat4')}</li></ul>`;
  }
  // 同步 chat suggestions
  document.querySelectorAll('.sugg[data-i18n]').forEach(el => {
    el.textContent = t(el.getAttribute('data-i18n'));
  });
  // 同步 chat input placeholder
  const chatInput = document.getElementById('chat-input');
  if(chatInput) chatInput.placeholder = t('ai_placeholder')||'Type a message...';
  // 同步页面标题（强制更新，不依赖条件）
  const titleEl = document.getElementById('page-title');
  if(titleEl){
    const activePage = window._currentPage || 'dashboard';
    const titleKey2 = 'page_' + activePage;
    const translated = t(titleKey2);
    // 有翻译就用翻译，没有就用中文pageTitles，再没有就用中文字典zh兜底，绝不显示key或name
    if(translated && translated !== titleKey2){
      titleEl.textContent = translated;
    } else {
      const zhTitle = (I18N.zh||{})[titleKey2];
      titleEl.textContent = zhTitle || pageTitles[activePage] || activePage;
    }
  }
}

function changeLang(v){
  // 不支持的语言 fallback 到 zh
  if(!I18N[v]) v = 'zh';
  localStorage.setItem('qlang', v);
  // 阿拉伯语启用 RTL
  document.documentElement.dir = (v === 'ar') ? 'rtl' : 'ltr';
  document.getElementById('lang-select').value = v;
  applyLang(v);
  toast(t('lang_switched'), 'success');
}
// ===================================================
// ===== 复制交易 =====
// ===================================================
const COPY_TRADERS = [
  {id:'ct1', name:'AlphaWolf', av:'🐺', tagKey:'ct_tag_ct1', wr:78.4, monthly:+24.6, dd:-8.2, followers:1842, category:'crypto', pnl30:+12400},
  {id:'ct2', name:'GoldHunter', av:'🦁', tagKey:'ct_tag_ct2', wr:71.2, monthly:+18.3, dd:-5.6, followers:2310, category:'forex', pnl30:+8700},
  {id:'ct3', name:'SteadyHands', av:'🐢', tagKey:'ct_tag_ct3', wr:65.8, monthly:+11.2, dd:-3.1, followers:3290, category:'stable', pnl30:+5200},
  {id:'ct4', name:'NightScalper', av:'🦅', tagKey:'ct_tag_ct4', wr:82.1, monthly:+31.0, dd:-14.8, followers:987, category:'crypto', pnl30:+18900},
  {id:'ct5', name:'MacroTrader', av:'🌍', tagKey:'ct_tag_ct5', wr:69.3, monthly:+15.8, dd:-6.4, followers:4120, category:'forex', pnl30:+7600},
  {id:'ct6', name:'ZenInvestor', av:'🎋', tagKey:'ct_tag_ct6', wr:61.5, monthly:+8.9, dd:-2.3, followers:5670, category:'stable', pnl30:+4100},
];
let _myFollows = {}; // {traderId: {ratio, maxPerTrade, pnl, since}}

function filterCopy(cat, btn){
  document.querySelectorAll('#copy-trader-list').forEach(()=>{});
  document.querySelectorAll('.tlog-filter-btn').forEach(b=>b.classList.remove('active'));
  if(btn) btn.classList.add('active');
  renderCopyTraders(cat);
}

function renderCopyPage(){
  renderMyFollows();
  renderCopyTraders('all');
  updateCopySourceSelect();
}

function renderMyFollows(){
  const sec = document.getElementById('copy-my-section');
  const list = document.getElementById('copy-my-list');
  const cnt  = document.getElementById('copy-my-count');
  const keys = Object.keys(_myFollows);
  if(!keys.length){ sec.style.display='none'; return; }
  sec.style.display='';
  if(cnt) cnt.textContent = `(${keys.length})`;
  list.innerHTML = keys.map(tid=>{
    const tr = COPY_TRADERS.find(c=>c.id===tid);
    const f  = _myFollows[tid];
    if(!tr) return '';
    const pnlStr = (f.pnl>=0?'+':'')+`$${f.pnl.toFixed(2)}`;
    const pnlCls = f.pnl>=0?'up':'down';
    return `<div class="my-follow-card">
      <div class="copy-av" style="width:38px;height:38px;font-size:16px">${tr.av}</div>
      <div class="mfc-info">
        <div class="mfc-name">${tr.name}</div>
        <div class="mfc-pnl ${pnlCls}">${t('copy_pnl')||'浮盈'}: ${pnlStr}</div>
        <div class="mfc-ratio">×${f.ratio} · ${t('copy_since')||'跟随自'} ${f.since}</div>
      </div>
      <div style="display:flex;gap:8px">
        <button class="btn btn-outline" style="font-size:12px;padding:5px 10px" onclick="showCopyDetail('${tid}')" data-i18n="copy_detail_btn">${t('copy_detail_btn')||'详情'}</button>
        <button class="btn btn-danger" style="font-size:12px;padding:5px 10px" onclick="unfollowTrader('${tid}')">${t('copy_unfollow')||'取消跟随'}</button>
      </div>
    </div>`;
  }).join('');
}

function renderCopyTraders(cat){
  const list = document.getElementById('copy-trader-list');
  if(!list) return;
  const traders = cat==='all' ? COPY_TRADERS : COPY_TRADERS.filter(c=>c.category===cat);
  list.innerHTML = traders.map(tr=>{
    const isFollowing = !!_myFollows[tr.id];
    const btnHtml = isFollowing
      ? `<button class="btn btn-outline" style="font-size:12px;padding:6px 12px;min-width:84px" onclick="unfollowTrader('${tr.id}')">${t('copy_following')||'✓ 已跟随'}</button>`
      : `<button class="btn btn-primary" style="font-size:12px;padding:6px 12px;min-width:84px" onclick="showFollowModal('${tr.id}')">${t('copy_follow_btn')||'跟单'}</button>`;
    const mrCls = tr.monthly>=0 ? 'up' : 'down';
    return `<div class="copy-trader-card">
      <div class="copy-av">${tr.av}</div>
      <div class="copy-info">
        <div class="copy-name">${tr.name}</div>
        <div class="copy-tag">${t(tr.tagKey)||tr.tagKey} · ${tr.followers.toLocaleString()} ${t('copy_followers')||'人跟随'}</div>
        <div class="copy-stats">
          <div class="copy-stat"><div class="copy-stat-val ${mrCls}">${tr.monthly>0?'+':''}${tr.monthly}%</div><div class="copy-stat-lbl">${t('copy_monthly')||'月收益'}</div></div>
          <div class="copy-stat"><div class="copy-stat-val">${tr.wr}%</div><div class="copy-stat-lbl">${t('copy_winrate')||'胜率'}</div></div>
          <div class="copy-stat"><div class="copy-stat-val down">${tr.dd}%</div><div class="copy-stat-lbl">${t('copy_maxdd')||'最大回撤'}</div></div>
          <div class="copy-stat"><div class="copy-stat-val">+$${tr.pnl30.toLocaleString()}</div><div class="copy-stat-lbl">${t('copy_30pnl')||'近30天盈利'}</div></div>
        </div>
      </div>
      <div class="copy-actions">${btnHtml}<button class="btn btn-outline" style="font-size:12px;padding:6px 12px" onclick="showCopyDetail('${tr.id}')">${t('copy_detail_btn')||'Details'}</button></div>
    </div>`;
  }).join('');
}

function showFollowModal(tid){
  const tr = COPY_TRADERS.find(c=>c.id===tid); if(!tr) return;
  const html = `<div class="modal-title">🔁 ${t('copy_follow_title')||'跟单设置'} — ${tr.name} <span class="modal-close" onclick="closeModal('copy-follow-modal')">✕</span></div>
    <div style="background:var(--card2);border-radius:12px;padding:14px;margin-bottom:16px;display:flex;gap:16px;align-items:center">
      <div class="copy-av" style="width:42px;height:42px;font-size:18px">${tr.av}</div>
      <div><div style="font-weight:700">${tr.name}</div><div style="font-size:12px;color:var(--muted)">${t('copy_winrate')||'胜率'} ${tr.wr}% · ${t('copy_monthly')||'月收益'} ${tr.monthly>0?'+':''}${tr.monthly}%</div></div>
    </div>
    <div class="form-grid" style="margin-bottom:16px">
      <div class="form-group"><label>${t('ao_copy_ratio')||'跟单倍数'}</label><select id="cfm-ratio"><option value="0.1">0.1x</option><option value="0.25">0.25x</option><option value="0.5" selected>0.5x</option><option value="1">1.0x</option><option value="2">2.0x</option></select></div>
      <div class="form-group"><label>${t('ao_copy_max')||'单笔最大 (USD)'}</label><input type="number" id="cfm-max" value="300" min="10"></div>
      <div class="form-group"><label>${t('ao_copy_daily_loss')||'日亏损保护 (USD)'}</label><input type="number" id="cfm-dloss" value="150" min="0"></div>
      <div class="form-group"><label>${t('ao_copy_filter')||'只跟方向'}</label><select id="cfm-filter"><option value="all">${t('ao_copy_all')||'多空均跟'}</option><option value="buy">${t('ao_copy_long_only')||'只跟做多'}</option><option value="sell">${t('ao_copy_short_only')||'只跟做空'}</option></select></div>
    </div>
    <button class="btn btn-primary" style="width:100%" onclick="confirmFollow('${tid}')">🔁 ${t('copy_confirm_follow')||'确认跟单'}</button>`;
  let modal = document.getElementById('copy-follow-modal');
  if(!modal){
    modal = document.createElement('div');
    modal.className='modal-overlay'; modal.id='copy-follow-modal';
    modal.innerHTML=`<div class="modal copy-modal" id="copy-follow-modal-inner"></div>`;
    document.body.appendChild(modal);
    modal.addEventListener('click',e=>{ if(e.target===modal) closeModal('copy-follow-modal'); });
  }
  modal.querySelector('#copy-follow-modal-inner').innerHTML = html;
  modal.classList.add('active');
}

function confirmFollow(tid){
  const ratio = parseFloat(document.getElementById('cfm-ratio')?.value||0.5);
  const max   = parseFloat(document.getElementById('cfm-max')?.value||300);
  const dloss = parseFloat(document.getElementById('cfm-dloss')?.value||150);
  _myFollows[tid] = { ratio, max, dloss, pnl: (Math.random()-.3)*800, since: new Date().toISOString().slice(0,10) };
  closeModal('copy-follow-modal');
  toast(`✅ ${t('copy_toast_follow')||'已开始跟单'} ${COPY_TRADERS.find(c=>c.id===tid)?.name}`, 'success');
  renderMyFollows();
  renderCopyTraders('all');
  updateCopySourceSelect();
}

function unfollowTrader(tid){
  const tr = COPY_TRADERS.find(c=>c.id===tid);
  delete _myFollows[tid];
  toast(`${t('copy_toast_unfollow')||'已取消跟随'} ${tr?.name||''}`, '');
  renderMyFollows();
  renderCopyTraders('all');
  updateCopySourceSelect();
}

function showCopyDetail(tid){
  const tr = COPY_TRADERS.find(c=>c.id===tid); if(!tr) return;
  toast(`📊 ${tr.name} — ${t('copy_monthly')||'月收益'} ${tr.monthly>0?'+':''}${tr.monthly}% · ${t('copy_winrate')||'胜率'} ${tr.wr}%`, 'success');
}

function updateCopySourceSelect(){
  const sel = document.getElementById('ao-copy-source'); if(!sel) return;
  const follows = Object.keys(_myFollows);
  sel.innerHTML = `<option value="">-- ${t('ao_copy_select')||'选择信号源'} --</option>` +
    COPY_TRADERS.map(tr=>`<option value="${tr.id}" ${follows.includes(tr.id)?'':'disabled style="color:var(--muted)"'}>${tr.av} ${tr.name}${follows.includes(tr.id)?'':' ('+t('ao_not_following')+')'}</option>`).join('');
}

// ===================================================
// ===== 排行榜升级 + 交易员详情面板 =====
// ===================================================

// 排行榜 Mock 扩展数据
const LB_EXTRA = {
  t1:{ bio:'专注BTC/ETH趋势交易，5年经验，年化稳定120%+', trades30:87, avgHold:'4.2h', bestTrade:'+$12,400', totalFollowers:3241, pnlHistory:[12,18,9,22,15,28,11,33,25,19] },
  t2:{ bio:'量化策略+手动复盘双轨制，擅长低回撤稳增长', trades30:134, avgHold:'1.8h', bestTrade:'+$8,200', totalFollowers:2108, pnlHistory:[8,11,6,14,10,17,9,13,16,12] },
  t3:{ bio:'宏观驱动型，重仓ETH生态，押注大级别行情', trades30:52, avgHold:'12.5h', bestTrade:'+$31,600', totalFollowers:1876, pnlHistory:[20,35,8,42,18,55,12,38,29,44] },
  t4:{ bio:'外汇老手转型加密，纪律严明，连续9个月盈利', trades30:203, avgHold:'0.9h', bestTrade:'+$4,100', totalFollowers:987, pnlHistory:[5,7,4,9,6,8,5,10,7,8] },
  t5:{ bio:'新锐交易员，以数据驱动选标，擅长震荡行情', trades30:76, avgHold:'3.1h', bestTrade:'+$6,800', totalFollowers:654, pnlHistory:[14,10,18,12,22,9,16,20,11,17] },
};

// 当前排行榜排序类型
let _lbSort = 'roi';

function switchLbTab(sort, el){
  _lbSort = sort;
  document.querySelectorAll('.lb-tab').forEach(b => b.classList.remove('active'));
  if(el) el.classList.add('active');
  let sorted = [...COPY_TRADERS];
  if(sort === 'roi')     sorted.sort((a,b) => b.monthly - a.monthly);
  if(sort === 'winrate') sorted.sort((a,b) => b.wr - a.wr);
  if(sort === 'stable')  sorted.sort((a,b) => a.dd - b.dd);
  if(sort === 'new')     sorted.sort((a,b) => a.id.localeCompare(b.id));
  renderLbList(sorted);
}

function renderLbList(traders){
  const list = document.getElementById('copy-trader-list');
  if(!list) return;
  list.innerHTML = traders.map((tr, idx) => {
    const isFollowing = !!_myFollows[tr.id];
    const mrCls = tr.monthly >= 0 ? 'up' : 'down';
    const medal = idx === 0 ? '\u{1F947}' : idx === 1 ? '\u{1F948}' : idx === 2 ? '\u{1F949}' : '<span style="color:var(--muted);font-size:13px">#'+(idx+1)+'</span>';
    const followBtn = isFollowing
      ? '<button class="btn btn-outline" style="font-size:12px;padding:5px 14px" onclick="unfollowTrader(\\'' + tr.id + '\\')">&#x2713; ' + (t('copy_following')||'已跟随') + '</button>'
      : '<button class="btn btn-primary" style="font-size:12px;padding:5px 14px" onclick="showFollowModal(\\'' + tr.id + '\\')">跟单</button>';
    return '<div class="lb-rank-row" onclick="openTraderDetail(\\'' + tr.id + '\\')">'
      + '<div class="lb-medal">' + medal + '</div>'
      + '<div class="copy-av" style="width:40px;height:40px;font-size:17px;flex-shrink:0">' + tr.av + '</div>'
      + '<div class="lb-info">'
        + '<div class="lb-name">' + tr.name + (isFollowing ? ' <span style="font-size:11px;background:var(--green);color:var(--dark);border-radius:8px;padding:1px 7px">跟随中</span>' : '') + '</div>'
        + '<div style="font-size:12px;color:var(--muted)">' + (t(tr.tagKey)||tr.tagKey) + ' &middot; ' + tr.followers.toLocaleString() + ' ' + (t('copy_followers')||'人跟随') + '</div>'
      + '</div>'
      + '<div class="lb-stats">'
        + '<div class="lb-stat-item"><span class="' + mrCls + '" style="font-weight:700;font-size:15px">' + (tr.monthly>0?'+':'') + tr.monthly + '%</span><span style="font-size:11px;color:var(--muted)">月收益</span></div>'
        + '<div class="lb-stat-item"><span style="font-weight:600">' + tr.wr + '%</span><span style="font-size:11px;color:var(--muted)">胜率</span></div>'
        + '<div class="lb-stat-item"><span class="down" style="font-weight:600">' + tr.dd + '%</span><span style="font-size:11px;color:var(--muted)">回撤</span></div>'
      + '</div>'
      + '<div onclick="event.stopPropagation()">' + followBtn + '</div>'
    + '</div>';
  }).join('');
}

function openTraderDetail(tid){
  const tr = COPY_TRADERS.find(c => c.id === tid); if(!tr) return;
  const ex = LB_EXTRA[tid] || {};
  const isFollowing = !!_myFollows[tid];
  const mrCls = tr.monthly >= 0 ? 'up' : 'down';
  const overlay = document.getElementById('tdp-overlay');
  const panel   = document.getElementById('trader-detail-panel');
  if(!overlay || !panel) return;

  // 迷你收益折线（SVG）
  const pts = ex.pnlHistory || [5,10,8,15,12,20,9,18,22,25];
  const max = Math.max(...pts), min = Math.min(...pts);
  const svgW = 220, svgH = 52;
  const toX = (i) => (i / (pts.length-1)) * svgW;
  const toY = (v) => svgH - ((v - min) / (max - min + 1)) * (svgH - 8) - 4;
  const polyline = pts.map((v,i) => toX(i)+','+toY(v)).join(' ');
  const circles  = pts.map((v,i) => '<circle cx="'+toX(i)+'" cy="'+toY(v)+'" r="3" fill="var(--green)"/>').join('');

  panel.innerHTML =
    '<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px">'
      + '<div style="display:flex;gap:12px;align-items:center">'
        + '<div class="copy-av" style="width:48px;height:48px;font-size:22px">' + tr.av + '</div>'
        + '<div><div style="font-size:17px;font-weight:800">' + tr.name + '</div>'
        + '<div style="font-size:12px;color:var(--muted)">' + (t(tr.tagKey)||tr.tagKey) + '</div></div>'
      + '</div>'
      + '<button onclick="closeTraderDetail()" style="background:none;border:none;color:var(--muted);font-size:20px;cursor:pointer">&times;</button>'
    + '</div>'
    + '<div style="font-size:13px;color:var(--text2);margin-bottom:16px;line-height:1.6">' + (ex.bio||'专业交易员') + '</div>'
    + '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px">'
      + '<div class="stat-card"><div class="stat-val ' + mrCls + '">' + (tr.monthly>0?'+':'') + tr.monthly + '%</div><div class="stat-lbl">月收益</div></div>'
      + '<div class="stat-card"><div class="stat-val">' + tr.wr + '%</div><div class="stat-lbl">胜率</div></div>'
      + '<div class="stat-card"><div class="stat-val down">' + tr.dd + '%</div><div class="stat-lbl">最大回撤</div></div>'
      + '<div class="stat-card"><div class="stat-val">' + (ex.trades30||'--') + '</div><div class="stat-lbl">近30天交易</div></div>'
      + '<div class="stat-card"><div class="stat-val">' + (ex.avgHold||'--') + '</div><div class="stat-lbl">平均持仓</div></div>'
      + '<div class="stat-card"><div class="stat-val up">' + (ex.bestTrade||'--') + '</div><div class="stat-lbl">最佳单笔</div></div>'
    + '</div>'
    + '<div style="margin-bottom:16px">'
      + '<div style="font-size:12px;color:var(--muted);margin-bottom:6px">近10次收益趋势</div>'
      + '<svg width="' + svgW + '" height="' + svgH + '" style="overflow:visible">'
        + '<polyline points="' + polyline + '" fill="none" stroke="var(--green)" stroke-width="2" stroke-linejoin="round"/>'
        + circles
      + '</svg>'
    + '</div>'
    + '<div style="display:flex;gap:10px">'
      + (isFollowing
        ? '<button class="btn btn-outline" style="flex:1" onclick="unfollowTrader(\\'' + tid + '\\');closeTraderDetail()">取消跟随</button>'
        : '<button class="btn btn-primary" style="flex:1" onclick="closeTraderDetail();showFollowModal(\\'' + tid + '\\')">&#x1F501; 开始跟单</button>'
      )
      + '<button class="btn btn-outline" style="flex:1" onclick="closeTraderDetail()">关闭</button>'
    + '</div>';

  overlay.classList.add('active');
  panel.classList.add('active');
}

function closeTraderDetail(){
  document.getElementById('tdp-overlay')?.classList.remove('active');
  document.getElementById('trader-detail-panel')?.classList.remove('active');
}

function initLbPage(){
  switchLbTab('roi', document.querySelector('.lb-tab.active'));
  renderMyFollows();
}

// ===================================================
// ===== 交易广场 =====
// ===================================================

// Mock 帖子数据
let _sqPosts = [
  { id:'sq1', uid:'u1', av:'🐂', name:'Alpha Bull', sentiment:'bull', pair:'BTC/USDT', content:'BTC突破前高，$72K确认！量能强劲，建议持仓等待$80K。MACD金叉+RSI未超买，底部抬升结构完整。', likes:234, comments:47, time:'10分钟前', tags:['BTC','突破','做多'] },
  { id:'sq2', uid:'u2', av:'🦊', name:'FoxQuant', sentiment:'bear', pair:'ETH/USDT', content:'ETH二次回踩$3200支撑失败，看空$2800。资金费率为负，多单在撤，小心拉高出货陷阱。', likes:178, comments:32, time:'28分钟前', tags:['ETH','做空','警惕'] },
  { id:'sq3', uid:'u3', av:'🎯', name:'Precision Pro', sentiment:'neutral', pair:'SOL/USDT', content:'SOL目前处于三角形整理，等待方向选择。$145支撑/$165压力，突破方向做方向，不提前押注。', likes:89, comments:15, time:'1小时前', tags:['SOL','整理','等待信号'] },
  { id:'sq4', uid:'u4', av:'🔥', name:'Degen King', sentiment:'bull', pair:'BNB/USDT', content:'BNB悄悄走强，关注$620突破。合约持仓量上升，机构在默默建仓。你们盯BTC，我盯BNB。', likes:156, comments:28, time:'2小时前', tags:['BNB','山寨行情','关注'] },
  { id:'sq5', uid:'u5', av:'📊', name:'DataMind', sentiment:'neutral', pair:'全市场', content:'昨日全市场总清算$4.2亿，多空各半。整体Greed指数77（贪婪），但链上大额转入交易所增加，谨慎。', likes:312, comments:63, time:'3小时前', tags:['市场情绪','数据','风控'] },
];

let _sqFilter = 'all';
let _sqMyLikes = new Set();

function renderSquare(filter){
  _sqFilter = filter || _sqFilter;
  document.querySelectorAll('.sq-filter-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.f === _sqFilter);
  });
  const feed = document.getElementById('sq-feed');
  if(!feed) return;
  let posts = [..._sqPosts];
  if(_sqFilter === 'bull')    posts = posts.filter(p => p.sentiment === 'bull');
  if(_sqFilter === 'bear')    posts = posts.filter(p => p.sentiment === 'bear');
  if(_sqFilter === 'hot')     posts = posts.sort((a,b) => b.likes - a.likes);
  feed.innerHTML = posts.map(p => {
    const sentMap = { bull:'🐂 看多', bear:'🐻 看空', neutral:'😐 中性' };
    const sentCls = { bull:'sq-sent-bull', bear:'sq-sent-bear', neutral:'sq-sent-neutral' };
    const liked = _sqMyLikes.has(p.id);
    return '<div class="sq-post">'
      + '<div class="sq-post-header">'
        + '<div class="copy-av" style="width:38px;height:38px;font-size:16px">' + p.av + '</div>'
        + '<div style="flex:1">'
          + '<div style="font-weight:700;font-size:14px">' + p.name + '</div>'
          + '<div style="font-size:12px;color:var(--muted)">' + p.time + ' &middot; <span style="color:var(--purple)">' + p.pair + '</span></div>'
        + '</div>'
        + '<span class="sq-sentiment ' + sentCls[p.sentiment] + '">' + sentMap[p.sentiment] + '</span>'
      + '</div>'
      + '<div class="sq-content">' + p.content + '</div>'
      + '<div class="sq-tags">' + p.tags.map(tag => '<span class="sq-tag">#' + tag + '</span>').join('') + '</div>'
      + '<div class="sq-actions">'
        + '<button class="sq-action ' + (liked ? 'liked' : '') + '" onclick="sqLike(\\'' + p.id + '\\')">'
          + (liked ? '&#x2764;' : '&#x1F90D;') + ' ' + (liked ? p.likes + 1 : p.likes)
        + '</button>'
        + '<button class="sq-action" onclick="sqComment(\\'' + p.id + '\\')">'
          + '&#x1F4AC; ' + p.comments
        + '</button>'
        + '<button class="sq-action" onclick="sqShare(\\'' + p.id + '\\')">'
          + '&#x1F517; 分享'
        + '</button>'
      + '</div>'
    + '</div>';
  }).join('');
}

function filterSquare(filter, el){
  _sqFilter = filter;
  renderSquare(filter);
}

function selectSqSentiment(val, el){
  document.querySelectorAll('.sq-sent-btn').forEach(b => b.classList.remove('active'));
  if(el) el.classList.add('active');
  document.getElementById('sq-sentiment-val').value = val;
}

function postSquare(){
  const content = document.getElementById('sq-content')?.value?.trim();
  const sentiment = document.getElementById('sq-sentiment-val')?.value || 'neutral';
  const pair = document.getElementById('sq-pair-select')?.value || 'BTC/USDT';
  if(!content || content.length < 10){
    toast('请输入至少10个字的观点内容', 'warn'); return;
  }
  const sentMap = { bull:'🐂 看多', bear:'🐻 看空', neutral:'😐 中性' };
  const newPost = {
    id: 'sq' + Date.now(), uid: 'me', av: '🌟', name: '我',
    sentiment, pair, content,
    likes: 0, comments: 0, time: '刚刚',
    tags: [pair.split('/')[0], sentMap[sentiment].split(' ')[1]]
  };
  _sqPosts.unshift(newPost);
  document.getElementById('sq-content').value = '';
  renderSquare(_sqFilter);
  toast('&#x1F4AC; 观点已发布！', 'success');
}

function sqLike(postId){
  const post = _sqPosts.find(p => p.id === postId); if(!post) return;
  if(_sqMyLikes.has(postId)){
    _sqMyLikes.delete(postId);
    toast('取消点赞', '');
  } else {
    _sqMyLikes.add(postId);
    toast('&#x2764; 已点赞！', 'success');
  }
  renderSquare(_sqFilter);
}

function sqComment(postId){
  toast('&#x1F4AC; 评论功能即将上线，敬请期待！', '');
}

function sqShare(postId){
  if(navigator.clipboard){
    navigator.clipboard.writeText('https://quantai.app/square/' + postId);
    toast('&#x1F517; 链接已复制！', 'success');
  }
}

// ===================================================
// ===== 策略市场 =====
// ===================================================

// 策略市场 Mock 数据
let _strategies = [
  { id:'st1', name:'BTC双均线金叉策略', author:'Alpha Bull', av:'🐂', category:'trend', asset:'BTC/USDT', price:0, priceLbl:'免费', returns:'月均+18.4%', dd:'6.2%', trades:1243, users:892, rating:4.8, desc:'经典双均线策略升级版，MA7/MA25金叉入场，RSI<70确认，动态止损跟踪。回测3年胜率71%，最大回撤可控。', tags:['趋势跟踪','BTC','免费'] },
  { id:'st2', name:'ETH震荡网格Pro', author:'GridMaster', av:'🔲', category:'grid', asset:'ETH/USDT', price:29, priceLbl:'$29/月', returns:'月均+12.1%', dd:'3.8%', trades:5621, users:2103, rating:4.6, desc:'专为ETH震荡行情设计，自动计算网格间距，波动率自适应，支持$2500-$4500区间做市。月均复利超12%。', tags:['网格','ETH','震荡行情'] },
  { id:'st3', name:'多品种动量轮动', author:'Quant流浪者', av:'🌊', category:'quant', asset:'多品种', price:79, priceLbl:'$79/月', returns:'月均+24.7%', dd:'12.1%', trades:387, users:341, rating:4.9, desc:'同时监控BTC/ETH/SOL/BNB，根据相对动量轮动持仓。月均收益最高，但回撤较大，适合风险承受能力强的用户。', tags:['多品种','动量','量化'] },
  { id:'st4', name:'低频高胜率外汇EA', author:'FX Veteran', av:'💱', category:'forex', asset:'EUR/USD', price:49, priceLbl:'$49/月', returns:'月均+7.3%', dd:'2.1%', trades:89, users:678, rating:4.7, desc:'外汇老手10年心血，只做EUR/USD。每月10-15笔，胜率82%，最大单笔风险1.5%，连续18个月盈利纪录。', tags:['外汇','高胜率','低频'] },
  { id:'st5', name:'套利监控机器人', author:'Arb Hunter', av:'⚡', category:'arb', asset:'全市场', price:0, priceLbl:'免费', returns:'月均+5.2%', dd:'0.8%', trades:9843, users:3201, rating:4.5, desc:'监控主流交易所价差，发现0.3%以上套利机会自动提醒。免费版仅提示，Pro版自动执行。稳定低风险。', tags:['套利','免费','低风险'] },
  { id:'st6', name:'AI情绪驱动策略', author:'NeuroBull', av:'🧠', category:'ai', asset:'BTC/ETH', price:99, priceLbl:'$99/月', returns:'月均+31.2%', dd:'18.4%', tags:['AI','情绪驱动','高收益'], users:234, rating:4.4, trades:456, desc:'接入链上数据+社媒情绪+期货持仓量，AI综合判断市场情绪分值，仅在分值>75时开仓。高收益高风险。' },
];

let _smFilter = 'all';
let _smShowUpload = false;

function renderStratMarket(filter){
  _smFilter = filter || _smFilter;
  document.querySelectorAll('.sm-filter-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.f === _smFilter);
  });
  const grid = document.getElementById('sm-grid');
  if(!grid) return;
  let strats = [..._strategies];
  if(_smFilter !== 'all') strats = strats.filter(s => s.category === _smFilter);
  strats.sort((a,b) => b.users - a.users);
  grid.innerHTML = strats.map(s => {
    const stars = '&#9733;'.repeat(Math.floor(s.rating)) + (s.rating % 1 >= 0.5 ? '&#9734;' : '');
    const priceCls = s.price === 0 ? 'up' : 'stat-val';
    return '<div class="sm-card" onclick="openStratDetail(\\'' + s.id + '\\')">'
      + '<div class="sm-card-head">'
        + '<div class="copy-av" style="width:38px;height:38px;font-size:17px">' + s.av + '</div>'
        + '<div style="flex:1;min-width:0">'
          + '<div style="font-weight:700;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + s.name + '</div>'
          + '<div style="font-size:12px;color:var(--muted)">' + s.author + ' &middot; ' + s.asset + '</div>'
        + '</div>'
        + '<div style="font-size:12px;font-weight:700;color:' + (s.price===0?'var(--green)':'var(--purple)') + '">' + s.priceLbl + '</div>'
      + '</div>'
      + '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:10px 0">'
        + '<div style="text-align:center"><div class="up" style="font-weight:700">' + s.returns + '</div><div style="font-size:11px;color:var(--muted)">月收益</div></div>'
        + '<div style="text-align:center"><div class="down" style="font-weight:600">' + s.dd + '</div><div style="font-size:11px;color:var(--muted)">最大回撤</div></div>'
        + '<div style="text-align:center"><div style="font-weight:600">' + s.users.toLocaleString() + '</div><div style="font-size:11px;color:var(--muted)">使用人数</div></div>'
      + '</div>'
      + '<div style="font-size:12px;color:var(--muted);margin-bottom:8px;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">' + s.desc + '</div>'
      + '<div style="display:flex;justify-content:space-between;align-items:center">'
        + '<div style="font-size:12px;color:#f59e0b">' + stars + ' <span style="color:var(--muted)">' + s.rating + '</span></div>'
        + '<div style="display:flex;gap:6px" onclick="event.stopPropagation()">'
          + '<button class="btn btn-outline" style="font-size:12px;padding:4px 10px" onclick="backtestStrat(\\'' + s.id + '\\')">&#x1F4CA; 回测</button>'
          + '<button class="btn btn-primary" style="font-size:12px;padding:4px 12px" onclick="copyStrat(\\'' + s.id + '\\')">' + (s.price===0 ? '&#x2B07; 免费复制' : '&#x1F6D2; 订阅') + '</button>'
        + '</div>'
      + '</div>'
    + '</div>';
  }).join('');
}

function filterStratMarket(filter){
  _smFilter = filter;
  renderStratMarket(filter);
}

function toggleSmUpload(){
  _smShowUpload = !_smShowUpload;
  const panel = document.getElementById('sm-upload-panel');
  if(panel) panel.style.display = _smShowUpload ? '' : 'none';
  const btn = document.getElementById('sm-upload-btn');
  if(btn) btn.textContent = _smShowUpload ? '&#x2715; 收起' : '&#x2B06; 上传策略';
}

function submitStrategy(){
  const name    = document.getElementById('sm-strat-name')?.value?.trim();
  const asset   = document.getElementById('sm-strat-asset')?.value?.trim();
  const price   = parseFloat(document.getElementById('sm-strat-price')?.value || 0);
  const code    = document.getElementById('sm-strat-code')?.value?.trim();
  if(!name || name.length < 4){ toast('请填写策略名称（至少4字）', 'warn'); return; }
  if(!code || code.length < 20){ toast('请填写策略代码（至少20字符）', 'warn'); return; }
  const newStrat = {
    id: 'st' + Date.now(), name, author: '我', av: '✨',
    category: 'quant', asset: asset || 'BTC/USDT',
    price, priceLbl: price === 0 ? '免费' : '$' + price + '/月',
    returns: '--', dd: '--', trades: 0, users: 0, rating: 5.0,
    desc: code.slice(0, 100) + '...', tags: [asset||'BTC', price===0?'免费':'付费']
  };
  _strategies.unshift(newStrat);
  toggleSmUpload();
  renderStratMarket(_smFilter);
  toast('&#x1F389; 策略已提交审核，通过后上架！', 'success');
}

function openStratDetail(sid){
  const s = _strategies.find(x => x.id === sid); if(!s) return;
  const modal = document.getElementById('sm-detail-modal');
  const body  = document.getElementById('sm-detail-body');
  if(!modal || !body) return;
  const stars = '&#9733;'.repeat(Math.floor(s.rating));
  body.innerHTML =
    '<div style="display:flex;justify-content:space-between;margin-bottom:14px">'
      + '<div style="display:flex;gap:12px;align-items:center">'
        + '<div class="copy-av" style="width:46px;height:46px;font-size:20px">' + s.av + '</div>'
        + '<div>'
          + '<div style="font-size:17px;font-weight:800">' + s.name + '</div>'
          + '<div style="font-size:12px;color:var(--muted)">' + s.author + ' &middot; ' + s.asset + '</div>'
        + '</div>'
      + '</div>'
      + '<button onclick="document.getElementById(\'sm-detail-modal\').classList.remove(\'active\')" style="background:none;border:none;color:var(--muted);font-size:20px;cursor:pointer">&times;</button>'
    + '</div>'
    + '<div style="font-size:13px;line-height:1.7;color:var(--text2);margin-bottom:14px">' + s.desc + '</div>'
    + '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px">'
      + '<div class="stat-card"><div class="stat-val up">' + s.returns + '</div><div class="stat-lbl">月均收益</div></div>'
      + '<div class="stat-card"><div class="stat-val down">' + s.dd + '</div><div class="stat-lbl">最大回撤</div></div>'
      + '<div class="stat-card"><div class="stat-val">' + s.trades + '</div><div class="stat-lbl">总交易次数</div></div>'
    + '</div>'
    + '<div style="display:flex;gap:10px">'
      + '<button class="btn btn-outline" style="flex:1" onclick="backtestStrat(\\'' + s.id + '\\')">&#x1F4CA; 一键回测</button>'
      + '<button class="btn btn-primary" style="flex:1" onclick="copyStrat(\\'' + s.id + '\\')">' + (s.price===0 ? '&#x2B07; 免费复制' : '&#x1F6D2; 订阅 ' + s.priceLbl) + '</button>'
    + '</div>';
  modal.classList.add('active');
  modal.onclick = e => { if(e.target === modal) modal.classList.remove('active'); };
}

function backtestStrat(sid){
  const s = _strategies.find(x => x.id === sid);
  if(!s) return;
  toast('&#x1F4CA; 正在对"' + s.name + '"执行回测...', '');
  setTimeout(() => {
    const ret = (Math.random() * 30 + 10).toFixed(1);
    const dd  = (Math.random() * 10 + 2).toFixed(1);
    const wr  = (Math.random() * 20 + 60).toFixed(0);
    toast('&#x2705; 回测完成：月均 +' + ret + '% | 最大回撤 ' + dd + '% | 胜率 ' + wr + '%', 'success');
  }, 1800);
}

function copyStrat(sid){
  const s = _strategies.find(x => x.id === sid);
  if(!s) return;
  if(s.price > 0){
    toast('&#x1F6D2; 即将跳转支付：' + s.priceLbl + '（功能即将上线）', '');
  } else {
    toast('&#x2705; 策略"' + s.name + '"已复制到我的策略库！', 'success');
  }
}

// ===================================================
// ===== 信号广播 =====
// ===================================================

// 信号广播 Mock 数据
let _liveSignals = [
  { id:'sig1', from:'Alpha Bull', av:'🐂', pair:'BTC/USDT', dir:'buy', entry:'71,200', sl:'69,800', tp1:'73,500', tp2:'76,000', desc:'BTC突破关键阻力，趋势做多，止损稳健', time:'2分钟前', status:'active', pnl:'+$842', subscribed:true },
  { id:'sig2', from:'FoxQuant', av:'🦊', pair:'ETH/USDT', dir:'sell', entry:'3,280', sl:'3,380', tp1:'3,100', tp2:'2,950', desc:'ETH破支撑看空，止损$3380保护', time:'15分钟前', status:'active', pnl:'+$234', subscribed:true },
  { id:'sig3', from:'Precision Pro', av:'🎯', pair:'SOL/USDT', dir:'buy', entry:'148.5', sl:'142.0', tp1:'158.0', tp2:'165.0', desc:'SOL三角形向上突破，追涨信号', time:'42分钟前', status:'tp1hit', pnl:'+$1,120', subscribed:false },
  { id:'sig4', from:'GridMaster', av:'🔲', pair:'BNB/USDT', dir:'buy', entry:'612', sl:'598', tp1:'628', tp2:'645', desc:'BNB底部放量，区间低买', time:'1小时前', status:'active', pnl:'-$156', subscribed:false },
  { id:'sig5', from:'NeuroBull', av:'🧠', pair:'BTC/USDT', dir:'sell', entry:'72,400', sl:'73,200', tp1:'70,500', tp2:'68,000', desc:'AI情绪指标回落，短空对冲', time:'2小时前', status:'closed', pnl:'+$3,200', subscribed:true },
];

let _broadcasters = [
  { id:'bc1', name:'Alpha Bull', av:'🐂', followers:3241, accuracy:'78%', avgReturn:'+14.2%', plan:'免费', desc:'专注BTC/ETH趋势，每日1-3条精准信号', subscribed:true },
  { id:'bc2', name:'FoxQuant', av:'🦊', followers:2108, accuracy:'72%', avgReturn:'+9.8%', plan:'免费', desc:'量化驱动，多品种信号，每周10条以上', subscribed:true },
  { id:'bc3', name:'Precision Pro', av:'🎯', followers:1876, accuracy:'85%', avgReturn:'+18.5%', plan:'Pro $19/月', desc:'高胜率低频信号，月均5-8条，质量极高', subscribed:false },
  { id:'bc4', name:'Degen King', av:'🔥', followers:987, accuracy:'65%', avgReturn:'+28.4%', plan:'Elite $49/月', desc:'高风险高回报，山寨币信号，暴利暴亏', subscribed:false },
  { id:'bc5', name:'NeuroBull', av:'🧠', followers:654, accuracy:'81%', avgReturn:'+22.1%', plan:'Pro $29/月', desc:'AI驱动，BTC/ETH/SOL，每日智能分析', subscribed:false },
];

let _sigHistRecords = [
  { pair:'BTC/USDT', dir:'buy', from:'Alpha Bull', av:'🐂', entry:'68,200', exit:'71,800', pnl:'+$3,600', result:'profit', date:'2026-03-28' },
  { pair:'ETH/USDT', dir:'sell', from:'FoxQuant', av:'🦊', entry:'3,420', exit:'3,180', pnl:'+$2,100', result:'profit', date:'2026-03-27' },
  { pair:'SOL/USDT', dir:'buy', from:'Precision Pro', av:'🎯', entry:'145', exit:'138', pnl:'-$680', result:'loss', date:'2026-03-26' },
  { pair:'BNB/USDT', dir:'buy', from:'Alpha Bull', av:'🐂', entry:'598', exit:'624', pnl:'+$1,280', result:'profit', date:'2026-03-25' },
  { pair:'BTC/USDT', dir:'sell', from:'NeuroBull', av:'🧠', entry:'70,200', exit:'67,500', pnl:'+$4,800', result:'profit', date:'2026-03-24' },
];

let _sigTab = 'live';
let _sigDirFilter = 'all';

function renderSignalsPage(){
  switchSigTab(_sigTab);
}

function switchSigTab(tab){
  _sigTab = tab;
  document.querySelectorAll('.sig-tab-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.t === tab);
  });
  document.getElementById('sig-live-panel').style.display  = tab === 'live'   ? '' : 'none';
  document.getElementById('sig-bc-panel').style.display    = tab === 'sources' ? '' : 'none';
  document.getElementById('sig-hist-panel').style.display  = tab === 'history' ? '' : 'none';
  if(tab === 'live')    renderLiveSignals(_sigDirFilter);
  if(tab === 'sources') renderBroadcasters();
  if(tab === 'history') renderSigHistory();
}

function filterSignals(dir){
  _sigDirFilter = dir;
  document.querySelectorAll('.sig-dir-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.d === dir);
  });
  renderLiveSignals(dir);
}

function renderLiveSignals(dir){
  dir = dir || _sigDirFilter;
  const panel = document.getElementById('sig-live-panel');
  if(!panel) return;
  let sigs = [..._liveSignals];
  if(dir === 'buy')  sigs = sigs.filter(s => s.dir === 'buy');
  if(dir === 'sell') sigs = sigs.filter(s => s.dir === 'sell');
  const dirBtns = panel.querySelector('.sig-dir-btns');

  const statusMap = { active:'&#x1F7E2; 进行中', tp1hit:'&#x1F3AF; TP1达到', closed:'&#x26AB; 已关闭' };
  const statusCls = { active:'up', tp1hit:'up', closed:'muted' };
  panel.innerHTML = (dirBtns ? dirBtns.outerHTML : '') + sigs.map(s => {
    const dirCls = s.dir === 'buy' ? 'up' : 'down';
    const dirLbl = s.dir === 'buy' ? '&#x2191; 做多' : '&#x2193; 做空';
    const pnlCls = s.pnl.startsWith('+') ? 'up' : 'down';
    return '<div class="sig-signal-card">'
      + '<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">'
        + '<div style="display:flex;gap:10px;align-items:center">'
          + '<div class="copy-av" style="width:36px;height:36px;font-size:15px">' + s.av + '</div>'
          + '<div>'
            + '<div style="font-weight:700;font-size:15px">' + s.pair + ' <span class="' + dirCls + '" style="font-size:12px;background:var(--card2);padding:2px 8px;border-radius:8px">' + dirLbl + '</span></div>'
            + '<div style="font-size:12px;color:var(--muted)">' + s.from + ' &middot; ' + s.time + '</div>'
          + '</div>'
        + '</div>'
        + '<div style="text-align:right">'
          + '<div class="' + pnlCls + '" style="font-weight:700">' + s.pnl + '</div>'
          + '<div style="font-size:11px;color:var(--muted)">' + (statusMap[s.status]||s.status) + '</div>'
        + '</div>'
      + '</div>'
      + '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:8px">'
        + '<div style="background:var(--card2);border-radius:8px;padding:6px;text-align:center"><div style="font-size:11px;color:var(--muted)">入场</div><div style="font-size:13px;font-weight:600">$' + s.entry + '</div></div>'
        + '<div style="background:var(--card2);border-radius:8px;padding:6px;text-align:center"><div style="font-size:11px;color:var(--muted)">止损</div><div class="down" style="font-size:13px;font-weight:600">$' + s.sl + '</div></div>'
        + '<div style="background:var(--card2);border-radius:8px;padding:6px;text-align:center"><div style="font-size:11px;color:var(--muted)">TP1</div><div class="up" style="font-size:13px;font-weight:600">$' + s.tp1 + '</div></div>'
        + '<div style="background:var(--card2);border-radius:8px;padding:6px;text-align:center"><div style="font-size:11px;color:var(--muted)">TP2</div><div class="up" style="font-size:13px;font-weight:600">$' + s.tp2 + '</div></div>'
      + '</div>'
      + '<div style="font-size:12px;color:var(--muted);margin-bottom:8px">' + s.desc + '</div>'
      + '<div style="display:flex;gap:8px" onclick="event.stopPropagation()">'
        + (s.status !== 'closed'
          ? '<button class="btn btn-primary" style="font-size:12px;padding:5px 12px" onclick="followSignal(\\'' + s.id + '\\')">&#x1F501; 跟单信号</button>'
          : ''
        )
        + '<button class="btn btn-outline" style="font-size:12px;padding:5px 12px" onclick="shareSignal(\\'' + s.id + '\\')">&#x1F517; 分享</button>'
      + '</div>'
    + '</div>';
  }).join('');
  // 重新挂载筛选按钮
  const filterBar = '<div class="sig-dir-btns" style="display:flex;gap:8px;margin-bottom:14px">'
    + '<button class="lb-tab' + (dir==='all'?' active':'') + '" data-d="all" onclick="filterSignals(\'all\',this)">全部</button>'
    + '<button class="lb-tab' + (dir==='buy'?' active':'') + '" data-d="buy" onclick="filterSignals(\'buy\',this)" style="background:' + (dir==='buy'?'var(--green)':'') + '">&#x2191; 做多</button>'
    + '<button class="lb-tab' + (dir==='sell'?' active':'') + '" data-d="sell" onclick="filterSignals(\'sell\',this)">&#x2193; 做空</button>'
    + '</div>';
  panel.innerHTML = filterBar + panel.innerHTML;
}

function renderBroadcasters(){
  const panel = document.getElementById('sig-bc-panel');
  if(!panel) return;
  panel.innerHTML = _broadcasters.map(bc => {
    return '<div class="sig-broadcaster-card">'
      + '<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">'
        + '<div style="display:flex;gap:10px;align-items:center">'
          + '<div class="copy-av" style="width:40px;height:40px;font-size:18px">' + bc.av + '</div>'
          + '<div>'
            + '<div style="font-weight:700;font-size:15px">' + bc.name + '</div>'
            + '<div style="font-size:12px;color:var(--muted)">' + bc.followers.toLocaleString() + ' 订阅者</div>'
          + '</div>'
        + '</div>'
        + '<div style="text-align:right">'
          + '<div style="font-size:12px;font-weight:700;color:' + (bc.plan==='免费'?'var(--green)':'var(--purple)') + '">' + bc.plan + '</div>'
        + '</div>'
      + '</div>'
      + '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:8px">'
        + '<div class="stat-card"><div class="stat-val up">' + bc.accuracy + '</div><div class="stat-lbl">准确率</div></div>'
        + '<div class="stat-card"><div class="stat-val up">' + bc.avgReturn + '</div><div class="stat-lbl">跟单均收益</div></div>'
      + '</div>'
      + '<div style="font-size:12px;color:var(--muted);margin-bottom:10px">' + bc.desc + '</div>'
      + '<button class="btn ' + (bc.subscribed?'btn-outline':'btn-primary') + '" style="width:100%" onclick="toggleBcSubscribe(\\'' + bc.id + '\\')">'
        + (bc.subscribed ? '&#x2705; 已订阅 &nbsp;取消' : '&#x1F514; 订阅信号') + '</button>'
    + '</div>';
  }).join('');
}

function renderSigHistory(){
  const panel = document.getElementById('sig-hist-panel');
  if(!panel) return;
  const total = _sigHistRecords.length;
  const wins  = _sigHistRecords.filter(r => r.result === 'profit').length;
  const wr    = ((wins/total)*100).toFixed(0);
  panel.innerHTML =
    '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px">'
      + '<div class="stat-card"><div class="stat-val">' + total + '</div><div class="stat-lbl">历史信号</div></div>'
      + '<div class="stat-card"><div class="stat-val up">' + wr + '%</div><div class="stat-lbl">胜率</div></div>'
      + '<div class="stat-card"><div class="stat-val up">+$11,100</div><div class="stat-lbl">累计盈利</div></div>'
    + '</div>'
    + _sigHistRecords.map(r => {
      const dirLbl = r.dir === 'buy' ? '&#x2191; 做多' : '&#x2193; 做空';
      const dirCls = r.dir === 'buy' ? 'up' : 'down';
      const pnlCls = r.result === 'profit' ? 'up' : 'down';
      return '<div style="background:var(--card2);border-radius:12px;padding:12px 14px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center">'
        + '<div style="display:flex;gap:10px;align-items:center">'
          + '<div class="copy-av" style="width:34px;height:34px;font-size:14px">' + r.av + '</div>'
          + '<div>'
            + '<div style="font-weight:700">' + r.pair + ' <span class="' + dirCls + '" style="font-size:11px">' + dirLbl + '</span></div>'
            + '<div style="font-size:12px;color:var(--muted)">' + r.from + ' &middot; ' + r.date + '</div>'
            + '<div style="font-size:12px;color:var(--muted)">$' + r.entry + ' &#x2192; $' + r.exit + '</div>'
          + '</div>'
        + '</div>'
        + '<div class="' + pnlCls + '" style="font-weight:700;font-size:15px">' + r.pnl + '</div>'
      + '</div>';
    }).join('');
}

function publishSignal(){
  const pair  = document.getElementById('sig-pub-pair')?.value?.trim();
  const dir   = document.getElementById('sig-pub-dir')?.value;
  const entry = document.getElementById('sig-pub-entry')?.value?.trim();
  const sl    = document.getElementById('sig-pub-sl')?.value?.trim();
  const tp1   = document.getElementById('sig-pub-tp1')?.value?.trim();
  const tp2   = document.getElementById('sig-pub-tp2')?.value?.trim();
  const desc  = document.getElementById('sig-pub-desc')?.value?.trim();
  if(!pair || !entry || !sl || !tp1){
    toast('请填写交易对、入场价、止损、TP1', 'warn'); return;
  }
  const newSig = {
    id: 'sig' + Date.now(), from: '我', av: '🌟',
    pair, dir, entry, sl, tp1: tp1, tp2: tp2||'--',
    desc: desc || '手动发布信号', time: '刚刚', status: 'active', pnl: '$0',
    subscribed: true
  };
  _liveSignals.unshift(newSig);
  switchSigTab('live');
  toast('&#x1F4E1; 信号已广播！', 'success');
}

function followSignal(sigId){
  const s = _liveSignals.find(x => x.id === sigId);
  if(!s) return;
  toast('&#x1F501; 跟单"' + s.pair + '"信号成功，已接入自动建仓！', 'success');
}

function shareSignal(sigId){
  if(navigator.clipboard){
    navigator.clipboard.writeText('https://quantai.app/signal/' + sigId);
    toast('&#x1F517; 信号链接已复制！', 'success');
  }
}

function toggleBcSubscribe(bcId){
  const bc = _broadcasters.find(x => x.id === bcId);
  if(!bc) return;
  bc.subscribed = !bc.subscribed;
  renderBroadcasters();
  toast(bc.subscribed ? '&#x1F514; 已订阅 ' + bc.name + ' 的信号！' : '已取消订阅 ' + bc.name, bc.subscribed ? 'success' : '');
}

// ===================================================
// ===== 自动建仓（Auto Open - Elite Only） =====
// ===================================================
// 模拟当前用户计划：'pro' | 'elite'
let _userPlan = 'elite';  // 已解锁 Elite
let _aoState  = { signal: false, dca: false, copy: false };
let _aoTimers = { signal: null, dca: null, copy: null };
let _aoMode   = 'signal';
let _dcaInvested = 0;

function initAutoOpen(){
  const isElite = _userPlan === 'elite';
  const banner  = document.getElementById('ao-lock-banner');
  const grid    = document.getElementById('ao-mode-grid');
  const panel   = document.getElementById('ao-config-panel');
  const planTag = document.getElementById('ao-plan-tag');

  if(banner) banner.style.display = isElite ? 'none' : 'flex';
  if(grid)   grid.querySelectorAll('.ao-mode-card').forEach(c=>c.classList.toggle('locked',!isElite));
  if(panel)  panel.style.opacity = isElite ? '1' : '0.4';
  if(panel)  panel.style.pointerEvents = isElite ? '' : 'none';
  if(planTag) planTag.innerHTML = isElite
    ? `<span class="elite-badge">✅ Elite</span>`
    : `<button class="btn btn-primary" onclick="upgradeToElite()" style="font-size:12px">💎 ${t('ao_lock_btn')||'升级 $199/月'}</button>`;

  selectAoMode(_aoMode);
  renderAoLog();
  updateCopySourceSelect();
  // 显式更新 placeholder（防止静态HTML中文未被翻译）
  const pairInput = document.getElementById('ao-copy-pairs');
  if(pairInput) pairInput.placeholder = t('ao_copy_pairs_ph') || 'BTC,ETH (empty=all)';
  // 恢复运行中状态的 badge
  ['signal','dca','copy'].forEach(m=>{
    const badge = document.getElementById(`aobadge-${m}`);
    if(badge) badge.style.display = _aoState[m] ? '' : 'none';
  });
}

function selectAoMode(mode){
  _aoMode = mode;
  document.querySelectorAll('.ao-mode-card').forEach(c=>c.classList.remove('active'));
  const card = document.getElementById(`aocard-${mode}`);
  if(card) card.classList.add('active');
  ['signal','dca','copy'].forEach(m=>{
    const p = document.getElementById(`ao-panel-${m}`);
    if(p) p.style.display = m===mode ? '' : 'none';
  });
}

function toggleAo(mode){
  if(_userPlan !== 'elite'){
    upgradeToElite(); return;
  }
  const running = _aoState[mode];
  if(running){
    // 停止
    clearInterval(_aoTimers[mode]); _aoTimers[mode]=null;
    _aoState[mode] = false;
    const btn  = document.getElementById(`ao-${mode}-btn`);
    const stat = document.getElementById(`ao-${mode}-status`);
    const badge= document.getElementById(`aobadge-${mode}`);
    if(btn)  btn.innerHTML=`▶ <span>${t('ao_start')||'启动自动建仓'}</span>`;
    if(stat) { stat.className='ao-status-off'; stat.innerHTML=`<span>${t('ao_status_off')||'● 未启动'}</span>`; }
    if(badge) badge.style.display='none';
    toast(`⏹ ${t('ao_stopped')||'已停止'}：${mode.toUpperCase()}`, '');
  } else {
    // 启动
    _aoState[mode] = true;
    const btn  = document.getElementById(`ao-${mode}-btn`);
    const stat = document.getElementById(`ao-${mode}-status`);
    const badge= document.getElementById(`aobadge-${mode}`);
    if(btn)  btn.innerHTML=`⏹ <span>${t('ao_stop')||'停止运行'}</span>`;
    if(stat) { stat.className='ao-status-on'; stat.innerHTML=`<span>🟢 ${t('ao_status_on')||'运行中'}</span>`; }
    if(badge) badge.style.display='';
    toast(`🚀 ${t('ao_started')||'已启动'}：${mode.toUpperCase()}`, 'success');
    // 模拟信号触发
    _aoTimers[mode] = setInterval(()=>simulateAoFire(mode), mode==='dca'?8000:5000+(Math.random()*4000|0));
    simulateAoFire(mode);
  }
}

const AO_PAIRS = ['BTC/USDT','XAU/USD','ETH/USDT','EUR/USD','NAS100','GBP/USD','SOL/USDT'];
const AO_INDS  = ['RSI(14)','MACD','EMA交叉','布林突破','CCI(20)'];

function simulateAoFire(mode){
  if(!_aoState[mode]) return;
  const pair = AO_PAIRS[Math.floor(Math.random()*AO_PAIRS.length)];
  const dir  = Math.random()>.45 ? 'buy' : 'sell';
  const price= getSimPrice(pair);
  const pnl  = parseFloat(((Math.random()-.35)*320).toFixed(2));
  let msg='', detail='';

  if(mode==='signal'){
    const ind = AO_INDS[Math.floor(Math.random()*AO_INDS.length)];
    const size = parseFloat(document.getElementById('ao-signal-size')?.value||200);
    detail = `[${ind}] ${pair} ${dir==='buy'?'做多':'做空'} @${price} · $${size}`;
    msg    = `📡 <b>${ind}</b> 触发 · ${pair}`;
  } else if(mode==='dca'){
    const amount = parseFloat(document.getElementById('ao-dca-amount')?.value||100);
    const limit  = parseFloat(document.getElementById('ao-dca-total')?.value||3000);
    _dcaInvested = Math.min(_dcaInvested + amount, limit);
    detail = `定投 ${pair} $${amount}，已投入 $${_dcaInvested}/${limit}`;
    msg    = `📅 <b>定投</b> · ${pair} +$${amount}`;
    updateDcaProgress(limit);
  } else if(mode==='copy'){
    const src = COPY_TRADERS.find(c=>c.id===document.getElementById('ao-copy-source')?.value) || COPY_TRADERS[0];
    const ratio= parseFloat(document.getElementById('ao-copy-ratio')?.value||0.5);
    detail = `跟随 ${src.name}×${ratio} · ${pair} ${dir==='buy'?'做多':'做空'} @${price}`;
    msg    = `🔁 跟单 <b>${src.name}</b> · ${pair}`;
  }

  addAoLiveFeed(mode, dir, msg);
  addAoLog(mode, dir, detail, pnl);
}

function updateDcaProgress(limit){
  const bar  = document.getElementById('ao-dca-bar');
  const val  = document.getElementById('ao-dca-inv-val');
  const pct  = document.getElementById('ao-dca-pct');
  const lim  = document.getElementById('ao-dca-limit');
  const prog = document.getElementById('ao-dca-progress');
  if(!prog) return;
  prog.style.display='';
  const p = Math.min(100,(_dcaInvested/limit)*100).toFixed(1);
  if(bar) bar.style.width=p+'%';
  if(val) val.textContent='$'+_dcaInvested.toFixed(0);
  if(pct) pct.textContent=p+'%';
  if(lim) lim.textContent='$'+limit;
}

function addAoLiveFeed(mode, dir, msg){
  const feed = document.getElementById(`ao-${mode}-live`); if(!feed) return;
  const el = document.createElement('div');
  el.className='ao-live-item';
  const now = new Date().toLocaleTimeString();
  el.innerHTML=`<span>${dir==='buy'?'🟢':'🔴'}</span><span style="font-size:11px;color:var(--muted)">${now}</span><span>${msg}</span>`;
  feed.insertBefore(el, feed.firstChild);
  if(feed.children.length>5) feed.removeChild(feed.lastChild);
}

// 日志数据
let _aoLogs = [];
function addAoLog(mode, dir, detail, pnl){
  const now = new Date();
  _aoLogs.unshift({mode, dir, detail, pnl, time: now.toISOString().slice(0,16).replace('T',' ')});
  if(_aoLogs.length>80) _aoLogs.pop();
  renderAoLog();
}

function renderAoLog(){
  const body = document.getElementById('ao-log-body'); if(!body) return;
  if(!_aoLogs.length){ body.innerHTML=`<div class="ao-log-empty" data-i18n="ao_log_empty">${t('ao_log_empty')||'暂无执行记录'}</div>`; return; }
  body.innerHTML = _aoLogs.map(l=>{
    const pnlStr = (l.pnl>=0?'+':'')+`$${l.pnl.toFixed(2)}`;
    const pnlCls = l.pnl>=0?'up':'down';
    return `<div class="ao-log-item aoli-${l.dir}">
      <span class="aoli-time">${l.time}</span>
      <span class="aoli-dir">${l.dir==='buy'?'BUY':'SELL'}</span>
      <span class="aoli-msg">[${l.mode.toUpperCase()}] ${l.detail}</span>
      <span class="${pnlCls}" style="font-size:12px;font-weight:600;flex-shrink:0">${pnlStr}</span>
    </div>`;
  }).join('');
}

function clearAoLog(){ _aoLogs=[]; renderAoLog(); }

function getSimPrice(pair){
  const base = {
    'BTC/USDT':83200,'ETH/USDT':3200,'XAU/USD':2340,'EUR/USD':1.0842,
    'GBP/USD':1.2634,'NAS100':17840,'SOL/USDT':145,'BNB/USDT':580
  };
  const p = base[pair]||1000;
  return (p*(1+(Math.random()-.5)*.012)).toFixed(p>100?2:4);
}

function upgradeToElite(){
  // 演示：直接升级
  _userPlan='elite';
  toast(`💎 ${t('toast_elite_unlocked')||'已解锁 Elite！自动建仓功能已开启'}`, 'success');
  initAutoOpen();
}


function showPricing(){ toast('💎 '+(t('toast_view_plans')||'View all plans'),''); }

function toast(msg,type){
  const box=document.getElementById('toast');
  const el=document.createElement('div');
  el.className='toast-item '+(type||'');
  el.textContent=msg;
  box.appendChild(el);
  setTimeout(()=>{ el.style.opacity='0'; el.style.transform='translateX(40px)'; el.style.transition='.3s'; setTimeout(()=>el.remove(),300); },3000);
}

// ===== 初始化 =====
window.addEventListener('load',()=>{
  // ① 先恢复语言设置，让 t() 在后续渲染中正确工作
  const lang = localStorage.getItem('qlang') || 'zh';
  _currentLang = lang;
  document.documentElement.lang = lang;
  document.documentElement.dir = (lang === 'ar') ? 'rtl' : 'ltr';
  const sel = document.getElementById('lang-select');
  if(sel) sel.value = lang;

  // ② 初始化图表和数据（此时 t() 已经指向正确语言）
  initKline();
  initTicker();
  renderMarket('all');
  renderPositions();
  renderStrategies();

  // ③ 应用 data-i18n 静态元素翻译
  applyLang(lang);

  // 模拟资产跳动
  setInterval(()=>{
    const base=12450+Math.random()*200-100;
    document.getElementById('total-asset').textContent='$'+Math.round(base).toLocaleString();
    const pnl=280+Math.random()*40-20;
    document.getElementById('daily-pnl').textContent='+'+'$'+Math.round(pnl);
  },3000);
});

// ======= Electron 桌面端适配 =======
(function initElectronBridge(){
  if(typeof window.electronAPI === 'undefined') return; // 非 Electron 环境跳过

  const api = window.electronAPI;

  // 1. 菜单快捷导航
  api.onMenuNav && api.onMenuNav(function(page){
    const navMap = {market:'market',ai:'ai',positions:'positions',strategies:'strategies'};
    if(navMap[page]) showPage(navMap[page]);
  });

  // 2. 紧急全部平仓（主进程确认后触发）
  api.onEmergencyCloseAll && api.onEmergencyCloseAll(function(){
    addAIMessage('assistant','🚨 已执行紧急全平指令，所有持仓已按市价平仓。');
    showPage('positions');
  });

  // 3. 自动更新提醒
  api.onUpdateAvailable && api.onUpdateAvailable(function(){
    const banner = document.createElement('div');
    banner.style.cssText = 'position:fixed;top:0;left:0;right:0;background:#3B82F6;color:#fff;text-align:center;padding:8px;font-size:13px;z-index:9999;cursor:pointer;';
    banner.textContent = '🔄 新版本可用，正在下载...';
    document.body.appendChild(banner);
  });
  api.onUpdateDownloaded && api.onUpdateDownloaded(function(){
    const banner = document.getElementById('update-banner') || document.querySelector('[data-update]');
    const btn = document.createElement('div');
    btn.style.cssText = 'position:fixed;top:0;left:0;right:0;background:#00C896;color:#fff;text-align:center;padding:8px;font-size:13px;z-index:9999;cursor:pointer;';
    btn.innerHTML = '✅ 更新已下载，<u>点击立即重启安装</u>';
    btn.onclick = () => api.installUpdate();
    document.body.appendChild(btn);
  });

  // 4. 原生通知（Electron环境使用系统通知）
  window._nativeNotify = function(title, body){
    api.showNotification(title, body);
  };

  // 5. 桌面端样式补丁：macOS 标题栏留白
  if(api.platform === 'darwin'){
    document.body.style.paddingTop = '28px';
    document.getElementById('sidebar') && (document.getElementById('sidebar').style.paddingTop = '28px');
  }

  console.log('[QuantAI] Electron 桥接初始化完成，平台:', api.platform);
})();

// ======= Capacitor 移动端适配 =======
(function initCapacitorBridge(){
  // 等待 Capacitor 加载（若不在 App 环境则跳过）
  document.addEventListener('deviceready', setupCapacitor, false);
  // Capacitor 不依赖 deviceready，用 DOMContentLoaded 也可
  if(window.Capacitor){
    setupCapacitor();
  }

  function setupCapacitor(){
    if(!window.Capacitor) return;
    const cap = window.Capacitor;
    console.log('[QuantAI] Capacitor 环境:', cap.getPlatform());

    // 状态栏颜色适配
    if(cap.isPluginAvailable('StatusBar')){
      cap.Plugins.StatusBar.setBackgroundColor({color:'#0A1628'}).catch(()=>{});
      cap.Plugins.StatusBar.setStyle({style:'DARK'}).catch(()=>{});
    }

    // 启动屏隐藏
    if(cap.isPluginAvailable('SplashScreen')){
      setTimeout(()=> cap.Plugins.SplashScreen.hide().catch(()=>{}), 300);
    }

    // 网络状态监听
    if(cap.isPluginAvailable('Network')){
      cap.Plugins.Network.addListener('networkStatusChange', status => {
        if(!status.connected){
          const toast = document.createElement('div');
          toast.style.cssText='position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:#FF4B6E;color:#fff;padding:8px 16px;border-radius:20px;font-size:12px;z-index:9999';
          toast.textContent='⚠️ 网络已断开，行情数据暂停更新';
          document.body.appendChild(toast);
          setTimeout(()=>toast.remove(),3000);
        }
      });
    }

    // 下单震动反馈
    window._hapticFeedback = function(){
      if(cap.isPluginAvailable('Haptics')){
        cap.Plugins.Haptics.impact({style:'MEDIUM'}).catch(()=>{});
      }
    };

    // Android 返回键处理
    if(cap.getPlatform()==='android'){
      document.addEventListener('backButton',()=>{
        // 如果不在仪表盘，返回仪表盘；否则最小化
        if(window._currentPage && window._currentPage !== 'dashboard'){
          showPage('dashboard');
        } else {
          cap.Plugins.App && cap.Plugins.App.minimizeApp().catch(()=>{});
        }
      });
    }
  }
})();
