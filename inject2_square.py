
# -*- coding: utf-8 -*-
# 注入模块2：交易广场 JS

MARKER = '// ===================================================\n// ===== 自动建仓（Auto Open - Elite Only） ====='

NEW_CODE = r"""// ===================================================
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

"""

with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

if MARKER in content:
    content = content.replace(MARKER, NEW_CODE + MARKER, 1)
    with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS - Module 2 (Trading Square) injected')
    print('New file size:', len(content), 'chars')
else:
    print('ERROR: Marker not found!')
