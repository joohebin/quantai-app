"""Complete rewrite: fix renderRequests by using simple string building"""
import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c = r[cs:eidx]
t = c.decode('utf-8', errors='replace')

# Find renderRequests function
idx = t.find('function renderRequests')
idx2 = t.find('function showAddFriend', idx)

if idx < 0 or idx2 < 0:
    print('renderRequests or showAddFriend not found')
    exit(1)

# Replace the entire function body with a cleaner version
old_fn = t[idx:idx2]

# Simple, clean implementation using array push + join approach (no complex ternaries)
new_fn = """function renderRequests(){
  loadFRData();
  var el=document.getElementById('fr-requests-panel');
  if(!el) return;
  var pending=_frData.requests.filter(function(r){return r.status==='pending';});
  var sent=_frData.sent||[];
  var html='<div style="font-size:12px;color:var(--muted);margin-bottom:8px">待处理请求 ('+pending.length+')</div>';
  if(pending.length===0){
    html+='<div style="padding:20px;text-align:center;color:var(--muted);font-size:13px">暂无待处理的请求</div>';
  }else{
    html+=pending.map(function(r){
      return '<div style="display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;margin-bottom:4px">'+
        '<span style="width:28px;height:28px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0">🧑</span>'+
        '<span style="flex:1;font-size:13px">'+r.name+'</span>'+
        '<button onclick="acceptRequest(\\''+r.id+'\\')" style="padding:4px 10px;border:none;border-radius:6px;background:var(--green);color:#fff;font-size:11px;cursor:pointer">接受</button>'+
        '<button onclick="rejectRequest(\\''+r.id+'\\')" style="padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer">拒绝</button>'+
      '</div>';
    }).join('');
  }
  if(sent.length>0){
    html+='<div style="font-size:12px;color:var(--muted);margin:8px 0 4px">已发送的请求</div>';
    html+=sent.map(function(r){
      return '<div style="display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;margin-bottom:4px">'+
        '<span style="width:28px;height:28px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0">🧑</span>'+
        '<span style="flex:1;font-size:13px">'+r.name+'</span>'+
        '<span style="font-size:11px;color:var(--muted)">等待中</span>'+
      '</div>';
    }).join('');
  }
  el.innerHTML=html;
}"""

t = t[:idx] + new_fn + t[idx2:]
r = t.encode('utf-8', errors='replace')
with open(filepath, 'wb') as f:
    f.write(r)

# Check syntax
sidx = r.find(b'<script>', 200000)
cs = sidx + 8
eidx = r.find(b'</script>', cs)
c2 = r[cs:eidx]
with open('/tmp/sc.js', 'wb') as f:
    f.write(c2)
res = subprocess.run(['node','--check','/tmp/sc.js'], capture_output=True, timeout=10)
print(f'Node check: {res.returncode}')
if res.returncode != 0:
    err = res.stderr[:400]
    print(f'Error: {err}')
else:
    print('Syntax OK!')
print(f'Saved: {len(r)} bytes')
