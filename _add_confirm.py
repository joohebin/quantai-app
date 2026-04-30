#!/usr/bin/env python3
PATH = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
f = open(PATH, 'rb')
c = f.read()
f.close()
t = c.decode('utf-8')

# 1. Add confirmation overlay HTML before </body>
confirm_html = """
<div id="trade-confirm-overlay" style="display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.7);z-index:10000;align-items:center;justify-content:center">
  <div style="background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px;max-width:420px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,.5)">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px">
      <span style="font-size:24px">\u26a0\ufe0f</span>
      <span style="font-size:16px;font-weight:700">\u786e\u8ba4\u6267\u884c</span>
    </div>
    <div id="trade-confirm-body" style="font-size:13px;color:var(--text);line-height:1.6;margin-bottom:20px;background:rgba(255,75,110,.1);padding:12px;border-radius:8px;border:1px solid rgba(255,75,110,.2)"></div>
    <div style="display:flex;gap:10px;justify-content:flex-end">
      <button onclick="document.getElementById('trade-confirm-overlay').style.display='none';window._pendingAction=null" style="padding:8px 20px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--muted);cursor:pointer;font-size:13px">\u53d6\u6d88</button>
      <button onclick="var f=window._pendingAction;document.getElementById('trade-confirm-overlay').style.display='none';window._pendingAction=null;if(f)f()" style="padding:8px 20px;border-radius:8px;border:none;background:var(--green);color:var(--dark);cursor:pointer;font-weight:600;font-size:13px">\u786e\u8ba4</button>
    </div>
  </div>
</div>
"""
body_end = t.find('</body>')
t = t[:body_end] + confirm_html + t[body_end:]
print('OK 1 confirm HTML')

# 2. Add confirm engine JS at end of last script
confirm_js = """
// ===== Confirm Engine =====
window._pendingAction=null;
window.showTradeConfirm=function(t,d,f){
  var b=document.getElementById('trade-confirm-body');if(!b)return;
  var h='<div style="font-weight:600;margin-bottom:8px">'+t+'</div><div style="font-size:12px;color:var(--muted)">';
  if(typeof d==='string')h+=d.replace(/\\n/g,'<br>');
  else if(Array.isArray(d))d.forEach(function(x){h+='\u2022 '+x+'<br>';});
  else h+=String(d);
  h+='</div>';b.innerHTML=h;
  document.getElementById('trade-confirm-overlay').style.display='flex';
  window._pendingAction=f;
};
console.log('[CE] OK');
"""
last_se = t.rfind('</script>', 0, t.rfind('</body>'))
t = t[:last_se] + confirm_js + t[last_se:]
print('OK 2 confirm JS')

# 3. Onboarding overlay before </body>
onboard_html = """
<div id="onboard-overlay" style="display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.7);z-index:9999;align-items:center;justify-content:center">
  <div style="background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px;max-width:500px;width:92%;max-height:80vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.5)">
    <div id="onboard-step-container"></div>
  </div>
</div>
"""
body_end = t.find('</body>')
t = t[:body_end] + onboard_html + t[body_end:]
print('OK 3 onboard HTML')

# 4. Sidebar "New here?" button
sidebar_bottom = t.find('sidebar-bottom')
if sidebar_bottom >= 0:
    t = t[:sidebar_bottom+15] + """
          <div onclick="window.startOnboarding()" style="display:flex;align-items:center;gap:8px;padding:8px 10px;margin-top:4px;margin-bottom:4px;border-radius:8px;cursor:pointer;font-size:12px;background:rgba(0,200,150,.1);border:1px solid rgba(0,200,150,.2);color:var(--green)" onmouseover="this.style.background='rgba(0,200,150,.2)'" onmouseout="this.style.background='rgba(0,200,150,.1)'">
            <span>\U0001f393</span>
            <span>\u65b0\u624b\u5165\u95e8</span>
          </div>
""" + t[sidebar_bottom+15:]
    print('OK 4 sidebar btn')
else:
    print('WARN: sidebar')

