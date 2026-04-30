# -*- coding: utf-8 -*-
"""
Clean fix: 1) 修复 QuantTalk 导航 + 页面标题（二进制级别）
2) 删除损坏的仲裁页面
3) 重新插入正确的 page-arbitrage（纯 UTF-8）
4) 在 GBK i18n 区域添加 arb_* 中文定义
"""
import re

filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'

with open(filepath, 'rb') as f:
    raw = bytearray(f.read())

def q(s):
    """安全地编码中文字符串为 UTF-8"""
    return s.encode('utf-8')

def qg(s):
    """安全地编码中文字符串为 GBK"""
    return s.encode('gbk')

# ===== 1. 移除所有损坏的仲裁引擎相关内容 =====
# 找各种旧插入的标记
markers_to_remove = [
    b'<!-- ===== \xe8\xb7\xa8\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe8\x81\x9a\xe5\x90\x88\xe5\xbc\x95\xe6\x93\x8e ===== -->',  # UTF-8 注释
    b'<!-- ===== ' + qg('跨交易所聚合引擎') + b' ===== -->',  # GBK 注释
    # 找之前 _binary_fix.py 插入的 GBK 注释（它的内容是 UTF-8 写的但实际存储可能坏了）
]

# 删除旧仲裁页面 div（找 page-arbitrage 之前的注释标记）
# 策略：从 page-square 结束到 page-stratmarket 开始之间的所有内容删除
square_start = raw.find(b'<div class="page" id="page-square"')
square_end = raw.find(b'<div class="page"', square_start + 20)
stratmarket_start = raw.find(b'id="page-stratmarket"')

if square_end > 0 and stratmarket_start > 0:
    between = raw[square_end:stratmarket_start]
    # 检查之间是否有旧仲裁页面
    has_arb = b'page-arbitrage' in between
    if has_arb:
        # 找到最近注释开始
        # 从 square_end 往后找第一个注释
        cmt_start = raw.find(b'<!--', square_end, stratmarket_start)
        if cmt_start > 0:
            # 删到 stratmarket 之前
            del raw[cmt_start:stratmarket_start]
            print(f"删除旧仲裁页面: {cmt_start}~{stratmarket_start}")
        else:
            print("仲裁页面之间没有注释标记")
    else:
        print("square 和 stratmarket 之间没有旧仲裁页面")
else:
    print(f"square_end={square_end}, stratmarket={stratmarket_start}")

# ===== 2. 删除旧的损坏 i18n 定义 =====
# 找 GBK "跨交易所聚合引擎" 的 i18n 定义
for needle in [qg('跨交易所聚合引擎')]:
    while needle in raw:
        idx = raw.find(needle)
        # 删除该行
        line_start = raw.rfind(b'\n', 0, idx)
        if line_start < 0:
            line_start = max(0, idx - 100)
        line_end = raw.find(b'\n', idx)
        if line_end < 0:
            line_end = min(len(raw), idx + 200)
        del raw[line_start:line_end + 1]
        print(f"删除 i18n 行: {line_start}~{line_end+1}")

# 找 English "Arbitrage Engine" 的 i18n 定义
for needle in [b'Arbitrage Engine', b'Cross-Exchange Arbitrage']:
    while needle in raw:
        idx = raw.find(needle)
        line_start = raw.rfind(b'\n', 0, idx)
        if line_start < 0:
            line_start = max(0, idx - 100)
        line_end = raw.find(b'\n', idx)
        if line_end < 0:
            line_end = min(len(raw), idx + 200)
        del raw[line_start:line_end + 1]
        print(f"删除英文 i18n 行: {line_start}~{line_end+1}")

print(f"清理后: {len(raw)/1024:.1f} KB")

# ===== 3. 重新定位插入点 =====
square_end = raw.find(b'<div class="page"', square_start + 20)
stratmarket_start = raw.find(b'id="page-stratmarket"')
print(f"新插入点: square_end={square_end}, stratmarket={stratmarket_start}")

