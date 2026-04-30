# -*- coding: utf-8 -*-
"""
Clean application of changes to original UTF-8 index.html (from Git)
1. 交易广场 -> QuantTalk (nav + title + all i18n)
2. Add 跨交易所聚合引擎 nav item + page
3. Add zh/en i18n definitions for arbitrage
"""
import re

filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'

with open(filepath, 'rb') as f:
    raw = bytearray(f.read())

# Confirm it's UTF-8
assert b'\xe4\xba\xa4\xe6\x98\x93\xe5\xb9\xbf\xe5\x9c\xba' in raw, "Missing 交易广场 UTF-8"
print(f"原始文件: {len(raw)/1024:.1f} KB")

# ===== 1. Replace 交易广场 with QuantTalk in HTML =====
old_nav = b'\xe4\xba\xa4\xe6\x98\x93\xe5\xb9\xbf\xe5\x9c\xba'  # 交易广场 in UTF-8
new_nav = b'QuantTalk'

# In nav menu: data-i18n="nav_square">交易广场</span>
# In page title: data-i18n="sq_title">交易广场</span>
# In i18n definitions: nav_square:'交易广场' etc

count = 0
while old_nav in raw:
    idx = raw.find(old_nav)
    raw[idx:idx+len(old_nav)] = new_nav
    count += 1
print(f"交易广场 -> QuantTalk: {count} 处替换")

# ===== 2. Add arbitrage nav item =====
# Find the square nav-item and insert after it
# Look for: showPage('square',this)
square_nav_idx = raw.find(b"showPage('square',this)")
if square_nav_idx >= 0:
    # Find the closing </div> of this nav-item
    div_end = raw.find(b'</div>', square_nav_idx)
    if div_end >= 0:
        arb_nav = b"""
          <div class="nav-item" onclick="showPage('arbitrage',this)" data-page="arbitrage">
            <span class="ni">\xf0\x9f\x94\x97</span><span data-i18n="nav_arbitrage"></span>
            <span class="badge">New</span>
          </div>"""
        raw[div_end+6:div_end+6] = arb_nav
        print(f"添加仲裁引擎导航菜单项: {len(arb_nav)} 字节")
else:
    print("未找到 square nav-item")

