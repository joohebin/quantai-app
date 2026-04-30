# -*- coding: utf-8 -*-
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# 在原始字节中提取导航菜单
nav_start = raw.find(b'<nav>')
nav_end = raw.find(b'</nav>', nav_start)
nav_bytes = raw[nav_start:nav_end+6]

# 提取每个菜单项（找 showPage → data-i18n → 标签文字）
# 直接解析字节
nav_items = []
pos = 0
while pos < len(nav_bytes):
    # 找 showPage
    p = nav_bytes.find(b"showPage('", pos)
    if p < 0:
        break
    # 提取 page name
    p_end = nav_bytes.find(b"',", p+10)
    page_name = nav_bytes[p+10:p_end].decode('ascii', errors='replace')
    
    # 找 data-i18n=
    d = nav_bytes.find(b'data-i18n="', p_end)
    if d < 0:
        pos = p_end
        continue
    d_end = nav_bytes.find(b'"', d+12)
    i18n_key = nav_bytes[d+12:d_end].decode('ascii', errors='replace')
    
    # 找 > 后到 < 的标签文字
    tag_start = nav_bytes.find(b'>', d_end)
    tag_end = nav_bytes.find(b'<', tag_start+1)
    if tag_end < 0 or tag_end - tag_start > 50:
        # 可能是嵌套标签
        # 找直接 span/text
        tag_start = nav_bytes.find(b'>', tag_start+1)
        tag_end = nav_bytes.find(b'<', tag_start+1)
    
    label = nav_bytes[tag_start+1:tag_end].decode('utf-8', errors='replace').strip()
    nav_items.append((page_name, i18n_key, label[:20]))
    pos = tag_end

print("=== 导航菜单 (二进制解析) ===")
for page, key, label in nav_items:
    print(f"  {page}: [{key}] {label}")

print(f"\n共 {len(nav_items)} 个菜单项")

# 检查新加的页面是否 showPage 支持
js = raw.find(b'function showPage')
if js >= 0:
    # 提取 showPage 函数
    func_end = raw.find(b'function', js+20)
    if func_end < 0:
        func_end = min(len(raw), js + 5000)
    show_func = raw[js:func_end].decode('utf-8', errors='replace')
    if 'arbitrage' in show_func:
        print("\n✅ showPage 支持 arbitrage")
    else:
        print("\n⚠️ showPage 中未找到 arbitrage 处理")

# 检查页面内容
for page_id in ['square', 'arbitrage', 'stratmarket']:
    target = f'id="page-{page_id}"'
    idx = raw.find(target.encode())
    if idx >= 0:
        # 直接用 UTF-8 解码看标题
        end = raw.find(b'<div class="page"', idx+10)
        if end < 0: end = idx + 1000
        section = raw[idx:end].decode('utf-8', errors='replace')
        # 取 data-i18n 和后面的文字
        m = __import__('re').search(r'data-i18n="([^"]+)"[^>]*>([^<]*)<', section)
        if m:
            label = m.group(2).strip()[:30]
            print(f"  页面 {page_id}: [{m.group(1)}] {label}")
