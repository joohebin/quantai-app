# -*- coding: utf-8 -*-
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# 找 page-arbitrage 并看原始字节
idx = raw.find(b'page-arbitrage')
if idx >= 0:
    print(f"page-arbitrage 在偏移 {idx}")
    # 看看前后字节，确认编码
    chunk = raw[max(0,idx-20):idx+100]
    print(f"原始字节: {chunk}")
    print(f"字节长度: {len(chunk)}")
    
    # 工具：尝试多种解码
    for enc in ['utf-8', 'gbk', 'gb18030', 'gb2312']:
        try:
            decoded = chunk.decode(enc)
            print(f"\n{enc} 解码: {repr(decoded)}")
        except:
            print(f"{enc}: 解码失败")
else:
    print("page-arbitrage 未找到！")
    
    # 检查原来的插入位置
    square = raw.find(b'id="page-square"')
    strat = raw.find(b'id="page-stratmarket"')
    if square >= 0 and strat >= 0:
        print(f"page-square: {square}, page-stratmarket: {strat}")
        gap = strat - square
        print(f"间距: {gap} 字节")
        # 看 page-square 和 stratmarket 之间的内容
        between = raw[square:strat]
        print(f"内容({len(between)} 字节):")
        print(between[:500])
