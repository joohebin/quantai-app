var sent = [1];
var result = (sent.length ? '<div>' + sent.map(function(x){return x;}).join('') : '');
console.log(result);
