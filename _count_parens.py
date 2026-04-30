import re
with open('index.html', 'rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
t = c.decode('utf-8', errors='replace')
lines = t.split('\n')

# Find renderRequests
idx = c.find(b'function renderRequests')
end = c.find(b'function showAddFriend', idx)

# Count parens from renderRequests to the error line
err_line = 6390  # 0-indexed
paren_count = 0
func_start_line = t[:c.find(b'function renderRequests')].count('\n')  # get actual line num
# Find the actual line number of renderRequests in the JS file
# Line number in node errors is 1-indexed relative to the whole JS
# Let's count lines from the beginning of c
lines_c = c.split(b'\n')
# Count parens in the section around the error
# The renderRequests function starts at line:
fn_req_line = None
for i, l in enumerate(lines_c):
    if b'function renderRequests' in l:
        fn_req_line = i
        break
print(f'renderRequests function at line {fn_req_line + 1} (1-indexed)')

# Count parens from fn_req_line to err_line
if fn_req_line:
    for i in range(fn_req_line, err_line):
        opens = lines_c[i].count(b'(')
        closes = lines_c[i].count(b')')
        paren_count += opens - closes
        if abs(opens - closes) > 0:
            print(f'  Line {i+1}: opens={opens}, closes={closes}, net={paren_count}: {lines_c[i][:60]}')
    print(f'Net paren count at line {err_line+1}: {paren_count}')
    print(f'Line {err_line+1}: {lines_c[err_line]}')