# 5. Onboard + quota JS (simplified - just core exchange list + start)
onboard_js = """
// ===== Onboard =====
window.EXCHANGE_LIST=[
{id:'binance',name:'Binance',link:'https://www.binance.com/register?ref=QUANTAI',desc:'\u5168\u7403\u6700\u5927\u52a0\u5bc6\u8d27\u5e01\u4ea4\u6613\u6240'},
{id:'okx',name:'OKX',link:'https://www.okx.com/join/QUANTAI',desc:'\u5168\u7403\u7b2c\u4e8c\u5927\u4ea4\u6613\u6240'},
{id:'bybit',name:'Bybit',link:'https://www.bybit.com/invite?ref=QUANTAI',desc:'\u884d\u751f\u54c1\u4ea4\u6613\u9996\u9009'},
{id:'bitget',name:'Bitget',link:'https://www.bitget.com/register/QUANTAI',desc:'\u5408\u7ea6\u8ddf\u5355\u5e73\u53f0'},
{id:'htx',name:'HTX',link:'https://www.htx.com/invite/QUANTAI',desc:'\u4e2d\u6587\u652f\u6301\u597d'},
{id:'gate',name:'Gate.io',link:'https://www.gate.io/signup/QUANTAI',desc:'Coin\u6700\u5168'}
];
window.BROKER_LIST=[
{id:'ibkr',name:'Interactive Brokers',desc:'\u5168\u7403\u80a1\u7968/\u671f\u8d27/\u5916\u6c47'},
{id:'tradestation',name:'TradeStation',desc:'\u7f8e\u56fd\u80a1\u7968\u4ea4\u6613'},
{id:'futu',name:'\u5bcc\u9014\u725b\u725b',desc:'\u6e2f\u80a1/\u7f8e\u80a1'}
];
window.COUNTRY_LIST=[
{code:'CN',name:'\u4e2d\u56fd',brokers:['futu','ibkr'],exchanges:['binance','okx','htx']},
{code:'US',name:'\u7f8e\u56fd',brokers:['tradestation','ibkr'],exchanges:['binance','okx','bybit']},
{code:'JP',name:'\u65e5\u672c',brokers:['ibkr'],exchanges:['binance','okx','gate']},
{code:'SG',name:'\u65b0\u52a0\u5761',brokers:['ibkr','futu'],exchanges:['binance','okx','bybit']},
{code:'HK',name:'\u9999\u6e2f',brokers:['futu','ibkr'],exchanges:['binance','okx','htx']},
{code:'UK',name:'\u82f1\u56fd',brokers:['ibkr'],exchanges:['binance','okx','gate']},
{code:'OTHER',name:'\u5176\u4ed6',brokers:['ibkr'],exchanges:['binance','okx','gate']}
];

window.startOnboarding=function(){
  var o=document.getElementById('onboard-overlay');if(o)o.style.display='flex';
  window._onb={step:1};window.renderOnboardStep(1);
};

window.renderOnboardStep=function(s){
  var c=document.getElementById('onboard-step-container');if(!c)return;
  var h='';
  if(s===1){
    h='<div style="text-align:center;margin-bottom:16px"><span style="font-size:36px">\U0001f44b</span></div>';
    h+='<div style="font-size:16px;font-weight:700;margin-bottom:12px;text-align:center">\u6b22\u8fce  QuantAI</div>';
    h+='<div style="font-size:12px;color:var(--muted);margin-bottom:16px">\u544a\u8bc9\u6211\u4f60\u7684\u60c5\u51b5\uff0c\u6211\u5e2e\u4f60\u5b89\u6392\uff1a</div>';
    h+='<div style="margin-bottom:10px"><label style="font-size:12px;color:var(--muted)">\u60f3\u4ea4\u6613\u4ec0\u4e48\uff1f</label><select id="ob-type" style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--card);color:var(--text);font-size:13px">';
    h+='<option value="crypto">\u52a0\u5bc6\u8d27\u5e01</option><option value="stock">\u80a1\u7968/\u6307\u6570</option><option value="both">\u90fd\u60f3</option></select></div>';
    h+='<div style="margin-bottom:14px"><label style="font-size:12px;color:var(--muted)">\u4f60\u5728\u54ea\u4e2a\u56fd\u5bb6\uff1f</label><select id="ob-country" style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--card);color:var(--text);font-size:13px">';
    for(var i=0;i<window.COUNTRY_LIST.length;i++)h+='<option value="'+window.COUNTRY_LIST[i].code+'">'+window.COUNTRY_LIST[i].name+'</option>';
    h+='</select></div>';
    h+='<button onclick="window.goOnboardStep(2)" style="width:100%;padding:12px;border-radius:10px;border:none;background:var(--green);color:var(--dark);font-weight:600;cursor:pointer;font-size:14px">\u4e0b\u4e00\u6b65 \u2192</button>';
  }else if(s===2){
    var cc=document.getElementById('ob-country')?.value||'OTHER';
    var tt=document.getElementById('ob-type')?.value||'crypto';
    var co=window.COUNTRY_LIST.find(function(x){return x.code===cc;})||window.COUNTRY_LIST[window.COUNTRY_LIST.length-1];
    window._onb.country=co;
    h='<div style="text-align:center;margin-bottom:12px"><span style="font-size:32px">\U0001f4cc</span></div>';
    h+='<div style="font-size:14px;font-weight:700;margin-bottom:12px">\u63a8\u8350\u4ea4\u6613\u5e73\u53f0</div>';
    if(tt!=='stock'){h+='<div style="font-size:12px;color:var(--yellow);font-weight:600;margin-bottom:6px">\U0001f4b0 \u52a0\u5bc6\u8d27\u5e01</div>';
      for(var i=0;i<co.exchanges.length;i++){
        var ex=window.EXCHANGE_LIST.find(function(x){return x.id===co.exchanges[i];});
        if(!ex)continue;
        h+='<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 10px;background:rgba(255,255,255,.04);border-radius:8px;margin-bottom:4px">';
        h+='<div><div style="font-weight:600;font-size:12px">'+ex.name+'</div><div style="font-size:10px;color:var(--muted)">'+ex.desc+'</div></div>';
        h+='<button onclick="window.selectOnboardEx(\\''+ex.id+'\\')" style="padding:5px 12px;border-radius:6px;border:1px solid var(--green);background:transparent;color:var(--green);cursor:pointer;font-size:11px">\u9009\u62e9\u6ce8\u518c</button></div>';
      }
    }
    if(tt!=='crypto'){h+='<div style="font-size:12px;color:var(--blue);font-weight:600;margin:10px 0 6px">\U0001f3e6 \u80a1\u7968\u5238\u5546</div>';
      for(var i=0;i<co.brokers.length;i++){
        var bk=window.BROKER_LIST.find(function(x){return x.id===co.brokers[i];});
        if(!bk)continue;
        h+='<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 10px;background:rgba(255,255,255,.04);border-radius:8px;margin-bottom:4px">';
        h+='<div><div style="font-weight:600;font-size:12px">'+bk.name+'</div><div style="font-size:10px;color:var(--muted)">'+bk.desc+'</div></div>';
        h+='<button onclick="window.selectOnboardBroker(\\''+bk.id+'\\')" style="padding:5px 12px;border-radius:6px;border:1px solid var(--blue);background:transparent;color:var(--blue);cursor:pointer;font-size:11px">\u9009\u62e9</button></div>';
      }
    }
    h+='<div style="margin-top:12px;display:flex;gap:8px">';
    h+='<button onclick="window.goOnboardStep(1)" style="flex:1;padding:8px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--muted);cursor:pointer;font-size:12px">\u2190 \u4e0a\u4e00\u6b65</button>';
    h+='<button onclick="window.goOnboardStep(3)" style="flex:1;padding:8px;border-radius:8px;border:none;background:var(--green);color:var(--dark);font-weight:600;cursor:pointer;font-size:12px">\u6211\u5df2\u9009\u597d \u2192</button></div>';
  }else if(s===3){
    h='<div style="text-align:center;margin-bottom:16px"><span style="font-size:36px">\U0001f511</span></div>';
    h+='<div style="font-size:14px;font-weight:700;margin-bottom:12px;text-align:center">\u5bf9\u63a5 API Key</div>';
    h+='<div style="font-size:12px;color:var(--muted);line-height:1.6;margin-bottom:14px">';
    h+='1. \u767b\u5f55\u4f60\u7684\u4ea4\u6613\u6240\u8d26\u6237<br>2. \u521b\u5efa API Key\uff08\u52fe\u9009\u5141\u8bb8\u4ea4\u6613\uff09<br>3. \u590d\u5236\u4ee5\u4e0b\u4fe1\u606f\uff1a</div>';
    h+='<div style="margin-bottom:10px"><label style="font-size:12px;color:var(--muted);display:block;margin-bottom:4px">API Key</label>';
    h+='<input id="ob-apikey" placeholder="\u8f93\u5165 API Key" style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--card);color:var(--text);font-size:13px"></div>';
    h+='<div style="margin-bottom:16px"><label style="font-size:12px;color:var(--muted);display:block;margin-bottom:4px">Secret Key</label>';
    h+='<input id="ob-secret" type="password" placeholder="\u8f93\u5165 Secret Key" style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--card);color:var(--text);font-size:13px"></div>';
    h+='<div style="display:flex;gap:10px">';
    h+='<button onclick="window.goOnboardStep(2)" style="flex:1;padding:10px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--muted);cursor:pointer;font-size:12px">\u2190 \u4e0a\u4e00\u6b65</button>';
    h+='<button onclick="window.goOnboardStep(4)" style="flex:1;padding:10px;border-radius:8px;border:none;background:var(--green);color:var(--dark);font-weight:600;cursor:pointer;font-size:12px">\u5b8c\u6210 \u2192</button></div>';
  }else if(s===4){
    h='<div style="text-align:center;margin-bottom:20px"><span style="font-size:48px">\u2705</span></div>';
    h+='<div style="font-size:16px;font-weight:700;margin-bottom:12px;text-align:center">\u5f00\u59cb\u4ea4\u6613\u5427\uff01</div>';
    h+='<div style="font-size:13px;color:var(--muted);line-height:1.6;text-align:center">\U0001f4ca \u67e5\u770b\u884c\u60c5 / \U0001f9e0 AI\u5206\u6790 / \u2699\ufe0f \u81ea\u52a8\u7b56\u7565 / \U0001f4f1 \u8bed\u97f3\u4e0b\u5355<br><br>\u4e0d\u61c2\u7684\u968f\u65f6\u95ee\u6211\uff01</div>';
    h+='<button onclick="window.closeOnboard()" style="width:100%;padding:12px;border-radius:10px;border:none;background:var(--green);color:var(--dark);font-weight:600;cursor:pointer;font-size:14px;margin-top:16px">\u5f00\u59cb \U0001f680</button>';
  }
  c.innerHTML=h;
};
window.goOnboardStep=function(s){window.renderOnboardStep(s);};
window.selectOnboardEx=function(id){
  var ex=window.EXCHANGE_LIST.find(function(x){return x.id===id;});
  if(ex&&ex.link)window.open(ex.link,'_blank');
  window._onb.exchange=id;
  document.getElementById('onboard-overlay').style.display='none';
  window.showTradeConfirm('\u6ce8\u518c '+(ex?ex.name:''), '\u5df2\u6253\u5f00\u6ce8\u518c\u94fe\u63a5\u3002\u5b8c\u6210\u540e\u786e\u8ba4\u3002',function(){
    document.getElementById('onboard-overlay').style.display='flex';
    window.goOnboardStep(3);
  });
};
window.selectOnboardBroker=function(id){
  window._onb.broker=id;
  document.getElementById('onboard-overlay').style.display='none';
  window.showTradeConfirm('\u9009\u62e9\u5238\u5546', '\u7ee7\u7eed\u4e0b\u4e00\u6b65',function(){
    document.getElementById('onboard-overlay').style.display='flex';
    window.goOnboardStep(3);
  });
};
window.closeOnboard=function(){
  document.getElementById('onboard-overlay').style.display='none';
  localStorage.setItem('onboarded','1');
};
// Auto-show for new users
window.addEventListener('load',function(){
  if(!localStorage.getItem('onboarded'))setTimeout(window.startOnboarding,5000);
});

// ===== Quota =====
window.checkQuota=function(t){
  var p=window.getUserPlan(),i=window.getPlanInfo(p);
  if(!i||!i.features)return{allowed:true,used:0,max:-1};
  if(t==='strategy'){
    var m=i.features.strategies;
    if(m<0)return{allowed:true,used:0,max:-1};
    var c=parseInt(localStorage.getItem('q_strategy_count')||'0');
    return{allowed:c<m,used:c,max:m};
  }
  if(t==='ai_call'){
    var m=i.features.aiCalls;
    if(m<0)return{allowed:true,used:0,max:-1};
    var u=(window.getQuotaUsed?window.getQuotaUsed('ai_call'):0);
    return{allowed:u<m,used:u,max:m};
  }
  return{allowed:true,used:0,max:-1};
};
window.showQuotaWarn=function(t){
  var q=window.checkQuota(t);
  window.showTradeConfirm('\u5957\u9910\u9650\u5236', '\u5f53\u524d'+t+'\u9650\u989d\u5df2\u6ee1 ('+q.used+'/'+q.max+')\n\u5347\u7ea7\u5957\u9910\u89e3\u9501\u66f4\u591a\u3002',function(){
    window.showPlanUpgradeModal?window.showPlanUpgradeModal():window.showPage('account');
  });
};
console.log('[OB+Q] OK');
"""

t = t.replace("console.log('[CE] OK');", "console.log('[CE] OK');" + onboard_js)
print('OK 5 onboard+quota JS')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(t)
print('SAVED')
