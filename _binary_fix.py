# -*- coding: utf-8 -*-
"""
二进制级别直接修复 index.html
1. 导航菜单: 交易广场 -> QuantTalk
2. data-i18n="nav_square">交易广场 -> QuantTalk
3. data-i18n="sq_title">交易广场 -> QuantTalk
4. 添加 跨交易所聚合引擎 菜单项 + 页面内容（纯二进制操作）
"""
import re

filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'

# 首先备份
with open(filepath, 'rb') as f:
    raw = f.read()

# ===== 修复1: 导航菜单中的 "交易广场" -> "QuantTalk" =====
# data-i18n="nav_square">后面接的是 gbk 编码的 "交易广场"
# 对应 UTF-8: \xe4\xba\xa4\xe6\x98\x93\xe5\xb9\xbf\xe5\x9c\xba
target_nav = b'data-i18n="nav_square">\xe4\xba\xa4\xe6\x98\x93\xe5\xb9\xbf\xe5\x9c\xba'
repl_nav = b'data-i18n="nav_square">QuantTalk'
raw = raw.replace(target_nav, repl_nav)

# ===== 修复2: 页面标题中的 "交易广场" -> "QuantTalk" =====
target_title = b'<span data-i18n="sq_title">\xe4\xba\xa4\xe6\x98\x93\xe5\xb9\xbf\xe5\x9c\xba'
repl_title = b'<span data-i18n="sq_title">QuantTalk'
raw = raw.replace(target_title, repl_title)

# ===== 修复3: 替换 i18n 定义中的 "交易广场" =====
# 在 i18n 定义中（GBK区域）
# "交易广场" GBK: bd bb d2 d7 b9 e3 b3 a1
target_gbk = b"nav_square:'\xbd\xbb\xd2\xd7\xb9\xe3\xb3\xa1'"
repl_gbk = b"nav_square:'QuantTalk'"
raw = raw.replace(target_gbk, repl_gbk)

target_sq_gbk = b"sq_title:'\xbd\xbb\xd2\xd7\xb9\xe3\xb3\xa1'"
repl_sq_gbk = b"sq_title:'QuantTalk'"
raw = raw.replace(target_sq_gbk, repl_sq_gbk)

# ===== 修复4: 修复被损坏的仲裁引擎菜单文字 =====
# nav_arbitrage 后面的文字被搞坏了，用正确的 UTF-8 替换
# 找到 nav_arbitrage"> 之后到 </span> 之间的内容替换
nav_arb_data = b'data-i18n="nav_arbitrage">'
idx = raw.find(nav_arb_data)
if idx >= 0:
    span_end = raw.find(b'</span>', idx)
    if span_end >= 0:
        old_content = raw[idx+len(nav_arb_data):span_end]
        correct = '\u8de8\u4ea4\u6613\u6240\u805a\u5408\u5f15\u64ce'.encode('utf-8')  # 跨交易所聚合引擎
        new_content = b'data-i18n="nav_arbitrage">' + correct
        old_tag = raw[idx:span_end]
        raw = raw.replace(old_tag, new_content)
        print(f"修复导航菜单仲裁引擎文字: {len(old_content)} bytes -> {len(correct)} bytes")
    else:
        print("未找到 </span>")
else:
    print("未找到 nav_arbitrage 菜单")

# ===== 修复5: 修复仲裁引擎页面中的乱码 =====
# 找到 page-arbitrage 区域，用 gbk 读出文本并修复中文
page_start = raw.find(b'page-arbitrage" style="display:none">')
page_end = raw.find(b'<!-- =====', page_start)
if page_end < 0:
    page_end = raw.find(b'<div class="page" id="page-', page_start+20)
if page_end < 0:
    page_end = page_start + 7000

