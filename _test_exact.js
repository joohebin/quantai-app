// Exact test of the ternary structure
var pending = [];
var sent = [{id: 1, name: 'test'}];

var result = '<div>1 (' + 0 + ')</div>' +
  (pending.length === 0 ? '<div>empty</div>' : 
  pending.map(function(r){
    return '<div>' + r + '</div>';
  }).join('') +
  (sent.length ? '<div>sent</div>' + 
  sent.map(function(r){
    return '<div>' + r.name + '</div>';
  }).join('') + '' : '')
);

console.log(result);
