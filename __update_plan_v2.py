#!/usr/bin/env python3
"""Update QuantAI plan system: 4 tiers + revenue sharing + node selection + addon packs."""

import re

def rb(path):
    with open(path, 'rb') as f:
        return f.read()

def rw(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def wb(path, data):
    with open(path, 'wb') as f:
        f.write(data)

def ww(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)

PATH = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
raw = rb(PATH)
t = rw(PATH)

# ==============================================================
# 1. PLAN CONFIG: replace QUOTA + plan functions
# ==============================================================
# Find the section from QUOTA definition to getUserPlan

OLD_PLAN_SECTION = """/* ── 配额常量 ────────────────────────────────────────────────── */
window.QUOTA = {
  free_daily:    20,      // 免费用户每日试用次数（上线前改回1-3）
  pro_daily:     100,     // Pro 用户每日调用次数
  elite_daily:   500,     // Elite 用户每日调用次数
  pro_tokens:    80000,   // Pro 用户每日 Token 软上限（估算）
  elite_tokens:  400000,  // Elite 用户每日 Token 软上限
};"""

NEW_PLAN_SECTION = """/* ── 套餐体系配置 ──────────────────────────────────────────── */
window.PLANS = {
  free: {
    id: 'free', name: '免费试用', nameEn: 'Free Trial', price: 0, period: '14天限时',
    icon: '🔓', nodes: ['default'], nodeCount: '固定默认节点',
    features: { strategies: 3, aiCalls: 20, metaApiCalls: 100, autoTrade: false, liveTrade: false,
      advancedBacktest: false, factorAnalysis: false, copyTrade: false, hft: false, tvUltimate: false,
      multiRegion: false, nodeSelectable: false },
    badge: '🔓', badgeColor: 'rgba(150,150,150,.2)'
  },
  basic: {
    id: 'basic', name: '基础套餐', nameEn: 'Basic', price: 29, period: '月',
    icon: '🥉', nodes: ['default'], nodeCount: '固定通用节点',
    features: { strategies: -1, aiCalls: 100, metaApiCalls: 500, autoTrade: false, liveTrade: false,
      advancedBacktest: false, factorAnalysis: false, copyTrade: false, hft: false, tvUltimate: false,
      multiRegion: false, nodeSelectable: false },
    badge: '🥉', badgeColor: 'rgba(205,127,50,.2)'
  },
  pro: {
    id: 'pro', name: '专业套餐', nameEn: 'Pro', price: 99, period: '月',
    icon: '🥈', nodes: ['tokyo','singapore'], nodeCount: '可选 2 区域',
    features: { strategies: -1, aiCalls: -1, metaApiCalls: 5000, autoTrade: true, liveTrade: true,
      advancedBacktest: true, factorAnalysis: true, copyTrade: true, hft: false, tvUltimate: false,
      multiRegion: false, nodeSelectable: true },
    badge: '🥈', badgeColor: 'rgba(192,192,192,.2)'
  },
  flagship: {
    id: 'flagship', name: '旗舰套餐', nameEn: 'Flagship', price: 149, period: '月',
    icon: '👑', nodes: ['tokyo','singapore','london','newyork'], nodeCount: '4 大区全节点',
    features: { strategies: -1, aiCalls: -1, metaApiCalls: -1, autoTrade: true, liveTrade: true,
      advancedBacktest: true, factorAnalysis: true, copyTrade: true, hft: true, tvUltimate: true,
      multiRegion: true, nodeSelectable: true },
    badge: '👑', badgeColor: 'rgba(255,215,0,.2)'
  }
};

/* ── 节点配置 ───────────────────────────────────────────────── */
window.NODES = {
  tokyo:    { id: 'tokyo',    name: '东京',     flag: '🇯🇵', region: 'ap-northeast-1', latency: 2,  color: '#E53935', desc: '日本东京 · 低延迟亚太' },
  singapore:{ id: 'singapore',name: '新加坡',   flag: '🇸🇬', region: 'ap-southeast-1', latency: 5,  color: '#FF6F00', desc: '新加坡 · 东南亚枢纽' },
  london:   { id: 'london',   name: '伦敦',     flag: '🇬🇧', region: 'eu-west-2',     latency: 85, color: '#1E88E5', desc: '英国伦敦 · 欧非覆盖' },
  newyork:  { id: 'newyork',  name: '纽约',     flag: '🇺🇸', region: 'us-east-1',     latency: 65, color: '#7B1FA2', desc: '美国东岸 · 北美专线' },
  default:  { id: 'default',  name: '通用节点', flag: '🌐', region: 'auto',          latency: 0,  color: '#666',   desc: '系统自动分配' }
};

/* ── 增值包配置 ─────────────────────────────────────────────── */
window.ADDONS = {
  tvUltimate:     { id: 'tvUltimate',     name: 'TradingView Ultimate 高级数据包',      icon: '📊', price: 29,  period: '月',
                    desc: '机构级盘口、逐笔成交、深度指标，提升策略精准度' },
  strategyCustom:{ id: 'strategyCustom',  name: '高级策略定制包',                       icon: '⚡', price: 49,  period: '月',
                    desc: 'AI+人工定制专属策略、参数迭代、专属交易模型' },
  backtestPro:    { id: 'backtestPro',    name: '专业回测增强包',                       icon: '🔬', price: 19,  period: '月',
                    desc: '全量参数优化、风险归因、多周期深度回测报告' },
  multiAccount:   { id: 'multiAccount',   name: '多账户扩容包',                         icon: '🏦', price: 39,  period: '月',
                    desc: '提升绑定 MetaAPI 交易账户数量上限' },
  nodeBoost:      { id: 'nodeBoost',      name: '单节点扩容增量包',                     icon: '🌍', price: 14,  period: '月',
                    desc: '低档位用户额外解锁任意国际节点' },
  vipSupport:     { id: 'vipSupport',     name: 'VIP 运维专属包',                       icon: '👨‍💻', price: 99,  period: '月',
                    desc: '1v1 技术支持、节点故障优先排查' }
};

/* ── 全球阶梯收益分成 ───────────────────────────────────────── */
window.REVENUE_SHARE = [
  { min: 0,      max: 1000,   rate: 0,   label: '≤$1,000' },
  { min: 1001,   max: 5000,   rate: 0.05,label: '$1,001~$5,000' },
  { min: 5001,   max: 20000,  rate: 0.08,label: '$5,001~$20,000' },
  { min: 20001,  max: Infinity,rate: 0.10,label: '>$20,000' }
];
window.calcRevenueShare = function(monthlyPnl){
  // Return {tiers[], totalShare, effectiveRate}
  if(!monthlyPnl || monthlyPnl <= 1000) return {tiers:[{from:0, to:1000, rate:0, amount:0, share:0}], totalShare:0, effectiveRate:0};
  var tiers = [];
  var total = 0;
  var remaining = Math.max(0, monthlyPnl - 1000); // first $1000 free
  var t;
  for(var i=1; i<window.REVENUE_SHARE.length; i++){
    t = window.REVENUE_SHARE[i];
    var bandMin = Math.max(0, t.min - 1001);
    var bandMax = Math.max(0, t.max - 1001);
    if(t.max === Infinity) bandMax = remaining;
    var bandAmount = Math.min(remaining, bandMax - bandMin);
    if(bandAmount <= 0) { tiers.push({from:Math.max(1001,t.min), to:t.max===Infinity?'∞':t.max, rate:t.rate, amount:0, share:0}); continue; }
    var share = Math.round(bandAmount * t.rate * 100) / 100;
    tiers.push({from:Math.max(1001,t.min), to:t.max===Infinity?'∞':t.max, rate:t.rate, amount:bandAmount, share:share});
    total += share;
    remaining -= bandAmount;
    if(remaining <= 0) break;
  }
  return {tiers:tiers, totalShare:Math.round(total*100)/100, effectiveRate:Math.round(total/monthlyPnl*10000)/100};
};

/* ── 队列映射 ─────────────────────────────────────────── */
window.PLAN_ORDER = ['free','basic','pro','flagship'];

window.getPlanInfo = function(planId){
  return window.PLANS[planId] || window.PLANS.free;
};
window.getPlanBadge = function(planId){
  var p = window.getPlanInfo(planId);
  return '<span style="font-size:11px;padding:1px 8px;border-radius:10px;background:' + p.badgeColor + ';color:var(--text)">' + p.badge + ' ' + p.name + '</span>';
};
window.getPlanPrice = function(planId){
  var p = window.getPlanInfo(planId);
  return p.price === 0 ? '免费' : '$' + p.price + '/' + p.period;
};
window.canUseNode = function(planId, nodeId){
  var p = window.getPlanInfo(planId);
  return p.nodes.indexOf(nodeId) >= 0;
};
window.getUserPlanNodes = function(planId){
  var p = window.getPlanInfo(planId);
  return p.nodes;
};
window.getUserPlanFeature = function(planId, feature){
  var p = window.getPlanInfo(planId);
  return p.features[feature] || false;
};"""

# Find the boundary: replace from QUOTA constant down to getUserPlan
t = t.replace('/* ── 配额常量 ────────────────────────────────────────────────── */\nwindow.QUOTA = {', '/* ── 套餐体系配置 ──────────────────────────────────────────── */\nwindow.PLANS = {')
# Find the end of QUOTA object (line with '};')
quota_start = t.find('window.PLANS = {')
quota_end = t.find('\n};', quota_start) + 3
# Find getUserPlan func
plan_func_start = t.find('function getUserPlan')
plan_func_end = t.find('\n\n/* ── 核心路由函数', plan_func_start)

# We need to remove the old QUOTA block and replace with PLANS block
# Actually let's just do a targeted replacement
OLD_QUOTA_BLOCK = t[quota_start:quota_end]
print(f"QUOTA block length: {len(OLD_QUOTA_BLOCK)}")
print(f"First 100 chars: {OLD_QUOTA_BLOCK[:100]}")

# Replace QUOTA block with PLANS
t = t.replace(OLD_QUOTA_BLOCK, NEW_PLAN_SECTION)

print("QUOTA replaced with PLANS config")

# ==============================================================
# 2. Remove old QUOTA const and update checkQuota
# ==============================================================
# Remove: const QUOTA_VERSION = ... and _cleanOldQuota
OLD_QUOTA_CRUD = """/* ── 每日配额追踪 ────────────────────────────────────────────── */
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
}"""

NEW_QUOTA_CRUD = """/* ── 每日配额追踪 ────────────────────────────────────────────── */
window._quotaKey = function(type){ return `quota_${type}_${new Date().toISOString().slice(0,10)}`; }
window.getQuotaUsed = function(type){ return parseInt(localStorage.getItem(_quotaKey(type))||'0'); }
window.incQuotaUsed = function(type){ localStorage.setItem(_quotaKey(type), getQuotaUsed(type)+1); }
// 自动清理过期配额
window.checkQuota = function(planId){
  var p = window.getPlanInfo(planId);
  var limit = p.features.aiCalls;
  if(limit < 0) return { used:0, limit:-1, ok:true };
  var used = window.getQuotaUsed(planId);
  return { used:used, limit:limit, ok: used < limit };
}"""

if OLD_QUOTA_CRUD in t:
    t = t.replace(OLD_QUOTA_CRUD, NEW_QUOTA_CRUD)
    print("QUOTA CRUD replaced")
else:
    print("WARN: OLD_QUOTA_CRUD not found")
    # Try partial match
    if 'getQuotaUsed' in t:
        print("getQuotaUsed found, doing line-level replacement")
    else:
        print("getQuotaUsed NOT found")

# ==============================================================
# 3. Update getUserPlan to use new 4-tier system
# ==============================================================
OLD_PLAN_FUNC = "// plan: 'free' | 'basic' | 'pro' | 'elite'\nfunction getUserPlan(){\n  return localStorage.getItem('qplan') || 'pro'; // 演示默认 pro\n}\nfunction setUserPlan(plan){\n  localStorage.setItem('qplan', plan);\n}"

NEW_PLAN_FUNC = "// plan: 'free' | 'basic' | 'pro' | 'flagship'\nfunction getUserPlan(){\n  return localStorage.getItem('qplan') || 'flagship'; // 演示默认旗舰\n}\nfunction setUserPlan(plan){\n  localStorage.setItem('qplan', plan);\n}"

if OLD_PLAN_FUNC in t:
    t = t.replace(OLD_PLAN_FUNC, NEW_PLAN_FUNC)
    print("User plan functions updated")
else:
    print("WARN: OLD_PLAN_FUNC not found")

# ==============================================================
# 4. Update sidebar plan badge (line ~1397)
# ==============================================================
OLD_SIDEBAR_PLAN = """          <div class="plan">⭐ <span data-i18n="acc_member_pro">Pro 会员</span></div>"""

NEW_SIDEBAR_PLAN = """          <div class="plan" id="sidebar-plan-badge"><span id="sidebar-plan-icon">👑</span> <span id="sidebar-plan-name">旗舰套餐</span></div>"""

if OLD_SIDEBAR_PLAN in t:
    t = t.replace(OLD_SIDEBAR_PLAN, NEW_SIDEBAR_PLAN)
    print("Sidebar plan badge updated")
else:
    print("WARN: Sidebar plan badge not found")

# ==============================================================
# 5. Update account page asset overview + add plan tab
# ==============================================================
OLD_ACCOUNT_HEADER = """        <!-- ===== 第1行：核心资产总览 ===== -->
        <div class="asset-overview" style="background:linear-gradient(135deg,rgba(0,200,150,.15),rgba(0,100,200,.1));border:1px solid rgba(0,200,150,.3);border-radius:16px;padding:20px;margin-bottom:16px">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
            <div style="font-size:14px;color:var(--muted)">💰 总资产</div>
            <div style="font-size:12px;padding:4px 10px;background:rgba(0,200,150,.2);color:var(--green);border-radius:20px">Pro 会员</div>
          </div>
          <div style="font-size:32px;font-weight:800;color:var(--text);margin-bottom:16px">$12,450.45</div>
          <div style="display:flex;gap:24px">
            <div>
              <div style="font-size:12px;color:var(--muted);margin-bottom:4px">📈 今日盈亏</div>
              <div style="font-size:16px;font-weight:600;color:var(--green)">+$328.50 <span style="font-size:12px;color:var(--green)">(2.70%)</span></div>
            </div>
            <div>
              <div style="font-size:12px;color:var(--muted);margin-bottom:4px">📊 累计盈亏</div>
              <div style="font-size:16px;font-weight:600;color:var(--green)">+$4,820.00 <span style="font-size:12px;color:var(--green)">(63.12%)</span></div>
            </div>
          </div>
        </div>"""

NEW_ACCOUNT_HEADER = """        <!-- ===== 第1行：套餐概览 ===== -->
        <div class="asset-overview" style="background:linear-gradient(135deg,rgba(255,215,0,.12),rgba(0,100,200,.1));border:1px solid rgba(255,215,0,.25);border-radius:16px;padding:20px;margin-bottom:16px">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:8px">
            <div style="display:flex;align-items:center;gap:10px">
              <span id="acc-plan-icon" style="font-size:28px">👑</span>
              <div>
                <div style="font-size:14px;font-weight:700" id="acc-plan-name">旗舰套餐</div>
                <div style="font-size:11px;color:var(--muted)" id="acc-plan-price">$149/月</div>
              </div>
            </div>
            <div style="display:flex;gap:8px">
              <button class="btn btn-primary" style="font-size:12px;padding:6px 14px" onclick="showPlanUpgradeModal()">🔄 升级</button>
              <button class="btn btn-outline" style="font-size:12px;padding:6px 14px" onclick="showAddonShop()">+ 增值包</button>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px">
            <div>
              <div style="font-size:11px;color:var(--muted);margin-bottom:4px">💰 总资产</div>
              <div style="font-size:24px;font-weight:800;color:var(--text)" id="acc-total-asset">$12,450.45</div>
            </div>
            <div>
              <div style="font-size:11px;color:var(--muted);margin-bottom:4px">📈 本月已结算盈亏</div>
              <div style="font-size:24px;font-weight:800;color:var(--green)" id="acc-monthly-pnl">+$4,820.00</div>
            </div>
            <div>
              <div style="font-size:11px;color:var(--muted);margin-bottom:4px">📊 应付分成</div>
              <div id="acc-revenue-share" style="font-size:24px;font-weight:800;color:var(--yellow)">$286.40</div>
              <div style="font-size:10px;color:var(--muted)" id="acc-revenue-rate">实际分成率 5.94%</div>
            </div>
          </div>
        </div>"""

if OLD_ACCOUNT_HEADER in t:
    t = t.replace(OLD_ACCOUNT_HEADER, NEW_ACCOUNT_HEADER)
    print("Account header replaced with plan overview")
else:
    print("WARN: Account header not found")

# ==============================================================
# 6. Add new account tab for Plan / Billing
# ==============================================================
# Find the account tabs and add a "方案" tab
OLD_TABS = """          <div class="acc-tab" onclick="switchAccountTab('wallet',this)" style="flex:1;text-align:center;padding:12px;font-size:13px;font-weight:600;color:var(--muted);cursor:pointer" data-i18n="acc_tab_wallet">💳 钱包</div>
        </div>"""

NEW_TABS = """          <div class="acc-tab" onclick="switchAccountTab('wallet',this)" style="flex:1;text-align:center;padding:12px;font-size:13px;font-weight:600;color:var(--muted);cursor:pointer" data-i18n="acc_tab_wallet">💳 钱包</div>
          <div class="acc-tab" onclick="switchAccountTab('plan',this)" style="flex:1;text-align:center;padding:12px;font-size:13px;font-weight:600;color:var(--muted);cursor:pointer">📋 方案</div>
          <div class="acc-tab" onclick="switchAccountTab('billing',this)" style="flex:1;text-align:center;padding:12px;font-size:13px;font-weight:600;color:var(--muted);cursor:pointer">💰 账单</div>
        </div>"""

if OLD_TABS in t:
    t = t.replace(OLD_TABS, NEW_TABS)
    print("Account tabs updated")
else:
    print("WARN: Account tabs not found")

# ==============================================================
# 6b. Add plan tab content + billing tab content before wallet tab
# ==============================================================
OLD_WALLET_START = """            <div id="acc-tab-wallet" style="display:none">"""

TAB_PLAN_CONTENT = """            <div id="acc-tab-plan" style="display:none">
            <div class="card" style="padding:16px">
              <div style="font-size:14px;font-weight:600;margin-bottom:12px">📋 当前方案 <span id="tab-plan-badge" style="font-size:11px;padding:2px 10px;border-radius:10px;background:rgba(255,215,0,.2);color:var(--green);margin-left:8px">👑 旗舰套餐</span></div>
              <div id="tab-plan-nodes" style="font-size:12px;color:var(--muted);margin-bottom:16px">节点：东京🇯🇵 新加坡🇸🇬 伦敦🇬🇧 纽约🇺🇸</div>
              
              <!-- 套餐选择网格 -->
              <div id="plan-select-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin-bottom:16px"></div>
              
              <!-- 节点选择（仅专业/旗舰） -->
              <div id="plan-node-selector" style="background:rgba(0,200,150,.06);border:1px solid rgba(0,200,150,.15);border-radius:10px;padding:14px;margin-bottom:14px;display:none">
                <div style="font-size:13px;font-weight:600;margin-bottom:10px">🌍 选择节点区域</div>
                <div id="node-options" style="display:flex;gap:8px;flex-wrap:wrap"></div>
                <div id="node-current" style="font-size:11px;color:var(--muted);margin-top:8px">当前：默认节点</div>
              </div>
              
              <!-- 增值包列表 -->
              <div style="border-top:1px solid var(--border);padding-top:14px;margin-top:14px">
                <div style="font-size:13px;font-weight:600;margin-bottom:10px">📦 已购增值包 <span style="font-size:11px;color:var(--muted);font-weight:400" id="addon-count">(0)</span></div>
                <div id="addon-list" style="display:flex;flex-direction:column;gap:6px"></div>
                <button class="btn btn-outline" style="margin-top:8px;font-size:12px;padding:8px 16px;width:100%" onclick="showAddonShop()">+ 前往增值包商店</button>
              </div>
            </div>
            </div>

            <div id="acc-tab-billing" style="display:none">
            <div class="card" style="padding:16px">
              <div style="font-size:14px;font-weight:600;margin-bottom:12px">💰 月度对账</div>
              <!-- 每月摘要 -->
              <div style="display:flex;justify-content:space-between;background:rgba(0,200,150,.06);border-radius:10px;padding:14px;margin-bottom:14px">
                <div>
                  <div style="font-size:11px;color:var(--muted)">本月净利润</div>
                  <div style="font-size:20px;font-weight:800;color:var(--green)" id="bill-month-pnl">$4,820.00</div>
                </div>
                <div style="text-align:right">
                  <div style="font-size:11px;color:var(--muted)">应付分成</div>
                  <div style="font-size:20px;font-weight:800;color:var(--yellow)" id="bill-month-share">$286.40</div>
                </div>
              </div>
              <!-- 分成明细 -->
              <div id="bill-tiers" style="display:flex;flex-direction:column;gap:4px;margin-bottom:14px;font-size:12px"></div>
              <!-- 结算操作 -->
              <div style="border-top:1px solid var(--border);padding-top:14px">
                <div style="font-size:13px;font-weight:600;margin-bottom:8px">💳 待结算余额</div>
                <div style="display:flex;justify-content:space-between;align-items:center">
                  <div>
                    <span style="font-size:18px;font-weight:800;color:var(--yellow)" id="bill-due">$286.40</span>
                    <span style="font-size:11px;color:var(--muted);margin-left:8px">含本月分成</span>
                  </div>
                  <div style="display:flex;gap:8px">
                    <button class="btn btn-primary" style="font-size:12px;padding:6px 14px">💳 充值结清</button>
                    <button class="btn btn-outline" style="font-size:12px;padding:6px 14px">📄 导出对账单</button>
                  </div>
                </div>
                <div style="margin-top:10px;font-size:11px;color:var(--muted);background:rgba(59,130,246,.08);border-radius:8px;padding:10px">
                  📌 分成费用将优先抵扣订阅月租，剩余部分可通过前台充值余额结算
                </div>
              </div>
            </div>
            </div>
            
            <div id="acc-tab-wallet" style="display:none">"""

if OLD_WALLET_START in t:
    t = t.replace(OLD_WALLET_START, TAB_PLAN_CONTENT)
    print("Account plan/billing tabs inserted")
else:
    print("WARN: Wallet tab start not found")

# ==============================================================
# 7. Update CS KB pricing
# ==============================================================
OLD_CS_PRICING = """  upgrade: `💳 **升级套餐**\n\n进入【我的账户】→【当前方案】，点击目标套餐即可升级：\n• Basic $29/月 — 行情+AI问答+2个策略\n• Pro $79/月 — 无限策略+AI自动交易+高级回测\n• Elite $199/月 — 自动建仓+复制交易无限跟单+VIP客服\n\n有疑问请告诉我 😊`,"""

NEW_CS_PRICING = """  upgrade: `💳 **升级套餐**\n\n进入【我的账户】→【方案】，点击目标套餐即可升级：\n• 🥉 基础 $29/月 — 行情+AI问答\n• 🥈 专业 $99/月 — 无限策略+AI自动交易\n• 👑 旗舰 $149/月 — 全节点+深度策略+复制跟单+VIP\n\n有疑问请告诉我 😊`,"""

if OLD_CS_PRICING in t:
    t = t.replace(OLD_CS_PRICING, NEW_CS_PRICING)
    print("CS KB pricing updated")
else:
    print("WARN: CS pricing not found")

# Also update the pricing entry
OLD_CS_PRICING2 = """  pricing: `💰 **订阅套餐**\n\n| 套餐 | 价格 | 特点 |\n|------|------|------|\n| Basic | $29/月 | 行情+AI+2策略 |\n| Pro | $79/月 | 无限策略+AI自动交易 |\n| Elite | $199/月 | 自动建仓+复制交易+VIP |\n\n进入【我的账户】→【当前方案】升级。`,"""

NEW_CS_PRICING2 = """  pricing: `💰 **订阅套餐**\n\n| 套餐 | 价格 | 特点 |\n|------|------|------|\n| 免费 | $0/14天 | 全功能限时体验 |\n| 基础 | $29/月 | 行情+AI问答 |\n| 专业 | $99/月 | 无限策略+AI自动交易+2节点 |\n| 旗舰 | $149/月 | 全4节点+复制跟单+VIP |\n\n进入【我的账户】→【方案】升级。`,"""

if OLD_CS_PRICING2 in t:
    t = t.replace(OLD_CS_PRICING2, NEW_CS_PRICING2)
    print("CS pricing KB entry updated")
else:
    print("WARN: CS pricing2 not found")

# ==============================================================
# 8. Add JS for plan/billing tab content + switchAccountTab
# ==============================================================
# Find switchAccountTab function
if 'function switchAccountTab' in t:
    print("switchAccountTab found")
else:
    print("WARN: switchAccountTab not found - need to create it")

# ==============================================================
# Write output
# ==============================================================
ww(PATH, t)
print(f"\nDone! File size: {len(t.encode('utf-8'))} bytes")
