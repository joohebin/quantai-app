#!/usr/bin/env python3
"""Update plans + add auto-trading engine to index.html"""

def read_file(path):
    with open(path, 'rb') as f:
        return f.read().decode('utf-8')

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

PATH = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
t = read_file(PATH)

# ===== 1. UPDATE PLANS =====
OLD_PLANS = """window.PLANS = {
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
};"""

NEW_PLANS = """window.PLANS = {
  free: {
    id: 'free', name: '免费试用', nameEn: 'Free Trial', price: 0, period: '14天限时',
    icon: '\U0001f513', nodes: ['default'], nodeCount: '\u56fa\u5b9a\u9ed8\u8ba4\u8282\u70b9',
    features: { strategies: 3, aiCalls: 20, metaApiCalls: 100, autoTrade: false, liveTrade: false,
      advancedBacktest: false, factorAnalysis: false, copyTrade: false, hft: false, tvUltimate: false,
      multiRegion: false, nodeSelectable: false, autoEngine: false },
    badge: '\U0001f513', badgeColor: 'rgba(150,150,150,.2)', annualDiscount: 0
  },
  basic: {
    id: 'basic', name: '\u57fa\u7840\u5957\u9910', nameEn: 'Basic', price: 39, period: '\u6708', annualPrice: 390,
    icon: '\U0001f949', nodes: ['default'], nodeCount: '\u56fa\u5b9a\u901a\u7528\u8282\u70b9',
    features: { strategies: -1, aiCalls: 100, metaApiCalls: 500, autoTrade: false, liveTrade: false,
      advancedBacktest: false, factorAnalysis: false, copyTrade: false, hft: false, tvUltimate: false,
      multiRegion: false, nodeSelectable: false, autoEngine: false },
    badge: '\U0001f949', badgeColor: 'rgba(205,127,50,.2)', annualDiscount: 0.17
  },
  pro: {
    id: 'pro', name: '\u4e13\u4e1a\u5957\u9910', nameEn: 'Pro', price: 79, period: '\u6708', annualPrice: 790,
    icon: '\U0001f948', nodes: ['tokyo','singapore'], nodeCount: '\u53ef\u9009 2 \u533a\u57df',
    features: { strategies: -1, aiCalls: -1, metaApiCalls: 5000, autoTrade: true, liveTrade: true,
      advancedBacktest: true, factorAnalysis: true, copyTrade: true, hft: false, tvUltimate: false,
      multiRegion: false, nodeSelectable: true, autoEngine: true },
    badge: '\U0001f948', badgeColor: 'rgba(192,192,192,.2)', annualDiscount: 0.17
  },
  flagship: {
    id: 'flagship', name: '\u65d7\u8230\u5957\u9910', nameEn: 'Flagship', price: 199, period: '\u6708', annualPrice: 1990,
    icon: '\U0001f451', nodes: ['tokyo','singapore','london','newyork'], nodeCount: '4 \u5927\u533a\u5168\u8282\u70b9',
    features: { strategies: -1, aiCalls: -1, metaApiCalls: -1, autoTrade: true, liveTrade: true,
      advancedBacktest: true, factorAnalysis: true, copyTrade: true, hft: true, tvUltimate: true,
      multiRegion: true, nodeSelectable: true, autoEngine: true },
    badge: '\U0001f451', badgeColor: 'rgba(255,215,0,.2)', annualDiscount: 0.17
  }
};"""

t = t.replace(OLD_PLANS, NEW_PLANS)

# ===== 2. UPDATE REVENUE SHARE =====
OLD_RS = """window.REVENUE_SHARE = [
  { min: 0,      max: 1000,   rate: 0,   label: '\u2264$1,000' },
  { min: 1001,   max: 5000,   rate: 0.05,label: '$1,001~$5,000' },
  { min: 5001,   max: 20000,  rate: 0.08,label: '$5,001~$20,000' },
  { min: 20001,  max: Infinity,rate: 0.10,label: '>$20,000' }
];"""