# ===== 3. Add arbitrage page div =====
# Find the closing </div> of page-square
sq_page_start = raw.find(b'<div class="page" id="page-square"')
sq_page_end = raw.find(b'<div class="page"', sq_page_start + 20)
if sq_page_start >= 0 and sq_page_end > sq_page_start:
    arb_page = b"""      <!-- ===== \xe8\xb7\xa8\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe8\x81\x9a\xe5\x90\x88\xe5\xbc\x95\xe6\x93\x8e ===== -->
      <div class="page" id="page-arbitrage" style="display:none">
        <div style="font-size:20px;font-weight:800;margin-bottom:4px">\xe2\x9a\xa1 <span data-i18n="arb_title"></span></div>
        <div style="font-size:13px;color:var(--muted);margin-bottom:16px" data-i18n="arb_subtitle"></div>

        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:16px">
          <div class="card" style="padding:16px">
            <div style="font-size:12px;color:var(--muted);margin-bottom:4px"><span data-i18n="arb_monitored"></span> <span id="arb-pairs-count">12</span></div>
            <div style="font-size:24px;font-weight:800;color:var(--green)">0</div>
          </div>
          <div class="card" style="padding:16px">
            <div style="font-size:12px;color:var(--muted);margin-bottom:4px"><span data-i18n="arb_active"></span> <span id="arb-active-opportunities">3</span></div>
            <div style="font-size:24px;font-weight:800;color:#f59e0b">0</div>
          </div>
          <div class="card" style="padding:16px">
            <div style="font-size:12px;color:var(--muted);margin-bottom:4px"><span data-i18n="arb_profit_24h"></span> <span id="arb-profit-24h">+$124.50</span></div>
            <div style="font-size:24px;font-weight:800;color:var(--green)">$0.00</div>
          </div>
          <div class="card" style="padding:16px">
            <div style="font-size:12px;color:var(--muted);margin-bottom:4px"><span data-i18n="arb_executed"></span> <span id="arb-executed-count">47</span></div>
            <div style="font-size:24px;font-weight:800">0</div>
          </div>
        </div>

        <div class="card" style="padding:16px;margin-bottom:16px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
            <div style="font-weight:700" data-i18n="arb_exchanges"></div>
            <button class="btn" style="padding:6px 14px;font-size:12px" onclick="refreshArbitrageStatus()" data-i18n="arb_refresh"></button>
          </div>
          <div id="arb-exchange-status" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px">
            <div class="exchange-item on" data-ex="binance">Binance <span data-i18n="arb_online"></span></div>
            <div class="exchange-item on" data-ex="okx">OKX <span data-i18n="arb_online"></span></div>
            <div class="exchange-item warn" data-ex="bybit">Bybit <span data-i18n="arb_lag"></span></div>
            <div class="exchange-item off" data-ex="kucoin">KuCoin <span data-i18n="arb_offline"></span></div>
          </div>
        </div>

        <div class="card" style="padding:16px;margin-bottom:16px">
          <div style="font-weight:700;margin-bottom:12px" data-i18n="arb_opportunities"></div>
          <div style="overflow-x:auto">
            <table style="width:100%;border-collapse:collapse;font-size:13px">
              <thead>
                <tr style="color:var(--muted);border-bottom:1px solid var(--border)">
                  <th style="padding:8px 6px;text-align:left" data-i18n="arb_th_pair">BTC/USDT</th>
                  <th style="padding:8px 6px;text-align:left" data-i18n="arb_th_buy"></th>
                  <th style="padding:8px 6px;text-align:left" data-i18n="arb_th_sell"></th>
                  <th style="padding:8px 6px;text-align:right" data-i18n="arb_th_spread"></th>
                  <th style="padding:8px 6px;text-align:right" data-i18n="arb_th_profit"></th>
                  <th style="padding:8px 6px;text-align:center" data-i18n="arb_th_action"></th>
                </tr>
              </thead>
              <tbody id="arb-opportunities-body">
                <tr style="border-bottom:1px solid var(--border)">
                  <td style="padding:8px 6px;font-weight:600">BTC/USDT</td>
                  <td style="padding:8px 6px;color:var(--green)">Binance</td>
                  <td style="padding:8px 6px;color:var(--blue)">OKX</td>
                  <td style="padding:8px 6px;text-align:right;color:var(--green)">+0.32%</td>
                  <td style="padding:8px 6px;text-align:right;color:var(--green)">$18.40</td>
                  <td style="padding:8px 6px;text-align:center">
                    <button class="btn" style="padding:4px 10px;font-size:11px" onclick="executeArbitrage('BTC/USDT')" data-i18n="arb_exec_btn"></button>
                  </td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                  <td style="padding:8px 6px;font-weight:600">ETH/USDT</td>
                  <td style="padding:8px 6px;color:var(--green)">OKX</td>
                  <td style="padding:8px 6px;color:var(--blue)">Binance</td>
                  <td style="padding:8px 6px;text-align:right;color:var(--green)">+0.18%</td>
                  <td style="padding:8px 6px;text-align:right;color:var(--green)">$6.72</td>
                  <td style="padding:8px 6px;text-align:center">
                    <button class="btn" style="padding:4px 10px;font-size:11px" onclick="executeArbitrage('ETH/USDT')" data-i18n="arb_exec_btn"></button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="card" style="padding:16px">
          <div style="font-weight:700;margin-bottom:12px" data-i18n="arb_history"></div>
          <div id="arb-history" style="font-size:13px;color:var(--muted)" data-i18n="arb_history_empty"></div>
        </div>
      </div>
"""
    raw[sq_page_end:sq_page_end] = arb_page
    print(f"添加仲裁引擎页面: {len(arb_page)} 字节")
else:
    print("未找到 page-square")

# ===== 4. Add i18n definitions =====
# Read as text for i18n manipulation
text = raw.decode('utf-8')
lines = text.split('\n')

