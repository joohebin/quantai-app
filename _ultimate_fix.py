# -*- coding: utf-8 -*-
"""
终极修复：重新从原始文件重建，确保编码无误
策略：对于 UTF-8 区域（HTML/JS），用 UTF-8 写入
      对于 GBK 区域（i18n 定义），用 GBK 写入
"""
import re

filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'

# 读取原始文件（备份已存在）
with open(filepath, 'rb') as f:
    raw = bytearray(f.read())

print(f"原始文件: {len(raw)/1024:.1f} KB")

# ===== 1. 修复导航菜单 =====
# data-i18n="nav_square">交易广场 -> QuantTalk
old_nav = b'data-i18n="nav_square">\xe4\xba\xa4\xe6\x98\x93\xe5\xb9\xbf\xe5\x9c\xba'
new_nav = b'data-i18n="nav_square">QuantTalk'
count = 0
while old_nav in raw:
    idx = raw.find(old_nav)
    raw[idx:idx+len(old_nav)] = new_nav
    count += 1
print(f"修复导航菜单: {count} 处")

# ===== 2. 修复页面标题 =====  
# <span data-i18n="sq_title">交易广场</span> -> QuantTalk
old_title = b'<span data-i18n="sq_title">\xe4\xba\xa4\xe6\x98\x93\xe5\xb9\xbf\xe5\x9c\xba</span>'
new_title = b'<span data-i18n="sq_title">QuantTalk</span>'
count = 0
while old_title in raw:
    idx = raw.find(old_title)
    raw[idx:idx+len(old_title)] = new_title
    count += 1
print(f"修复页面标题: {count} 处")

# ===== 3. 修复 GBK i18n 定义 =====
# 在 GBK 编码的 i18n 区域中替换
# "nav_square:'交易广场'" -> "nav_square:'QuantTalk'"
old_sq_gbk = b"nav_square:'\xbd\xbb\xd2\xd7\xb9\xe3\xb3\xa1'"
new_sq_gbk = b"nav_square:'QuantTalk'"
count = 0
while old_sq_gbk in raw:
    idx = raw.find(old_sq_gbk)
    raw[idx:idx+len(old_sq_gbk)] = new_sq_gbk
    count += 1
print(f"修复 GBK nav_square: {count} 处")

old_sq2_gbk = b"sq_title:'\xbd\xbb\xd2\xd7\xb9\xe3\xb3\xa1'"
new_sq2_gbk = b"sq_title:'QuantTalk'"
count = 0
while old_sq2_gbk in raw:
    idx = raw.find(old_sq2_gbk)
    raw[idx:idx+len(old_sq2_gbk)] = new_sq2_gbk
    count += 1
print(f"修复 GBK sq_title: {count} 处")

# ===== 4. 删除之前错误插入的损坏仲裁页面 =====
# 找到并删除之前插入的 page-arbitrage 内容
cmt_start = '\u00b7\u00b7\u00b7\u00b7\u00b7\u00b7\u00b7\u00b7\u00b7'.encode('utf-8')
# 改为搜索已知的标记
arb_start = raw.find(b'<!-- ===== ')
# 实际上用字符串来构建搜索
arb_comment = u'<!-- ===== \u8de8\u4ea4\u6613\u6240\u805a\u5408\u5f15\u64ce ===== -->'.encode('utf-8')
arb_start = raw.find(arb_comment)
if arb_start >= 0:
    # 找到这个注释开始～下一个注释或 page- 结束
    arb_end_patterns = [
        u'\u7b56\u7565\u5e02\u573a'.encode('utf-8'),  # 策略市场
        b'<div class="page" id="page-stratmarket"',
        b'<div class="page" id="page-signals"',
    ]
    # 用已知标记
    stratmarket = raw.find(b'id="page-stratmarket"')
    if stratmarket >= 0:
        arb_end = stratmarket
    else:
        arb_end = len(raw)
    # 移除
    del raw[arb_start:arb_end]
    print(f"删除损坏的仲裁页面: {arb_start}~{arb_end}")
else:
    print("未找到先前插入的仲裁页面")

# 也找 _binary_fix.py 插入的版本
arb_start2 = raw.find(b'id="page-arbitrage"')
if arb_start2 >= 0:
    # 找到结束位置
    # 找上一个注释
    comment_start = raw.rfind(b'<!--', 0, arb_start2)
    if comment_start < 0:
        comment_start = raw.rfind(b'<div class="page" id="page-square"', 0, arb_start2)
    
    # 找下一个 page- 或下一个注释
    page_end = raw.find(b'<div class="page"', arb_start2+20)
    
    if comment_start >= 0 and page_end > arb_start2:
        del raw[comment_start:page_end]
        print(f"删除之前插入的有问题的仲裁页面: {comment_start}~{page_end} ({page_end-comment_start}字节)")
    elif page_end > arb_start2:
        del raw[arb_start2:page_end]
        print(f"删除部分仲裁页面: {arb_start2}~{page_end}")
    else:
        # 找不到结束位置，保守删除整个 section
        # 找 </div><!-- ===== 下一个 page
        next_page = raw.find(b'id="page-', arb_start2+30)
        if next_page >= 0:
            del raw[arb_start2-20:next_page]
            print(f"删除仲裁页面 (保守): {arb_start2-20}~{next_page}")
