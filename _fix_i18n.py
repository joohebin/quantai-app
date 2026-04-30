# -*- coding: utf-8 -*-
import re

filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 找到第一个中文 i18n 块（nav_square: 后面的值应该是中文的）
# 找到第一个 nav_square: 后面的中文翻译
matches = list(re.finditer(r"nav_square:'([^']+)'", content))

# 分类：哪些是中文（包含中文字符）
chinese_idx = -1
for i, m in enumerate(matches):
    val = m.group(1)
    # 检查是否包含中文字符
    if re.search(r'[\u4e00-\u9fff]', val):
        chinese_idx = i
        print(f"中文 nav_square 在第 #{i}: {val}")
        break

# 为中文 i18n 块添加仲裁引擎翻译
# 找到 sq_subtitle: 这一行，在后面追加
zh_block_start = matches[chinese_idx].start()
zh_block_end = content.find("nav_stratmarket:", zh_block_start)
block = content[zh_block_start:zh_block_end]

# 在 sq_subtitle 后面插入仲裁 i18n
old_zh = r"sq_subtitle:'分享观点，发现市场情绪，与全球交易者同频'"
new_zh = r"""sq_subtitle:'分享观点，发现市场情绪，与全球交易者同频',
    // 跨交易所聚合引擎
    nav_arbitrage:'跨交易所聚合引擎', arb_title:'跨交易所聚合引擎', arb_subtitle:'实时监控加密货币交易所价差，AI 自动执行搬砖套利',
    arb_monitored:'监控交易对', arb_active:'活跃套利机会', arb_profit_24h:'24h 套利收益', arb_executed:'已执行套利',
    arb_exchanges:'交易所连接状态', arb_refresh:'🔄 刷新',
    arb_opportunities:'实时套利机会', arb_th_pair:'交易对', arb_th_buy:'买入所', arb_th_sell:'卖出所',
    arb_th_spread:'价差', arb_th_profit:'预期盈利', arb_th_action:'操作', arb_exec_btn:'执行',
    arb_history:'套利执行历史', arb_history_empty:'暂无历史记录'"""

if old_zh in block:
    content = content.replace(old_zh, new_zh)
    print("✅ 中文 i18n 已添加")
else:
    print("⚠️ 中文 i18n 匹配失败，检查文件编码")
    print(repr(block[block.find("sq_subtitle"):block.find("sq_subtitle")+200]))

# 保存
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 文件已保存")

# 验证
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
n = content.count('nav_arbitrage')
print(f"✅ nav_arbitrage 出现 {n} 次")
