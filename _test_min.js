// Minimal: does .join('')+'' : '' work inline?
function test(){
  var sent = ['a'];
  var r = sent.length ? '<div>' + sent.map(function(x){return x;}).join('') + '' : '';
}
console.log('pass');