else:
    print("无损坏的 page-arbitrage div 需要删除")

# 删除之前添加的损坏 i18n 定义
# 找的 "// 跨交易所聚合引擎" 注释（GBK 或 UTF-8）
for needle in [b'\xa1\xf1\xbf\xe7\xbd\xbb\xd2\xd7\xcb\xf9\xbe\xdb\xba\xcf\xd2\xfd\xc7\xe6',  # GBK
               u'// 跨交易所聚合引擎'.encode('utf-8')]:  # UTF-8
    while needle in raw:
        idx = raw.find(needle)
        # 找到这一行的结尾（下一个 */
        line_end = raw.find(b'\n', idx)
        next_line = raw.find(b'\n', line_end + 1)
        # 删除这一行到下一行
        del raw[idx:next_line+1]
        print(f"删除损坏的 i18n 定义: {idx}~{next_line+1}")

print(f"清理后文件: {len(raw)/1024:.1f} KB")

# ===== 5. 重新插入正确的仲裁引擎页面 =====
# 找到 page-square 的结尾，在其后插入
# 先找到完整 page-square
square_start = raw.find(b'<div class="page" id="page-square"')
if square_start >= 0:
    square_end = raw.find(b'<div class="page"', square_start + 20)
    if square_end < 0:
        square_end = square_start + 4000
    
    # 构建仲裁页面（纯 UTF-8，用 ASCII 中文字符变量）
    arb_html = b"""
      <!-- ===== 跨交易所聚合引擎 ===== -->
      <div class="page" id="page-arbitrage" style="display:none">
        <div style="font-size:20px;font-weight:800;margin-bottom:4px">\xe2\x9a\xa1 <span data-i18n="arb_title"></span></div>
        <div style="font-size:13px;color:var(--muted);margin-bottom:16px" data-i18n="arb_subtitle"></div>

        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:16px">
          <div class="card" style="padding:16px">
            <div style="font-size:12px;color:var(--muted);margin-bottom:4px" data-i18n="arb_monitored">0</div>
            <div style="font-size:24px;font-weight:800;color:var(--green)" id="arb-pairs-count">12</div>
          </div>
          <div class="card" style="padding:16px">
            <div style="font-size:12px;color:var(--muted);margin-bottom:4px" data-i18n="arb_active">0</div>
            <div style="font-size:24px;font-weight:800;color:#f59e0b" id="arb-active-opportunities">3</div>
          </div>
          <div class="card" style="padding:16px">
            <div style="font-size:12px;color:var(--muted);margin-bottom:4px" data-i18n="arb_profit_24h">$0.00</div>
            <div style="font-size:24px;font-weight:800;color:var(--green)" id="arb-profit-24h">+$124.50</div>
          </div>
          <div class="card" style="padding:16px">
            <div style="font-size:12px;color:var(--muted);margin-bottom:4px" data-i18n="arb_executed">0</div>
            <div style="font-size:24px;font-weight:800" id="arb-executed-count">47</div>
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
    # 插入到 page-square 之后
    raw[square_end:square_end] = arb_html
    print(f"插入正确的仲裁页面: {len(arb_html)} 字节")
else:
    print("未找到 page-square 插入点")

# ===== 6. 在 GBK i18n 区域插入中文定义 =====
# 找到第一个 nav_square 定义的位置（中文 GBK 区域）
zh_block_idx = raw.find(b"nav_square:'QuantTalk', sq_title:'QuantTalk'")
if zh_block_idx >= 0:
    # 找到中文 i18n 块的结尾（下一个 // 注释或 nav_ 开头）
    next_comment = raw.find(b'\n    //', zh_block_idx + 50)
    if next_comment < 0:
        next_comment = raw.find(b'\n    nav_stratmarket', zh_block_idx + 50)
    
    # GBK 编码的中文 i18n 定义
    arb_i18n_cn = b"""
    // \xb1\xe8\xbd\xbb\xd2\xd7\xcb\xf9\xbe\xdb\xba\xcf\xd2\xfd\xc7\xe6
    nav_arbitrage:'\xb1\xe8\xbd\xbb\xd2\xd7\xcb\xf9\xbe\xdb\xba\xcf\xd2\xfd\xc7\xe6', arb_title:'\xb1\xe8\xbd\xbb\xd2\xd7\xcb\xf9\xbe\xdb\xba\xcf\xd2\xfd\xc7\xe6', arb_subtitle:'\xca\xb5\xca\xb1\xbc\xe0\xbf\xd8\xbc\xd3\xc3\xdc\xbb\xf5\xb1\xd2\xd2\xd7\xcb\xf9\xbc\xdb\xb2\xee\xa3\xacAI\xd7\xd4\xb6\xaf\xd6\xb4\xd0\xd0\xb0\xe1\xd7\xa9\xcc\xd7\xc0\xfb',
    arb_monitored:'\xbc\xe0\xbf\xd8\xbd\xbb\xd2\xd7\xb6\xd4', arb_active:'\xbb\xee\xd4\xbe\xcc\xd7\xc0\xfb\xbb\xfa\xbb\xe1', arb_profit_24h:'24h \xcc\xd7\xc0\xfb\xca\xd5\xd2\xe6', arb_executed:'\xd2\xd1\xd6\xb4\xd0\xd0\xcc\xd7\xc0\xfb',
    arb_exchanges:'\xbd\xbb\xd2\xd7\xcb\xf9\xc1\xac\xbd\xd3\xd7\xb4\xcc\xac', arb_refresh:'\xcb\xa2\xd0\xc2',
    arb_opportunities:'\xca\xb5\xca\xb1\xcc\xd7\xc0\xfb\xbb\xfa\xbb\xe1', arb_th_pair:'\xbd\xbb\xd2\xd7\xb6\xd4', arb_th_buy:'\xc2\xf2\xc8\xeb\xcb\xf9', arb_th_sell:'\xc2\xf4\xb3\xf6\xcb\xf9',
    arb_th_spread:'\xbc\xdb\xb2\xee', arb_th_profit:'\xd4\xa4\xc6\xda\xd3\xaf\xc0\xfb', arb_th_action:'\xb2\xd9\xd7\xf7', arb_exec_btn:'\xd6\xb4\xd0\xd0',
    arb_history:'\xcc\xd7\xc0\xfb\xd6\xb4\xd0\xd0\xc0\xfa\xca\xb7', arb_history_empty:'\xd4\xdd\xce\xde\xc0\xfa\xca\xb7\xbc\xc7\xc2\xbc',
