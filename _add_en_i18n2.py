# -*- coding: utf-8 -*-
"""在英文 i18n 块后插入仲裁引擎定义，纯二进制操作"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'

with open(filepath, 'rb') as f:
    raw = bytearray(f.read())

# 找到英文块 "// Trading Square" 之后的 nav_square:'QuantTalk' 行末尾
# 英文 nav_square 定义在二进制中是 UTF-8 的（因为英文是 ASCII）
target_en = b"nav_square:'QuantTalk', sq_title:'QuantTalk',"
idx = raw.find(target_en)
if idx >= 0:
    # 找到这一行的行尾
    line_end = raw.find(b'\n', idx)
    if line_end >= 0:
        arb_en = b'\n    // Arbitrage Engine\n    nav_arbitrage:\'Cross-Exchange Arbitrage\', arb_title:\'Cross-Exchange Arbitrage\', arb_subtitle:\'Real-time crypto exchange spread monitoring with AI arbitrage execution\',\n    arb_monitored:\'Monitored Pairs\', arb_active:\'Active Opps\', arb_profit_24h:\'24h Profit\', arb_executed:\'Executed\',\n    arb_exchanges:\'Exchange Status\', arb_refresh:\'Refresh\',\n    arb_online:\'Online\', arb_lag:\'Slow\', arb_offline:\'Offline\',\n    arb_opportunities:\'Opportunities\', arb_th_pair:\'Pair\', arb_th_buy:\'Buy\', arb_th_sell:\'Sell\',\n    arb_th_spread:\'Spread\', arb_th_profit:\'Profit\', arb_th_action:\'Action\', arb_exec_btn:\'Execute\',\n    arb_history:\'History\', arb_history_empty:\'No history\','
        raw[line_end+1:line_end+1] = arb_en
        print(f"在偏移 {line_end+1} 插入英文 i18n: {len(arb_en)} 字节")
    else:
        print("找不到行尾")
else:
    # 可能有多个，找第2个
    idx2 = raw.find(target_en, len(raw)//4)
    if idx2 >= 0:
        line_end = raw.find(b'\n', idx2)
        if line_end >= 0:
            arb_en = b'\n    // Arbitrage Engine\n    nav_arbitrage:\'Cross-Exchange Arbitrage\', arb_title:\'Cross-Exchange Arbitrage\', arb_subtitle:\'Real-time crypto exchange spread monitoring with AI arbitrage execution\',\n    arb_monitored:\'Monitored Pairs\', arb_active:\'Active Opps\', arb_profit_24h:\'24h Profit\', arb_executed:\'Executed\',\n    arb_exchanges:\'Exchange Status\', arb_refresh:\'Refresh\',\n    arb_online:\'Online\', arb_lag:\'Slow\', arb_offline:\'Offline\',\n    arb_opportunities:\'Opportunities\', arb_th_pair:\'Pair\', arb_th_buy:\'Buy\', arb_th_sell:\'Sell\',\n    arb_th_spread:\'Spread\', arb_th_profit:\'Profit\', arb_th_action:\'Action\', arb_exec_btn:\'Execute\',\n    arb_history:\'History\', arb_history_empty:\'No history\','
            raw[line_end+1:line_end+1] = arb_en
            print(f"在第2个位置 {line_end+1} 插入英文 i18n: {len(arb_en)} 字节")
    else:
        print("未找到英文 nav_square 定义")

# 写入
with open(filepath, 'wb') as f:
    f.write(raw)

# 验证
with open(filepath, 'rb') as f:
    raw2 = f.read()

for target, name in [
    (b"nav_arbitrage:'Cross-Exchange Arbitrage'", "英文 nav_arbitrage"),
    (b"arb_title:'Cross-Exchange Arbitrage'", "英文 arb_title"),
    (b"arb_subtitle:'Real-time", "英文 arb_subtitle"),
    (b"arb_online:'Online'", "arb_online"),
    ('跨交易所聚合引擎'.encode('gbk'), "GBK 中文 nav_arbitrage"),
]:
    cnt = raw2.count(target)
    print(f"  {name}: {cnt} 处")

print(f"文件: {len(raw2)/1024:.1f} KB")
