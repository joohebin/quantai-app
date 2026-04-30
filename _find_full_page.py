import sys
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Get the full page-square block from id to the next .page div
idx = t.find('id="page-square"')
if idx > 0:
    # Find where page-square ends by looking for '<!--' which separates pages
    next_page = t.find('id="page-', idx + 100)
    # But this might be inside the same page. Better: find the closing div
    # A simpler approach - just dump from page-square to next page
    next_elem = t.find('<div class="page" id="page-', idx + 50)
    if next_elem > idx:
        safe = t[idx:next_elem].encode('ascii', errors='replace').decode('ascii')
        print(f'Content from page-square to next page ({next_elem - idx} bytes):')
        print(safe)
