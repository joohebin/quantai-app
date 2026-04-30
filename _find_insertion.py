"""Find page insertion point"""
import sys, re
sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)
with open('index.html', 'rb') as f:
    d = f.read().decode('utf-8', errors='replace')

# Find all page-content
poses = [m.start() for m in re.finditer(r'page-content', d)]
print(f'page-content count: {len(poses)}')

# Show around last one
last = d.rfind('id="page-')
print(f'\nLast id="page- at: {last}')
print(d[last:last+500])

# What after it?
end = last + 500
print(f'\n--- chars 4 to 5 ---')
# Look for </div> closing the page-content
close_pos = d.find('</div>', last)
if close_pos > 0:
    close2 = d.find('</div>', close_pos+6)
    close3 = d.find('</div>', close2+6)
    print(f'Three </div> after last page: {close_pos}, {close2}, {close3}')
    print(f'Context after close3: {d[close3:close3+200]}')
