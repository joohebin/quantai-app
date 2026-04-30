# -*- coding: utf-8 -*-
"""
Core fix: Move flow+log INSIDE page-arbitrage div.
The page-arbitrage div currently has barely any content (289 bytes).
The flow+log are outside it at ~132821.
We need to:
1. Cut the flow+log+style block from its current position 
2. Insert it INSIDE page-arbitrage div before </div>
"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# 1. Locate page-arbitrage div
arb_start = t.find('id="page-arbitrage"')
open_tag_start = t.rfind('<div', arb_start-20, arb_start)
open_tag_end = t.find('>', open_tag_start) + 1
# Find close of page-arbitrage div
depth = 1; i = open_tag_end
while depth > 0:
    i = t.find('</', i)
    if i < 0: break
    end_tag_end = t.find('>', i)
    tag_name = t[i+2:end_tag_end].strip()
    if tag_name == 'div':
        depth -= 1
    i = end_tag_end + 1
arb_inner_end = i - 6  # position before </div>
arb_close = i

print(f'page-arbitrage: {open_tag_start} to {arb_close}')
print(f'Inner content ends at: {arb_inner_end}')

# 2. Find the flow card, log card, and style
flow_card = t.find('<!-- 搬砖流向可视化 -->')
print(f'Flow card starts at: {flow_card}')
if flow_card < 0:
    flow_card = t.find('arb-flow-container')
    # Go back to find wrapper div
    flow_wrap = t.rfind('<div', flow_card-300, flow_card)
    print(f'Flow wrapper at: {flow_wrap}')
    print(f'Context: {repr(t[flow_wrap:flow_wrap+80])}')
else:
    flow_wrap = flow_card

# Find where the block ends - after log card style
log_card = t.find('<!-- 交易日志 -->')
style_block = t.find('@keyframes arb-flow-bar')

print(f'Log card: {log_card}')
print(f'Style block: {style_block}')

style_end = t.find('</style>', style_block) + 8
print(f'Style end: {style_end}')

# 3. Cut the flow+log+style block
block_start = flow_wrap
block_end = style_end

print(f'\nBlock to move: {block_start} to {block_end} ({block_end - block_start} bytes)')
print(f'First: {repr(t[block_start:block_start+100])}')
print(f'Last: {repr(t[block_end-50:block_end])}')

# 4. Remove block from current position and insert inside page-arbitrage
# Only if not already inside
if block_start < arb_close and block_end < arb_close:
    print('Block is already inside page-arbitrage - no change needed')
else:
    before = t[:block_start].rstrip()
    after = t[block_end:].lstrip()
    block_content = t[block_start:block_end]
    t = before + '\n\n' + after
    
    # Now insert block inside page-arbitrage
    # Find new arb_inner_end (same offset as before since we removed content after)
    # Actually we removed content that was AFTER arb_close, so arb_inner_end stays same
    # But we need the current arb_inner_end position
    arb_inner_end = before.find('</div>\n', before.rfind('<div', 0, before.find('id="page-arbitrage"')-20))
    # Simpler: find the closing </div> of page-arbitrage
    new_arb_close = before.find('</div>', before.find('id="page-arbitrage"'))
    
    print(f'New arb close at: {new_arb_close}')
    t = t[:new_arb_close] + '\n' + block_content + '\n' + t[new_arb_close:]
    print('Inserted block inside page-arbitrage')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Verify
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')
arb_pos = text.find('id="page-arbitrage"')
flow_pos = text.find('arb-flow-container')
log_pos = text.find('arb-trade-log')
# Check they're inside page div
page_close = None
depth = 1; i = text.find('>', text.find('<div', arb_pos-20)) + 1
while depth > 0:
    i = text.find('</', i)
    if i < 0: break
    e = text.find('>', i)
    if text[i+2:e].strip() == 'div': depth -= 1
    i = e + 1
page_close = i

print(f'\nVerification:')
print(f'page-arbitrage: {arb_pos} to {page_close}')
print(f'arb-flow-container: {flow_pos} (inside: {flow_pos > arb_pos and flow_pos < page_close})')
print(f'arb-trade-log: {log_pos} (inside: {log_pos > arb_pos and log_pos < page_close})')
print(f'File: {len(data)/1024:.1f} KB')
