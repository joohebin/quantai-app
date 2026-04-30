# -*- coding: utf-8 -*-
"""
Fix: remove double-encoded arb i18n, insert correct UTF-8
"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'

with open(filepath, 'rb') as f:
    raw = bytearray(f.read())

# Remove the old wrong i18n block (L3609-L3616)
# These contain double-encoded UTF-8
# Find the section from "// è·¨äº¤æ" (double-encoded comment) to before "// 信号广播"
old_start = raw.find(b'\xc2\xb7\xc2\xa8\xc3\xa4\xc2\xba\xc2\xa4\xc3\xa6\xc2\x98\xc2\x93')
old_end = raw.find(b'// \xe4\xbf\xa1\xe5\x8f\xb7\xe5\xb9\xbf\xe6\x92\xad')  # // 信号广播

if old_start >= 0 and old_end > old_start:
    # Find the beginning of the line with "// 跨交易所"
    line_start = raw.rfind(b'\n', 0, old_start - 50)
    if line_start >= 0:
        del raw[line_start:old_end]
        print(f"删除旧错误 i18n 块: {line_start}~{old_end}")
else:
    print("未找到旧 i18n 块")

# Now find the correct insertion point
text = raw.decode('utf-8')
lines = text.split('\n')

# Find Chinese block end (last line with sq_ or sm_ before signals)
for i, line in enumerate(lines):
    if '// 信号广播' in line and i > 3500:
        # The line before this is where we insert
        insert_line = i
        break

# Chinese arbitrage i18n - real Chinese this time
arb_zh_lines = [
    '    // 跨交易所聚合引擎',
    "    nav_arbitrage:'跨交易所聚合引擎', arb_title:'跨交易所聚合引擎', arb_subtitle:'实时监控加密货币交易所价差，AI 自动执行搬砖套利',",
    "    arb_monitored:'监控交易对', arb_active:'活跃套利机会', arb_profit_24h:'24h 套利收益', arb_executed:'已执行套利',",
    "    arb_exchanges:'交易所连接状态', arb_refresh:'刷新',",
    "    arb_online:'在线', arb_lag:'延迟', arb_offline:'离线',",
    "    arb_opportunities:'实时套利机会', arb_th_pair:'交易对', arb_th_buy:'买入所', arb_th_sell:'卖出所',",
    "    arb_th_spread:'价差', arb_th_profit:'预期盈利', arb_th_action:'操作', arb_exec_btn:'执行',",
    "    arb_history:'套利执行历史', arb_history_empty:'暂无历史记录',",
]
for line in reversed(arb_zh_lines):
    lines.insert(insert_line, line)

print(f"正确中文 i18n 已插入 L{insert_line}")

# Find English block and insert
for i, line in enumerate(lines):
    if "nav_square:'Trading Square'" in line:
        # Find end of this block
        for k in range(i+1, min(len(lines), i+15)):
            if k+1 < len(lines) and lines[k+1].strip().startswith('//') and not lines[k+1].strip().startswith('// Trading'):
                en_insert = k + 1
                break
        
        arb_en_lines = [
            '    // Arbitrage Engine',
            "    nav_arbitrage:'Cross-Exchange Arbitrage', arb_title:'Cross-Exchange Arbitrage', arb_subtitle:'Real-time crypto exchange spread monitoring with AI arbitrage execution',",
            "    arb_monitored:'Monitored Pairs', arb_active:'Active Opps', arb_profit_24h:'24h Profit', arb_executed:'Executed',",
            "    arb_exchanges:'Exchange Status', arb_refresh:'Refresh',",
            "    arb_online:'Online', arb_lag:'Slow', arb_offline:'Offline',",
            "    arb_opportunities:'Opportunities', arb_th_pair:'Pair', arb_th_buy:'Buy', arb_th_sell:'Sell',",
            "    arb_th_spread:'Spread', arb_th_profit:'Profit', arb_th_action:'Action', arb_exec_btn:'Execute',",
            "    arb_history:'History', arb_history_empty:'No history',",
        ]
        for line in reversed(arb_en_lines):
            lines.insert(en_insert, line)
        print(f"正确英文 i18n 已插入 (after L{i})")
        break

# Save
output = '\n'.join(lines)
with open(filepath, 'wb') as f:
    f.write(output.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    raw2 = f.read()

print(f"\n=== 验证 ===")
for term, name in [
    ('跨交易所聚合引擎'.encode('utf-8'), '中文 cross-exchange'),
    ('实时监控加密货币交易所价差'.encode('utf-8'), '中文 arb_subtitle'),
    (b'Cross-Exchange Arbitrage', '英文 nav_arbitrage'),
    (b"arb_online:'Online'", 'arb_online'),
    (b'\xe4\xbf\xa1\xe5\x8f\xb7\xe5\xb9\xbf\xe6\x92\xad', 'signals block intact'),  # 信号广播
]:
    cnt = raw2.count(term)
    icon = 'OK' if cnt > 0 else 'XX'
    print(f"  [{icon}] {name}: {cnt}")

# Check no double-encoded garbage remains
double_check = b'\xc3\xa8\xc2\xb7\xc2\xa8'
if double_check in raw2:
    print(f"  \u26a0 Still has {raw2.count(double_check)} double-encoded bytes!")
else:
    print(f"  \u2713 No double-encoded bytes")

import os
print(f"文件大小: {os.path.getsize(filepath)/1024:.1f} KB")
