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

// ===== AI 客服 =====
function getAIResponse(msg){
  const m=msg.toLowerCase();
  if(m.includes('btc')||m.includes('比特币')||m.includes('bitcoin')) return t('ai_resp_btc');
  if(m.includes('黄金')||m.includes('gold')||m.includes('xau')||m.includes('ذهب')||m.includes('ゴールド')||m.includes('금')) return t('ai_resp_gold');
  if(m.includes('仓位')||m.includes('分配')||m.includes('position')||m.includes('allocation')||m.includes('1000')||m.includes('ポジション')||m.includes('포지션')) return t('ai_resp_position');
  if(m.includes('策略')||m.includes('推荐')||m.includes('strategy')||m.includes('strategi')||m.includes('استراتيجية')||m.includes('戦略')||m.includes('전략')) return t('ai_resp_strategy');
  return t('ai_resp_default');
}

function sendChat(){
  const input=document.getElementById('chat-input');
  const msg=input.value.trim();
  if(!msg) return;
  input.value='';
  addMsg(msg,'user');
  document.getElementById('chat-sugg').style.display='none';
  // 打字中
  const typingId='typing-'+Date.now();
  addMsg('<div class="typing"><span></span><span></span><span></span></div>','ai',typingId);
  setTimeout(()=>{
    const el=document.getElementById(typingId);
    if(el) el.querySelector('.bubble').innerHTML=getAIResponse(msg).replace(/\n/g,'<br>').replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>');
    scrollChat();
  },1200+Math.random()*800);
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
const pageTitles={dashboard:'仪表盘',market:'行情',ai:'AI 客服',positions:'我的持仓',strategies:'策略管理',backtest:'策略回测',account:'我的账户'};

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
  // 标题：优先用 i18n，降级用 pageTitles
  const titleKey = 'page_' + name;
  const titleText = (typeof t === 'function' && t(titleKey) !== titleKey) ? t(titleKey) : (pageTitles[name]||name);
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
  if(name==='copy') renderCopyPage();
  if(name==='autoopen') initAutoOpen();

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
    ao_copy_pairs:'限制品种',
    ao_pos_size:'每笔仓位 (USD)', ao_sl:'止损 (%)', ao_tp:'止盈 (%)', ao_max_pos:'最大同时持仓',
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
    ao_copy_pairs:'Limit Symbols',
    ao_pos_size:'Position Size (USD)', ao_sl:'Stop Loss (%)', ao_tp:'Take Profit (%)', ao_max_pos:'Max Open Positions',
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
    ao_copy_pairs:'銘柄制限',
    ao_pos_size:'ポジションサイズ(USD)', ao_sl:'SL(%)', ao_tp:'TP(%)', ao_max_pos:'最大同時ポジション',
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
    ao_copy_pairs:'종목 제한',
    ao_pos_size:'포지션 크기(USD)', ao_sl:'손절(%)', ao_tp:'익절(%)', ao_max_pos:'최대 동시 포지션',
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
    ao_copy_pairs:'Лимит инструментов',
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
    ao_copy_pairs:'تقييد الرموز',
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
  // 同步页面标题
  const titleEl = document.getElementById('page-title');
  if(titleEl){
    const activePage = window._currentPage || 'dashboard';
    titleEl.textContent = t('page_' + activePage) || titleEl.textContent;
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
  {id:'ct1', name:'AlphaWolf', av:'🐺', tag:'BTC/ETH 专家 · 3年', wr:78.4, monthly:+24.6, dd:-8.2, followers:1842, category:'crypto', pnl30:+12400},
  {id:'ct2', name:'GoldHunter', av:'🦁', tag:'黄金/外汇 · 5年', wr:71.2, monthly:+18.3, dd:-5.6, followers:2310, category:'forex', pnl30:+8700},
  {id:'ct3', name:'SteadyHands', av:'🐢', tag:'低回撤稳健型 · 4年', wr:65.8, monthly:+11.2, dd:-3.1, followers:3290, category:'stable', pnl30:+5200},
  {id:'ct4', name:'NightScalper', av:'🦅', tag:'夜盘剥头皮 · 2年', wr:82.1, monthly:+31.0, dd:-14.8, followers:987, category:'crypto', pnl30:+18900},
  {id:'ct5', name:'MacroTrader', av:'🌍', tag:'宏观多品种 · 6年', wr:69.3, monthly:+15.8, dd:-6.4, followers:4120, category:'forex', pnl30:+7600},
  {id:'ct6', name:'ZenInvestor', av:'🎋', tag:'定投+趋势 · 7年', wr:61.5, monthly:+8.9, dd:-2.3, followers:5670, category:'stable', pnl30:+4100},
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
        <button class="btn btn-outline" style="font-size:12px;padding:5px 10px" onclick="showCopyDetail('${tid}')" data-i18n="copy_detail_btn">详情</button>
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
        <div class="copy-tag">${tr.tag} · ${tr.followers.toLocaleString()} ${t('copy_followers')||'人跟随'}</div>
        <div class="copy-stats">
          <div class="copy-stat"><div class="copy-stat-val ${mrCls}">${tr.monthly>0?'+':''}${tr.monthly}%</div><div class="copy-stat-lbl">${t('copy_monthly')||'月收益'}</div></div>
          <div class="copy-stat"><div class="copy-stat-val">${tr.wr}%</div><div class="copy-stat-lbl">${t('copy_winrate')||'胜率'}</div></div>
          <div class="copy-stat"><div class="copy-stat-val down">${tr.dd}%</div><div class="copy-stat-lbl">${t('copy_maxdd')||'最大回撤'}</div></div>
          <div class="copy-stat"><div class="copy-stat-val">+$${tr.pnl30.toLocaleString()}</div><div class="copy-stat-lbl">${t('copy_30pnl')||'近30天盈利'}</div></div>
        </div>
      </div>
      <div class="copy-actions">${btnHtml}<button class="btn btn-outline" style="font-size:12px;padding:6px 12px" onclick="showCopyDetail('${tr.id}')" data-i18n="copy_detail_btn">详情</button></div>
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
    COPY_TRADERS.map(tr=>`<option value="${tr.id}" ${follows.includes(tr.id)?'':'disabled style="color:var(--muted)"'}>${tr.av} ${tr.name}${follows.includes(tr.id)?'':' (未跟随)'}</option>`).join('');
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
