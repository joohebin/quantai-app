# -*- coding: utf-8 -*-
"""从 Git 恢复原始 index.html，再从备份恢复，重新应用修改"""
import subprocess

repo_dir = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app'

# 获取第一个 commit 中的 index.html
result = subprocess.run(
    ['git', 'show', '790b469:index.html'],
    capture_output=True,
    cwd=repo_dir
)
if result.returncode == 0:
    raw = result.stdout
    print(f"Git 初始 index.html: {len(raw)/1024:.1f} KB")
    
    # 保存
    with open(f'{repo_dir}/index.html', 'wb') as f:
        f.write(raw)
    print("已恢复为 Git 初始版本")
else:
    print(f"Git 提取失败: {result.stderr.decode('utf-8', errors='replace')}")
    exit(1)

# 验证
with open(f'{repo_dir}/index.html', 'rb') as f:
    raw = f.read()

needle = '交易广场'.encode('utf-8')
if needle in raw:
    print("✅ 文件中含有 交易广场 (UTF-8)")
else:
    print("❌ 没有 交易广场")
    # 检查编码
    needle_gbk = '交易广场'.encode('gbk')
    if needle_gbk in raw:
        print("⚠️ 但是有 GBK 编码的交易广场")
    else:
        # 看头几行
        head = raw[:2000]
        print(f"前2000字节: {head.decode('utf-8', errors='replace')[:200]}")

# 检查 meta charset
import re
try:
    head_text = raw[:5000].decode('utf-8')
    cm = re.search(r'charset=([^\s\"\'/>]+)', head_text)
    print(f"charset: {cm.group(1) if cm else '默认 UTF-8'}")
except:
    print("不能 UTF-8 解码头部")
