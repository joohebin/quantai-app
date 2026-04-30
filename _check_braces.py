# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
# find CS Widget section
cs = t.find('// ===== 客服 Widget 逻辑 =====')
end = t.find('\n\n\n }\n  }', cs)
print(f'CS at {cs}')
print(f'Trailing: {repr(t[end-50:end+50])}')

# Count braces from CS to end of file
from_end = t[end:]
opens = from_end.count('{')
closes = from_end.count('}')
print(f'After CS Widget: {{ = {opens}, }} = {closes}, diff={opens-closes}')
