import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找并替换 openTraderDetail 函数
idx_fn = content.find('function openTraderDetail(tid){')
if idx_fn < 0:
    print('openTraderDetail NOT FOUND')
    # 试着找其他写法
    for pat in ['function openTraderDetail(', 'openTraderDetail']:
        idx = content.find(pat)
        if idx >= 0:
            print(f'Found "{pat}" at {idx}: {content[idx:idx+80]}')
    exit(1)

idx_next = content.find('\nfunction ', idx_fn + 10)
fn_body = content[idx_fn:idx_next]
print(f'openTraderDetail found at char {idx_fn}, length {len(fn_body)}')

new_openTraderDetail = r"""function openTraderDetail(tid){
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
  const svgW = 200, svgH = 50;
  const toX = (i) => (i / (pts.length-1)) * svgW;
  const toY = (v) => svgH - ((v - min) / (max - min + 1)) * (svgH - 6) - 3;
  const polyline = pts.map((v,i) => `${toX(i)},${toY(v)}`).join(' ');
  const dots = pts.map((v,i) => `<circle cx="${toX(i)}" cy="${toY(v)}" r="3" fill="var(--green)"/>`).join('');

  const actionBtn = isFollowing
    ? `<button class="btn btn-outline" style="flex:1" onclick="unfollowTrader('${tid}');closeTraderDetail()">取消跟随</button>`
    : `<button class="btn btn-primary" style="flex:1" onclick="closeTraderDetail();showFollowModal('${tid}')">&#x1F501; 开始跟单</button>`;

  panel.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px">
      <div style="display:flex;gap:12px;align-items:center">
        <div class="copy-av" style="width:48px;height:48px;font-size:22px">${tr.av}</div>
        <div>
          <div style="font-size:17px;font-weight:800">${tr.name}</div>
          <div style="font-size:12px;color:var(--muted)">${t(tr.tagKey)||tr.tagKey}</div>
        </div>
      </div>
      <button onclick="closeTraderDetail()" style="background:none;border:none;color:var(--muted);font-size:20px;cursor:pointer">✕</button>
    </div>
    <div style="font-size:13px;color:var(--text2);margin-bottom:16px;line-height:1.6">${ex.bio||'专业交易员'}</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px">
      <div class="stat-card"><div class="stat-val ${mrCls}">${tr.monthly>0?'+':''}${tr.monthly}%</div><div class="stat-lbl">月收益</div></div>
      <div class="stat-card"><div class="stat-val">${tr.wr}%</div><div class="stat-lbl">胜率</div></div>
      <div class="stat-card"><div class="stat-val down">${tr.dd}%</div><div class="stat-lbl">最大回撤</div></div>
      <div class="stat-card"><div class="stat-val">${ex.trades30||'--'}</div><div class="stat-lbl">近30天交易</div></div>
      <div class="stat-card"><div class="stat-val">${ex.avgHold||'--'}</div><div class="stat-lbl">平均持仓</div></div>
      <div class="stat-card"><div class="stat-val up">${ex.bestTrade||'--'}</div><div class="stat-lbl">最佳单笔</div></div>
    </div>
    <div style="margin-bottom:16px">
      <div style="font-size:12px;color:var(--muted);margin-bottom:6px">近10次收益趋势</div>
      <svg width="${svgW}" height="${svgH}" style="overflow:visible">
        <polyline points="${polyline}" fill="none" stroke="var(--green)" stroke-width="2" stroke-linejoin="round"/>
        ${dots}
      </svg>
    </div>
    <div style="display:flex;gap:10px">
      ${actionBtn}
      <button class="btn btn-outline" style="flex:1" onclick="closeTraderDetail()">关闭</button>
    </div>`;

  overlay.classList.add('active');
  panel.classList.add('active');
}

"""

content = content[:idx_fn] + new_openTraderDetail + content[idx_next:]
print('openTraderDetail replaced successfully')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved index.html')

# 重新生成 _check.js
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
js = scripts[2]
with open('_check.js', 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print(f'Regenerated _check.js: {js.count(chr(10))} lines')
