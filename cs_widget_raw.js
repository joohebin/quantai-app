
// ===== 客服 Widget 逻辑 =====

// ---- 配置区（老板可修改） ----
const CS_CONFIG = {
  groqKey: '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',  // Groq API Key
  groqModel: 'llama-3.3-70b-versatile',
  tgLink: 'https://t.me/QuantAI_Support',  // Telegram 人工客服链接
  handoffKeywords: ['人工','转人工','真人','complaint','human','staff','urgent','紧急','投诉'],
  greetDelay: 600,        // 欢迎语延迟（毫秒）
};

// ---- 知识库（精简版 FAQ，完整版在 SUPPORT_KB.md 供服务端使用）----
const CS_KB = {
  upgrade: `💳 **升级套餐**

进入【我的账户】→【当前方案】，点击目标套餐即可升级：
• Basic $29/月 — 全品种行情+AI顾问+2个策略
• Pro $79/月 — 无限策略+AI自动交易+高级回测+多券商
• Elite $199/月 — 自动建仓(策略/定投/跟单)+复制交易无限跟单+VIP客服

有疑问请告诉我 😊`,
  kline_issue: `📊 **K线图加载问题**

请依次尝试：
1. 按 Ctrl+Shift+R 强制刷新页面
2. 换个浏览器（推荐 Chrome）
3. 检查 AdBlock 等插件是否拦截了请求
4. 等待1-2分钟后重试（Binance 偶有波动）

如果还不行，请截图发给我，我协助排查。`,
  autoopen: `⚙️ **自动建仓使用方法**

自动建仓是 Elite 专属功能（$199/月）。提供3种模式：
• **策略触发**：RSI/MACD/EMA 条件满足时自动开仓
• **定时定投**：按时间周期自动分批买入（DCA）
• **跟单同步**：绑定信号源，自动复制其开仓

进入【自动建仓】页面配置参数后点击「启动」即可。`,
  fred_offline: `🏛️ **FRED 宏观数据显示 offline**

FRED 数据来自美联储 API，中国大陆网络通常无法直连。显示"offline · static data"时，展示的是上次已知值，不影响平台其他功能正常使用。`,
  copy_trading: `🔁 **复制交易说明**

在【复制交易】页选择交易者 → 点击「跟单」→ 设置跟单比例和最大金额。

⚠️ 风险提示：跟单存在亏损风险，建议设置日亏损保护，不要把全部资金投入单一信号源。`,
  pricing: `💰 **订阅套餐**

| 套餐 | 价格 | 特点 |
|------|------|------|
| Basic | $29/月 | 全品种行情+AI顾问+2策略 |
| Pro | $79/月 | 无限策略+AI自动交易+多券商 |
| Elite | $199/月 | 自动建仓+复制交易+VIP客服 |

进入【我的账户】→【当前方案】升级。`,
  language: `🌐 **切换语言**

右上角语言下拉菜单，支持中文/English/日本語/한국어/Русский/العربية，实时生效，自动记忆。`,
  broker: `🏦 **连接券商**

进入【我的账户】→【已连接券商】→「添加新券商」。支持：
• 加密货币交易所（币安、OKX等）
• MT5 券商账户（INFINOX 等）

⚠️ 安全建议：API Key 只开「读取+交易」权限，不要开「提现」权限，并设置 IP 白名单。`,
  backtest: `🔬 **策略回测**

进入【回测】页面，选择品种、策略类型、日期范围（建议 ≥90天）、初始资金、仓位比例，点击「开始回测」。

结果包含：总收益率、年化收益、最大回撤、夏普比率、胜率、交易次数。`,
  strategy_market: `📦 **策略市场**

进入【策略市场】页面，可以发现和购买其他用户发布的量化策略。点击「复制」将策略导入自己的【策略管理】页面。发布策略需审核1-3工作日。`,
  signal: `📡 **信号广播**

进入【信号广播】页面 → 填写交易对/方向/入场价/止损止盈 → 点击「广播」。其他用户订阅后，可在【自动建仓-跟单同步】中绑定你作为信号源。`,
  mt5: `📈 **INFINOX MT5 账户**

INFINOX MT5 账户显示在【我的账户】页面。账户号、服务器地址、余额等信息在此查看。如需查看持仓，进入【持仓】页面。`,
  legal: `📋 **法律文档**

在【我的账户】页面底部可找到：隐私政策、服务条款、Cookie 政策、社区准则。`,
  square: `💬 **交易广场**

进入【交易广场】，可以分享交易观点、给品种贴情绪标签（看多/看空/观望），与其他 QuantAI 用户交流。`,
  default: `🤖 **QuantAI 客服助手**

您好！我可以帮您解答：
• 平台功能使用方法
• 套餐升级咨询
• K线/行情/持仓问题
• 策略/回测/复制交易
• 账户连接（券商/API）
• 故障排查

请描述您的问题，或点击上方快捷问题。如需人工客服，请说「转人工」。`
};

// ---- 状态 ----
let _csOpen = false;
let _csHistory = []; // {role, content}
let _csSending = false;
let _csGreeted = false;

