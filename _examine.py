# -*- coding: utf-8 -*-
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# #1 是中文部分，看其前后边界
target = b"nav_square:'"
idx = raw.find(target)  # first one is Chinese

# 从这个位置往前找 "//" 或换行
start = idx
while start > 0:
    if raw[start-1:start+1] == b'\n//' or (start > idx - 200 and raw[start:start+2] == b'//'):
        break
    start -= 1

# 往后到下一个 // 或 nav_ 开头
end = idx + 200
while end < min(idx + 5000, len(raw)):
    if raw[end:end+2] == b'//' or raw[end:end+4] == b'nav_':
        break
    end += 1

print(f"Chinese block: offset {start} to {end}")
context = raw[max(0,start-50):min(len(raw),end+50)]
print(f"Block bytes ({len(context)}):")
print(context[:500])
print("...")
print()

# 用 gb18030 解码整个块
try:
    block_text = raw[start:end].decode('gb18030', errors='replace')
    print("GB18030 decode:")
    print(block_text[:500])
except:
    print("GB18030 decode failed")

# 看 HTML 中的页面内容 - 找到 page-square 的中文
target_page = b'<div class="page" id="page-square">'
idx_page = raw.find(target_page)
if idx_page >= 0:
    html_block = raw[idx_page:idx_page+500].decode('utf-8', errors='replace')
    print("HTML page-square:")
    print(html_block[:300])
