# -*- coding: utf-8 -*-
"""
Phase 1: index.html modifications
- Wallet tab in account page
- QuantTalk channel system
- TradingView + YouTube widgets
- Wallet JS functions
"""
filepath = 'index.html'
with open(filepath, 'rb') as f:
    raw = f.read()
t = raw.decode('utf-8', errors='replace')

# ============================================================
# 1. WALLET TAB BUTTON
# ============================================================
ex_tab = "switchAccountTab('exchanges', this)\">\U0001f3e6 交易所</button>"
wallet_btn = "\n            <button class=\"acc-tab\" onclick=\"switchAccountTab('wallet', this)\">\U0001f4b3 钱包</button>"
new_ex_tab = ex_tab + wallet_btn
t = t.replace(ex_tab, new_ex_tab)
t = t.replace(
    "const tabIds = ['positions', 'trades', 'signals', 'manual', 'market', 'strategies', 'exchanges'];",
    "const tabIds = ['positions', 'trades', 'signals', 'manual', 'market', 'strategies', 'exchanges', 'wallet'];"
)

# ============================================================
# 2. WALLET TAB CONTENT
# ============================================================
wallet_html = """
            <div id="acc-tab-wallet" style="display:none">
            <div class="card" style="padding:16px">
              <div style="font-size:14px;font-weight:600;margin-bottom:12px">\U0001f4b3 \u7ed1\u5b9a\u52a0\u5bc6\u8d27\u5e01\u94b1\u5305</div>
              <div style="font-size:12px;color:var(--muted);margin-bottom:16px">\u7ed1\u5b9a\u94b1\u5305\u7528\u4e8e\u8d2d\u4e70\u5957\u9910\u3001\u7b56\u7565\u7b49</div>
              <div style="margin-bottom:16px">
                <div style="font-size:12px;color:var(--muted);margin-bottom:8px">\u9009\u62e9\u94b1\u5305</div>
                <select id="wallet-select" style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--input-bg);color:var(--text);font-size:14px">
                  <option value="">-- \u8bf7\u9009\u62e9\u94b1\u5305 --</option>
                  <option value="metamask">\U0001f98a MetaMask</option>
                  <option value="walletconnect">\U0001f517 WalletConnect</option>
                  <option value="trustwallet">\U0001f6e1\ufe0f Trust Wallet</option>
                  <option value="okx">\U0001f536 OKX Wallet</option>
                  <option value="exchange">\U0001f3db\ufe0f \u4ea4\u6613\u6240\u94b1\u5305</option>
                  <option value="cold">\u2744\ufe0f \u51b7\u94b1\u5305</option>
                </select>
              </div>
              <div id="wallet-connect-area">
                <button id="wallet-connect-btn" onclick="connectWallet()" style="width:100%;padding:12px;border:none;border-radius:8px;background:var(--accent);color:#fff;font-size:14px;font-weight:600;cursor:pointer">\U0001f517 \u8fde\u63a5\u94b1\u5305</button>
              </div>
              <div id="wallet-connected-area" style="display:none;margin-top:12px;background:rgba(0,200,150,.1);border:1px solid rgba(0,200,150,.3);border-radius:8px;padding:12px">
                <div style="font-size:12px;color:var(--muted);margin-bottom:6px">\u2705 \u5df2\u8fde\u63a5\u5730\u5740</div>
                <div id="wallet-display-address" style="font-size:13px;font-weight:600;color:var(--green);word-break:break-all;font-family:monospace"></div>
                <div style="margin-top:8px;display:flex;gap:8px">
                  <span style="font-size:12px;padding:4px 8px;background:rgba(0,200,150,.2);border-radius:4px;color:var(--green)" id="wallet-type-badge">MetaMask</span>
                </div>
                <button onclick="disconnectWallet()" style="margin-top:10px;padding:8px 16px;border:1px solid #ff4b6e;border-radius:6px;background:transparent;color:#ff4b6e;font-size:12px;cursor:pointer">\u65ad\u5f00\u8fde\u63a5</button>
              </div>
              <div id="wallet-manual-area" style="display:none;margin-top:12px">
                <div style="font-size:12px;color:var(--muted);margin-bottom:6px">\u8f93\u5165\u94b1\u5305\u5730\u5740</div>
                <input id="wallet-manual-address" type="text" placeholder="0x... \u6216 bc1..." style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--input-bg);color:var(--text);font-size:13px">
                <button onclick="saveManualWallet()" style="margin-top:8px;width:100%;padding:10px;border:none;border-radius:8px;background:var(--accent);color:#fff;font-size:14px;font-weight:600;cursor:pointer">\U0001f4be \u4fdd\u5b58\u5730\u5740</button>
              </div>
              <div id="wallet-history" style="margin-top:16px;display:none">
                <div style="font-size:13px;font-weight:600;margin-bottom:8px;color:var(--muted)">\U0001f4cb \u7ed1\u5b9a\u5386\u53f2</div>
                <div id="wallet-history-list"></div>
              </div>
            </div>
            </div>
            
            <div id="acc-tab-exchanges" """

t = t.replace('<div id="acc-tab-exchanges" ', wallet_html, 1)

# ============================================================
# 3. QUANTTALK HTML REPLACEMENT
# ============================================================
# Find QuantTalk page HTML bounds
sq_html_start = t.find('<!-- ===== QuantTalk ===== -->')
sq_id_start = t.find('<div class="page" id="page-square"', sq_html_start)
sq_html_end = t.find('<!-- ===== \u7b56\u7565\u5e02\u573a ===== -->', sq_html_start)
print(f'QuantTalk HTML: {sq_id_start} -> {sq_html_end} ({sq_html_end - sq_id_start} bytes)')

