# -*- coding: utf-8 -*-
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# 看整个文件的编码模式
# 检查 BOM
print(f"BOM: {raw[:4].hex()}")
print(f"First bytes: {raw[:20]}")

# 找 HTML 中的 "QuantTalk" 和 "跨交易所聚合引擎"
for term in [b'QuantTalk', b'\xe8\xb7\xa8\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80', b'arbitrage', b'nav_arbitrage']:
    idx = raw.find(term)
    if idx >= 0:
        print(f'Found {term} at {idx}')
        # 检查周围字节
        chunk = raw[max(0,idx-30):idx+len(term)+30]
        print(f'  Context: {chunk}')
    else:
        print(f'NOT found: {term}')

# 看 // 注释行和 nav_square 的原始字节
# 找第一个 // 
idx_double_slash = raw.find(b'// ')
print(f'\nFirst "// " at {idx_double_slash}')

# 找中文 "分享" 的各种编码
for enc_name in ['utf-8', 'gbk', 'gb18030', 'big5', 'shift_jis']:
    try:
        data = '\u5206\u4eab'  # 分享
        target = data.encode(enc_name)
        idx = raw.find(target)
        if idx >= 0:
            print(f'分享 ({enc_name}) at {idx}')
    except:
        pass

# 看第一个 nav_square: 附近是否包含可识别的标记
target_nav = b"nav_square:'"
idx = raw.find(target_nav)
if idx >= 0:
    # 看前面30字节有没有 // 注释
    before = raw[max(0,idx-40):idx]
    print(f'\nBefore nav_square#1: {before}')
    # 看后面的内容能否用 GBK 解码
    chunk = raw[idx:idx+100]
    try:
        decoded = chunk.decode('gbk')
        print(f'GBK: {repr(decoded)}')
    except:
        # 逐步修复解码
        result = []
        i = 0
        while i < len(chunk):
            try:
                c = chunk[i:i+1].decode('gbk')
                result.append(c)
                i += 1
            except:
                result.append(f'\\x{chunk[i]:02x}')
                i += 1
        print('Partial GBK:', ''.join(result))

# 确认文件中最常用的中文字符编码
# 取一部分中文字符区域看
for i in range(252000, min(260000, len(raw))):
    if raw[i] >= 0x80 and raw[i+1] >= 0x80:
        pair = raw[i:i+2]
        if i % 100 == 0:
            continue
# 用 chardet 检测
try:
    import chardet
    result = chardet.detect(raw[:100000])
    print(f'\nChardet: {result}')
except:
    print('无 chardet，跳过')
    
# 手动检测 - 取中文区域查看字节分布
sample = raw[252000:260000]
utf8_count = 0
gbk_count = 0
i = 0
while i < len(sample):
    if sample[i] < 0x80:
        i += 1
        continue
    # 尝试 UTF-8 3字节
    if i + 2 < len(sample) and (sample[i] & 0xF0) == 0xE0:
        utf8_count += 1
        i += 3
    # 尝试 UTF-8 2字节
    elif i + 1 < len(sample) and (sample[i] & 0xE0) == 0xC0:
        utf8_count += 1
        i += 2
    # 尝试 GBK 2字节
    elif 0x81 <= sample[i] <= 0xFE and 0x40 <= sample[i+1] <= 0xFE:
        gbk_count += 1
        i += 2
    else:
        i += 1
print(f'\nSample (252000-260000): UTF-8 seqs={utf8_count}, GBK seqs={gbk_count}')
