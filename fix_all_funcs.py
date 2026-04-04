import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ==============================================================
# 重写 renderSquare - 用模板字符串
# ==============================================================
def replace_func(content, func_name, new_body):
    idx_fn = content.find(f'function {func_name}(')
    if idx_fn < 0:
        print(f'ERROR: {func_name} not found')
        return content
    idx_next = content.find('\nfunction ', idx_fn + 10)
    if idx_next < 0:
        idx_next = content.find('\n</script>', idx_fn)
    old_body = content[idx_fn:idx_next]
    content = content[:idx_fn] + new_body + content[idx_next:]
    print(f'Replaced {func_name} (was {len(old_body)} chars, now {len(new_body)} chars)')
    return content

# --- renderSquare ---
new_renderSquare = r"""function renderSquare(posts){
  const container = document.getElementById('sq-posts');
  if(!container) return;
  if(!posts || posts.length === 0){
    container.innerHTML = '<div style="text-align:center;padding:40px;color:var(--muted)">暂无帖子</div>';
    return;
  }
  container.innerHTML = posts.map(p => {
    const liked = _sqLikes[p.id];
    const sentMap = {bull:'&#x1F4C8; 看涨', bear:'&#x1F4C9; 看跌', neutral:'&#x1F4CA; 中性'};
    const sentCls = p.sentiment === 'bull' ? 'up' : p.sentiment === 'bear' ? 'down' : '';
    return `<div class="sq-post">
      <div class="sq-header">
        <div style="display:flex;align-items:center;gap:8px">
          <div class="copy-av" style="width:34px;height:34px;font-size:15px">${p.av}</div>
          <div>
            <div style="font-weight:700;font-size:14px">${p.author}</div>
            <div style="font-size:11px;color:var(--muted)">${p.time} &middot; ${p.asset}</div>
          </div>
        </div>
        <span class="${sentCls}" style="font-size:12px;font-weight:600">${sentMap[p.sentiment]||''}</span>
      </div>
      <div class="sq-content">${p.content}</div>
      <div class="sq-tags">${p.tags.map(tag => `<span class="sq-tag">#${tag}</span>`).join('')}</div>
      <div class="sq-actions">
        <button class="sq-action ${liked ? 'liked' : ''}" onclick="sqLike('${p.id}')">
          ${liked ? '&#x2764;' : '&#x1F90D;'} ${liked ? p.likes + 1 : p.likes}
        </button>
        <button class="sq-action" onclick="sqComment('${p.id}')">&#x1F4AC; ${p.comments}</button>
        <button class="sq-action" onclick="sqShare('${p.id}')">&#x1F517; 分享</button>
      </div>
    </div>`;
  }).join('');
}

"""

# --- renderStratMarket 中的列表部分 ---
# 找到 renderStratMarket 函数
new_renderStratMarket = r"""function renderStratMarket(list){
  const container = document.getElementById('sm-list');
  if(!container) return;
  if(!list || list.length === 0){
    container.innerHTML = '<div style="text-align:center;padding:40px;color:var(--muted)">暂无策略</div>';
    return;
  }
  container.innerHTML = list.map(s => {
    const isCopied = !!_copiedStrats[s.id];
    const priceLbl = s.price === 0 ? '免费' : `$${s.price}/月`;
    return `<div class="sm-card" onclick="openStratDetail('${s.id}')">
      <div class="sm-card-header">
        <div style="display:flex;gap:10px;align-items:center">
          <div class="copy-av" style="width:38px;height:38px;font-size:17px">${s.av}</div>
          <div>
            <div style="font-weight:700;font-size:14px">${s.name}</div>
            <div style="font-size:11px;color:var(--muted)">${s.author} &middot; ${s.asset}</div>
          </div>
        </div>
        <span class="sm-price-tag ${s.price===0?'free':''}">${priceLbl}</span>
      </div>
      <div class="sm-desc">${s.desc}</div>
      <div class="sm-stats">
        <div class="sm-stat"><span class="up" style="font-weight:700">${s.returns}</span><span>月均收益</span></div>
        <div class="sm-stat"><span style="font-weight:700">${s.wr}%</span><span>胜率</span></div>
        <div class="sm-stat"><span class="down" style="font-weight:700">${s.dd}</span><span>回撤</span></div>
        <div class="sm-stat"><span style="font-weight:700">${s.users}</span><span>使用者</span></div>
      </div>
      <div style="display:flex;gap:8px;margin-top:10px" onclick="event.stopPropagation()">
        <button class="btn btn-outline" style="font-size:12px;padding:4px 10px" onclick="backtestStrat('${s.id}')">&#x1F4CA; 回测</button>
        <button class="btn ${isCopied?'btn-outline':'btn-primary'}" style="font-size:12px;padding:4px 12px;flex:1" onclick="copyStrat('${s.id}')">
          ${isCopied ? '&#x2713; 已复制' : (s.price===0 ? '&#x2B07; 免费复制' : '&#x1F6D2; 订阅 ' + priceLbl)}
        </button>
      </div>
    </div>`;
  }).join('');
}

"""