new_sq_html = '''<!-- ===== QuantTalk ===== -->
      <div class="page" id="page-square" style="display:flex;gap:0;height:calc(100vh - 140px);overflow:hidden">
        <!-- Left: Channel List -->
        <div style="width:200px;min-width:200px;background:var(--card);border:1px solid var(--border);border-radius:12px;display:flex;flex-direction:column;overflow:hidden">
          <div style="padding:12px 14px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between">
            <span style="font-weight:700;font-size:14px">\U0001f4ac \u9891\u9053</span>
            <button onclick="createChannel()" style="width:28px;height:28px;border:none;border-radius:6px;background:var(--accent);color:#fff;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center">+</button>
          </div>
          <div id="channel-list" style="flex:1;overflow-y:auto;padding:6px"></div>
        </div>
        <!-- Middle: Chat Area -->
        <div style="flex:1;display:flex;flex-direction:column;margin:0 12px">
          <div id="channel-header" style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:10px 14px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between">
            <div><span id="channel-name-display" style="font-weight:700;font-size:15px"># \u5168\u5c40</span><span id="channel-desc-display" style="font-size:11px;color:var(--muted);margin-left:8px">\u95f2\u804a</span></div>
            <div style="display:flex;gap:6px">
              <button onclick="toggleWidget('tv')" id="tv-widget-btn" style="padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer">\U0001f4c8 \u56fe\u8868</button>
              <button onclick="toggleWidget('yt')" id="yt-widget-btn" style="padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer">\U0001f3a5 \u76f4\u64ad</button>
            </div>
          </div>
          <div id="widget-tv" style="display:none;margin-bottom:8px;border-radius:12px;overflow:hidden;border:1px solid var(--border);height:380px"></div>
          <div id="widget-yt" style="display:none;margin-bottom:8px;border-radius:12px;overflow:hidden;border:1px solid var(--border);height:380px"><div id="yt-player" style="width:100%;height:100%"></div></div>
          <div id="sq-msgs" style="flex:1;overflow-y:auto;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:12px;margin-bottom:8px"></div>
          <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:10px 14px">
            <div style="display:flex;gap:8px">
              <div style="flex:1;display:flex;gap:6px">
                <input id="sq-input" type="text" placeholder="\u8f93\u5165\u6d88\u606f..." style="flex:1;padding:10px 14px;border:1px solid var(--border);border-radius:8px;background:var(--input-bg);color:var(--text);font-size:13px" onkeydown="if(event.key==='Enter') sendMsg()">
                <button onclick="shareChart()" style="padding:8px 12px;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--muted);font-size:13px;cursor:pointer" title="\u5206\u4eab\u56fe\u8868">\U0001f4f7</button>
              </div>
              <button onclick="sendMsg()" style="padding:10px 20px;border:none;border-radius:8px;background:var(--accent);color:#fff;font-size:13px;font-weight:600;cursor:pointer">\u53d1\u9001</button>
            </div>
          </div>
        </div>
        <!-- Right: Post Feed -->
        <div style="width:280px;min-width:280px;background:var(--card);border:1px solid var(--border);border-radius:12px;display:flex;flex-direction:column;overflow:hidden">
          <div style="padding:10px 14px;border-bottom:1px solid var(--border);font-weight:600;font-size:13px">\u89c2\u70b9\u5e7f\u573a</div>
          <div id="sq-posts" style="flex:1;overflow-y:auto;padding:8px"></div>
        </div>
      </div>'''

t = t[:sq_id_start] + new_sq_html + t[sq_html_end:]

# ============================================================
# 4. REPLACE QUANTTALK JS
# ============================================================
qt_js_start = t.rfind('// ===== QuantTalk =====', 600000)
qt_js_end = t.find('// ===== \u7b56\u7565\u5e02\u573a =====', qt_js_start)
print(f'QuantTalk JS: {qt_js_start} -> {qt_js_end} ({qt_js_end - qt_js_start} bytes)')

new_qt_js = open('_qt_functions.js', 'r', encoding='utf-8').read()
t = t[:qt_js_start] + new_qt_js + t[qt_js_end:]

# ============================================================
# 5. CSS ADDITIONS
# ============================================================
# Add CSS before @media section
media_idx = t.rfind('@media')
if media_idx > 0:
    sq_css = '''
/* QuantTalk Widgets */
.ch-item { padding:8px 10px; border-radius:8px; cursor:pointer; margin-bottom:2px; font-size:13px; display:flex; align-items:center; gap:6px; }
.ch-item:hover { background:rgba(255,255,255,.08); }
.ch-item.active { background:rgba(0,200,150,.15); color:var(--green); }
#channel-list::-webkit-scrollbar { width:4px; }
#channel-list::-webkit-scrollbar-thumb { background:var(--border); border-radius:4px; }
#sq-msgs::-webkit-scrollbar { width:4px; }
#sq-msgs::-webkit-scrollbar-thumb { background:var(--border); border-radius:4px; }
.sq-post { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:10px; }
'''
    t = t[:media_idx] + sq_css + '\n' + t[media_idx:]

# ============================================================
# 6. INIT QUANTTALK ON SQUARE PAGE SHOW
# ============================================================
init_sq = t.find("if(name==='square')")
if init_sq > 0:
    old_init = t[init_sq:init_sq+60]
    new_init = "if(name==='square'){ initQuantTalk(); renderSquare('all'); }"
    t = t.replace(old_init, new_init)
    print(f'Init replaced at {init_sq}')

# ============================================================
# SAVE
# ============================================================
with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8', errors='replace'))
print(f'Saved! Size: {len(t.encode("utf-8"))} bytes')
