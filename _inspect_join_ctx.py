import subprocess
with open('index.html', 'rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
t = c.decode('utf-8', errors='replace')
idx_req = t.find('function renderRequests')
idx_showa = t.find('function showAddFriend')
code = t[idx_req:idx_showa]
join_idx = code.find("join('')+'':''")
print(f'Join at offset: {join_idx}')
# Show surrounding context
start = max(0, join_idx - 300)
end = min(len(code), join_idx + 30)
excerpt = code[start:end]
safe = excerpt.encode('ascii', errors='replace').decode('ascii')
print('Context:')
print(safe)
