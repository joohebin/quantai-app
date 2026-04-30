"""Debug renderRequests full function and fix syntax"""
import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()

sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
t = c.decode('utf-8', errors='replace')

# Find renderRequests
idx = t.find('function renderRequests')
end = t.find('function showAddFriend', idx)
print(f'renderRequests: {idx} -> {end} ({end-idx} chars)')
print(t[idx:end])