function toggleCS(){
  console.log('[客服] 点击了客服按钮, 当前状态:', _csOpen);
  _csOpen = !_csOpen;
  const panel = document.getElementById('cs-panel');
  if(_csOpen){
    panel.classList.add('open');
    document.getElementById('cs-fab').innerHTML = '✕<span class="cs-badge" id="cs-badge" style="display:none"></span>';
    document.getElementById('cs-badge') && (document.getElementById('cs-badge').style.display='none');
    if(!_csGreeted){ _csGreeted=true; setTimeout(csGreet, CS_CONFIG.greetDelay); }
    setTimeout(()=>document.getElementById('cs-input').focus(), 300);
  } else {
    panel.classList.remove('open');
    document.getElementById('cs-fab').innerHTML = '💬<span class="cs-badge" id="cs-badge" style="display:none"></span>';
  }
}

function csGreet(){
  csAddMsg('bot', `👋 **你好！我是 QuantAI 客服助手。**\n\n我可以帮您解答平台功能、套餐升级、故障排查等问题。\n\n请问有什么可以帮您？`);
}

function csAddMsg(role, text){
  const msgs = document.getElementById('cs-msgs');
  const isUser = role === 'user';
  const div = document.createElement('div');
  div.className = `cs-msg ${isUser?'cs-user':'cs-bot'}`;
  div.innerHTML = `
    ${!isUser?'<div class="cs-av-s">🤖</div>':''}
    <div class="cs-bubble">${csFormatText(text)}</div>
    ${isUser?'<div class="cs-av-s">👤</div>':''}
  `;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function csFormatText(t){
  // 简单 markdown-ish 格式化
  return t
    .replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')
    .replace(/\n/g,'<br>')
    .replace(/•/g,'&nbsp;•');
}

function csShowTyping(){
  const msgs = document.getElementById('cs-msgs');
  const div = document.createElement('div');
  div.className = 'cs-msg cs-bot';
  div.id = 'cs-typing-indicator';
  div.innerHTML = '<div class="cs-av-s">🤖</div><div class="cs-bubble"><div class="cs-typing"><span></span><span></span><span></span></div></div>';
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function csHideTyping(){
  const el = document.getElementById('cs-typing-indicator');
  if(el) el.remove();
}

function csSendQuick(el){
  const text = el.textContent;
  document.getElementById('cs-input').value = text;
  csDoSend();
}

async function csDoSend(){
  if(_csSending) return;
  const inp = document.getElementById('cs-input');
  const text = inp.value.trim();
  if(!text) return;
  inp.value = '';
  inp.style.height = 'auto';

  csAddMsg('user', text);
  _csHistory.push({role:'user', content:text});

  // 检查是否转人工
  if(CS_CONFIG.handoffKeywords.some(k => text.toLowerCase().includes(k))){
    csShowHandoff();
    return;
  }

  _csSending = true;
  document.getElementById('cs-send').disabled = true;
  csShowTyping();

  let reply;
  // 始终走 window.csFetchGroqGateway（若已注入）或 window.csFetchGroq（可被外部覆盖）
  if(typeof window.csFetchGroqGateway === 'function'){
    const result = await window.csFetchGroqGateway(text);
    reply = (result !== null && result !== undefined) ? result : await csLocalReply(text);
  } else if(CS_CONFIG.groqKey && CS_CONFIG.groqKey !== 'USE_GATEWAY'){
    reply = await csFetchGroq(text);
  } else {
    reply = await csLocalReply(text);
  }

  csHideTyping();
  csAddMsg('bot', reply);
  _csHistory.push({role:'assistant', content:reply});
  _csSending = false;
  document.getElementById('cs-send').disabled = false;
}

// 本地知识库匹配（离线模式）
async function csLocalReply(text){
  await new Promise(r=>setTimeout(r, 600 + Math.random()*800)); // 模拟延迟
  const t = text.toLowerCase();
  if(/升级|套餐|价格|付费|basic|pro|elite|订阅/.test(t)) return CS_KB.upgrade;
  if(/k线|kline|图|chart|加载|blank|空白|不显示/.test(t)) return CS_KB.kline_issue;
  if(/自动建仓|auto.?open|定投|dca|跟单同步/.test(t)) return CS_KB.autoopen;
  if(/fred|宏观|offline|利率|cpi|非农/.test(t)) return CS_KB.fred_offline;
  if(/复制交易|copy.?trad|跟单|信号源/.test(t)) return CS_KB.copy_trading;
  if(/价格|收费|多少钱|how much/.test(t)) return CS_KB.pricing;
  if(/语言|language|切换|中文|english|日本|한국/.test(t)) return CS_KB.language;
  if(/券商|broker|binance|okx|mt5|infin|api.?key/.test(t)) return CS_KB.broker;
  if(/回测|backtest|历史|performance/.test(t)) return CS_KB.backtest;
  if(/策略市场|策略购买|发布策略/.test(t)) return CS_KB.strategy_market;
  if(/信号广播|订阅信号/.test(t)) return CS_KB.signal;
  if(/infinox|infin|mt5账户|m t5/.test(t)) return CS_KB.mt5;
  if(/法律|隐私政策|服务条款|cookie|社区准则/.test(t)) return CS_KB.legal;
  if(/交易广场|情绪|观点/.test(t)) return CS_KB.square;
  // 使用AI顾问页回复（用户可能在问AI相关）
  if(/ai|智能|顾问|分析|策略建议/.test(t)) return `🤖 **AI 顾问功能**\n\n进入左侧菜单【AI 顾问】页面，即可与 AI 对话。\n\nAI 可以帮您：分析行情、建议仓位分配、推荐策略、解读指标等。\n\n快捷提问可点击输入框上方的建议按钮。`;
  return CS_KB.default;
}

// Groq API 调用（如果配置了 Key）
async function csFetchGroq(userMsg){
  // 如果设置为走 Gateway，直接调 Gateway（在注入JS中被覆盖前的兜底）
  if(CS_CONFIG.groqKey === 'USE_GATEWAY'){
    return await csLocalReply(userMsg); // 会被Gateway覆盖，这里只是兜底
  }
  const SYSTEM_PROMPT = `你是 QuantAI 量化交易平台的 AI 客服助手，熟悉平台所有功能，可回答用户关于使用方法的任何问题。

【平台功能模块】
• 仪表盘：资产总览、实时行情
• 行情：22个交易品种K线（BTC/ETH/SOL/BNB/XRP外汇/黄金/原油/纳指/标普/恒生等）
• AI顾问：行情分析、仓位建议、策略推荐、指标解读
• 持仓：查看当前持仓、AI分析按钮
• 策略管理：MACD/EMA/RSI/网格/布林带策略创建和启动
• 回测：历史数据验证策略（日期范围/品种/仓位比例可配置）
• 复制交易：跟随交易者、自动同步开仓
• 自动建仓（Elite专属）：策略触发/定时定投(DCA)/跟单同步
• 交易广场：分享观点、情绪标签
• 策略市场：发现/购买/发布量化策略
• 信号广播：发布交易信号供他人订阅
• 我的账户：券商连接（币安/OKX/INFINOX MT5）、套餐升级、风控设置
• FRED宏观数据：美联储利率/CPI/非农/GDP（offline时显示静态默认值）
• 法律文档：隐私政策/服务条款/Cookie政策/社区准则（在"我的账户"底部）

【订阅套餐】
| 套餐 | 价格 | 核心功能 |
| Basic | $29/月 | 全品种行情、AI顾问、2个策略、自动交易 |
| Pro | $79/月 | 无限策略、AI自动交易、高级回测、多券商 |
| Elite | $199/月 | 自动建仓(策略/定投/跟单)、复制交易无限跟单、VIP客服、优先通道 |

【支持的交易品种】22个
加密货币：BTC/USDT、ETH/USDT、SOL/USDT、BNB、XRP
外汇：EUR/USD、GBP/USD、USD/JPY、USD/CHF、AUD/USD
贵金属：XAU/USD(黄金)、XAG/USD(白银)
能源：WTI原油、BRENT原油
指数：NAS100(纳指)、SPX500(标普)、DOW(道指)、HSI(恒生)、SX5E(欧洲斯托克50)
国债：US10Y、US02Y

【支持语言】中文/English/日本語/한국어/Русский/العربية，右上角切换，实时生效

【常见问题参考】
Q:K线图加载不出来？→ Ctrl+Shift+R强制刷新/换浏览器/关AdBlock
Q:FRED显示offline？→ 中国大陆网络无法访问美联储API，显示静态默认值不影响使用
Q:如何连接券商？→ 我的账户→已连接券商→添加新券商→填API Key/Secret
Q:自动建仓怎么用？→ Elite专属，3种模式：策略触发/定时定投/跟单同步
Q:API Key安全吗？→ 存在本地浏览器localStorage，不上传服务器；建议不开提现权限+设IP白名单
Q:策略最多几个？→ Basic 2个，Pro/Elite 无限
Q:风控怎么设置？→ 我的账户→风控设置：单日最大亏损/最大持仓比例/夜间保护
Q:订阅如何升级/取消？→ 我的账户→当前方案；取消联系客服
Q:如何发布策略？→ 策略市场→发布策略→填名称/品种/定价/代码→审核1-3工作日
Q:怎么成为信号源？→ 信号广播页面→填交易对/方向/止损止盈→广播

【回复规则】（严格遵守）
1. 简洁友好，不超过200字，用Markdown加粗**重点**
2. 涉及支付/账户安全/数据异常 → 说"需要人工客服协助，请说【转人工】"
3. 功能问题 → 明确告知【具体页面名称和操作步骤】
4. 语言跟随用户输入语言
5. 不确定的问题 → 引导转人工，不胡乱回答`;

  try {
    const messages = [
      {role:'system', content: SYSTEM_PROMPT},
      ..._csHistory.slice(-6), // 最近6条上下文
      {role:'user', content: userMsg}
    ];
    const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${CS_CONFIG.groqKey}`
      },
      body: JSON.stringify({
        model: CS_CONFIG.groqModel,
        messages,
        max_tokens: 300,
        temperature: 0.5
      }),
      signal: AbortSignal.timeout(15000)
    });
    if(!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return data.choices?.[0]?.message?.content || CS_KB.default;
  } catch(e){
    console.warn('[CS] Groq error:', e);
    return await csLocalReply(userMsg); // 降级到本地
  }
}

// 转人工提示框
function csShowHandoff(){
  csHideTyping();
  const msgs = document.getElementById('cs-msgs');
  const div = document.createElement('div');
  div.className = 'cs-msg cs-bot';
  div.innerHTML = `
    <div class="cs-av-s">🤖</div>
    <div class="cs-bubble">
      <div class="cs-handoff">
        <div><strong>🙋 转接人工客服</strong></div>
        <div style="font-size:11px;color:var(--muted)">将为您跳转到 Telegram 客服频道，工作日 9:00-18:00（UTC+8）在线。</div>
        <div class="cs-handoff-btns">
          <button class="cs-handoff-btn confirm" onclick="csGoHuman()">前往 Telegram 客服</button>
          <button class="cs-handoff-btn cancel" onclick="this.closest('.cs-msg').remove();csAddMsg('bot','好的，如果您还有其他问题随时告诉我 😊')">继续 AI 客服</button>
        </div>
      </div>
    </div>
  `;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
  _csSending = false;
  document.getElementById('cs-send').disabled = false;
}

function csGoHuman(){
  window.open(CS_CONFIG.tgLink, '_blank');
  csAddMsg('bot', `✅ 已为您跳转到人工客服频道。\n\n如果 Telegram 无法打开，也可以发邮件至：**support@quantai.app**`);
}

// Widget 挂载
window.addEventListener('load', ()=>{
  // 3秒后显示未读红点（引导注意）
  setTimeout(()=>{
    if(!_csOpen){
      const badge = document.getElementById('cs-badge');
      if(badge){ badge.style.display='block'; badge.textContent='1'; }
    }
  }, 3000);
});

// ═══════════════════════════════════════════════════════════════
// QuantAI AI GATEWAY  v1.0
// 三层通道路由：自带Key → Pro平台Key → 免费试用/模板
// ═══════════════════════════════════════════════════════════════

/* ── 平台配置（运营方填写） ─────────────────────────────────── */
window.PLATFORM_GROQ_KEY = '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';   // 平台 Groq Key
window.PLATFORM_GROQ_MODEL = 'llama-3.3-70b-versatile';

/* ── 配额常量 ────────────────────────────────────────────────── */
window.QUOTA = {
  free_daily:    20,      // 免费用户每日试用次数（上线前改回1-3）
  pro_daily:     100,     // Pro 用户每日调用次数
  elite_daily:   500,     // Elite 用户每日调用次数
  pro_tokens:    80000,   // Pro 用户每日 Token 软上限（估算）
  elite_tokens:  400000,  // Elite 用户每日 Token 软上限
};

/* ── IndexedDB 加密存储（用户自带 Key 只存本地，不过服务器）── */
const IDB_NAME = 'quantai_secure', IDB_STORE = 'kv', IDB_VER = 1;

function _idbOpen(){
  return new Promise((res,rej)=>{
    const req = indexedDB.open(IDB_NAME, IDB_VER);
    req.onupgradeneeded = e => e.target.result.createObjectStore(IDB_STORE);
    req.onsuccess = e => res(e.target.result);
    req.onerror   = e => rej(e.target.error);
  });
}
async function idbSet(key, val){
  const db = await _idbOpen();
  return new Promise((res,rej)=>{
    const tx = db.transaction(IDB_STORE,'readwrite');
    tx.objectStore(IDB_STORE).put(val, key);
    tx.oncomplete = ()=>res(); tx.onerror = e=>rej(e.target.error);
  });
}
async function idbGet(key){
  const db = await _idbOpen();
  return new Promise((res,rej)=>{
    const tx = db.transaction(IDB_STORE,'readonly');
    const req = tx.objectStore(IDB_STORE).get(key);
    req.onsuccess = e => res(e.target.result);
    req.onerror   = e => rej(e.target.error);
  });
}
async function idbDel(key){
  const db = await _idbOpen();
  return new Promise((res,rej)=>{
    const tx = db.transaction(IDB_STORE,'readwrite');
    tx.objectStore(IDB_STORE).delete(key);
    tx.oncomplete = ()=>res(); tx.onerror = e=>rej(e.target.error);
  });
}

/* 简单 XOR 混淆（防止明文展示，非加密级安全）*/
function _xorEncode(str, seed='quantai2026'){
  return btoa(str.split('').map((c,i)=>
    String.fromCharCode(c.charCodeAt(0)^seed.charCodeAt(i%seed.length))
  ).join(''));
}
function _xorDecode(enc, seed='quantai2026'){
  try{
    return atob(enc).split('').map((c,i)=>
      String.fromCharCode(c.charCodeAt(0)^seed.charCodeAt(i%seed.length))
    ).join('');
  }catch{ return ''; }
}

/* ── 用户档案（前端模拟，真实项目接后端） ───────────────────── */
// plan: 'free' | 'basic' | 'pro' | 'elite'
function getUserPlan(){
  return localStorage.getItem('qplan') || 'pro'; // 演示默认 pro
}
function setUserPlan(plan){
  localStorage.setItem('qplan', plan);
}

/* ── 每日配额追踪 ────────────────────────────────────────────── */
window._quotaKey = function(type){ return `quota_${type}_${new Date().toISOString().slice(0,10)}`; }
window.getQuotaUsed = function(type){ return parseInt(localStorage.getItem(_quotaKey(type))||'0'); }
window.incQuotaUsed = function(type){ localStorage.setItem(_quotaKey(type), getQuotaUsed(type)+1); }
// 自动清理过期配额（非今日的全部删掉）
(window._cleanOldQuota = function(){
  const today = new Date().toISOString().slice(0,10);
  // v1.1: 配额上限已更新，清除所有旧记录（含今日，避免卡在旧上限）
  const QUOTA_VERSION = 'v20260330';
  if(localStorage.getItem('quota_version') !== QUOTA_VERSION){
    Object.keys(localStorage).forEach(k => {
      if(k.startsWith('quota_')) localStorage.removeItem(k);
    });
    localStorage.setItem('quota_version', QUOTA_VERSION);
  } else {
    // 仅清理非今日的过期记录
    Object.keys(localStorage).forEach(k => {
      if(k.startsWith('quota_') && !k.endsWith('_'+today) && k !== 'quota_version'){
        localStorage.removeItem(k);
      }
    });
  }
})();

window.checkQuota = function(plan){
  const used = getQuotaUsed(plan);
  const limit = QUOTA[plan+'_daily'] || 0;
  return { used, limit, ok: used < limit };
}

/* ── 核心路由函数 ────────────────────────────────────────────── */
/**
 * aiGateway(messages, systemPrompt)
 * 按优先级选择通道：自带Key > Pro平台Key > 免费试用 > 模板
 * @returns { text: string, channel: 'own'|'platform'|'free'|'template' }
 */
window.aiGateway = async function(messages, systemPrompt){
  const plan = getUserPlan();

  // ① 检查用户自带 Key
  const ownKeyEnc = await idbGet('user_own_key');
  const ownProvider = localStorage.getItem('user_own_provider') || 'groq';
  if(ownKeyEnc){
    const ownKey = _xorDecode(ownKeyEnc);
    if(ownKey){
      try{
        const text = await _callAI(ownKey, ownProvider, messages, systemPrompt);
        return { text, channel: 'own' };
      }catch(e){
        console.warn('[GW] own key error:', e.message);
        // Key 失效，继续向下路由
      }
    }
  }

  // ② Pro/Elite 使用平台 Key
  if((plan === 'pro' || plan === 'elite') && PLATFORM_GROQ_KEY){
    const q = checkQuota(plan);
    if(q.ok){
      try{
        const text = await _callAI(PLATFORM_GROQ_KEY, 'groq', messages, systemPrompt);
        incQuotaUsed(plan);
        return { text, channel: 'platform' };
      }catch(e){
        console.warn('[GW] platform key error:', e.message);
      }
    } else {
      return { text: _quotaExceededMsg(plan, q), channel: 'quota' };
    }
  }

  // ③ 免费用户每日1次试用
  if(PLATFORM_GROQ_KEY){
    const q = checkQuota('free');
    if(q.ok){
      try{
        const text = await _callAI(PLATFORM_GROQ_KEY, 'groq', messages, systemPrompt);
        incQuotaUsed('free');
        return { text, channel: 'free' };
      }catch(e){
        console.warn('[GW] free trial error:', e.message);
      }
    }
  }

  // ④ 降级模板回复
  return { text: null, channel: 'template' };
}

window._quotaExceededMsg = function(plan, q){
  if(plan === 'pro')
    return `⚡ **今日 AI 额度已用完**（${q.used}/${q.limit} 次）\n\n升级到 **Elite $199/月** 可获得 ${QUOTA.elite_daily} 次/天，或配置您自己的 API Key 无限使用。\n\n[⚙️ 配置自己的 Key](javascript:showPage('account',null))`;
  return `⚡ **今日 AI 额度已用完**\n\n升级到 **Pro $79/月** 可获得 ${QUOTA.pro_daily} 次/天。\n\n[💎 查看套餐](javascript:showPage('account',null))`;
}

window._callAI = async function(apiKey, provider, messages, systemPrompt){
  let url, headers, body;
  const sys = systemPrompt ? [{role:'system', content: systemPrompt}] : [];
  const allMsgs = [...sys, ...messages];

  if(provider === 'openai'){
    url = 'https://api.openai.com/v1/chat/completions';
    headers = { 'Content-Type':'application/json', 'Authorization': `Bearer ${apiKey}` };
    body = JSON.stringify({ model: 'gpt-4o-mini', messages: allMsgs, max_tokens: 400, temperature: 0.6 });
  } else {
    // 默认 Groq（也兼容 OpenAI 格式）
    url = 'https://api.groq.com/openai/v1/chat/completions';
    headers = { 'Content-Type':'application/json', 'Authorization': `Bearer ${apiKey}` };
    body = JSON.stringify({ model: PLATFORM_GROQ_MODEL, messages: allMsgs, max_tokens: 400, temperature: 0.6 });
  }

  const res = await fetch(url, { method:'POST', headers, body, signal: AbortSignal.timeout(15000) });
  if(!res.ok){
    const err = await res.text();
    throw new Error(`HTTP ${res.status}: ${err.slice(0,200)}`);
  }
  const data = await res.json();
  return data.choices?.[0]?.message?.content || '';
}

/* ── 升级引导提示（模板回复时插入） ────────────────────────── */
window._upgradeHint = function(plan){
  if(plan === 'free'){
    const q = checkQuota('free');
    const trialLeft = Math.max(0, QUOTA.free_daily - q.used);
    if(trialLeft > 0){
      return `\n\n---\n💡 *今日还有 **${trialLeft}** 次免费 AI 体验。[升级 Pro →](javascript:showPage('account',null))*`;
    }
    return `\n\n---\n⚡ *今日免费额度已用完。[升级 Pro $79/月](javascript:showPage('account',null)) 或 [配置自己的 Key](javascript:openAIKeyModal()) 无限使用。*`;
  }
  return '';
}

/* ── API Key 设置弹窗 ────────────────────────────────────────── */
async function openAIKeyModal(){
  const existing = await idbGet('user_own_key');
  const decoded  = existing ? _xorDecode(existing) : '';
  const prov = localStorage.getItem('user_own_provider') || 'groq';
  const plan = getUserPlan();
  const q    = checkQuota(plan);

  // 状态说明
  let statusHtml = '';
  if(decoded){
    const masked = decoded.slice(0,8)+'••••••••'+decoded.slice(-4);
    statusHtml = `<div style="background:rgba(0,200,150,.08);border:1px solid rgba(0,200,150,.3);border-radius:8px;padding:10px 14px;margin-bottom:14px;font-size:13px">
      ✅ <strong>已配置自带 Key</strong>：<code>${masked}</code>（${prov}）
      <br><span style="color:var(--muted);font-size:12px">AI 请求直接发送到供应商，不经过本平台服务器</span>
    </div>`;
  } else if(PLATFORM_GROQ_KEY){
    statusHtml = `<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.3);border-radius:8px;padding:10px 14px;margin-bottom:14px;font-size:13px">
      🔵 <strong>使用平台 AI</strong>（${plan === 'free' ? '免费试用 '+Math.max(0,QUOTA.free_daily-q.used)+'/'+QUOTA.free_daily+' 次剩余' : plan+' 会员 '+Math.max(0,(QUOTA[plan+'_daily']||0)-q.used)+' 次剩余今日'}）
    </div>`;
  } else {
    statusHtml = `<div style="background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.3);border-radius:8px;padding:10px 14px;margin-bottom:14px;font-size:13px">
      ⚠️ 平台 AI 未配置，请使用自带 Key 或联系管理员
    </div>`;
  }

  const html = `
    <div class="modal-title">⚙️ AI 配置
      <span class="modal-close" onclick="closeModal('ai-key-modal')">✕</span>
    </div>
    ${statusHtml}

    <div style="margin-bottom:16px">
      <div style="font-size:13px;font-weight:600;margin-bottom:6px;color:var(--text)">选择 AI 供应商</div>
      <div style="display:flex;gap:8px;margin-bottom:12px">
        <button class="btn ${prov==='groq'?'btn-primary':'btn-outline'}" style="flex:1;font-size:13px" onclick="selectAIProvider('groq')">
          🚀 Groq（免费·快）
        </button>
        <button class="btn ${prov==='openai'?'btn-primary':'btn-outline'}" style="flex:1;font-size:13px" onclick="selectAIProvider('openai')">
          🧠 OpenAI GPT
        </button>
      </div>

      <div style="font-size:13px;font-weight:600;margin-bottom:6px;color:var(--text)">自带 API Key（存储在本地，不上传服务器）</div>
      <div style="display:flex;gap:8px">
        <input id="ai-key-input" type="password" placeholder="粘贴您的 API Key…"
          value="${decoded}"
          style="flex:1;background:var(--card2);border:1px solid var(--border);border-radius:8px;padding:10px 12px;color:var(--text);font-size:13px;font-family:monospace">
        <button class="btn btn-outline" style="font-size:12px;padding:0 12px" onclick="toggleAIKeyVisibility()">👁</button>
      </div>
      <div style="font-size:11px;color:var(--muted);margin-top:6px">
        🔒 Key 使用 XOR 混淆后存入 IndexedDB，不会上传到任何服务器
      </div>
    </div>

    <div style="background:var(--card2);border-radius:10px;padding:12px 14px;margin-bottom:16px;font-size:12px;color:var(--muted);line-height:1.7">
      <strong style="color:var(--text)">📖 如何获取免费 Groq Key：</strong><br>
      1. 访问 <a href="https://console.groq.com" target="_blank" style="color:var(--green)">console.groq.com</a> → 注册免费账号<br>
      2. 进入 API Keys → Create API Key<br>
      3. 复制 Key 粘贴到上方输入框<br>
      <span style="color:var(--green)">✅ Groq 免费层每天有充足额度，个人使用完全够用</span>
    </div>

    <div style="display:flex;gap:8px">
      <button class="btn btn-primary" style="flex:1" onclick="saveAIKey()">💾 保存 Key</button>
      ${decoded ? '<button class="btn btn-danger" style="flex:1" onclick="clearAIKey()">🗑 清除 Key</button>' : ''}
    </div>
  `;

  let modal = document.getElementById('ai-key-modal');
  if(!modal){
    modal = document.createElement('div');
    modal.id = 'ai-key-modal';
    modal.className = 'modal-overlay';
    modal.innerHTML = `<div class="modal-box" style="max-width:480px">${html}</div>`;
    modal.addEventListener('click', e=>{ if(e.target===modal) closeModal('ai-key-modal'); });
    document.body.appendChild(modal);
  } else {
    modal.querySelector('.modal-box').innerHTML = html;
  }
  modal.style.display = 'flex';
  setTimeout(()=>modal.classList.add('open'),10);
}

function selectAIProvider(prov){
  localStorage.setItem('user_own_provider', prov);
  openAIKeyModal(); // 刷新弹窗
}

function toggleAIKeyVisibility(){
  const inp = document.getElementById('ai-key-input');
  if(inp) inp.type = inp.type === 'password' ? 'text' : 'password';
}

async function saveAIKey(){
  const inp = document.getElementById('ai-key-input');
  const key = inp ? inp.value.trim() : '';
  if(!key){ toast('请输入 API Key','error'); return; }
  // 基本格式校验
  const prov = localStorage.getItem('user_own_provider') || 'groq';
  if(prov === 'groq' && !key.startsWith('gsk_')){ toast('Groq Key 应以 gsk_ 开头，请检查','error'); return; }
  if(prov === 'openai' && !key.startsWith('sk-')){ toast('OpenAI Key 应以 sk- 开头，请检查','error'); return; }

  await idbSet('user_own_key', _xorEncode(key));
  closeModal('ai-key-modal');
  toast('✅ API Key 已保存，AI 请求将直接走您的 Key','');
}

async function clearAIKey(){
  await idbDel('user_own_key');
  closeModal('ai-key-modal');
  toast('已清除自带 Key，恢复使用平台 AI','');
}

/* ── 把 CS 客服模块接入 AI Gateway ─────────────────────────── */
// 覆盖 csDoSend 的 AI 调用部分，走 Gateway 路由
async function csFetchGroqGateway(userMsg){
  const SYSTEM_PROMPT = `你是 QuantAI 量化交易平台的 AI 客服助手，熟悉平台所有功能，可回答用户关于使用方法的任何问题。

【平台功能模块】
• 仪表盘：资产总览、实时行情
• 行情：22个交易品种K线（BTC/ETH/SOL/BNB/XRP外汇/黄金/原油/纳指/标普/恒生等）
• AI顾问：行情分析、仓位建议、策略推荐、指标解读
• 持仓：查看当前持仓、AI分析按钮
• 策略管理：MACD/EMA/RSI/网格/布林带策略创建和启动
• 回测：历史数据验证策略（日期范围/品种/仓位比例可配置）
• 复制交易：跟随交易者、自动同步开仓
• 自动建仓（Elite专属）：策略触发/定时定投(DCA)/跟单同步
• 交易广场：分享观点、情绪标签
• 策略市场：发现/购买/发布量化策略
• 信号广播：发布交易信号供他人订阅
• 我的账户：券商连接（币安/OKX/INFINOX MT5）、套餐升级、风控设置
• FRED宏观数据：美联储利率/CPI/非农/GDP（offline时显示静态默认值）
• 法律文档：隐私政策/服务条款/Cookie政策/社区准则（在"我的账户"底部）

【订阅套餐】
| 套餐 | 价格 | 核心功能 |
| Basic | $29/月 | 全品种行情、AI顾问、2个策略、自动交易 |
| Pro | $79/月 | 无限策略、AI自动交易、高级回测、多券商 |
| Elite | $199/月 | 自动建仓(策略/定投/跟单)、复制交易无限跟单、VIP客服、优先通道 |

【支持语言】中文/English/日本語/한국어/Русский/العربية，右上角切换，实时生效

【常见问题】
Q:K线不显示？→ Ctrl+Shift+R强制刷新/换浏览器/关AdBlock
Q:FRED offline？→ 中国大陆网络无法访问，显示静态默认值不影响使用
Q:连接券商？→ 我的账户→已连接券商→添加新券商
Q:自动建仓？→ Elite专属，策略触发/定时定投/跟单同步3种模式
Q:API Key安全？→ 存本地localStorage，不上传；建议不开提现权限+IP白名单

【回复规则】
1.简洁友好，不超过200字，**加粗重点**
2.涉及支付/账户安全 → "需要人工客服协助，请说【转人工】"
3.功能问题 → 告知【具体页面和操作步骤】
4.语言跟随用户
5.不确定 → 转人工，不胡乱回答`;

  const msgs = [..._csHistory.slice(-6), {role:'user', content: userMsg}];
  const result = await aiGateway(msgs, SYSTEM_PROMPT);

  if(result.channel === 'template') return null; // 降级本地
  if(result.channel === 'quota') return result.text;
  return result.text || null;
}

/* ── 覆盖原 CS 发送函数，接入 Gateway ── */
const _origCsDoSend = typeof csDoSend !== 'undefined' ? csDoSend : null;
// 直接挂钩到 csFetchGroq，保持兼容
window._origCsFetchGroq = window.csFetchGroq;
window.csFetchGroq = async function(userMsg){
  // 先尝试 Gateway
  const result = await csFetchGroqGateway(userMsg);
  if(result !== null) return result;
  // 降级本地知识库
  return await csLocalReply(userMsg);
};

// 覆盖客服发送逻辑：免费用户无自带Key且无平台Key时，加引导提示
const _origCsSend = window.csDoSend;
window.csDoSend = async function(){
  // 原始逻辑不变，追加在 csAddMsg 后注入提示（通过monkey-patch）
  if(typeof _origCsSend === 'function') return _origCsSend.apply(this, arguments);
};/* ── 账户页 AI 配置卡片渲染 ─────────────────────────────────── */
async function renderAIConfigCard(){
  const plan = getUserPlan();
  const ownKeyEnc = await idbGet('user_own_key');
  const hasOwnKey = !!(ownKeyEnc && _xorDecode(ownKeyEnc));
  const prov = localStorage.getItem('user_own_provider') || 'groq';

  let channelDesc, channelBadge, channelBadgeStyle;
  if(hasOwnKey){
    channelDesc = `使用您自己的 ${prov === 'openai' ? 'OpenAI' : 'Groq'} Key，无限调用，不消耗平台配额`;
    channelBadge = '自带 Key ✅';
    channelBadgeStyle = 'background:rgba(0,200,150,.15);color:var(--green)';
  } else if(PLATFORM_GROQ_KEY && (plan === 'pro' || plan === 'elite')){
    channelDesc = `使用平台 Groq AI（${plan === 'pro' ? 'Pro' : 'Elite'} 会员权益）`;
    channelBadge = '平台 AI 🔵';
    channelBadgeStyle = 'background:rgba(59,130,246,.15);color:#60a5fa';
  } else if(PLATFORM_GROQ_KEY){
    channelDesc = '免费试用模式，每日限1次 AI 回答';
    channelBadge = '试用 ⚡';
    channelBadgeStyle = 'background:rgba(245,158,11,.15);color:#f59e0b';
  } else {
    channelDesc = '知识库模式（平台 AI 未配置）';
    channelBadge = '离线模式';
    channelBadgeStyle = 'background:rgba(239,68,68,.15);color:#ef4444';
  }

  const q = checkQuota(hasOwnKey ? 'own' : plan === 'free' ? 'free' : plan);
  const limit = hasOwnKey ? null : (QUOTA[plan+'_daily'] || QUOTA.free_daily);
  const used  = hasOwnKey ? 0 : getQuotaUsed(plan === 'free' ? 'free' : plan);
  const pct   = (limit && limit > 0) ? Math.min(100, Math.round(used/limit*100)) : 0;

  const desc   = document.getElementById('ai-channel-desc');
  const badge  = document.getElementById('ai-channel-badge');
  const qdesc  = document.getElementById('ai-quota-desc');
  const qbar   = document.getElementById('ai-quota-bar');
  const qtext  = document.getElementById('ai-quota-text');
  const kbtn   = document.getElementById('ai-key-status-btn');

  if(desc)  desc.textContent = channelDesc;
  if(badge){ badge.textContent = channelBadge; badge.style.cssText += ';'+channelBadgeStyle; }
  if(qdesc) qdesc.textContent = hasOwnKey ? '自带 Key，无配额限制' : `今日已使用 ${used} / ${limit} 次`;
  if(qbar)  qbar.style.width = pct+'%';
  if(pct > 80 && qbar) qbar.style.background = '#ef4444';
  if(qtext) qtext.textContent = hasOwnKey ? '∞ 无限制' : `${used}/${limit}`;
  if(kbtn)  kbtn.textContent = hasOwnKey ? '已配置 ✅ 修改' : '设置 Key';
}

// 页面切换到 account 时刷新
const _origShowPage = window.showPage;
window.showPage = function(page, el){
  if(typeof _origShowPage === 'function') _origShowPage.call(this, page, el);
  if(page === 'account'){
    setTimeout(renderAIConfigCard, 200);
  }
};

// 初始化时渲染一次
window.addEventListener('load', ()=>{ setTimeout(renderAIConfigCard, 500); });


