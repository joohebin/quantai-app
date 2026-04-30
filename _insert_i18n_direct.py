# -*- coding: utf-8 -*-
"""
Direct insertion of arbitrage i18n into the correct Chinese block
"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'

with open(filepath, 'rb') as f:
    raw = bytearray(f.read())

# ===== Find the correct i18n insertion point =====
# The Chinese block starts at "// 排行榜升级" or "// Leaderboard" (Chinese)
# Actually: the first nav_square block is Chinese (L3583)
# We need to find "nav_square:'QuantTalk'" with Chinese lines around it

# Strategy: Find "nav_square:'QuantTalk'" and check the lines before it
# If the line before it has Chinese comment (like // 排行榜升级), it's the Chinese block
text = raw.decode('utf-8')
lines = text.split('\n')

# Find all nav_square definitions and their preceding comments
chinese_block_start = None
chinese_block_end = None
for i, line in enumerate(lines):
    if "nav_square:'QuantTalk'" in line:
        # Check preceding comment
        for j in range(max(0,i-5), i):
            stripped = lines[j].strip()
            if stripped.startswith('//'):
                # Check if it's Chinese comment (contains CJK chars)
                has_cjk = any('\u4e00' <= c <= '\u9fff' for c in stripped)
                if has_cjk:
                    chinese_block_start = i
                    # Find end of this block
                    for k in range(i+1, min(len(lines), i+20)):
                        if lines[k].strip() == '' or (lines[k].strip().startswith('//') and k > i+2):
                            chinese_block_end = k
                            break
                    break
        if chinese_block_start:
            break

if chinese_block_start:
    print(f"中文 i18n 块: L{chinese_block_start} to L{chinese_block_end}")
    print(f"最后一行: {lines[chinese_block_end-1][:60]}")
    print(f"下一行: {lines[chinese_block_end][:60] if chinese_block_end < len(lines) else 'EOF'}")
    
    # Insert Chinese arbitrage i18n
    arb_zh = """    // 跨交易所聚合引擎
    nav_arbitrage:'跨交易所聚合引擎', arb_title:'跨交易所聚合引擎', arb_subtitle:'实时监控加密货币交易所价差，AI 自动执行搬砖套利',
    arb_monitored:'监控交易对', arb_active:'活跃套利机会', arb_profit_24h:'24h 套利收益', arb_executed:'已执行套利',
    arb_exchanges:'交易所连接状态', arb_refresh:'刷新',
    arb_online:'在线', arb_lag:'延迟', arb_offline:'离线',
    arb_opportunities:'实时套利机会', arb_th_pair:'交易对', arb_th_buy:'买入所', arb_th_sell:'卖出所',
    arb_th_spread:'价差', arb_th_profit:'预期盈利', arb_th_action:'操作', arb_exec_btn:'执行',
    arb_history:'套利执行历史', arb_history_empty:'暂无历史记录',
"""
    lines.insert(chinese_block_end, arb_zh.rstrip('\n'))
    new_end = chinese_block_end + 1
    print(f"中文 i18n 已插入 (L{new_end})")
else:
    print("未找到中文 i18n 块")
    # Fallback: insert after first nav_square line
    for i, line in enumerate(lines):
        if "nav_square:'QuantTalk'" in line:
            lines.insert(i+1, """    // 跨交易所聚合引擎
    nav_arbitrage:'跨交易所聚合引擎', arb_title:'跨交易所聚合引擎', arb_subtitle:'实时监控加密货币交易所价差，AI 自动执行搬砖套利',
    arb_monitored:'监控交易对', arb_active:'活跃套利机会', arb_profit_24h:'24h 套利收益', arb_executed:'已执行套利',
    arb_exchanges:'交易所连接状态', arb_refresh:'刷新',
    arb_online:'在线', arb_lag:'延迟', arb_offline:'离线',
    arb_opportunities:'实时套利机会', arb_th_pair:'交易对', arb_th_buy:'买入所', arb_th_sell:'卖出所',
    arb_th_spread:'价差', arb_th_profit:'预期盈利', arb_th_action:'操作', arb_exec_btn:'执行',
    arb_history:'套利执行历史', arb_history_empty:'暂无历史记录',
""")
            print(f"后备: 中文 i18n 已插入 L{i+1}")
            new_end = i + 1
            break

# ===== Find English block =====
# English is the second block (// Leaderboard upgrade / Trading Square)
en_block_start = None
en_block_end = None
for i, line in enumerate(lines):
    if i > (new_end if 'new_end' in dir() else 0):
        if "nav_square:'Trading Square'" in line:
            en_block_start = i
            for k in range(i+1, min(len(lines), i+20)):
                if lines[k].strip() == '' or (lines[k].strip().startswith('//') and k > i+2):
                    en_block_end = k
                    break
            break

if en_block_start:
    print(f"英文 i18n 块: L{en_block_start} to L{en_block_end}")
    
    arb_en = """    // Arbitrage Engine
    nav_arbitrage:'Cross-Exchange Arbitrage', arb_title:'Cross-Exchange Arbitrage', arb_subtitle:'Real-time crypto exchange spread monitoring with AI arbitrage execution',
    arb_monitored:'Monitored Pairs', arb_active:'Active Opps', arb_profit_24h:'24h Profit', arb_executed:'Executed',
    arb_exchanges:'Exchange Status', arb_refresh:'Refresh',
    arb_online:'Online', arb_lag:'Slow', arb_offline:'Offline',
    arb_opportunities:'Opportunities', arb_th_pair:'Pair', arb_th_buy:'Buy', arb_th_sell:'Sell',
    arb_th_spread:'Spread', arb_th_profit:'Profit', arb_th_action:'Action', arb_exec_btn:'Execute',
    arb_history:'History', arb_history_empty:'No history',
"""
    lines.insert(en_block_end, arb_en.rstrip('\n'))
    print(f"英文 i18n 已插入 (L{en_block_end})")
else:
    print("未找到英文 i18n 块")

# ===== Save =====
output = '\n'.join(lines)
with open(filepath, 'wb') as f:
    f.write(output.encode('utf-8'))

print(f"\n保存完成: {len(output.encode('utf-8'))/1024:.1f} KB")

# ===== Verify =====
with open(filepath, 'rb') as f:
    raw2 = f.read()

for term, name in [
    ('跨交易所聚合引擎'.encode('utf-8'), '中文 跨交易所聚合引擎'),
    ('实时监控加密货币交易所价差'.encode('utf-8'), '中文 arb_subtitle'),
    (b'Cross-Exchange Arbitrage', '英文 nav_arbitrage'),
    (b"arb_online:'Online'", '英文 arb_online'),
    (b"arb_online:'" + '在线'.encode('utf-8') + b"'", '中文 arb_online'),
]:
    cnt = raw2.count(term)
    icon = 'OK' if cnt > 0 else 'XX'
    print(f"  [{icon}] {name}: {cnt}")

import os
print(f"文件大小: {os.path.getsize(filepath)/1024:.1f} KB")
