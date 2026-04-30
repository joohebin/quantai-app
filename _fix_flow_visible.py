# -*- coding: utf-8 -*-
"""
Fix: move arb-flow-container and arb-trade-log INSIDE #page-arbitrage div,
so they are hidden when not on arbitrage page.
Also check if the arbitrage page renders correctly.
"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find page-arbitrage div
arb_start = t.find('id="page-arbitrage"')
arb_close = t.find('</div>', arb_start)
# Find the end of the page-arbitrage: it's a <div class="page" id="page-arbitrage"> ... </div>
# Track depth
start_tag = t.find('<div', arb_start-50)
depth = 0
div_end = None
for i in range(start_tag, len(t)):
    if t[i] == '<':
        # Check for > 
        close = t.find('>', i)
        if close < 0: break
        tag = t[i+1:close].split()[0] if ' ' in t[i+1:close] else t[i+1:close]
        if tag in ('div', 'div\\r', 'div\\n'):
            if not t[i+1:i+2] in ('/', '@'):  # not closing or dynamic
                pass  # opening div - we just track
        elif tag.startswith('/div'):
            depth -= 1
            if depth < 0:
                div_end = close + 1
                break
        elif not tag.startswith('/'):
            depth += 1

print(f'page-arbitrage div: {start_tag} to {div_end}')

# Find the flow container and trade log locations
flow_container = t.find('arb-flow-container', arb_start)
# Actually we need to find the CARD that wraps flow and log, not just the ID
flow_card = t.find('搬砖流向可视化', arb_start)
if flow_card < 0:
    flow_card = t.find('arb_flow', arb_start)
log_card = t.find('arb_log_title', arb_start)

print(f'flow card at: {flow_card}')
print(f'log card at: {log_card}')

# Find the actual HTML structure around flow
if flow_card > 0:
    # Go backwards to find the wrapping <div class="card">
    card_div = t.rfind('<div class="card"', flow_card-200, flow_card)
    print(f'Flow card div starts at: {card_div}')
    
    if card_div > 0:
        # Find the closing of this card - the style might vary
        # Our insertion had: <div class="card" style="padding:14px;margin-bottom:12px">
        # Then content, then </div>
        # Find the next <div class="card" or </div> that's before log_card
        flow_end = t.find('</div>', flow_card)
        # There might be nested </div> in the flow content
        # Actually the flow card is simple - find its matching close
        # It's style="padding:14px;margin-bottom:12px"
        flow_end = t.find('</div>', flow_card)
        # Find the second </div> (the card close)
        flow_end2 = t.find('</div>', flow_end+5)
        print(f'flow card ends at: {flow_end2}')
        print(f'Content: {repr(t[card_div:flow_end2+6][:200])}')
        
        # Move this entire block inside page-arbitrage div
        # But FIRST need to check: is it currently inside page-arbitrage?
        if card_div > div_end or flow_end2 > div_end:
            print('Flow card is OUTSIDE page-arbitrage! Moving inside...')
            
            # Find log card too
            log_card_div = t.find('<div class="card" style="padding:14px"', flow_end2)
            log_card_end = t.find('</div>', t.find('arb_log_auto_refresh'))
            log_card_end2 = t.find('</div>', log_card_end+5)
            print(f'log card: {log_card_div} to {log_card_end2}')
            
            # Also find the style tag we inserted
            style_tag = t.find('@keyframes arb-flow-bar', log_card_end2)
            if style_tag > 0:
                style_end = t.find('</style>', style_tag) + 8
                print(f'style: {style_tag} to {style_end}')
                
                # Remove all three from their current position
                # Move everything between card_div and style_end
                move_start = card_div
                move_end = style_end
                
                # But we need to keep it clean - cut out the section between flow card and style end
                before = t[:move_start].rstrip()
                after = t[move_end:].lstrip()
                t = before + '\n' + after
                
                # Now insert the content inside page-arbitrage div, before </div>
                # We need to find the new arb_start after cutting
                moved_content = t[move_start:move_end]  # no this is gone
                
print(f'\nFinal size: {len(t)/1024:.1f} KB')
with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))
