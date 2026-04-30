# -*- coding: utf-8 -*-
"""在英文 i18n 块后插入仲裁引擎定义"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'

with open(filepath, 'rb') as f:
    raw = bytearray(f.read())

# 用 GBK 定位
text = raw.decode('gbk', errors='replace')
lines = text.split('\n')

# 英文块是 #2, L3800
# 找 "// Trading Square" 之后 L3800 的结尾
eng_block_start = None
eng_block_end = None
for i, line in enumerate(lines):
    if i >= 3795 and i <= 3810:
        stripped = line.strip()
        if stripped == "// Trading Square":
            eng_block_start = i
        if eng_block_start and line.startswith('    ') and i > eng_block_start:
            # 找到块的最后一行（下一行是 // 或空行）
            if i > eng_block_start + 1:
                next_line = lines[i+1].strip() if i+1 < len(lines) else ''
                if next_line.startswith('//') or next_line == '':
                    eng_block_end = i
                    break

if eng_block_end is None:
    # 简单方式：直接找 L3800 行的结束
    target_line_idx = None
    for i, line in enumerate(lines):
        if i >= 3798 and i <= 3810:
            if "nav_square:'QuantTalk'" in line and "//" not in line:
                target_line_idx = i
                # 找到这一行的末尾（下一行是 //开头）
                for j in range(i+1, min(i+10, len(lines))):
                    if lines[j].strip().startswith('//'):
                        eng_block_end = j-1
                        break
                if eng_block_end is None:
                    eng_block_end = i
                break

print(f"英文块: 开始行 {eng_block_start}, 结束行 {eng_block_end}")

# 计算二进制插入位置
insert_pos = 0
end_line = eng_block_end if eng_block_end else target_line_idx
for k in range(end_line + 1):
    insert_pos += len(lines[k].encode('gbk', errors='surrogateescape')) + 1

# 仲裁引擎英文 i18n
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
arb_en = '\n'.join(arb_en_lines).encode('utf-8')
raw[insert_pos:insert_pos] = b'\n' + arb_en
print(f"插入英文 i18n 定义: {len(arb_en)} 字节, 位置 {insert_pos}")

# 写入
with open(filepath, 'wb') as f:
    f.write(raw)

# 验证
with open(filepath, 'rb') as f:
    raw2 = f.read()

text2 = raw2.decode('gbk', errors='replace')
for term in ["nav_arbitrage:'Cross-Exchange Arbitrage'", "arb_title:'Cross-Exchange Arbitrage'",
             "arb_subtitle:'Real-time crypto exchange spread monitoring",
             "nav_arbitrage:'" + '跨交易所聚合引擎'.encode('gbk').decode('gbk') + "'"]:
    cnt = text2.count(term)
    print(f"  {term[:50]}: {cnt} 处")

print(f"文件: {len(raw2)/1024:.1f} KB")
