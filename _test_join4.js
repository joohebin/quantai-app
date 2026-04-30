// Test: the .join('') + '' : issue - maybe the +'' is parsed as unary plus
var foobar = function() {
  var sent = [];
  var result = '<div>' +
    (sent.length ? '<div>s</div>' + 
    sent.map(function(r){
      return '<div>'+r+'</div>';
    }).join('')+'':'');  // This exact line
};
console.log('done');
