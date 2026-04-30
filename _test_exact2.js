var el = document ? document : {innerHTML: ''};
var _frData = {
  requests: [{id: '1', name: 'Alice', status: 'pending'}],
  sent: [{id: '2', name: 'Bob'}]
};

function renderRequests(){
  var el = document.getElementById('fr-requests-panel');
  if(!el) return;
  var pending=_frData.requests.filter(function(r){return r.status==='pending';});
  var sent=_frData.sent||[];
  el.innerHTML='<div style="font-size:12px;color:var(--muted);margin-bottom:8px">待处理请求 ('+pending.length+')</div>'+
    (pending.length===0?'<div style="padding:20px;text-align:center;color:var(--muted);font-size:13px">暂无待处理的请求</div>':
    pending.map(function(r){
      return '<div style="display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;margin-bottom:4px">'+
        '<span style="width:28px;height:28px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0">🧑</span>'+
        '<span style="flex:1;font-size:13px">'+r.name+'</span>'+
        '<button onclick="acceptRequest(\''+r.id+'\')" style="padding:4px 10px;border:none;border-radius:6px;background:var(--green);color:#fff;font-size:11px;cursor:pointer">接受</button>'+
        '<button onclick="rejectRequest(\''+r.id+'\')" style="padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:11px;cursor:pointer">拒绝</button>'+
      '</div>';
    }).join('')+
    (sent.length?'<div style="font-size:12px;color:var(--muted);margin:8px 0 4px">已发送的请求</div>'+
    sent.map(function(r){
      return '<div style="display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;margin-bottom:4px">'+
        '<span style="width:28px;height:28px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0">🧑</span>'+
        '<span style="flex:1;font-size:13px">'+r.name+'</span>'+
        '<span style="font-size:11px;color:var(--muted)">等待中</span>'+
      '</div>';
    }).join('')+'':'');
}

renderRequests();
console.log('OK');
