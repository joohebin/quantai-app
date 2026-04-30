// EXACT byte-for-byte copy of the problematic pattern
var sent = ['a', 'b'];
var pending = [];

function testIt(){
  var el = {innerHTML: ''};
  el.innerHTML = '<div>(' + 0 + ')</div>' +
  (pending.length === 0 ? '<div>empty</div>' :
  pending.map(function(r){ return '<div>' + r + '</div>'; }).join('') +
  (sent.length ? '<div>sent</div>' +
  sent.map(function(r){ return '<div>' + r + '</div>'; }).join('') + '' : '')
  );
}

testIt();
console.log('OK');
