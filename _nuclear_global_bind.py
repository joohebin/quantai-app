# -*- coding: utf-8 -*-
"""
Nuclear option: add a global binding script at the end of the file.
This script assigns all CS functions to window, ensuring they're available.
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find the last </script> before </body>
last_script = t.rfind('</script>', 0, t.rfind('</body>'))

# Inject a binding script AFTER the last script
bindings = '''
<script>
// ===== CS Global Bindings (guaranteed execution) =====
(function(){
  var fns = ['toggleCS','csGreet','csAddMsg','csFormatText','csShowTyping','csHideTyping','csSendQuick','csDoSend','csLocalReply','csFetchGroq','csShowHandoff','csGoHuman','csSendMessage'];
  var code = document.documentElement.outerHTML;
  for(var i=0;i<fns.length;i++){
    var name = fns[i];
    if(typeof window[name] === 'undefined'){
      try{
        // Parse the function from the script text
        var scripts = document.getElementsByTagName('script');
        for(var j=0;j<scripts.length;j++){
          var s = scripts[j].textContent || '';
          var idx = s.indexOf('function ' + name);
          if(idx < 0) idx = s.indexOf('async function ' + name);
          if(idx >= 0){
            // Find matching closing brace
            var fnText = s.substring(idx);
            var depth = 0;
            var endPos = 0;
            for(var k=0;k<fnText.length;k++){
              if(fnText[k] === '{') depth++;
              if(fnText[k] === '}') depth--;
              if(depth === 0 && k > 5){
                endPos = k + 1;
                break;
              }
            }
            fnText = fnText.substring(0, endPos);
            try{
              eval('window["' + name + '"] = ' + fnText);
              console.log('[CS Bind] Bound ' + name);
            }catch(e){
              console.warn('[CS Bind] Failed ' + name + ': ' + e.message);
            }
            break;
          }
        }
      }catch(e){
        console.warn('[CS Bind] Error ' + name + ': ' + e.message);
      }
    }
  }
  console.log('[CS Bind] Complete. toggleCS=' + typeof window.toggleCS + ' csGreet=' + typeof window.csGreet);
})();
</script>
'''

t = t[:last_script + 9] + bindings + t[last_script + 9:]

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

print(f'File: {len(t)/1024:.1f} KB')
print('Injected CS global bindings at end of file')
