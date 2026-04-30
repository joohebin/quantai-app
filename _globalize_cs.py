# -*- coding: utf-8 -*-
"""Simple fix: add a script at file end that re-exposes all CS functions on window."""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Build the binding JS
binding = '''
<script>
// === CS Function Globalizer ===
// Ensure all CS functions are accessible globally
(function(){
  var fns = ['csGreet','csAddMsg','csFormatText','csShowTyping','csHideTyping','csSendQuick','csGoHuman','csShowHandoff','csSendMessage'];
  for(var i=0;i<fns.length;i++){
    try{
      if(typeof eval(fns[i]) === 'function'){
        window[fns[i]] = eval(fns[i]);
      }
    }catch(e){}
  }
})();
</script>
'''

# Insert before </html>
t = t.replace('</html>', binding + '\n</html>')
print('Added CS function globalizer')

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

print(f'File: {len(t)/1024:.1f} KB')
print(f'globalizer count: {t.count("CS Function Globalizer")}')
