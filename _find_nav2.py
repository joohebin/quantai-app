"""Find sidebar nav items in index.html"""
import re

with open('index.html', 'rb') as f:
    data = f.read()

# Find <nav> tag
idx = data.find(b'<nav')
if idx < 0:
    idx = data.find(b'<nav ')
if idx < 0:
    print("No <nav> found")
    exit()

# Get nav block
block = data[idx:idx+5000]

# Find each nav-item
pos = 0
while True:
    start = block.find(b'class="nav-item"', pos)
    if start < 0:
        start = block.find(b"class='nav-item'", pos)
    if start < 0:
        break
    # Find the <li> start
    li_start = block.rfind(b'<li', start-50, start)
    if li_start < 0:
        li_start = start
    # Find the </li> end
    li_end = block.find(b'</li>', start)
    if li_end < 0:
        break
    item = block[li_start:li_end+5]
    # Extract raw bytes for icon and text
    print(f"--- Item at offset {idx+li_start} ---")
    
    # Decode what we can
    try:
        text = item.decode('utf-8')
        print(text[:300])
    except:
        text = item.decode('utf-8', errors='replace')
        print(text[:300])
    
    pos = li_end
    break  # just first few
