
# -*- coding: utf-8 -*-
# 注入模块1：排行榜升级 + 交易员详情面板

MARKER = '// ===================================================\n// ===== 自动建仓（Auto Open - Elite Only） ====='

NEW_CODE = r"""// ===================================================
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

"""

with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

if MARKER in content:
    content = content.replace(MARKER, NEW_CODE + MARKER, 1)
    with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS - Module 1 (Leaderboard) injected')
    print('New file size:', len(content), 'chars')
else:
    print('ERROR: Marker not found!')
