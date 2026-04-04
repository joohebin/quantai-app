import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 检查 _check.js 文件的原始字节（前100行）
with open('_check.js', 'rb') as f:
    raw = f.read()

# 找 MARKET_DATA 的位置
idx = raw.find(b'MARKET_DATA')
print(f'MARKET_DATA raw position: {idx}')
if idx > 0:
    chunk = raw[idx:idx+500]
    print('Raw bytes (hex):', chunk[:200].hex())
    print()
    # 尝试不同编码
    for enc in ['utf-8', 'utf-8-sig', 'gbk', 'latin-1']:
        try:
            decoded = chunk.decode(enc, errors='replace')
            print(f'{enc}: {decoded[:200]}')
        except Exception as e:
            print(f'{enc}: ERROR {e}')
        print()

# 同时检查 index.html 里的 MARKET_DATA
with open('index.html', 'rb') as f:
    html_raw = f.read()

idx2 = html_raw.find(b'MARKET_DATA')
print(f'\nindex.html MARKET_DATA raw position: {idx2}')
if idx2 > 0:
    chunk2 = html_raw[idx2:idx2+300]
    print('UTF-8 decode:', chunk2.decode('utf-8', errors='replace')[:200])
