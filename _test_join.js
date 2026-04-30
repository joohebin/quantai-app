// Test if .join('')+'' : '' is valid JS
var a = true;
var b = ['hello', 'world'];
var result = a ? '<div>' + b.map(function(x){return x;}).join('')+'' : '';
console.log('Result:', result, '| length:', result.length);
