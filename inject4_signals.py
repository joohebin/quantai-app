
# -*- coding: utf-8 -*-
# 注入模块4：信号广播 JS

MARKER = '// ===================================================\n// ===== 自动建仓（Auto Open - Elite Only） ====='

NEW_CODE = r"""// ===================================================
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

"""

with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

if MARKER in content:
    content = content.replace(MARKER, NEW_CODE + MARKER, 1)
    with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS - Module 4 (Signal Broadcast) injected')
    print('New file size:', len(content), 'chars')
else:
    print('ERROR: Marker not found!')
