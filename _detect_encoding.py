# -*- coding: utf-8 -*-
"""确定文件实际编码"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# 检查 charset
import re
head = raw[:5000].decode('utf-8', errors='replace')
cm = re.search(r'charset=([^\s"\'>]+)', head)
print(f"声明的 charset: {cm.group(1) if cm else '未找到'}")

# 检查 BOM
print(f"BOM: {raw[:4].hex()}")

# 检查常见中文字符的编码模式
# 取一段中文区域
chunks_to_test = [
    ('导航菜单区域', 49000, 1000),
    ('i18n 中文区域', 252000, 2000),
    ('i18n 英文区域', 284000, 2000),
]

for name, start, length in chunks_to_test:
    chunk = raw[start:start+length]
    # 尝试 UTF-8 解码
    try:
        utf8_decoded = chunk.decode('utf-8')
        utf8_ok = True
    except:
        utf8_ok = False
    
    # 尝试 GBK 解码
    try:
        gbk_decoded = chunk.decode('gbk')
        gbk_ok = True
    except:
        gbk_ok = False
    
    print(f"{name} ({start}): UTF-8={'OK' if utf8_ok else 'FAIL'}, GBK={'OK' if gbk_ok else 'FAIL'}")

# 检查关键中文字符区域——导航菜单
nav_start = raw.find(b'<nav>')
nav_chunk = raw[nav_start:nav_start+2000]
try:
    nav_utf8 = nav_chunk.decode('utf-8')
    print(f"\n导航区域 UTF-8 解码成功: {len(nav_utf8)} 字符")
    # 检查中文字符
    cn_chars = sum(1 for c in nav_utf8 if ord(c) > 127)
    print(f"  中文字符数: {cn_chars}")
except Exception as e:
    print(f"\n导航区域 UTF-8 解码失败: {e}")
    try:
        nav_gbk = nav_chunk.decode('gbk')
        print(f"  GBK 解码成功: {len(nav_gbk)} 字符")
    except:
        print(f"  GBK 也失败")

# 找到真正的中文字符位置
print("\n寻找中文文本区域...")
found_zh = False
for i in range(48000, 52000):
    if raw[i] >= 0xE0:
        # 可能是 UTF-8 中文字符起始
        if i+2 < len(raw):
            try:
                pair = raw[i:i+3].decode('utf-8')
                if ord(pair) > 127:
                    context = raw[max(48000,i-10):min(i+100,len(raw))].decode('utf-8', errors='replace')
                    print(f"UTF-8 中文在 {i}: ...{context[:60]}...")
                    found_zh = True
                    break
            except:
                pass

if not found_zh:
    print("在 48000-52000 未找到 UTF-8 中文")