# ===== 4. 插入正确的仲裁页面 =====
arb_page_html = """      <!-- ===== \xe8\xb7\xa8\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80\xe8\x81\x9a\xe5\x90\x88\xe5\xbc\x95\xe6\x93\x8e ===== -->
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
raw[square_end:square_end] = arb_page_html.encode('utf-8')
print(f"插入仲裁页面 HTML: {len(arb_page_html)} 字节")

# ===== 5. 在 GBK i18n 区域插入中文定义 =====
# 找到中文 i18n 块的「最后一行」
# 用 GBK 解码找到位置
gbk_text = raw.decode('gbk', errors='surrogateescape')

# 找 zh i18n 块的 "nav_square" 所在行后
zh_blocks = []
lines = gbk_text.split('\n')
for i, line in enumerate(lines):
    if "nav_square:'QuantTalk'" in line and '//' not in line:
        zh_blocks.append((i, line))

if zh_blocks:
    # 第一个中文块
    block_line_no = zh_blocks[0][0]
    # 找到此块中最后一个 // 注释（下一个语言的标记）
    block_start = block_line_no
    block_end = block_line_no
    for j in range(block_line_no, min(block_line_no + 50, len(lines))):
        if lines[j].strip().startswith('//') and j > block_line_no + 2:
            block_end = j
            break
        block_end = j
    
    # 在块的最后一行后插入
    if block_end < len(lines):
        # GBK 编码的仲裁引擎 i18n（不带 emoji）
        arb_zh = [
            '    // ' + qg('跨交易所聚合引擎').decode('gbk') + '',
            "    nav_arbitrage:'" + qg('跨交易所聚合引擎').decode('gbk') + "', arb_title:'" + qg('跨交易所聚合引擎').decode('gbk') + "', arb_subtitle:'" + qg('实时监控加密货币交易所价差，AI 自动执行搬砖套利').decode('gbk') + "',",
            "    arb_monitored:'" + qg('监控交易对').decode('gbk') + "', arb_active:'" + qg('活跃套利机会').decode('gbk') + "', arb_profit_24h:'" + qg('24h 套利收益').decode('gbk') + "', arb_executed:'" + qg('已执行套利').decode('gbk') + "',",
            "    arb_exchanges:'" + qg('交易所连接状态').decode('gbk') + "', arb_refresh:'" + qg('刷新').decode('gbk') + "',",
            "    arb_opportunities:'" + qg('实时套利机会').decode('gbk') + "', arb_th_pair:'" + qg('交易对').decode('gbk') + "', arb_th_buy:'" + qg('买入所').decode('gbk') + "', arb_th_sell:'" + qg('卖出所').decode('gbk') + "',",
            "    arb_th_spread:'" + qg('价差').decode('gbk') + "', arb_th_profit:'" + qg('预期盈利').decode('gbk') + "', arb_th_action:'" + qg('操作').decode('gbk') + "', arb_exec_btn:'" + qg('执行').decode('gbk') + "',",
            "    arb_history:'" + qg('套利执行历史').decode('gbk') + "', arb_history_empty:'" + qg('暂无历史记录').decode('gbk') + "',",
        ]
        arb_gbk = '\n'.join(arb_zh).encode('gbk', errors='replace')
        
        insert_pos = 0
        for k, line in enumerate(lines):
            if k == block_end:
                break
            insert_pos += len(line.encode('gbk', errors='surrogateescape')) + 1
        
        raw[insert_pos:insert_pos] = b'\n' + arb_gbk
        print(f"插入中文 i18n: {len(arb_gbk)} 字节")

    # 英文块：找第二个 nav_square 定义后的块
    if len(zh_blocks) >= 2:
        en_block_line_no = zh_blocks[1][0]
        block_end_en = en_block_line_no
        for j in range(en_block_line_no, min(en_block_line_no + 50, len(lines))):
            if lines[j].strip().startswith('//') and j > en_block_line_no + 2:
                block_end_en = j
                break
            block_end_en = j
        
        if block_end_en < len(lines):
            arb_en = [
                '    // Arbitrage Engine',
                "    nav_arbitrage:'Cross-Exchange Arbitrage', arb_title:'Cross-Exchange Arbitrage', arb_subtitle:'Real-time crypto exchange spread monitoring with AI arbitrage execution',",
                "    arb_monitored:'Monitored Pairs', arb_active:'Active Opps', arb_profit_24h:'24h Profit', arb_executed:'Executed',",
                "    arb_exchanges:'Exchange Status', arb_refresh:'Refresh',",
                "    arb_opportunities:'Opportunities', arb_th_pair:'Pair', arb_th_buy:'Buy', arb_th_sell:'Sell',",
                "    arb_th_spread:'Spread', arb_th_profit:'Profit', arb_th_action:'Action', arb_exec_btn:'Execute',",
                "    arb_history:'History', arb_history_empty:'No history',",
            ]
            arb_en_b = '\n'.join(arb_en).encode('utf-8')
            
            insert_pos_en = 0
            for k, line in enumerate(lines):
                if k == block_end_en:
                    break
                insert_pos_en += len(line.encode('gbk', errors='surrogateescape')) + 1
            
            raw[insert_pos_en:insert_pos_en] = b'\n' + arb_en_b
            print(f"插入英文 i18n: {len(arb_en_b)} 字节")
    else:
        print("英文 zh_blocks count < 2, 手动找英文块")
else:
    print("未找到中文 i18n nav_square 定义")
    # 尝试直接查找 nav_square 的二进制
    raw_text = bytes(raw)
    idx = raw_text.find(b"nav_square:'QuantTalk'")
    if idx >= 0:
        print(f"二进制中找到 nav_square: {idx}")

# ===== 6. 写入 =====
with open(filepath, 'wb') as f:
    f.write(raw)

# ===== 7. 验证 =====
with open(filepath, 'rb') as f:
    raw2 = f.read()

print(f"\n=== 验证 ===")
checks = {
    'nav_square > QuantTalk': b"nav_square:'QuantTalk'",
    'sq_title > QuantTalk': b"sq_title:'QuantTalk'",
    '导航 QuantTalk': b'data-i18n="nav_square">QuantTalk',
    '页面 QuantTalk': b'data-i18n="sq_title">QuantTalk',
    'arb 页面 div': b'id="page-arbitrage"',
    'nav_arbitrage 菜单': b'data-i18n="nav_arbitrage">',
    'nav_arbitrage 定义': b"nav_arbitrage:'Cross-Exchange Arbitrage'",
    'arb_title 定义': b"arb_title:'Cross-Exchange Arbitrage'",
}

# 也用 GBK 检查中文定义
zk = qg('跨交易所聚合引擎')
cn_checks = {
    'nav_arbitrage 中文': b"nav_arbitrage:'" + zk + b"'",
    'arb_title 中文': b"arb_title:'" + zk + b"'",
}

all_checks = {**checks, **cn_checks}
for name, target in all_checks.items():
    cnt = raw2.count(target)
    if cnt > 0:
        print(f"  ✅ {name}: {cnt} 处")
    else:
        print(f"  ❌ {name}: 不存在")

# 检查剩余 交易广场
old_gbk = b"nav_square:'\xbd\xbb\xd2\xd7\xb9\xe3\xb3\xa1'"
if old_gbk in raw2:
    print(f"  ⚠️ 仍有旧 GBK 交易广场: {raw2.count(old_gbk)} 处")

print(f"\n文件大小: {len(raw2)/1024:.1f} KB")