# --- openStratDetail 里的 HTML ---
new_openStratDetail = r"""function openStratDetail(sid){
  const s = SM_DATA.find(x => x.id === sid); if(!s) return;
  const modal = document.getElementById('sm-detail-modal');
  if(!modal) return;
  const isCopied = !!_copiedStrats[s.id];
  const priceLbl = s.price === 0 ? '免费' : `$${s.price}/月`;
  modal.querySelector('.sm-detail-inner').innerHTML = `
    <div style="display:flex;justify-content:space-between;margin-bottom:14px">
      <div style="display:flex;gap:12px;align-items:center">
        <div class="copy-av" style="width:46px;height:46px;font-size:20px">${s.av}</div>
        <div>
          <div style="font-size:17px;font-weight:800">${s.name}</div>
          <div style="font-size:12px;color:var(--muted)">${s.author} &middot; ${s.asset}</div>
        </div>
      </div>
      <button onclick="document.getElementById('sm-detail-modal').classList.remove('active')" style="background:none;border:none;color:var(--muted);font-size:20px;cursor:pointer">&times;</button>
    </div>
    <div style="font-size:13px;line-height:1.7;color:var(--text2);margin-bottom:14px">${s.desc}</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px">
      <div class="stat-card"><div class="stat-val up">${s.returns}</div><div class="stat-lbl">月均收益</div></div>
      <div class="stat-card"><div class="stat-val down">${s.dd}</div><div class="stat-lbl">最大回撤</div></div>
      <div class="stat-card"><div class="stat-val">${s.trades}</div><div class="stat-lbl">总交易次数</div></div>
    </div>
    <div style="display:flex;gap:10px">
      <button class="btn btn-outline" style="flex:1" onclick="backtestStrat('${s.id}')">&#x1F4CA; 一键回测</button>
      <button class="btn ${isCopied?'btn-outline':'btn-primary'}" style="flex:1" onclick="copyStrat('${s.id}')">
        ${isCopied ? '&#x2713; 已复制' : (s.price===0 ? '&#x2B07; 免费复制' : '&#x1F6D2; 订阅 ' + priceLbl)}
      </button>
    </div>`;
  modal.classList.add('active');
  modal.onclick = e => { if(e.target === modal) modal.classList.remove('active'); };
}

"""

