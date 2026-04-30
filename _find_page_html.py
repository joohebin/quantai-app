import sys
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Find the quanttalk HTML area - search for page-square in body
idx = t.find('id="page-square"')
if idx < 0:
    idx = t.find("id='page-square'")
if idx > 0:
    print(f'page-square HTML at: {idx}')
    # Find the matching </div>
    depth = 0
    i = t.find('<div', idx)
    j = t.find('</div>', idx)
    div_count = 0
    pos = idx
    while True:
        next_div = t.find('<div', pos + 1)
        next_close = t.find('</div>', pos + 1)
        if next_close < 0:
            break
        if next_div > 0 and next_div < next_close:
            div_count += 1
            pos = next_div + 1
        else:
            div_count -= 1
            pos = next_close + 6
            if div_count == 0:
                end_pos = pos
                break
    safe = t[idx:end_pos].encode('ascii', errors='replace').decode('ascii')
    print(f'Full page-square HTML ({end_pos - idx} bytes):')
    print(safe)
