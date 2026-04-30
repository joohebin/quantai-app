# -*- coding: utf-8 -*-
"""
Fix: 交易广场 -> QuantTalk and add 仲裁引擎 i18n in index.html
The file has mixed encoding: HTML is UTF-8, Chinese i18n is GBK/GB18030
"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'

with open(filepath, 'rb') as f:
    raw = f.read()

# 1. 在 HTML 中修复 <div class="page" id="page-square"> 里的标题
# UTF-8 部分
target_html = b'<span data-i18n="sq_title">\xe6\xb5\xa0\xe5\xad\x98\xe5\x9a\x8e\xe9\x8d\x8a\xe6\xa0\xa7</span>'
replacement = b'<span data-i18n="sq_title">QuantTalk</span>'
count = raw.count(target_html)
print(f'HTML sq_title 匹配: {count} 处')
if count > 0:
    raw = raw.replace(target_html, replacement)

# 备用：不同版本的中文 "交易广场" 可能不同编码
# 用正则匹配 data-i18n="sq_title">...< 
import re
def replace_sq_title(m):
    return m.group(0).encode('utf-8').replace(b'>\xe6\xb5\xa0\xe5\xad\x98\xe5\x9a\x8e\xe9\x8d\x8a\xe6\xa0\xa7<', b'>QuantTalk<')

# 2. 在 GBK 区域替换 nav_square:'中文' -> nav_square:'QuantTalk'
# 找到第一个 nav_square: 后面的 GBK 中文
# 用字节操作：nav_square: 后面的值看起来是 14 字节的 GBK
# 用更稳健的方式 - 找到 // 注释行后的 GBK "交易广场" 对应内容
# nav_square:'xx...xx' 中 'xx...xx' 是 GBK 编码的 "娣樺瓨鍙ラ崼妤呯潐闃佸獎瀵? (或类似)

# 读取文件，用 GBK 解码处理
with open(filepath, 'r', encoding='gb18030', errors='surrogateescape') as f:
    text = f.read()

# 找到中文 i18n 块
# 直接在 gb18030 解码的文本中找
zh_marker = '// 交易广场'
if zh_marker in text:
    print('找到 // 交易广场 注释')
else:
    # 尝试找到注释块
    for line in text.split('\n'):
        if '交易广场' in line or 'nav_square' in line:
            print(f'Found: {line.strip()[:80]}')
            break

# 直接找 '交易广场' 出现的地方
idx = text.find('交易广场')
print(f'交易广场 在 gb18030 解码中的位置: {idx}')
if idx >= 0:
    ctx = text[max(0,idx-20):idx+60]
    print(f'Context: {repr(ctx)}')

# 替换导航部分
text = text.replace("nav_square:'交易广场'", "nav_square:'QuantTalk'")
text = text.replace("sq_title:'交易广场'", "sq_title:'QuantTalk'")
text = text.replace("sq_subtitle:'分享观点，发现市场情绪，与全球交易者同频'",
                    "sq_subtitle:'分享观点，发现市场情绪，与全球交易者同频'")

# 在第一个中文 i18n 块之后添加仲裁引擎的翻译
# 找 sq_subtitle 在中文块中的位置
zh_subtitle = "sq_subtitle:'分享观点，发现市场情绪，与全球交易者同频'"
zh_arb_block = """    // 跨交易所聚合引擎
    nav_arbitrage:'跨交易所聚合引擎', arb_title:'跨交易所聚合引擎', arb_subtitle:'实时监控加密货币交易所价差，AI 自动执行搬砖套利',
    arb_monitored:'监控交易对', arb_active:'活跃套利机会', arb_profit_24h:'24h 套利收益', arb_executed:'已执行套利',
    arb_exchanges:'交易所连接状态', arb_refresh:'🔄 刷新',
    arb_opportunities:'实时套利机会', arb_th_pair:'交易对', arb_th_buy:'买入所', arb_th_sell:'卖出所',
    arb_th_spread:'价差', arb_th_profit:'预期盈利', arb_th_action:'操作', arb_exec_btn:'执行',
    arb_history:'套利执行历史', arb_history_empty:'暂无历史记录'"""

if zh_subtitle in text:
    text = text.replace(zh_subtitle, zh_subtitle + ',\n' + zh_arb_block)
    print("✅ 中文 i18n 已添加")
else:
    print("⚠️ 中文 sq_subtitle 未找到")
    # 试试找其他格式
    for i, line in enumerate(text.split('\n')):
        if 'sq_subtitle' in line and ('分享' in line or '观点' in line):
            print(f'Line {i}: {repr(line)}')

# 也替换尾部页面中的中文
text = text.replace('<span data-i18n="sq_title">娣樺瓨鍙ラ崼妤呯潐闃佸獎瀵?span>', '<span data-i18n="sq_title">QuantTalk</span>')
text = text.replace('<span data-i18n="sq_title">濞存嚎鍊栧Σ妤呯嵁閸?span>', '<span data-i18n="sq_title">QuantTalk</span>')

# 写入回 GB18030
with open(filepath, 'w', encoding='gb18030', errors='surrogateescape') as f:
    f.write(text)

# 验证
with open(filepath, 'r', encoding='gb18030', errors='surrogateescape') as f:
    text2 = f.read()

n = text2.count('QuantTalk')
a = text2.count('nav_arbitrage')
print(f"✅ QuantTalk 出现 {n} 次，nav_arbitrage 出现 {a} 次")
