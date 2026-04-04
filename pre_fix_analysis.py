import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 最简洁修复：把文件中 \\'' 字节序列（5c5c27 27）替换为 \x27（5c 78 32 37）
# 在JS字符串中:
#   \\'' 解析为: \\ (转义反斜杠->字面\) + '' (空字符串) + ...
#   \x27 解析为: 字符 ' (单引号)   <- 这才是我们想要的
# 
# 但 \x27 会被当作 JS 十六进制转义，在字符串外不同上下文会有不同效果
# 
# ===== 更根本的方法 =====
# 注入时生成了 onclick="fn(\\'' + id + '\\')" 这种字符串拼接
# 实际上在浏览器的 HTML 解析 + JS 解析流程里：
# 1. HTML 解析 onclick 属性：得到字符串 fn(\\'' + id + '\\')"
# 2. 这里的 \\\\ 就是字面的 \\，不是 HTML 实体
# 3. JS 执行时这是字符串拼接，onclick="fn(\\'' + id...  不对，onclick属性直接是JS
# 
# onclick 属性里的内容是直接的 JS 表达式，不是字符串！
# onclick="sqLike(\\'' + p.id + '\\')"
# 这里 p.id 等是 HTML 模板渲染时的变量，不是 JS 运行时变量！！！
# 
# 所以这行代码的目的是：
# list.innerHTML = ... + '<button onclick="sqLike(\\'' + p.id + '\\')">' + ...
# 当 p.id = 'sq1' 时，拼接结果：
# '<button onclick="sqLike(\\'' + p.id + '\\')">' -> 这只是固定字符串，p.id已在JS中求值
# 等等，不对，这是 JS 的 innerHTML 赋值，p.id 是 JS 变量
# 
# 所以整个表达式：
# '<button onclick="sqLike(\\'' + p.id + '\\')">'
# = '<button onclick="sqLike(\\' + p.id + '\')">
# = (当p.id='sq1') '<button onclick="sqLike(\'sq1\')">'
# 
# 这个 HTML 字符串被写到 DOM 里，onclick 里的 \'sq1\' 就是带反斜杠转义的单引号
# 在 HTML onclick 属性里 \' 不是有效的 JS 转义，会被忽略，只留下 sq1
# 实际 onclick 执行的是 sqLike(sq1) 而不是 sqLike('sq1')
# sq1 会被当成变量名，会报 ReferenceError
# 
# 正确写法应该是：
# '<button onclick="sqLike(\'' + p.id + '\')">' 
# 或: '<button onclick="sqLike(&apos;' + p.id + '&apos;)">'
# 或: `<button onclick="sqLike('${p.id}')">` <- 最简单
#
# ====================================================
# 方案：全部11处改用模板字符串，直接包含变量
# ====================================================
# 
# 但函数里的其他字符串拼接也需要一起处理
# 直接重写整个 renderSquare 函数里的 sq 列表部分

# 先找相关函数
def find_and_check_func(name):
    idx = content.find(f'function {name}(')
    if idx < 0:
        print(f'{name}: NOT FOUND')
        return None, None, None
    idx_next = content.find('\nfunction ', idx + 10)
    body = content[idx:idx_next]
    print(f'{name}: found at {idx}, len={len(body)}')
    return idx, idx_next, body

print('Checking functions with \\\\\\' issues:')
find_and_check_func('renderSquare')
find_and_check_func('renderStratMarket')
find_and_check_func('renderLiveSignals')
find_and_check_func('renderBroadcasters')
