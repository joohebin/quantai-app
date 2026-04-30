#!/usr/bin/env python3
"""
Modify index.html with 4 changes:
1. Add Web3 Wallet Tab to Account Page
2. Replace QuantTalk HTML
3. Replace QuantTalk JS
4. Add CSS styles
"""

import re
import shutil

def main(target_file):
    with open(target_file, 'rb') as f:
        content = f.read()

    # ========================================================
    # CHANGE 1A: Add wallet tab button after exchanges tab button
    # ========================================================
    old_tab_buttons = b'''          <div class="acc-tab" onclick="switchAccountTab('exchanges',this)" style="flex:1;text-align:center;padding:12px;font-size:13px;font-weight:600;color:var(--muted);cursor:pointer" data-i18n="acc_tab_exchanges">\xf0\x9f\x8f\xa6 \xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80</div>
        </div>'''

    new_tab_buttons = b'''          <div class="acc-tab" onclick="switchAccountTab('exchanges',this)" style="flex:1;text-align:center;padding:12px;font-size:13px;font-weight:600;color:var(--muted);cursor:pointer" data-i18n="acc_tab_exchanges">\xf0\x9f\x8f\xa6 \xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80</div>
          <div class="acc-tab" onclick="switchAccountTab('wallet',this)" style="flex:1;text-align:center;padding:12px;font-size:13px;font-weight:600;color:var(--muted);cursor:pointer">\xf0\x9f\x92\xb3 \xe9\x92\xb1\xe5\x8c\x85</div>
        </div>'''

    if old_tab_buttons in content:
        content = content.replace(old_tab_buttons, new_tab_buttons, 1)
        print("CHANGE 1A: Wallet tab button added")
    else:
        print("CHANGE 1A FAILED: Old tab buttons not found!")
        return

    # ========================================================
    # CHANGE 1B: Add wallet tab content before exchanges tab div
    # ========================================================
    wallet_tab_html = b'''          <!-- \xe9\x92\xb1\xe5\x8c\x85\xe9\x85\x8d\xe7\xbd\xae\xe6\xa0\x87\xe7\xad\xbe\xe9\xa1\xb5\xe5\x86\x85\xe5\xae\xb9 -->
          <div id="acc-tab-wallet" style="display:none">
            <div class="card" style="padding:16px">
              <div style="font-size:14px;font-weight:600;margin-bottom:12px">\xf0\x9f\x92\xb3 \xe8\xbf\x9e\xe6\x8e\xa5\xe9\x92\xb1\xe5\x8c\x85</div>
              <div style="font-size:12px;color:var(--muted);margin-bottom:16px">\xe9\x80\x89\xe6\x8b\xa9\xe6\x82\xa8\xe7\x9a\x84\xe9\x92\xb1\xe5\x8c\x85\xe6\x88\x96\xe8\xbe\x93\xe5\x85\xa5\xe5\x9c\xb0\xe5\x9d\x80\xe8\xbf\x9b\xe8\xa1\x8c\xe8\xb7\x9f\xe8\xb8\xaa</div>

              <!-- \xe9\x80\x89\xe6\x8b\xa9\xe9\x92\xb1\xe5\x8c\x85 -->
              <div style="margin-bottom:16px">
                <div style="font-size:12px;color:var(--muted);margin-bottom:6px">\xe9\x92\xb1\xe5\x8c\x85\xe7\xb1\xbb\xe5\x9e\x8b</div>
                <select id="wallet-type-select" onchange="showManualInput()" style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-size:13px">
                  <option value="metamask">MetaMask</option>
                  <option value="walletconnect">WalletConnect</option>
                  <option value="trustwallet">Trust Wallet</option>
                  <option value="okxwallet">OKX Wallet</option>
                  <option value="exchange">\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe9\x92\xb1\xe5\x8c\x85</option>
                  <option value="coldwallet">\xe5\x86\xb7\xe9\x92\xb1\xe5\x8c\x85</option>
                </select>
              </div>

              <!-- \xe8\xbf\x9e\xe6\x8e\xa5\xe6\x8c\x89\xe9\x92\xae -->
              <button class="btn btn-primary" onclick="connectWallet()" style="width:100%;margin-bottom:12px">\xf0\x9f\x94\x97 \xe8\xbf\x9e\xe6\x8e\xa5\xe9\x92\xb1\xe5\x8c\x85</button>

              <!-- \xe5\xb7\xb2\xe8\xbf\x9e\xe6\x8e\xa5\xe9\x92\xb1\xe5\x8c\x85\xe4\xbf\xa1\xe6\x81\xaf -->
              <div id="wallet-connected-info" style="display:none;background:rgba(0,200,150,.1);border:1px solid rgba(0,200,150,.3);border-radius:10px;padding:14px;margin-bottom:12px">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
                  <div style="font-weight:600" id="wallet-display-name">MetaMask</div>
                  <span style="color:var(--green);font-size:12px">\xe2\x9c\x93 \xe5\xb7\xb2\xe8\xbf\x9e\xe6\x8e\xa5</span>
                </div>
                <div style="font-size:12px;color:var(--muted);word-break:break-all;background:var(--bg);padding:8px;border-radius:6px;font-family:monospace" id="wallet-display-address">0x0000...0000</div>
                <button class="btn btn-outline" onclick="disconnectWallet()" style="width:100%;margin-top:10px;font-size:12px">\xf0\x9f\x94\x93 \xe6\x96\xad\xe5\xbc\x80\xe8\xbf\x9e\xe6\x8e\xa5</button>
              </div>

              <!-- \xe6\x89\x8b\xe5\x8a\xa8\xe8\xbe\x93\xe5\x85\xa5\xe5\x9c\xb0\xe5\x9d\x80 -->
              <div id="wallet-manual-input" style="display:none;margin-bottom:12px">
                <div style="font-size:12px;color:var(--muted);margin-bottom:6px">\xe9\x92\xb1\xe5\x8c\x85\xe5\x9c\xb0\xe5\x9d\x80</div>
                <input type="text" id="wallet-address-input" placeholder="\xe8\xbe\x93\xe5\x85\xa5\xe9\x92\xb1\xe5\x8c\x85\xe5\x9c\xb0\xe5\x9d\x80..." style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-size:13px;margin-bottom:8px">
                <button class="btn btn-primary" onclick="saveManualWallet()" style="width:100%;font-size:12px">\xe4\xbf\x9d\xe5\xad\x98\xe5\x9c\xb0\xe5\x9d\x80</button>
              </div>

              <!-- \xe9\x92\xb1\xe5\x8c\x85\xe5\x8e\x86\xe5\x8f\xb2 -->
              <div style="margin-top:16px">
                <div style="font-size:14px;font-weight:600;margin-bottom:10px">\xf0\x9f\x93\x9c \xe9\x92\xb1\xe5\x8c\x85\xe5\x8e\x86\xe5\x8f\xb2</div>
                <div id="wallet-history-list" style="display:flex;flex-direction:column;gap:8px;max-height:300px;overflow-y:auto">
                  <div style="text-align:center;padding:20px;color:var(--muted);font-size:13px">\xe5\xb0\x9a\xe6\x97\xa0\xe9\x92\xb1\xe5\x8c\x85\xe5\x8e\x86\xe5\x8f\xb2\xe8\xae\xb0\xe5\xbd\x95</div>
                </div>
              </div>
            </div>
          </div>
'''

    old_exchanges_comment = b'          <!-- \xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe9\x85\x8d\xe7\xbd\xae\xe6\xa0\x87\xe7\xad\xbe\xe9\xa1\xb5\xe5\x86\x85\xe5\xae\xb9 -->'
    content = content.replace(old_exchanges_comment, wallet_tab_html + old_exchanges_comment, 1)
    print("CHANGE 1B: Wallet tab content added")

    # ========================================================
    # CHANGE 1C: Add 'wallet' to tabIds list
    # ========================================================
    old_tab_ids = b"const tabIds = ['positions', 'trades', 'signals', 'manual', 'market', 'strategies', 'exchanges'];"
    new_tab_ids = b"const tabIds = ['positions', 'trades', 'signals', 'manual', 'market', 'strategies', 'exchanges', 'wallet'];"

    if old_tab_ids in content:
        content = content.replace(old_tab_ids, new_tab_ids, 1)
        print("CHANGE 1C: Added 'wallet' to tabIds")
    else:
        print("CHANGE 1C FAILED: tabIds not found!")

    # ========================================================
    # CHANGE 2: Replace QuantTalk HTML
    # ========================================================
    qt_html_start_str = b'<!-- ===== QuantTalk ===== -->'
    qt_html_end_str = b'<!-- ===== \xe7\xad\x96\xe7\x95\xa5\xe5\xb8\x82\xe5\x9c\xba ===== -->'

    qt_html_start = content.find(qt_html_start_str)
    qt_html_end = content.find(qt_html_end_str, qt_html_start)

    if qt_html_start >= 0 and qt_html_end > qt_html_start:
        old_qt_html = content[qt_html_start:qt_html_end + len(qt_html_end_str)]

        new_qt_html = qt_html_start_str + b'''
      <div class="page" id="page-square" style="display:flex;gap:16px;padding:0">
        <!-- Left: Channel List -->
        <div class="ch-sidebar" style="width:200px;min-width:200px;background:var(--card);border:1px solid var(--border);border-radius:14px;display:flex;flex-direction:column;overflow:hidden">
          <div style="display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid var(--border)">
            <span style="font-weight:700;font-size:14px">\xf0\x9f\x93\xa1 \xe9\xa2\x91\xe9\x81\x93</span>
            <span onclick="createChannel()" style="width:28px;height:28px;border-radius:8px;background:var(--green);color:var(--dark);display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px;font-weight:700;line-height:1">+</span>
          </div>
          <div id="channel-list" style="flex:1;overflow-y:auto;padding:8px">
            <!-- channels rendered by JS -->
          </div>
        </div>

        <!-- Middle: Channel Content -->
        <div style="flex:1;display:flex;flex-direction:column;min-width:0">
          <!-- Channel Header -->
          <div class="ch-header" style="display:flex;align-items:center;justify-content:space-between;padding:14px 16px;background:var(--card);border:1px solid var(--border);border-radius:14px 14px 0 0;margin-bottom:1px">
            <div style="display:flex;align-items:center;gap:10px">
              <span id="ch-current-name" style="font-weight:700;font-size:15px">\xe9\x80\x89\xe6\x8b\xa9\xe9\xa2\x91\xe9\x81\x93</span>
              <span id="ch-current-count" style="font-size:12px;color:var(--muted)">0 \xe4\xba\xba</span>
            </div>
            <div style="display:flex;gap:6px">
              <button id="ch-toggle-tv" class="btn btn-outline" onclick="toggleWidget('tv')" style="font-size:11px;padding:4px 10px;display:none">\xf0\x9f\x93\x8a TV</button>
              <button id="ch-toggle-yt" class="btn btn-outline" onclick="toggleWidget('yt')" style="font-size:11px;padding:4px 10px;display:none">\xf0\x9f\x93\xb9 YT</button>
            </div>
          </div>

          <!-- TV Chart Widget -->
          <div id="ch-widget-tv" class="ch-widget" style="display:none;height:360px;background:var(--card);border:1px solid var(--border);margin-bottom:1px;overflow:hidden">
            <div id="tv-chart-container" style="width:100%;height:100%"></div>
          </div>

          <!-- YT Embed Widget -->
          <div id="ch-widget-yt" class="ch-widget" style="display:none;height:360px;background:var(--card);border:1px solid var(--border);margin-bottom:1px">
            <iframe id="ch-yt-iframe" style="width:100%;height:100%;border:none" allow="autoplay; encrypted-media" allowfullscreen></iframe>
          </div>

          <!-- Messages Area -->
          <div id="ch-messages" style="flex:1;overflow-y:auto;background:var(--card);border-left:1px solid var(--border);border-right:1px solid var(--border);padding:12px;min-height:200px;max-height:400px">
            <div style="text-align:center;padding:40px;color:var(--muted);font-size:13px">\xf0\x9f\x91\x8b \xe9\x80\x89\xe6\x8b\xa9\xe4\xb8\x80\xe4\xb8\xaa\xe9\xa2\x91\xe9\x81\x93\xe5\xbc\x80\xe5\xa7\x8b\xe8\x81\x8a\xe5\xa4\xa9</div>
          </div>

          <!-- Input Bar -->
          <div id="ch-input-bar" style="display:none;background:var(--card);border:1px solid var(--border);border-radius:0 0 14px 14px;padding:12px">
            <div style="display:flex;gap:8px;align-items:center">
              <input type="text" id="ch-msg-input" placeholder="\xe8\xbe\x93\xe5\x85\xa5\xe6\xb6\x88\xe6\x81\xaf..." style="flex:1;padding:10px 14px;border-radius:20px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-size:13px">
              <label for="ch-chart-share" style="width:34px;height:34px;border-radius:8px;background:var(--card2);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:16px">\xf0\x9f\x93\x8a</label>
              <input id="ch-chart-share" type="file" accept="image/*" style="display:none" onchange="shareChartImage(event)">
              <label for="ch-img-upload" style="width:34px;height:34px;border-radius:8px;background:var(--card2);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:16px">\xf0\x9f\x96\xbc\xef\xb8\x8f</label>
              <input id="ch-img-upload" type="file" accept="image/*" style="display:none" onchange="uploadChannelImage(event)">
              <button onclick="sendChannelMsg()" style="width:34px;height:34px;border-radius:8px;background:var(--green);color:var(--dark);border:none;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:16px">\xe2\x9e\xa1\xef\xb8\x8f</button>
            </div>
          </div>
        </div>

        <!-- Right: \xe8\xa7\x82\xe7\x82\xb9\xe5\xb9\xbf\xe5\x9c\xba -->
        <div style="width:280px;min-width:280px;display:flex;flex-direction:column;gap:12px">
          <div style="font-size:14px;font-weight:700">\xf0\x9f\x92\xa1 \xe8\xa7\x82\xe7\x82\xb9\xe5\xb9\xbf\xe5\x9c\xba</div>
          <div class="sq-composer" style="background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px">
            <div style="display:flex;gap:10px;align-items:flex-start">
              <div class="sq-av" style="background:linear-gradient(135deg,var(--green),var(--blue));flex-shrink:0;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:17px">\xf0\x9f\x91\xa4</div>
              <textarea id="sq-content" style="flex:1;width:100%;background:var(--card2);border:1px solid var(--border);border-radius:10px;padding:10px;color:var(--text);font-size:13px;resize:none;min-height:60px" placeholder="" data-i18n-ph="sq_input_ph"></textarea>
            </div>
            <div class="sq-composer-row" style="display:flex;align-items:center;gap:8px;margin-top:10px;flex-wrap:wrap">
              <div class="sq-tag-btns" style="display:flex;gap:4px;flex-wrap:wrap;flex:1">
                <span class="sq-tag bull active sq-sent-btn" onclick="selectSqSentiment('bull',this)" style="padding:3px 10px;border-radius:20px;font-size:11px;cursor:pointer;border:1px solid var(--border);color:var(--green)">\xf0\x9f\x93\x88 \xe7\x9c\x8b\xe5\xa4\x9a</span>
                <span class="sq-tag bear sq-sent-btn" onclick="selectSqSentiment('bear',this)" style="padding:3px 10px;border-radius:20px;font-size:11px;cursor:pointer;border:1px solid var(--border);color:var(--red)">\xf0\x9f\x93\x89 \xe7\x9c\x8b\xe7\xa9\xba</span>
                <span class="sq-tag neutral sq-sent-btn" onclick="selectSqSentiment('neutral',this)" style="padding:3px 10px;border-radius:20px;font-size:11px;cursor:pointer;border:1px solid var(--border);color:var(--yellow)">\xe2\x9e\xa1\xef\xb8\x8f \xe4\xb8\xad\xe6\x80\xa7</span>
              </div>
              <input type="hidden" id="sq-sentiment-val" value="bull">
              <select id="sq-pair-select" style="background:var(--card2);border:1px solid var(--border);border-radius:8px;padding:4px 6px;color:var(--text);font-size:11px">
                <option value="BTC/USDT">BTC/USDT</option>
                <option value="ETH/USDT">ETH/USDT</option>
                <option value="XAU/USD">XAU/USD</option>
              </select>
              <button class="btn btn-primary" onclick="postSquare()" style="font-size:12px;padding:5px 12px">\xe5\x8f\x91\xe5\xb8\x83</button>
            </div>
          </div>
          <div style="display:flex;gap:6px;flex-wrap:wrap">
            <button class="tlog-filter-btn active" onclick="renderSquare('all')" style="padding:4px 10px;font-size:11px;border-radius:20px;border:1px solid var(--border);background:transparent;color:var(--muted);cursor:pointer">\xe5\x85\xa8\xe9\x83\xa8</button>
            <button class="tlog-filter-btn" onclick="renderSquare('bull')" style="padding:4px 10px;font-size:11px;border-radius:20px;border:1px solid var(--border);background:transparent;color:var(--muted);cursor:pointer">\xe7\x9c\x8b\xe5\xa4\x9a</button>
            <button class="tlog-filter-btn" onclick="renderSquare('bear')" style="padding:4px 10px;font-size:11px;border-radius:20px;border:1px solid var(--border);background:transparent;color:var(--muted);cursor:pointer">\xe7\x9c\x8b\xe7\xa9\xba</button>
          </div>
          <div id="sq-posts" style="display:flex;flex-direction:column;gap:0;max-height:500px;overflow-y:auto"></div>
        </div>
      </div>

      ''' + qt_html_end_str

        content = content[:qt_html_start] + new_qt_html + content[qt_html_end + len(qt_html_end_str):]
        print("CHANGE 2: QuantTalk HTML replaced")
    else:
        print(f"CHANGE 2 FAILED: QuantTalk HTML markers not found! start={qt_html_start}, end={qt_html_end}")

    # ========================================================
    # CHANGE 3: Replace QuantTalk JS
    # ========================================================
    js_qt_start_str = b'// ===== QuantTalk ====='
    js_qt_end_str = b'// ===== \xe7\xad\x96\xe7\x95\xa5\xe5\xb8\x82\xe5\x9c\xba ====='

    js_qt_start = content.find(js_qt_start_str)
    js_qt_end = content.find(js_qt_end_str, js_qt_start + len(js_qt_start_str))

    if js_qt_start >= 0 and js_qt_end > js_qt_start:
        new_qt_js = b'''// ===== QuantTalk =====
// ===================================================

// --- Wallet Functions ---

let _walletState = { connected: false, type: '', name: '', address: '', history: [] };

function initWalletUI() {
  const saved = localStorage.getItem('quantai_wallet');
  if (saved) {
    try {
      _walletState = JSON.parse(saved);
      if (_walletState.connected && _walletState.address) {
        showWalletConnected(_walletState.name, _walletState.address);
      }
    } catch(e) {}
  }
  renderWalletHistory();
}

function connectWallet() {
  const sel = document.getElementById('wallet-type-select');
  const type = sel ? sel.value : 'metamask';
  const walletNames = {
    metamask: 'MetaMask', walletconnect: 'WalletConnect', trustwallet: 'Trust Wallet',
    okxwallet: 'OKX Wallet', exchange: '\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe9\x92\xb1\xe5\x8c\x85', coldwallet: '\xe5\x86\xb7\xe9\x92\xb1\xe5\x8c\x85'
  };
  if (type === 'exchange' || type === 'coldwallet') {
    showManualInput();
    return;
  }
  const name = walletNames[type] || 'MetaMask';
  // Simulate connect
  const fakeAddr = '0x' + Array.from({length:40}, () => '0123456789abcdef'[Math.floor(Math.random()*16)]).join('');
  _walletState = { connected: true, type, name, address: fakeAddr, history: [] };
  localStorage.setItem('quantai_wallet', JSON.stringify(_walletState));
  showWalletConnected(name, fakeAddr);
  renderWalletHistory();
  toast('\xf0\x9f\x94\x97 ' + name + ' \xe8\xbf\x9e\xe6\x8e\xa5\xe6\x88\x90\xe5\x8a\x9f', 'success');
}

function showManualInput() {
  const el = document.getElementById('wallet-manual-input');
  if (el) el.style.display = 'block';
}

function saveManualWallet() {
  const input = document.getElementById('wallet-address-input');
  const sel = document.getElementById('wallet-type-select');
  const type = sel ? sel.value : 'exchange';
  const addr = input ? input.value.trim() : '';
  if (!addr || addr.length < 10) {
    toast('\xe8\xaf\xb7\xe8\xbe\x93\xe5\x85\xa5\xe6\x9c\x89\xe6\x95\x88\xe7\x9a\x84\xe9\x92\xb1\xe5\x8c\x85\xe5\x9c\xb0\xe5\x9d\x80', 'error');
    return;
  }
  const walletNames = { metamask: 'MetaMask', walletconnect: 'WalletConnect', trustwallet: 'Trust Wallet',
    okxwallet: 'OKX Wallet', exchange: '\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe9\x92\xb1\xe5\x8c\x85', coldwallet: '\xe5\x86\xb7\xe9\x92\xb1\xe5\x8c\x85' };
  const name = walletNames[type] || '\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe9\x92\xb1\xe5\x8c\x85';
  _walletState = { connected: true, type, name, address: addr, history: [] };
  localStorage.setItem('quantai_wallet', JSON.stringify(_walletState));
  showWalletConnected(name, addr);
  renderWalletHistory();
  if (input) input.value = '';
  toast('\xe2\x9c\x85 \xe9\x92\xb1\xe5\x8c\x85\xe5\x9c\xb0\xe5\x9d\x80\xe5\xb7\xb2\xe4\xbf\x9d\xe5\xad\x98', 'success');
}

function showWalletConnected(name, address) {
  const infoEl = document.getElementById('wallet-connected-info');
  const nameEl = document.getElementById('wallet-display-name');
  const addrEl = document.getElementById('wallet-display-address');
  if (infoEl) infoEl.style.display = 'block';
  if (nameEl) nameEl.textContent = name;
  if (addrEl) addrEl.textContent = address;
  const manualEl = document.getElementById('wallet-manual-input');
  if (manualEl) manualEl.style.display = 'none';
}

function disconnectWallet() {
  _walletState = { connected: false, type: '', name: '', address: '', history: [] };
  localStorage.removeItem('quantai_wallet');
  const infoEl = document.getElementById('wallet-connected-info');
  if (infoEl) infoEl.style.display = 'none';
  toast('\xf0\x9f\x94\x93 \xe9\x92\xb1\xe5\x8c\x85\xe5\xb7\xb2\xe6\x96\xad\xe5\xbc\x80', '');
}

function renderWalletHistory() {
  const list = document.getElementById('wallet-history-list');
  if (!list) return;
  const saved = localStorage.getItem('quantai_wallet');
  if (!saved) {
    list.innerHTML = '<div style="text-align:center;padding:20px;color:var(--muted);font-size:13px">\xe5\xb0\x9a\xe6\x97\xa0\xe9\x92\xb1\xe5\x8c\x85\xe5\x8e\x86\xe5\x8f\xb2\xe8\xae\xb0\xe5\xbd\x95</div>';
    return;
  }
  try {
    const state = JSON.parse(saved);
    if (!state.address) throw 'no addr';
    list.innerHTML = '<div style="background:var(--card2);border:1px solid var(--border);border-radius:10px;padding:12px">' +
      '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">' +
      '<span style="font-weight:600;font-size:13px">' + state.name + '</span>' +
      '<span style="font-size:11px;color:var(--green)">\xe2\x97\x8f \xe5\xb7\xb2\xe8\xbf\x9e\xe6\x8e\xa5</span></div>' +
      '<div style="font-size:11px;color:var(--muted);word-break:break-all;font-family:monospace">' + state.address + '</div>' +
      '<div style="font-size:11px;color:var(--muted);margin-top:6px">\xe8\xbf\x9e\xe6\x8e\xa5\xe6\x97\xb6\xe9\x97\xb4: ' + new Date().toLocaleString() + '</div></div>';
  } catch(e) {
    list.innerHTML = '<div style="text-align:center;padding:20px;color:var(--muted);font-size:13px">\xe5\xb0\x9a\xe6\x97\xa0\xe9\x92\xb1\xe5\x8c\x85\xe5\x8e\x86\xe5\x8f\xb2\xe8\xae\xb0\xe5\xbd\x95</div>';
  }
}

// --- Channel System ---

let _channels = [];
let _activeChannel = null;
let _chMessages = {};

function initChannels() {
  const saved = localStorage.getItem('quantai_channels');
  if (saved) {
    try {
      const data = JSON.parse(saved);
      _channels = data.channels || [];
      _chMessages = data.messages || {};
    } catch(e) {
      _channels = [];
      _chMessages = {};
    }
  }
  if (_channels.length === 0) {
    _channels.push({ id: 'ch-general', name: '\xe5\x85\xa8\xe5\xb1\x80\xe8\x81\x8a\xe5\xa4\xa9', members: 42, tvPair: 'BTCUSDT', ytUrl: '' });
    _channels.push({ id: 'ch-btc', name: 'BTC\xe8\xae\xa8\xe8\xae\xba', members: 28, tvPair: 'BTCUSDT', ytUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ' });
    _channels.push({ id: 'ch-eth', name: 'ETH\xe8\xae\xa8\xe8\xae\xba', members: 19, tvPair: 'ETHUSDT', ytUrl: '' });
    _chMessages['ch-general'] = [
      { id: 'm1', uid: 'u1', name: '\xe4\xba\xa4\xe6\x98\x93\xe8\x80\x85A', av: '\xf0\x9f\x90\x82', text: '\xe5\xa4\xa7\xe5\xae\xb6\xe5\xa5\xbd\xef\xbc\x81\xe4\xbb\x8a\xe5\xa4\xa9BTC\xe6\x80\x8e\xe4\xb9\x88\xe7\x9c\x8b\xef\xbc\x9f', time: '\xe5\x88\x9a\xe5\x88\x9a', likes: 3 },
      { id: 'm2', uid: 'u2', name: '\xe9\x87\x8f\xe5\x8c\x96\xe7\x8b\x90', av: '\xf0\x9f\xa6\x8a', text: '\xe6\x88\x91\xe7\x9c\x8b\xe5\xa4\x9a\xef\xbc\x8c$72K\xe6\x94\xaf\xe6\x92\x91\xe5\xbe\x88\xe5\xbc\xba', time: '2\xe5\x88\x86\xe9\x92