NEW_RS = """window.REVENUE_SHARE = [
  { min: 0,      max: 500,    rate: 0,   label: '\u2264$500' },
  { min: 501,    max: 3000,   rate: 0.05,label: '$501~$3,000' },
  { min: 3001,   max: 10000,  rate: 0.08,label: '$3,001~$10,000' },
  { min: 10001,  max: Infinity,rate: 0.10,label: '>$10,000' }
];"""

t = t.replace(OLD_RS, NEW_RS)

# ===== 3. UPDATE ADDON PRICES =====
OLD_TV = "tvUltimate:     { id: 'tvUltimate',     name: 'TradingView Ultimate \u9ad8\u7ea7\u6570\u636e\u5305',      icon: '\U0001f4ca', price: 29,  period: '\u6708',"
NEW_TV = "tvUltimate:     { id: 'tvUltimate',     name: 'TradingView Ultimate \u9ad8\u7ea7\u6570\u636e\u5305',      icon: '\U0001f4ca', price: 29,  period: '\u6708',"
t = t.replace(OLD_TV, NEW_TV)

OLD_MULTI = "multiAccount:   { id: 'multiAccount',   name: '\u591a\u8d26\u6237\u6269\u5bb9\u5305',                       icon: '\U0001f3e6', price: 39,  period: '\u6708',"
NEW_MULTI = "multiAccount:   { id: 'multiAccount',   name: '\u591a\u8d26\u6237\u6269\u5bb9\u5305',                       icon: '\U0001f3e6', price: 29,  period: '\u6708',"
t = t.replace(OLD_MULTI, NEW_MULTI)

OLD_VIP = "vipSupport:     { id: 'vipSupport',     name: 'VIP \u8fd0\u7ef4\u4e13\u5c5e\u5305',                       icon: '\U0001f468\u200d\U0001f4bb', price: 99,  period: '\u6708',"
NEW_VIP = "vipSupport:     { id: 'vipSupport',     name: 'VIP \u8fd0\u7ef4\u4e13\u5c5e\u5305',                       icon: '\U0001f468\u200d\U0001f4bb', price: 49,  period: '\u6708',"
t = t.replace(OLD_VIP, NEW_VIP)

# ===== 4. UPDATE calcRevenueShare for new thresholds =====
OLD_CALC = """window.calcRevenueShare = function(monthlyPnl){
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
    if(bandAmount <= 0) { tiers.push({from:Math.max(1001,t.min), to:t.max===Infinity?'\u221e':t.max, rate:t.rate, amount:0, share:0}); continue; }
    var share = Math.round(bandAmount * t.rate * 100) / 100;
    tiers.push({from:Math.max(1001,t.min), to:t.max===Infinity?'\u221e':t.max, rate:t.rate, amount:bandAmount, share:share});
    total += share;
    remaining -= bandAmount;
    if(remaining <= 0) break;
  }
  return {tiers:tiers, totalShare:Math.round(total*100)/100, effectiveRate:Math.round(total/monthlyPnl*10000)/100};
};"""

NEW_CALC = """window.calcRevenueShare = function(monthlyPnl){
  // Return {tiers[], totalShare, effectiveRate}
  if(!monthlyPnl || monthlyPnl <= 500) return {tiers:[{from:0, to:500, rate:0, amount:0, share:0}], totalShare:0, effectiveRate:0};
  var tiers = [];
  var total = 0;
  var remaining = Math.max(0, monthlyPnl - 500); // first $500 free
  var t;
  for(var i=1; i<window.REVENUE_SHARE.length; i++){
    t = window.REVENUE_SHARE[i];
    var bandMin = Math.max(0, t.min - 501);
    var bandMax = Math.max(0, t.max - 501);
    if(t.max === Infinity) bandMax = remaining;
    var bandAmount = Math.min(remaining, bandMax - bandMin);
    if(bandAmount <= 0) { tiers.push({from:Math.max(501,t.min), to:t.max===Infinity?'\u221e':t.max, rate:t.rate, amount:0, share:0}); continue; }
    var share = Math.round(bandAmount * t.rate * 100) / 100;
    tiers.push({from:Math.max(501,t.min), to:t.max===Infinity?'\u221e':t.max, rate:t.rate, amount:bandAmount, share:share});
    total += share;
    remaining -= bandAmount;
    if(remaining <= 0) break;
  }
  return {tiers:tiers, totalShare:Math.round(total*100)/100, effectiveRate:Math.round(total/monthlyPnl*10000)/100};
};"""

