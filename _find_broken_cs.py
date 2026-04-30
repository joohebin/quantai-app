# -*- coding: utf-8 -*-
"""Fix corrupted CS Widget HTML - restore missing cs-fab + cs-panel + cs-head containers"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find the broken area
broken = t.find('<!-- 悬浮按钮 -->')
print(f'Broken at: {broken}')
print(f'Context: {repr(t[broken:broken+300])}')

if broken > 0:
    # The original structure should be:
    # <!-- 悬浮按钮 -->
    # <button id="cs-fab" ...>💬<span class="cs-badge" id="cs-badge">1</span></button>
    # 
    # <!-- 聊天面板 -->
    # <div id="cs-panel">
    #   <div id="cs-head">
    #     <div class="cs-av">🤖</div>
    #     <div class="cs-info">
    #       <div class="cs-name">QuantAI 客服助手</div>
    #       <div class="cs-status" id="cs-status-txt">在线 · AI 自动回复</div>
    #     </div>
    #     <button class="cs-close" onclick="toggleCS()" title="关闭">✕</button>
    #   </div>
    #   <div id="cs-msgs"></div>
    #   <div id="cs-quickq">...</div>
    #   <div id="cs-foot">...</div>
    # </div>

    # Also need to handle the CSS #cs-fab still being in the page (it's styling for the removed FAB)
    # But we don't want the button to float - CSS is still there though, which is fine
    
    # Let's rebuild the structure
    # First let me see exactly what we have
    after_broken = t[broken:]
    print(f'\nFull broken block ({len(after_broken)} chars):')
    end_cs = t.find('</script>', broken)
    next_script = t.find('<script', broken+1)
    print(f'Next script at: {next_script}')
    # Show the broken structure
    print(repr(t[broken:next_script][:2000]))

# Let me check what came BEFORE the broken area
# The style block closed with </style>, then we have the broken HTML
style_close = t.rfind('</style>', 0, broken)
print(f'\nStyle closes at: {style_close}')
print(f'After style: {repr(t[style_close:broken+1])}')
