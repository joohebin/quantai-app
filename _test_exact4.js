// Exact match to problematic code
var sent = [{id: 1, name: 'Bob'}];
var pending = [{id: 2, name: 'Alice', status: 'pending'}];

function testRender(){
  var el = document.getElementById('x') || {};
  var pending_f = pending.filter(function(r){return r.status==='pending';});
  var sent_f = sent;
  el.innerHTML='<div>x ('+pending_f.length+')</div>'+
    (pending_f.length===0?'<div>empty</div>':
    pending_f.map(function(r){
      return '<div>'+'<span>'+r.name+'</span>'+'</div>';
    }).join('')+
    (sent_f.length?'<div>sent</div>'+
    sent_f.map(function(r){
      return '<div>'+'<span>'+r.name+'</span>'+'<span>wait</span>'+'</div>';
    }).join('')+'':'');
}

console.log('done');
