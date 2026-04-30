# -*- coding: utf-8 -*-
"""Syntax check the whole CS Widget block"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
# Extract CS Widget from Script 0
s0 = t.find('<script>', 910)
s0_close = t.find('</script>', s0)
cs_start = t.find('// ===== CS Widget', s0)
cs_end = t.rfind('\n\n\n', cs_start, s0_close)
if cs_end < 0:
    cs_end = s0_close

cs_content = t[cs_start:cs_end]
print(f'CS content: {len(cs_content)} chars')

# Check syntax
import subprocess
with open('/tmp/check_syntax.js', 'w', encoding='utf-8') as f:
    f.write('"use strict";\n' + cs_content)
result = subprocess.run(['node', '--check', '/tmp/check_syntax.js'], capture_output=True, text=True)
print(f'Node check: {result.returncode}')
if result.stderr: print(f'  Error: {result.stderr[:200]}')

# Count braces
opens = cs_content.count('{')
closes = cs_content.count('}')
print(f'Braces: {{ = {opens}, }} = {closes}, diff = {opens - closes}')