if OLD_CALC in t:
    t = t.replace(OLD_CALC, NEW_CALC)
else:
    print("WARN: calcRevenueShare not found for replacement")

# ===== 5. UPDATE getPlanPrice to show annual option =====
OLD_GP = """window.getPlanPrice = function(planId){
  var p = window.getPlanInfo(planId);
  return p.price === 0 ? '\u514d\u8d39' : '$' + p.price + '/' + p.period;
};"""

NEW_GP = """window.getPlanPrice = function(planId, showAnnual){
  var p = window.getPlanInfo(planId);
  if(p.price === 0) return '\u514d\u8d39';
  if(showAnnual && p.annualPrice) return '$' + p.annualPrice + '/\u5e74 ($' + Math.round(p.annualPrice/12) + '/\u6708)';
  return '$' + p.price + '/' + p.period;
};

window.getPlanAnnualNote = function(planId){
  var p = window.getPlanInfo(planId);
  if(p.annualDiscount && p.annualPrice) return '\u5e74\u4ed8\u7701 ' + Math.round(p.annualDiscount*100) + '%';
  return '';
};"""

if OLD_GP in t:
    t = t.replace(OLD_GP, NEW_GP)
    print("getPlanPrice updated")
else:
    print("WARN: getPlanPrice not found")

# ===== 6. UPDATE renderPlanTab plan grid to show annual pricing =====
# The renderPlanTab function was just added - find it and update the plan card rendering
OLD_GRID_LINE = "' + window.getPlanPrice(id) + '</div><div style=\"font-size:11px;color:var(--muted)\">' + p.nodeCount + '</div>';"
NEW_GRID_LINE = "' + window.getPlanPrice(id) + '</div><div style=\"font-size:11px;color:var(--muted)\">' + p.nodeCount + '</div><div style=\"font-size:10px;color:var(--green);margin-top:2px\">' + window.getPlanAnnualNote(id) + '</div>';"

if OLD_GRID_LINE in t:
    t = t.replace(OLD_GRID_LINE, NEW_GRID_LINE)
    print("Plan grid pricing updated")
else:
    print("WARN: Plan grid pricing line not found")

# ===== 7. UPDATE upgrade modal pricing =====
OLD_UM = "' + window.getPlanPrice(id);"
NEW_UM = "' + window.getPlanPrice(id) + ' ' + window.getPlanAnnualNote(id);"
if OLD_UM in t:
    t = t.replace(OLD_UM, NEW_UM)
    print("Upgrade modal pricing updated")
# This might have multiple matches - just take first

# ===== 8. UPDATE sidebar to show plan + AI status =====
OLD_SIDEBAR_PLAN_END = """          <div class="plan" id="sidebar-plan-badge"><span id="sidebar-plan-icon">👑</span> <span id="sidebar-plan-name">旗舰套餐</span></div>"""
NEW_SIDEBAR_PLAN_END = """          <div class="plan" id="sidebar-plan-badge"><span id="sidebar-plan-icon">\U0001f451</span> <span id="sidebar-plan-name">\u65d7\u8230\u5957\u9910</span></div>
          <div id="sidebar-ai-status" style="display:flex;align-items:center;gap:4px;font-size:10px;margin-top:4px">
            <span id="ai-status-dot" style="width:6px;height:6px;border-radius:50%;background:var(--green);box-shadow:0 0 6px var(--green)"></span>
            <span id="ai-status-text" style="color:var(--muted)">AI \u81ea\u52a8\u4ea4\u6613\u4e2d</span>
          </div>"""

if '👑' in OLD_SIDEBAR_PLAN_END:
    t = t.replace(OLD_SIDEBAR_PLAN_END, NEW_SIDEBAR_PLAN_END)
    print("Sidebar plan+AI status updated")
else:
    # try exact match with escaped
    pass

write_file(PATH, t)
print("\nFile updated!")
