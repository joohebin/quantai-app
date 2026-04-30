f=open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','rb')
c=f.read()
f.close()
t=c.decode('utf-8')

# Find the full PLANS object and replace it entirely
i=t.find('window.PLANS = {')
j=t.find('};', i)
# Find 4th closing brace (free, basic, pro, flagship)
j2=t.find('};', j+2)
j3=t.find('};', j2+2)
j4=t.find('};', j3+2)  # flagship closing

# Actually just find the start of NODES
j5=t.find('window.NODES', i)

clean_plans = """window.PLANS = {
  free: {
    id: 'free', name: '\u514d\u8d39\u8bd5\u7528', nameEn: 'Free Trial', price: 0, period: '14\u5929\u9650\u65f6',
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

# Now replace from 'window.PLANS = {' to the start of NODES section
t = t[:i] + clean_plans + t[j5:]
print('PLANS block fully replaced')

# Fix calcRevenueShare - any remaining 1000/1001
old_calc = t.find('window.calcRevenueShare')
calc_end = t.find('};', old_calc) + 2
old_calc_block = t[old_calc:calc_end]
print('calc block:', repr(old_calc_block[:200]))

# Build clean calc function
clean_calc = """window.calcRevenueShare = function(monthlyPnl){
  if(!monthlyPnl || monthlyPnl <= 500) return {tiers:[{from:0, to:500, rate:0, amount:0, share:0}], totalShare:0, effectiveRate:0};
  var tiers = [];
  var total = 0;
  var remaining = Math.max(0, monthlyPnl - 500);
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

t = t[:old_calc] + clean_calc + t[calc_end:]
print('calcRevenueShare fully replaced')

# Fix ADDONS - multiAccount was supposed to be $29 not $39
if "price: 39,  period: '\u6708',\n                    desc: '\u63d0\u5347\u7ed1\u5b9a MetaAPI \u4ea4\u6613\u8d26\u6237\u6570\u91cf\u4e0a\u9650'" in t:
    t = t.replace("price: 39,  period: '\u6708',\n                    desc: '\u63d0\u5347\u7ed1\u5b9a MetaAPI \u4ea4\u6613\u8d26\u6237\u6570\u91cf\u4e0a\u9650'", "price: 29,  period: '\u6708',\n                    desc: '\u63d0\u5347\u7ed1\u5b9a MetaAPI \u4ea4\u6613\u8d26\u6237\u6570\u91cf\u4e0a\u9650'")
    print('MultiAccount price fixed to $29')

# Fix VIP price from 99 to 49
if "price: 99,  period: '\u6708',\n                    desc: '1v1 \u6280\u672f\u652f\u6301\u3001\u8282\u70b9\u6545\u969c\u4f18\u5148\u6392\u67e5'" in t:
    t = t.replace("price: 99,  period: '\u6708',\n                    desc: '1v1 \u6280\u672f\u652f\u6301\u3001\u8282\u70b9\u6545\u969c\u4f18\u5148\u6392\u67e5'", "price: 49,  period: '\u6708',\n                    desc: '1v1 \u6280\u672f\u652f\u6301\u3001\u8282\u70b9\u6545\u969c\u4f18\u5148\u6392\u67e5'")
    print('VIP price fixed to $49')

with open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','w',encoding='utf-8') as f:
    f.write(t)
print('Saved!')
