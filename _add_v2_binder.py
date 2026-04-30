# -*- coding: utf-8 -*-
"""
Add a final script that properly extracts and binds all CS functions to window.
Uses the corrected brace-matching algorithm (handles strings, templates, async).
"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

binding_script = '''<script>
// ===== CS Function Global Binder v2 (fixed brace matching) =====
(function(){
  var s0 = document.getElementsByTagName('script')[0].textContent;
  var csFns = ['csGreet','csAddMsg','csFormatText','csShowTyping','csHideTyping','csSendQuick','csLocalReply','csShowHandoff','csGoHuman'];
  
  function extractFunction(name) {
    var idx = s0.indexOf('function ' + name);
    if (idx < 0) idx = s0.indexOf('async function ' + name);
    if (idx < 0) return null;
    
    var fnText = s0.substring(idx);
    var depth = 0, end = 0, inStr = false, inTmpl = false, strChar = null, sawBrace = false;
    
    for (var i = 0; i < fnText.length; i++) {
      var ch = fnText[i], prev = i > 0 ? fnText[i-1] : '';
      if (!inTmpl && (ch === '"' || ch === "'") && prev !== '\\\\') {
        if (!inStr) { inStr = true; strChar = ch; }
        else if (ch === strChar) { inStr = false; strChar = null; }
      }
      if (!inStr && ch === '`' && prev !== '\\\\') inTmpl = !inTmpl;
      if (!inStr && !inTmpl) {
        if (ch === '{') { depth++; sawBrace = true; }
        if (ch === '}') depth--;
      }
      if (sawBrace && depth === 0 && i > 1) { end = i + 1; break; }
    }
    
    if (end === 0) return null;
    return fnText.substring(0, end);
  }
  
  for (var i = 0; i < csFns.length; i++) {
    var name = csFns[i];
    if (typeof window[name] === 'function') continue;
    var fnCode = extractFunction(name);
    if (!fnCode) { console.warn('[CS Bind] Cannot find: ' + name); continue; }
    try {
      if (fnCode.indexOf('async ') === 0) {
        // Wrap async functions
        eval('window["' + name + '"] = (async function(){})');
        // Re-evaluate with Function constructor
        var asyncWrapper = new Function('return ' + fnCode)();
        window[name] = asyncWrapper;
      } else {
        eval('window["' + name + '"] = ' + fnCode);
      }
      console.log('[CS Bind] Bound: ' + name);
    } catch(e) {
      console.warn('[CS Bind] Failed: ' + name + ' - ' + e.message);
    }
  }
  
  console.log('[CS Bind] Done. toggleCS=' + typeof window.toggleCS + ' csGreet=' + typeof window.csGreet);
})();
</script>'''

# Insert after the last script before </body>
last_script = t.rfind('</script>', 0, t.rfind('</body>'))
t = t[:last_script + 9] + binding_script + t[last_script + 9:]

with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))
print(f'File: {len(t)/1024:.1f} KB')
print('Added v2 global binder')
