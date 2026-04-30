#!/usr/bin/env python3
import re

with open('index.html', 'rb') as f:
    content = f.read()

# 1. Find the exchanges tab button in HTML (for account page)
print("=== ACCOUNT TAB BUTTONS ===")
pattern = re.compile(rb"switchAccountTab\('[^']+'")
for m in pattern.finditer(content):
    start = max(0, m.start()-100)
    end = min(len(content), m.end()+50)
    text = content[start:end]
    if b'acc-tab' in text or b'class="btn' in text or b'button' in text:
        print(f'Pos {m.start()}: {repr(text)}')

# 2. Find acc-tab buttons specifically
print("\n=== ACC TAB BUTTONS ===")
pattern2 = re.compile(rb"<button[^>]*acc-tab[^>]*>.*?</button>", re.DOTALL)
for m in pattern2.finditer(content):
    print(f'Pos {m.start()}: {repr(m.group()[:200])}')

# 3. Find the exchange tab button specifically  
print("\n=== EXCHANGE TAB BUTTON ===")
exc = content.find(b'\xe4\xba\xa4\xe6\x98\x93\xe6\x89\x80')
# Find nearest <button that looks like exchange tab
start = max(0, exc-500)
end = min(len(content), exc+100)
chunk = content[start:end]
# Find the button tag around this
btn_start = chunk.find(b'acc-tab')
if btn_start >= 0:
    print(f'Found acc-tab at offset {btn_start}')
    print(repr(chunk[btn_start:btn_start+200]))
else:
    print('No acc-tab found nearby')
    # Just print from the area
    print(repr(chunk))

# Find the nearest <button before this
start = max(0, exc-300)
end = min(len(content), exc+50)
print(repr(content[start:end]))