# --- renderLiveSignals ---
new_renderLiveSignals = r"""function renderLiveSignals(signals){
  const container = document.getElementById('sig-live-list');
  if(!container) return;
  if(!signals || signals.length === 0){
    container.innerHTML = '<div style="text-align:center;padding:30px;color:var(--muted)">暂无实时信号</div>';
    return;
  }
  container.innerHTML = signals.map(s => {
    const dirCls = s.dir === 'long' ? 'up' : 'down';
    const dirLabel = s.dir === 'long' ? '做多' : '做空';
    const confW = Math.round(s.confidence * 100);
    return `<div class="sig-card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
        <div>
          <span style="font-weight:800;font-size:15px">${s.asset}</span>
          <span class="${dirCls}" style="font-size:12px;font-weight:700;margin-left:8px;background:${s.dir==='long'?'rgba(0,255,159,.15)':'rgba(255,75,110,.15)'};padding:2px 8px;border-radius:12px">${dirLabel}</span>
        </div>
        <span class="sig-conf" style="font-size:12px">置信度 <span style="font-weight:800">${confW}%</span></span>
      </div>
      <div class="sig-conf-bar"><div class="sig-conf-fill" style="width:${confW}%"></div></div>
      <div style="display:flex;gap:16px;margin:8px 0;font-size:12px;color:var(--muted)">
        <span>入场: <span style="color:var(--text)">${s.entry}</span></span>
        <span>止盈: <span class="up">${s.tp}</span></span>
        <span>止损: <span class="down">${s.sl}</span></span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span style="font-size:11px;color:var(--muted)">${s.source} &middot; ${s.time}</span>
        <button class="btn btn-primary" style="font-size:11px;padding:4px 12px" onclick="followSignal('${s.id}')">&#x1F501; 跟单信号</button>
      </div>
    </div>`;
  }).join('');
}

"""

# --- renderBroadcasters ---
new_renderBroadcasters = r"""function renderBroadcasters(bcs){
  const container = document.getElementById('sig-bc-list');
  if(!container) return;
  if(!bcs || bcs.length === 0){
    container.innerHTML = '<div style="text-align:center;padding:30px;color:var(--muted)">暂无播报员</div>';
    return;
  }
  container.innerHTML = bcs.map(bc => {
    const isSubscribed = bc.subscribed;
    return `<div class="bc-card">
      <div style="display:flex;gap:10px;align-items:center;margin-bottom:10px">
        <div class="copy-av" style="width:42px;height:42px;font-size:19px">${bc.av}</div>
        <div style="flex:1">
          <div style="font-weight:700">${bc.name}</div>
          <div style="font-size:11px;color:var(--muted)">${bc.asset} &middot; ${bc.followers.toLocaleString()} 订阅</div>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:10px;font-size:12px;text-align:center">
        <div><div class="up" style="font-weight:700">${bc.accuracy}%</div><div style="color:var(--muted)">准确率</div></div>
        <div><div style="font-weight:700">${bc.signals}</div><div style="color:var(--muted)">总信号</div></div>
        <div><div class="up" style="font-weight:700">${bc.avgReturn}</div><div style="color:var(--muted)">平均收益</div></div>
      </div>
      <button class="btn ${isSubscribed?'btn-outline':'btn-primary'}" style="width:100%" onclick="toggleBcSubscribe('${bc.id}')">
        ${isSubscribed ? '&#x2713; 已订阅' : '+ 订阅播报'}
      </button>
    </div>`;
  }).join('');
}

"""

# 执行替换
content = replace_func(content, 'renderSquare', new_renderSquare)
content = replace_func(content, 'renderStratMarket', new_renderStratMarket)
content = replace_func(content, 'openStratDetail', new_openStratDetail)
content = replace_func(content, 'renderLiveSignals', new_renderLiveSignals)
content = replace_func(content, 'renderBroadcasters', new_renderBroadcasters)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved index.html')

# 重新生成 _check.js
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
js = scripts[2]
with open('_check.js', 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print(f'Regenerated _check.js: {js.count(chr(10))} lines')

# 检查还有没有双反斜杠问题
remaining = content.count("\\\\'")  # \\\\ in Python = \\ in file
print(f'Remaining problematic patterns: checking...')
lines = content.split('\n')
prob_count = 0
for i, line in enumerate(lines):
    if "\\\\'" in line and ('onclick' in line):
        print(f'  L{i+1}: {line[:160]}')
        prob_count += 1
print(f'Total problematic onclick lines: {prob_count}')
