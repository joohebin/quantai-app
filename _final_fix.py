# -*- coding: utf-8 -*-
import re

filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'

with open(filepath, 'rb') as f:
    raw = f.read()

# ===== 1. HTML 导航菜单中的替换 =====
# 交易广场 -> QuantTalk (UTF-8)
# 替换 data-i18n="nav_square">交易广场</span>
nav_square_utf8 = b'data-i18n="nav_square">\xe4\xba\xa4\xe6\x98\x93\xe5\xb9\xbf\xe5\x9c\xba</span>'
nav_square_new = b'data-i18n="nav_square">QuantTalk</span>'
raw = raw.replace(nav_square_utf8, nav_square_new)

# 替换页面标题中的
sq_title_utf8 = b'<span data-i18n="sq_title">\xe4\xba\xa4\xe6\x98\x93\xe5\xb9\xbf\xe5\x9c\xba</span>'
sq_title_new = b'<span data-i18n="sq_title">QuantTalk</span>'
raw = raw.replace(sq_title_utf8, sq_title_new)

# ===== 2. 在 i18n 定义中替换 =====
# 用 GBK 解码处理中文部分
text = raw.decode('gbk', errors='surrogateescape')

# 替换中文 i18n 定义
text = text.replace("nav_square:'交易广场'", "nav_square:'QuantTalk'")
text = text.replace("sq_title:'交易广场'", "sq_title:'QuantTalk'")

# ===== 3. 添加仲裁引擎 i18n =====
zh_subtitle = "sq_subtitle:'分享观点，发现市场情绪，与全球交易者同频'"
arb_block = """    // 跨交易所聚合引擎
    nav_arbitrage:'跨交易所聚合引擎', arb_title:'跨交易所聚合引擎', arb_subtitle:'实时监控加密货币交易所价差，AI 自动执行搬砖套利',
    arb_monitored:'监控交易对', arb_active:'活跃套利机会', arb_profit_24h:'24h 套利收益', arb_executed:'已执行套利',
    arb_exchanges:'交易所连接状态', arb_refresh:'🔄 刷新',
    arb_opportunities:'实时套利机会', arb_th_pair:'交易对', arb_th_buy:'买入所', arb_th_sell:'卖出所',
    arb_th_spread:'价差', arb_th_profit:'预期盈利', arb_th_action:'操作', arb_exec_btn:'执行',
    arb_history:'套利执行历史', arb_history_empty:'暂无历史记录',
    """
if zh_subtitle in text:
    text = text.replace(zh_subtitle, zh_subtitle + ',\n' + arb_block)

# ===== 4. 写入 =====
with open(filepath, 'wb') as f:
    f.write(text.encode('gbk', errors='surrogateescape'))

print("写入完成，验证中...")

# ===== 5. 验证 =====
with open(filepath, 'rb') as f:
    raw2 = f.read()

# 用 GBK 解码来验证
text2 = raw2.decode('gbk', errors='replace')

n_quantalk = text2.count('QuantTalk')
n_arb = text2.count('nav_arbitrage')
n_arb_cn = text2.count('跨交易所聚合引擎')

print(f"QuantTalk 出现: {n_quantalk} 次")
print(f"nav_arbitrage 出现: {n_arb} 次")
print(f"跨交易所聚合引擎 出现: {n_arb_cn} 次")

# 检查菜单
nav_start = text2.find('showPage')
nav_end = text2.find('</nav>', nav_start)
nav_text = text2[nav_start:nav_end] if nav_end > nav_start else text2[nav_start:nav_start+3000]
print("\n导航菜单:")
pages = re.findall(r"showPage\('(\w+)'.*?data-i18n=\"([^\"]+)\"[^>]*>([^<]*)<", nav_text)
for page, i18n_key, label in pages:
    print(f"  {page}: [{i18n_key}] {label.strip()[:30]}")
