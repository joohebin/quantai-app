"""Find exact HTML positions for input bars"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# CS Widget: find the exact closing div for the input section
# The textarea is at 735941, and its containing structure is:
# <div class="cs-input-wrap"> (or similar)
#   <textarea id="cs-input" ...
#   <button id="cs-send" ...
# </div>

print('=== CS Widget Input Section ===')
ta = t.rfind('<textarea', 735000, 736000)
print(f'textarea at: {ta}')
print(t[ta:ta+200])
print()

# Go back to find the wrapper div start
start = t.rfind('<div', 0, ta)
# Go backwards until we find a div that contains both textarea and the send button
# The wrapper likely has a class like "cs-input-wrap" or just "<div ...>"
# Try going back a reasonable amount
candidates = []
pos = ta
while True:
    pos = t.rfind('<div', 0, pos)
    if pos < 0 or pos < ta - 300:
        break
    candidates.append(pos)
print(f'Candidate wrapper divs: {candidates[:5]}')

# Check each candidate - the right one contains both textarea and button
btn_pos = t.find('cs-send', ta, ta+200)
print(f'send button near: {btn_pos}')
btn_start = t.rfind('<button', 0, btn_pos)
print(f'button at: {btn_start}')
print(t[btn_start:btn_start+100])

# Find the actual wrapper - just go back from textarea until we find a div that contains BOTH
for cp in candidates:
    snippet = t[cp:ta+300]
    if '<textarea' in snippet and '<button' in snippet:
        print(f'\nMost likely wrapper starts at: {cp}')
        # Find its closing tag
        opens = snippet.count('<div')
        closes = snippet.count('</div>')
        print(f'  opens: {opens}, closes: {closes}')
        # Close tags
        end_pos = ta + 300
        while opens > closes:
            next_close = t.find('</div>', end_pos)
            if next_close < 0: break
            end_pos = next_close + 6
            closes += 1
        print(f'  section: {safe(t[max(0,cp-20):end_pos])}')
        break

def safe(s):
    return s.encode('utf-8', errors='replace').decode('utf-8', errors='replace')

# QuantTalk input - directly find
print('\n\n=== QuantTalk Input Section ===')
sq = t.find('<input id="sq-input"')
print(f'sq-input at: {sq}')
print(safe(t[sq:sq+300]))
