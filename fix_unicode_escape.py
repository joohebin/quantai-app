import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复：将字符串里的 \u{XXXXX} 替换为对应的实际 emoji 或 \uXXXX\uXXXX 代理对
# 🥇 U+1F947 -> \uD83E\uDD47
# 🥈 U+1F948 -> \uD83E\uDD48  
# 🥉 U+1F949 -> \uD83E\uDD49
# 但这些是在 JS 字符串里，直接用 emoji 最简单

# 替换 renderLbList 里的 medal 那行
old_medal = r"    const medal = idx === 0 ? '\u{1F947}' : idx === 1 ? '\u{1F948}' : idx === 2 ? '\u{1F949}' : '<span style=\"color:var(--muted);font-size:13px\">#'+(idx+1)+'</span>';"
new_medal = "    const medal = idx === 0 ? '\U0001F947' : idx === 1 ? '\U0001F948' : idx === 2 ? '\U0001F949' : '<span style=\"color:var(--muted);font-size:13px\">#'+(idx+1)+'</span>';"

if old_medal in content:
    content = content.replace(old_medal, new_medal, 1)
    print('Fixed medal line (\\u{} -> emoji)')
else:
    # 尝试不同写法
    import re
    m = re.search(r"const medal = idx === 0 \? '[^']*' : idx === 1", content)
    if m:
        print('Found medal line at:', content[:m.start()].count('\n')+1)
        print('Content:', repr(content[m.start():m.start()+200]))
    else:
        print('Medal line NOT FOUND')
        # 搜索 \u{1F947
        idx = content.find('\\u{1F947}')
        if idx >= 0:
            print(f'Found \\u{{1F947}} at char {idx}, line {content[:idx].count(chr(10))+1}')
            print('Ctx:', repr(content[idx-50:idx+100]))
        else:
            print('Not found with \\u{1F947} either')
            # 在字节里找
            raw = content.encode('utf-8')
            idx2 = raw.find(b'\\u{1F947}')
            print(f'Bytes find: {idx2}')

    # 无论如何，用正则替换所有 \u{XXXXX} 形式的 JS 转义（在字符串里）
    def replace_unicode_escape(m):
        codepoint = int(m.group(1), 16)
        try:
            return chr(codepoint)
        except (ValueError, OverflowError):
            return m.group(0)  # 无法转换就保留
    
    fixed = re.sub(r'\\u\{([0-9A-Fa-f]+)\}', replace_unicode_escape, content)
    if fixed != content:
        content = fixed
        print('Fixed all \\u{...} escapes via regex')
    else:
        print('No \\u{...} found via regex either')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved.')

# 验证修复
with open('index.html', 'r', encoding='utf-8') as f:
    check = f.read()
remaining = re.findall(r'\\u\{[0-9A-Fa-f]+\}', check)
print(f'Remaining \\u{{...}} patterns: {len(remaining)}')
if remaining:
    print('Still has:', remaining[:5])