"""
    if next_comment > zh_block_idx:
        raw[next_comment:next_comment] = arb_i18n_cn
        print(f"插入中文 i18n 定义: {len(arb_i18n_cn)} 字节 (GBK)")
    
    # 也在英文区域插入
    en_block_idx = raw.find(b"nav_square:'QuantTalk', sq_title:'QuantTalk'", zh_block_idx + 100)
    if en_block_idx > zh_block_idx:
        next_comment_en = raw.find(b'\n    //', en_block_idx + 50)
        if next_comment_en < 0:
            next_comment_en = raw.find(b'\n    nav_stratmarket', en_block_idx + 50)
        
        arb_i18n_en = b"""
    // Arbitrage Engine
    nav_arbitrage:'Cross-Exchange Arbitrage', arb_title:'Cross-Exchange Arbitrage', arb_subtitle:'Real-time crypto exchange spread monitoring with AI arbitrage execution',
    arb_monitored:'Monitored Pairs', arb_active:'Active Opportunities', arb_profit_24h:'24h Profit', arb_executed:'Executed',
    arb_exchanges:'Exchange Status', arb_refresh:'Refresh',
    arb_opportunities:'Live Arbitrage Opportunities', arb_th_pair:'Pair', arb_th_buy:'Buy Exchange', arb_th_sell:'Sell Exchange',
    arb_th_spread:'Spread', arb_th_profit:'Est. Profit', arb_th_action:'Action', arb_exec_btn:'Execute',
    arb_history:'Arbitrage History', arb_history_empty:'No history yet',
"""
        if next_comment_en > en_block_idx:
            raw[next_comment_en:next_comment_en] = arb_i18n_en
            print(f"插入英文 i18n 定义: {len(arb_i18n_en)} 字节")

# ===== 7. 添加页面 JS 函数（showPage 支持仲裁引擎页面）=====
# 检查 showPage 函数是否已支持 arbitrage
showpage_idx = raw.find(b'function showPage')
if showpage_idx >= 0:
    showpage_end = raw.find(b'{', showpage_idx)
    showpage_func = raw[showpage_idx:showpage_end+2000].decode('utf-8', errors='replace')
    # 检查是否有 arbitrage 处理逻辑
    if 'arbitrage' not in showpage_func:
        print("注意: showPage 可能需要添加 arbitrage 处理（可稍后完善）")
    else:
        print("showPage 已有 arbitrage 处理")

# ===== 写入 =====
with open(filepath, 'wb') as f:
    f.write(raw)

print(f"\n写入完成！新文件: {len(raw)/1024:.1f} KB")

# ===== 最终验证 =====
with open(filepath, 'rb') as f:
    raw2 = f.read()

# 用 UTF-8 解码特定区域
utf8_area = raw2[:80000].decode('utf-8', errors='replace')
print(f"\nUTF-8 区域验证:")
print(f"  QuantTalk 导航菜单: {'QuantTalk' in utf8_area[50000:51000]}")

# 检查 i18n 定义
arb_def = b"nav_arbitrage:'"
def_count = raw2.count(arb_def)
print(f"  nav_arbitrage i18n 定义数: {def_count}")

# 检查仲裁页面
has_page = b'id="page-arbitrage"' in raw2
print(f"  仲裁引擎页面存在: {has_page}")

# GBK 区域中的中文
text_gbk = raw2.decode('gbk', errors='replace')
print(f"  GBK 区域有 arb_title: {'arb_title' in text_gbk}")
print(f"  GBK 区域有 跨交易所聚合引擎: {'跨交易所聚合引擎' in text_gbk}")
