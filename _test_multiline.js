// Test the EXACT multiline structure
var pending = [];
var sent = [{id:1, name:'Bob'}];

function test() {
  var el = document.getElementById('x') || {innerHTML: ''};
  el.innerHTML = '<div>x</div>' +
    (pending.length === 0 ? '<div>empty</div>' : 
    pending.map(function(r){
      return '<div>' + r.name + '</div>';
    }).join('') +
    (sent.length ? '<div>sent</div>' +
    sent.map(function(r){
      return '<div>' + r.name + '</div>';
    }).join('') : '')
  );
}

test();
console.log('OK');
