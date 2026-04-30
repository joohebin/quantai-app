# -*- coding: utf-8 -*-
"""
Pull original index.html from GitHub, then re-apply our changes cleanly
"""
import os, re, urllib.request

filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
backup_path = filepath + '.bak2'

# Backup current corrupted file
if os.path.exists(filepath):
    os.rename(filepath, backup_path)
    print(f"已备份损坏文件: {backup_path}")

# Download original from GitHub
url = 'https://raw.githubusercontent.com/joohebin220/quantai-app/main/index.html'
print(f"从 GitHub 下载原始文件: {url}")
try:
    with urllib.request.urlopen(url, timeout=30) as response:
        raw = response.read()
    print(f"下载成功: {len(raw)/1024:.1f} KB")
except Exception as e:
    print(f"下载失败: {e}")
    print("尝试从备份还原...")
    if os.path.exists(backup_path):
        os.rename(backup_path, filepath)
    exit(1)

# 确认编码
print(f"文件前30字节: {raw[:30]}")
# 检测 UTF-8
try:
    test = raw.decode('utf-8')
    print("UTF-8 编码: OK")
except:
    print("不是 UTF-8 编码")

# 搜索关键标记（用 UTF-8 编码的字符串）
markers = [
    (b'\xe4\xba\xa4\xe6\x98\x93\xe5\xb9\xbf\xe5\x9c\xba', '交易广场'),
    (b'QuantTalk', 'QuantTalk'),
    (b'nav_square', 'nav_square'),
    (b'Trading Square', 'Trading Square'),
]
for marker, name in markers:
    idx = raw.find(marker)
    if idx >= 0:
        ctx = raw[max(0,idx-10):idx+len(marker)+50]
        try:
            decoded = ctx.decode('utf-8', errors='replace')
            print(f"找到 '{name}' 在 {idx}: {decoded[:80]}")
        except:
            print(f"找到 '{name}' 在 {idx}")

# 保存原始
with open(filepath, 'wb') as f:
    f.write(raw)
print(f"\n原始文件已保存: {len(raw)/1024:.1f} KB")
print("\n现在需要重新应用修改：")
print("1. 交易广场 → QuantTalk")
print("2. 新增 跨交易所聚合引擎 页面 + 菜单")
print("3. 添加中文 + 英文 i18n 定义")
print("4. 添加 arb_online/lag/offline 等 i18n")
