import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 问题：所有 onclick 里用 \\'' + var + '\\' 拼接单引号，正确写法应该是 onclick="fn('${var}')"
# 
# 修复策略：找到包含这个模式的行，把 ' + var + ' 前后的 \\\\ 引号改为 \\x27（单引号HTML实体或JS转义）
# 
# 实际上正确的 JS 字符串拼接 onclick 写法：
# '<button onclick="fn(\\'' + id + '\\')">' 
# 这里 \\' 是 JS 字符串转义序列，在字符串求值后得到 '
# 但只有一个 \\ 才是转义！两个 \\\\ 得到字面 \，然后 '' 结束字符串！
#
# 所以11处代码里的 \\\\ 都是多了一个 \
# 原来: onclick="fn(\\\\'' + id + '\\\\')"  (文件里: onclick="fn(\\'' + id + '\\')")  -> 错误
# 正确: onclick="fn(\\'' + id + '\\'"  (文件里: onclick="fn(\'' + id + '\')") -> 对
#
# 但我们用模板字符串最简单：
# 原来: '..onclick="fn(\\'' + id + '\\')"'  
# 改为: `..onclick="fn('${id}')"`
#
# 但这需要把整行字符串拼接都改为模板，范围可能跨多行。
# 
# 最简单可靠：把 (\\'' 替换为 ('  ,  '\\') 替换为 ')
# 即: \\\\'' -> (  ,  '\\\\' -> '
# 但要注意上下文避免误替换
#
# 实际做法：用正则，把 "fn(\\\\'" + varname + "'\\\\') 替换为 "fn(\\'${varname}\\')"
# 
# 我们来做这个替换：
# Pattern in file: "fn(\\\\''" + space + + space + var + space + + space + "'\\\\')"
# 替换为: "fn(\\'" + var + "\\')"  即在字符串里用正确的转义
#
# 但实际上我们想要最终字符串是 fn('xxx')，用 \\x27 更保险
#
# ===== 实际修复 =====
# 把 \\\\'' 模式改为单引号，并确保引号正确

# Step 1: 找到每一处 \\\\'  ... \\\\' 模式（在JS字符串拼接中）
# 文件中的字面字符序列: \\'  和  \\'  之间夹着 + var +
# 这是11处 onclick 的问题

# 直接字符串替换：把 onclick 里的 \\'' 改为 &apos; (HTML实体单引号)
# 这样生成的HTML就是 onclick="fn(&apos;id&apos;)" 
# 在HTML中 &apos; 就是 ' 所以onclick里的JS会正确得到 fn('id')
# 
# 文件里: onclick="fn(\\'' + id + '\\')"
# Python: content里是: onclick="fn(\\\\'' + id + '\\\\')"
# 
# 用正则替换:
# 把 (\\'' 改为 (&apos;
# 把 '\\') 改为 &apos;)

# 先看实际文件里的字节
idx = content.find("sqLike(\\\\''")
if idx >= 0:
    print('Found pattern, context:', repr(content[idx-10:idx+50]))
else:
    idx = content.find("sqLike(\\\\'")
    if idx >= 0:
        print('Found alt pattern:', repr(content[idx-10:idx+50]))
    else:
        # 找 sqLike
        idx = content.find("sqLike")
        print('sqLike at:', idx)
        if idx >= 0:
            print('Context:', repr(content[idx:idx+80]))

# 读一下L3451的原始内容
lines = content.split('\n')
print('\nL3450-3452:')
for i in range(3448, 3453):
    print(f'  L{i+1}: {repr(lines[i][:160])}')