# Find the first zh i18n block: "// 交易广场" (now "// QuantTalk")
i18n_block_start = None
i18n_block_end = None
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == '// QuantTalk' and i18n_block_start is None:
        i18n_block_start = i
    if i18n_block_start is not None and i > i18n_block_start and stripped == '':
        # End of block (empty line)
        i18n_block_end = i
        break
    # Also check for start of next language block
    if i18n_block_start is not None and i > i18n_block_start + 1 and stripped.startswith('//') and stripped != '// QuantTalk':
        i18n_block_end = i
        break

if i18n_block_start is not None and i18n_block_end is not None:
    # Insert Chinese i18n for arbitrage
    arb_zh = """    // \xe8\xb7\xa8\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe8\x81\x9a\xe5\x90\x88\xe5\xbc\x95\xe6\x93\x8e
    nav_arbitrage:'\xe8\xb7\xa8\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe8\x81\x9a\xe5\x90\x88\xe5\xbc\x95\xe6\x93\x8e', arb_title:'\xe8\xb7\xa8\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe8\x81\x9a\xe5\x90\x88\xe5\xbc\x95\xe6\x93\x8e', arb_subtitle:'\xe5\xae\x9e\xe6\x97\xb6\xe7\x9b\x91\xe6\x8e\xa7\xe5\x8a\xa0\xe5\xaf\x86\xe8\xb4\xa7\xe5\xb8\x81\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe4\xbb\xb7\xe5\xb7\xae\xef\xbc\x8cAI \xe8\x87\xaa\xe5\x8a\xa8\xe6\x89\xa7\xe8\xa1\x8c\xe6\x90\xac\xe7\xa0\x96\xe5\xa5\x97\xe5\x88\xa9',
    arb_monitored:'\xe7\x9b\x91\xe6\x8e\xa7\xe4\xba\xa4\xe6\x98\x93\xe5\xaf\xb9', arb_active:'\xe6\xb4\xbb\xe8\xb7\x83\xe5\xa5\x97\xe5\x88\xa9\xe6\x9c\xba\xe4\xbc\x9a', arb_profit_24h:'24h \xe5\xa5\x97\xe5\x88\xa9\xe6\x94\xb6\xe7\x9b\x8a', arb_executed:'\xe5\xb7\xb2\xe6\x89\xa7\xe8\xa1\x8c\xe5\xa5\x97\xe5\x88\xa9',
    arb_exchanges:'\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe8\xbf\x9e\xe6\x8e\xa5\xe7\x8a\xb6\xe6\x80\x81', arb_refresh:'\xe5\x88\xb7\xe6\x96\xb0',
    arb_online:'\xe5\x9c\xa8\xe7\xba\xbf', arb_lag:'\xe8\xbf\x9f\xe7\xbc\x93', arb_offline:'\xe7\xa6\xbb\xe7\xba\xbf',
    arb_opportunities:'\xe5\xae\x9e\xe6\x97\xb6\xe5\xa5\x97\xe5\x88\xa9\xe6\x9c\xba\xe4\xbc\x9a', arb_th_pair:'\xe4\xba\xa4\xe6\x98\x93\xe5\xaf\xb9', arb_th_buy:'\xe4\xb9\xb0\xe5\x85\xa5\xe6\x89\x80', arb_th_sell:'\xe5\x8d\x96\xe5\x87\xba\xe6\x89\x80',
    arb_th_spread:'\xe4\xbb\xb7\xe5\xb7\xae', arb_th_profit:'\xe9\xa2\x84\xe6\x9c\x9f\xe7\x9b\x88\xe5\x88\xa9', arb_th_action:'\xe6\x93\x8d\xe4\xbd\x9c', arb_exec_btn:'\xe6\x89\xa7\xe8\xa1\x8c',
    arb_history:'\xe5\xa5\x97\xe5\x88\xa9\xe6\x89\xa7\xe8\xa1\x8c\xe5\x8e\x86\xe5\x8f\xb2', arb_history_empty:'\xe6\x9a\x82\xe6\x97\xa0\xe5\x8e\x86\xe5\x8f\xb2\xe8\xae\xb0\xe5\xbd\x95',
"""
    # Insert before empty line
    lines.insert(i18n_block_end, arb_zh.rstrip('\n'))
    insert_line = i18n_block_end
    print(f"插入中文 i18n 定义")
    
    # Now find english block
    # After our insert, find next "// Trading Square" or "nav_square:'QuantTalk'"
    text = '\n'.join(lines)
    en_block_markers = ['// Trading Square', "nav_square:'QuantTalk'"]
    for marker in en_block_markers:
        idx = text.find(marker, text.find(marker) + 10 if text.find(marker) >= 0 else 0)
        if idx >= 0 and idx > text.find("nav_arbitrage"):  # After our zh insert
            break
    
    # Actually simpler: find the SECOND occurrence of "nav_square:'QuantTalk'"
    text = '\n'.join(lines)
    first = text.find("nav_square:'QuantTalk'")
    second = text.find("nav_square:'QuantTalk'", first + 10)
    
    if second >= 0:
        # Find the end of this block
        end_pos = text.find('\n    //', second + 10)
        if end_pos < 0:
            end_pos = text.find('\n\n', second)
        if end_pos < 0:
            end_pos = text.find('\n    nav_stratmarket', second)
        
        # Convert back to line number
        before = text[:end_pos]
        line_no = before.count('\n') + 1  # 1-indexed
        
        arb_en = """    // Arbitrage Engine
    nav_arbitrage:'Cross-Exchange Arbitrage', arb_title:'Cross-Exchange Arbitrage', arb_subtitle:'Real-time crypto exchange spread monitoring with AI arbitrage execution',
    arb_monitored:'Monitored Pairs', arb_active:'Active Opps', arb_profit_24h:'24h Profit', arb_executed:'Executed',
    arb_exchanges:'Exchange Status', arb_refresh:'Refresh',
    arb_online:'Online', arb_lag:'Slow', arb_offline:'Offline',
    arb_opportunities:'Opportunities', arb_th_pair:'Pair', arb_th_buy:'Buy', arb_th_sell:'Sell',
    arb_th_spread:'Spread', arb_th_profit:'Profit', arb_th_action:'Action', arb_exec_btn:'Execute',
    arb_history:'History', arb_history_empty:'No history',
"""
        # Insert before line_no
        lines.insert(line_no - 1, arb_en.rstrip('\n'))
        print(f"插入英文 i18n 定义")
    else:
        print("未找到英文 i18n 块")
