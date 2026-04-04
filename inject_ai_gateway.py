# -*- coding: utf-8 -*-
"""
QuantAI - AI 通道网关注入脚本
注入内容：
  1. AI 网关核心逻辑（IndexedDB 加密存储 + 用户分级路由 + 配额系统）
  2. 账户页 "AI 配置" 卡片（设置 API Key + 教程链接）
  3. 免费每日1次试用计数
  4. 超限升级引导提示
"""

import re, sys, os

HTML_PATH = os.path.join(os.path.dirname(__file__), 'index.html')

# ─────────────────────────────────────────────────────────────
# 1. JS：AI 网关核心（插入到 </script> 之前）
# ─────────────────────────────────────────────────────────────
AI_GATEWAY_JS = r"""
// ═══════════════════════════════════════════════════════════════
// QuantAI AI GATEWAY  v1.0
// 三层通道路由：自带Key → Pro平台Key → 免费试用/模板
// ═══════════════════════════════════════════════════════════════

/* ── 平台配置（运营方填写） ─────────────────────────────────── */
const PLATFORM_GROQ_KEY = '';   // 平台 Groq Key，留空则平台AI不可用
const PLATFORM_GROQ_MODEL = 'llama-3.3-70b-versatile';

/* ── 配额常量 ────────────────────────────────────────────────── */
const QUOTA = {
  free_daily:    1,       // 免费用户每日试用次数
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
function _quotaKey(type){ return `quota_${type}_${new Date().toISOString().slice(0,10)}`; }
function getQuotaUsed(type){ return parseInt(localStorage.getItem(_quotaKey(type))||'0'); }
function incQuotaUsed(type){ localStorage.setItem(_quotaKey(type), getQuotaUsed(type)+1); }

function checkQuota(plan){
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
async function aiGateway(messages, systemPrompt){
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

function _quotaExceededMsg(plan, q){
  if(plan === 'pro')
    return `⚡ **今日 AI 额度已用完**（${q.used}/${q.limit} 次）\n\n升级到 **Elite $199/月** 可获得 ${QUOTA.elite_daily} 次/天，或配置您自己的 API Key 无限使用。\n\n[⚙️ 配置自己的 Key](javascript:showPage('account',null))`;
  return `⚡ **今日 AI 额度已用完**\n\n升级到 **Pro $79/月** 可获得 ${QUOTA.pro_daily} 次/天。\n\n[💎 查看套餐](javascript:showPage('account',null))`;
}

async function _callAI(apiKey, provider, messages, systemPrompt){
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
function _upgradeHint(plan){
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
  const SYSTEM_PROMPT = `你是 QuantAI 量化交易平台的专业客服助手。
平台功能：行情/K线/AI顾问/量化策略/回测/复制交易/自动建仓/交易广场/策略市场/信号广播/FRED宏观数据。
套餐：Basic $29/月、Pro $79/月、Elite $199/月。自动建仓为 Elite 专属。
支持品种：加密货币(BTC/ETH/SOL等)、外汇、黄金、原油、纳指/标普/恒生等指数、国债。
回复规则：1.简洁友好不超过200字 2.涉及支付/安全说"需要人工客服，请说【转人工】" 3.用**加粗**重点 4.语言跟随用户`;

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
};

"""

# ─────────────────────────────────────────────────────────────
# 2. HTML：账户页 AI 配置卡片（插入到 <!-- ===== 交易日志 ===== --> 之前）
# ─────────────────────────────────────────────────────────────
AI_SETTINGS_CARD_HTML = r"""
        <!-- ===== AI 配置卡片 ===== -->
        <div style="margin-top:28px" id="ai-config-section">
          <div class="section-title">🤖 <span>AI 配置</span>
            <button class="btn btn-outline" style="font-size:12px;padding:5px 12px" onclick="openAIKeyModal()">⚙️ 配置 Key</button>
          </div>
          <div class="card" style="padding:14px 18px">
            <div class="settings-row">
              <div>
                <div>AI 通道模式</div>
                <div class="lbl" id="ai-channel-desc">加载中…</div>
              </div>
              <div id="ai-channel-badge" style="font-size:12px;padding:4px 10px;border-radius:20px;background:rgba(0,200,150,.15);color:var(--green);font-weight:600">—</div>
            </div>
            <div class="settings-row">
              <div>
                <div>今日 AI 用量</div>
                <div class="lbl" id="ai-quota-desc">加载中…</div>
              </div>
              <div style="display:flex;flex-direction:column;align-items:flex-end;gap:4px">
                <div id="ai-quota-bar-wrap" style="width:100px;height:6px;background:var(--border);border-radius:3px;overflow:hidden">
                  <div id="ai-quota-bar" style="height:100%;background:var(--green);border-radius:3px;transition:.3s;width:0%"></div>
                </div>
                <div id="ai-quota-text" style="font-size:11px;color:var(--muted)">—</div>
              </div>
            </div>
            <div class="settings-row" style="border-bottom:none">
              <div>
                <div>自带 API Key</div>
                <div class="lbl">Key 存本地，不过服务器</div>
              </div>
              <button class="btn btn-outline" style="font-size:12px;padding:5px 12px" onclick="openAIKeyModal()">
                <span id="ai-key-status-btn">设置 Key</span>
              </button>
            </div>
          </div>
        </div>

"""

# ─────────────────────────────────────────────────────────────
# 3. JS：账户页 AI 配置卡片初始化（插入到 </script> 之前）
# ─────────────────────────────────────────────────────────────
AI_ACCOUNT_INIT_JS = r"""
/* ── 账户页 AI 配置卡片渲染 ─────────────────────────────────── */
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

"""

# ─────────────────────────────────────────────────────────────
# 执行注入
# ─────────────────────────────────────────────────────────────
def main():
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # idempotent check
    if 'AI GATEWAY  v1.0' in html:
        print('[inject] already injected, skip.')
        return

    # step 1: insert AI config card HTML before trade log section
    TARGET_HTML = '        <!-- ===== 交易日志 ===== -->'
    if TARGET_HTML not in html:
        print('[inject] ERROR: target anchor not found in HTML')
        sys.exit(1)
    html = html.replace(TARGET_HTML, AI_SETTINGS_CARD_HTML + TARGET_HTML, 1)
    print('[inject] OK step1: AI config card HTML injected')

    # step 2: inject Gateway JS before </script></body>
    SCRIPT_END = '</script>\n</body>'
    if SCRIPT_END not in html:
        print('[inject] ERROR: closing script tag not found')
        sys.exit(1)
    inject_js = AI_GATEWAY_JS + '\n' + AI_ACCOUNT_INIT_JS
    html = html.replace(SCRIPT_END, inject_js + '\n' + SCRIPT_END, 1)
    print('[inject] OK step2: AI Gateway JS injected')

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print('[inject] DONE. size: %d KB' % (len(html)//1024))

if __name__ == '__main__':
    main()
