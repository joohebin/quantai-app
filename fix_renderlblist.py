import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 核心问题: renderLbList 函数中的 followBtn 字符串使用了混乱的单引号转义
# 原代码：
#   const followBtn = isFollowing
#     ? '<button ...onclick="unfollowTrader(\\'' + tr.id + '\\')">...' + ... + '</button>'
#     : '<button ...onclick="showFollowModal(\\'' + tr.id + '\\')">' + ... + '</button>';
#   return '<div ...onclick="openTraderDetail(\\'' + tr.id + '\\')">' + ...
#
# 修复：改用 data-id 属性避免字符串拼接转义地狱，或改用反引号模板字符串
# 最简单的修复：用函数调用传整个对象，不用字符串拼接

# 找到这段代码的精确位置并替换
# 先找 renderLbList 函数
idx_fn = content.find('function renderLbList(traders){')
if idx_fn < 0:
    print('renderLbList NOT FOUND')
    exit(1)

# 找到函数内容结束位置 (找下一个顶层 function)
idx_next = content.find('\nfunction ', idx_fn + 10)
fn_body = content[idx_fn:idx_next]
print(f'renderLbList found at char {idx_fn}, length {len(fn_body)}')
print('First 200:', fn_body[:200])

# 替换整个 renderLbList 为干净版本（用反引号模板字符串）
new_renderLbList = r"""function renderLbList(traders){
  const list = document.getElementById('copy-trader-list');
  if(!list) return;
  list.innerHTML = traders.map((tr, idx) => {
    const isFollowing = !!_myFollows[tr.id];
    const mrCls = tr.monthly >= 0 ? 'up' : 'down';
    const medal = idx === 0 ? '🥇' : idx === 1 ? '🥈' : idx === 2 ? '🥉' : `<span style="color:var(--muted);font-size:13px">#${idx+1}</span>`;
    const followBtn = isFollowing
      ? `<button class="btn btn-outline" style="font-size:12px;padding:5px 14px" onclick="unfollowTrader('${tr.id}')">&#x2713; ${t('copy_following')||'已跟随'}</button>`
      : `<button class="btn btn-primary" style="font-size:12px;padding:5px 14px" onclick="showFollowModal('${tr.id}')">${t('copy_follow_btn')||'跟单'}</button>`;
    return `<div class="lb-rank-row" onclick="openTraderDetail('${tr.id}')">
      <div class="lb-medal">${medal}</div>
      <div class="copy-av" style="width:40px;height:40px;font-size:17px;flex-shrink:0">${tr.av}</div>
      <div class="lb-info">
        <div class="lb-name">${tr.name} ${isFollowing ? '<span style="font-size:11px;background:var(--green);color:var(--dark);border-radius:8px;padding:1px 7px">跟随中</span>' : ''}</div>
        <div style="font-size:12px;color:var(--muted)">${t(tr.tagKey)||tr.tagKey} &middot; ${tr.followers.toLocaleString()} ${t('copy_followers')||'人跟随'}</div>
      </div>
      <div class="lb-stats">
        <div class="lb-stat-item"><span class="${mrCls}" style="font-weight:700;font-size:15px">${tr.monthly>0?'+':''}${tr.monthly}%</span><span style="font-size:11px;color:var(--muted)">月收益</span></div>
        <div class="lb-stat-item"><span style="font-weight:600">${tr.wr}%</span><span style="font-size:11px;color:var(--muted)">胜率</span></div>
        <div class="lb-stat-item"><span class="down" style="font-weight:600">${tr.dd}%</span><span style="font-size:11px;color:var(--muted)">回撤</span></div>
      </div>
      <div onclick="event.stopPropagation()">${followBtn}</div>
    </div>`;
  }).join('');
}

"""

content = content[:idx_fn] + new_renderLbList + content[idx_next:]
print('renderLbList replaced successfully')

# 保存
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved index.html')

# 重新生成 _check.js 并快速检查
import re as _re
scripts = _re.findall(r'<script[^>]*>(.*?)</script>', content, _re.DOTALL)
js = scripts[2]
with open('_check.js', 'w', encoding='utf-8', newline='\n') as f:
    f.write(js)
print(f'Regenerated _check.js: {js.count(chr(10))} lines')