else:
    print(f"未找到中文 i18n 块 (start={i18n_block_start}, end={i18n_block_end})")

# ===== 5. Save =====
output = '\n'.join(lines)
with open(filepath, 'wb') as f:
    f.write(output.encode('utf-8'))

print(f"\n保存完成: {len(output.encode('utf-8'))/1024:.1f} KB")

# ===== 6. Verify =====
with open(filepath, 'rb') as f:
    raw2 = f.read()

text2 = raw2.decode('utf-8')
print(f"\n=== 验证 ===")
for term in ['QuantTalk', 'arbitrage', 'nav_arbitrage', 'arb_title',
             '跨交易所聚合引擎', '实时监控加密货币交易所价差',
             'Cross-Exchange Arbitrage', 'arb_online:\'Online\'']:
    cnt = text2.count(term)
    icon = 'OK' if cnt > 0 else 'XX'
    print(f"  [{icon}] {term}: {cnt}")

# Check nav items
nav_text = text2[text2.find('<nav>'):text2.find('</nav>')]
nav_items = re.findall(r"showPage\('(\w+)'", nav_text)
print(f"\n导航菜单项 ({len(nav_items)}):")
for item in nav_items:
    print(f"  - {item}")

# Check pages
for page in ['square', 'arbitrage', 'stratmarket']:
    marker = f'id="page-{page}"'
    if marker in text2:
        print(f"  \u2713 page-{page}")
    else:
        print(f"  \u2717 page-{page}")

import os
fsize = os.path.getsize(filepath)
print(f"\n文件大小: {fsize/1024:.1f} KB")
