# -*- coding: utf-8 -*-
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

idx = raw.find(b'page-arbitrage')
start = idx
end = raw.find(b'<div class="page"', idx+20)
if end < 0:
    end = raw.find(b'<!-- =====', idx+20)
if end < 0:
    # 找下一个 page-
    end = raw.find(b'id="page-', idx+30)
if end < 0:
    end = idx + 3000

print(f"page-arbitrage: {start} to {end} ({end-start} bytes)")
section = raw[start:end]

# 写到一个文件查看字节
with open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\_arb_section.bin', 'wb') as f:
    f.write(section)

# 尝试用 gbk 解码并比较
try:
    decoded = section.decode('gbk', errors='replace')
    print("GBK 解码:")
    print(decoded[:500])
except:
    pass

# 看看是否有正确的 "跨交易所聚合引擎" UTF-8 字节
arb_utf8 = '跨交易所聚合引擎'.encode('utf-8')
print(f"\n跨交易所聚合引擎 UTF-8: {arb_utf8.hex()}")
idx2 = raw.find(arb_utf8)
print(f"UTF-8 版本在偏移: {idx2}")

# 查看 nav_arbitrage 数据
nav_idx = raw.find(b'nav_arbitrage')
if nav_idx >= 0:
    print(f"\nnav_arbitrage 在偏移 {nav_idx}")
    context = raw[nav_idx-20:nav_idx+100]
    print(f"原始字节: {context}")
    try:
        print(f"UTF-8解码: {context.decode('utf-8', errors='replace')}")
    except:
        pass
