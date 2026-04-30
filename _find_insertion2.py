"""Find the right insertion point for bot page"""
import sys, re
sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)
with open('index.html', 'rb') as f:
    d = f.read().decode('utf-8', errors='replace')

# Find all pages
pages = [m.start() for m in re.finditer(r'id="page-(\w+)"', d)]
print(f'Page IDs ({len(pages)}):')
for p in pages:
    pid = re.search(r'id="page-(\w+)"', d[p:])
    print(f'  {p}: {pid.group(1) if pid else "?"}')

# Find last page
last_pg_name = re.search(r'id="page-(\w+)"', d[pages[-1]:])
print(f'\nLast page: {last_pg_name.group(1) if last_pg_name else "?"}')

# Find where the autoopen page fully ends
idx = pages[-1]
close1 = d.find('</div>', idx+10)
close2 = d.find('</div>', close1+6)
close3 = d.find('</div>', close2+6)
close4 = d.find('</div>', close3+6)
print(f'4 closing divs at: {close1}, {close2}, {close3}, {close4}')
print(f'After close4:')
print(d[close4:close4+300])
