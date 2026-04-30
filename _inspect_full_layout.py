import sys
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Find the middle/right panel structure
idx = t.find('widget-tv')
end = t.find('</div>', idx + 200)
while t[end:end+6] != '</div>' and end - idx < 3000:
    end = t.find('</div>', end + 6)
safe = t[idx:end+6].encode('ascii', errors='replace').decode('ascii')
print('Widget-TV to end of div:')
print(safe)

# Find the right panel (viewpoint square)
idx2 = t.find('观点广场')
if idx2 > 0:
    print(f'\n\n观点广场 at {idx2}')
    # Find the right panel structure
    rstart = max(0, idx2 - 300)
    rend = min(len(t), idx2 + 1500)
    safe2 = t[rstart:rend].encode('ascii', errors='replace').decode('ascii')
    print(safe2)

# Also find the end of page-square
idx3 = t.find('page-square')
if idx3 > 0:
    pstart = idx3 - 100
    # Find the closing </div> of page-square
    # Look for the outermost </div>
    depth = 0
    i = t.find('<div', idx3)
    j = t.find('</div>', idx3)
    # Simple approach: find all div nesting
    total_divs = 0
    i = idx3
    while True:
        op = t.find('<div ', i)
        cl = t.find('</div>', i)
        if cl < 0:
            break
        if op < cl and op > 0:
            total_divs += 1
            i = op + 5
        else:
            total_divs -= 1
            i = cl + 6
            if total_divs == 0:
                break
    safe3 = t[idx3-100:i].encode('ascii', errors='replace').decode('ascii')
    print(f'\n\nPage-square ends at {i}:')
    print('...' + safe3[-200:])
