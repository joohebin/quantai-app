f=open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','rb')
c=f.read()
f.close()
t=c.decode('utf-8')

# Fix the sidebar plan escaped unicode
old_escaped = '\\u65d7\\u8230\\u5957\\u9910'
if old_escaped in t:
    t = t.replace(old_escaped, '\u65d7\u8230\u5957\u9910')
    print('Fixed escaped flagship in sidebar')

# Fix the icon too
old_icon = '\\U0001f451'
if old_icon in t:
    t = t.replace(old_icon, '\U0001f451')
    print('Fixed escaped crown icon')

# Also fix in plan grid pricing
old_gp_bad = t.find('\\u514d\\u8d39')
if old_gp_bad >= 0:
    t = t.replace('\\u514d\\u8d39', '\u514d\u8d39')
    print('Fixed escaped free text')

# Check for any other \uXXXX escapes that are not in JS strings
import re
# Find \uXXXX that appear in HTML (not JS string literals)
# These should be actual Unicode chars
def fix_unicode_escapes(text):
    """Replace literal backslash-u sequences in HTML context with actual unicode chars"""
    # Only fix inside HTML, not JS (JS can have \u escapes in strings)
    # We look for \uXXXX outside <script> tags
    parts = []
    last_end = 0
    for m in re.finditer(r'<script[^>]*>.*?</script>', text, re.DOTALL):
        # Before this script tag - in HTML - fix escapes
        html_part = text[last_end:m.start()]
        html_part = re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), html_part)
        html_part = re.sub(r'\\U([0-9a-fA-F]{8})', lambda x: chr(int(x.group(1), 16)), html_part)
        parts.append(html_part)
        parts.append(text[m.start():m.end()])
        last_end = m.end()
    # Remaining after last script tag
    html_part = text[last_end:]
    html_part = re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), html_part)
    html_part = re.sub(r'\\U([0-9a-fA-F]{8})', lambda x: chr(int(x.group(1), 16)), html_part)
    parts.append(html_part)
    return ''.join(parts)

t = fix_unicode_escapes(t)
print('Fixed unicode escapes in HTML')

with open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','w',encoding='utf-8') as f:
    f.write(t)
print('Saved')
