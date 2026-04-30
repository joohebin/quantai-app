# -*- coding: utf-8 -*-
"""Add new i18n keys for the redesigned arbitrage page"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'

with open(filepath, 'rb') as f:
    raw = bytearray(f.read())
text = raw.decode('utf-8')

# New keys needed: arb_bind, arb_flow, arb_log_title, arb_log_auto_refresh

# 1. Add to Chinese i18n block (find after arb_history_empty)
# Find Chinese block
zh_needle = "arb_history_empty:'暂无历史记录'"
zh_insert = """    arb_bind:'绑定交易所', arb_flow:'搬砖流向', arb_log_title:'交易日志', arb_log_auto_refresh:'自动刷新中',"""

pos = text.find(zh_needle)
if pos >= 0:
    line_end = text.find('\n', pos)
    text = text[:line_end+1] + '    ' + zh_insert + '\n' + text[line_end+1:]
    print(f"Chinese i18n inserted at {pos}")
else:
    print("Chinese i18n NOT FOUND")
    # Try partial match
    pos = text.find('arb_history_empty')
    if pos >= 0:
        line_end = text.find('\n', pos)
        print(f"Found arb_history_empty at {pos}, line={line_end}")

# 2. Add to English i18n block (find after arb_history_empty:'No history')
en_needle = "arb_history_empty:'No history'"
en_insert = """    arb_bind:'Connect Exchange', arb_flow:'Flow Visualization', arb_log_title:'Execution Log', arb_log_auto_refresh:'Auto-refreshing',"""

pos = text.find(en_needle)
if pos >= 0:
    line_end = text.find('\n', pos)
    text = text[:line_end+1] + '    ' + en_insert + '\n' + text[line_end+1:]
    print(f"English i18n inserted at {pos}")
else:
    print("English i18n NOT FOUND")

# Also update arb_lock_title and arb_lock_desc - move them after arb_offline
old_line = "arb_lock_title:'跨交易所聚合引擎为 Elite 专属功能', arb_lock_desc:'升级到 Elite 计划，解锁AI自动交易能力',"
# Check if this exists and position it properly
# First, let's not break existing lock logic, just update arb subtitle

# Save
output = text.encode('utf-8')
with open(filepath, 'wb') as f:
    f.write(output)

print(f"File: {len(output)/1024:.1f} KB")
print(f"arb_bind CN: {output.count('arb_bind:'.encode() + '绑定交易所'.encode('utf-8'))}")
print(f"arb_bind EN: {output.count('arb_bind:'.encode() + 'Connect Exchange'.encode('utf-8'))}")
print(f"arb_flow: {output.count(b'arb_flow')}")
print(f"arb_log_title: {output.count(b'arb_log_title')}")
