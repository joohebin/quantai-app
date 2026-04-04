
# -*- coding: utf-8 -*-
# 注入模块3：策略市场 JS

MARKER = '// ===================================================\n// ===== 自动建仓（Auto Open - Elite Only） ====='

NEW_CODE = r"""// ===================================================
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

"""

with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

if MARKER in content:
    content = content.replace(MARKER, NEW_CODE + MARKER, 1)
    with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS - Module 3 (Strategy Market) injected')
    print('New file size:', len(content), 'chars')
else:
    print('ERROR: Marker not found!')
