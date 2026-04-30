// Test: is it '') that's the issue?
var a = ['x'];
var sent = [1,2,3];

// Pattern 1: +'':
var r1 = (sent.length ? '<div>' + sent.map(function(r){return '<div>'+r+'</div>';}).join('') + '' : '');
console.log('Pattern1:', r1);

// Pattern 2: +'':
var r2 = (sent.length ? '<div>' + sent.map(function(r){return '<div>'+r+'</div>';}).join('') + '' : '');
console.log('Pattern2:', r2);