if page_start >= 0:
    section = raw[page_start:page_end]
    print(f"仲裁页面: {page_start} 到 {page_end} ({page_end-page_start} bytes)")
    
    # 用 gbk 解码修复中文字符
    try:
        decoded = section.decode('gbk', errors='replace')
        # 修复常见乱码映射
        # "鐠恒劋姘﹂弰鎾村�嶉懕姘�鎮庡��鏇熸惛" 应该是 "跨交易所聚合引擎"
        # 但解码后的文本混杂了乱码和可读的部分
        # 替换整个 section 为正确 UTF-8 的中文
        new_section_utf8 = b''
        i = 0
        while i < len(section):
            try:
                # 检查是否是 ASCII
                if section[i] < 0x80:
                    new_section_utf8 += bytes([section[i]])
                    i += 1
                    continue
                # 尝试 UTF-8 解码单个字符
                if section[i] & 0xE0 == 0xC0:
                    c = section[i:i+2].decode('utf-8')
                    new_section_utf8 += c.encode('utf-8')
                    i += 2
                    continue
                elif section[i] & 0xF0 == 0xE0:
                    c = section[i:i+3].decode('utf-8')
                    new_section_utf8 += c.encode('utf-8')
                    i += 3
                    continue
                else:
                    # 非 UTF-8 字节（GBK），跳过
                    new_section_utf8 += b'?'
                    i += 1
            except:
                # 解码失败，可能是 GBK
                try:
                    gbk_bytes = section[i:i+2]
                    if len(gbk_bytes) == 2:
                        c = gbk_bytes.decode('gbk')
                        new_section_utf8 += c.encode('utf-8')
                        i += 2
                    else:
                        new_section_utf8 += b'?'
                        i += 1
                except:
                    new_section_utf8 += b'?'
                    i += 1
        
        # 替换原始 section
        raw = raw[:page_start] + new_section_utf8 + raw[page_end:]
        print(f"修复仲裁页面编码, 新长度: {len(new_section_utf8)}")
        
    except Exception as e:
        print(f"解码失败: {e}")

# ===== 修复6: 添加 i18n 中文定义 =====  
# i18n 中文定义部分应该是 GBK 编码，我们直接用 GBK 字节写入
# 找到中文 zh i18n 区域最后
zh_block_start = raw.find(b"nav_square:'QuantTalk', sq_title:'QuantTalk'")
if zh_block_start >= 0:
    # 找到中文块的结束（下一个 // 注释）
    next_comment = raw.find(b'\n    //', zh_block_start + 50)
    if next_comment < 0:
        next_comment = raw.find(b'\n    nav_stratmarket', zh_block_start + 50)
    
    if next_comment > zh_block_start:
        arb_i18n_gbk = """
    // 跨交易所聚合引擎
    nav_arbitrage:'跨交易所聚合引擎', arb_title:'跨交易所聚合引擎', arb_subtitle:'实时监控加密货币交易所价差，AI 自动执行搬砖套利',
    arb_monitored:'监控交易对', arb_active:'活跃套利机会', arb_profit_24h:'24h 套利收益', arb_executed:'已执行套利',
    arb_exchanges:'交易所连接状态', arb_refresh:'刷新',
    arb_opportunities:'实时套利机会', arb_th_pair:'交易对', arb_th_buy:'买入所', arb_th_sell:'卖出所',
    arb_th_spread:'价差', arb_th_profit:'预期盈利', arb_th_action:'操作', arb_exec_btn:'执行',
    arb_history:'套利执行历史', arb_history_empty:'暂无历史记录',
""".encode('gbk', errors='replace')
        raw = raw[:next_comment] + arb_i18n_gbk + raw[next_comment:]
        print(f"添加仲裁引擎 i18n GBK 定义 ({len(arb_i18n_gbk)} bytes)")
    else:
        print("未找到中文 i18n 插入点")

# ===== 写入 =====
with open(filepath, 'wb') as f:
    f.write(raw)

print("\n文件写入完成！")

# ===== 验证 =====
import io
with open(filepath, 'rb') as f:
    raw2 = f.read()
# 用 UTF-8 解码 HTML 部分（导航菜单验证）
text_utf8 = raw2.decode('utf-8', errors='replace')
print(f"\n最终验证:")
print(f"  QuantTalk 出现: {text_utf8.count('QuantTalk')} 次")
print(f"  nav_arbitrage 出现: {text_utf8.count('nav_arbitrage')} 次")
print(f"  square nav: {'QuantTalk' in text_utf8[text_utf8.find('showPage'):text_utf8.find('showPage', 1000)]}")

# 验证仲裁引擎菜单
nav_idx = text_utf8.find("nav_arbitrage")
if nav_idx >= 0:
    ctx = text_utf8[nav_idx-30:nav_idx+60]
    print(f"  nav_arbitrage 菜单: ...{ctx[:60]}...")

# 验证仲裁引擎页面
arb_page = text_utf8.find("page-arbitrage")
if arb_page >= 0:
    ctx = text_utf8[arb_page:arb_page+120]
    print(f"  仲裁引擎页面: {ctx[:120]}")

# 验证英文 i18n (也修复一下)
en_check = text_utf8.find("nav_square:'Trading Square'")
if en_check >= 0:
    print(f"  ⚠️ 英文 i18n 仍有 Trading Square: {text_utf8[en_check:en_check+80]}")
else:
    print(f"  英文 i18n 已正确: QuantTalk 替换完成")
