"""Find CS template literal with input area"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# Find the main app script (not CS Widget script)
# Search for 'cs-send' in the context of HTML creation
idx = t.find('cs-send', 0, 720000)
if idx < 0: idx = t.find('cs-send', 720000)
print(f'cs-send at: {idx}')
# Show context
start = max(0, idx-300)
end = min(len(t), idx+200)
print(t[start:end])
print('\n' + '='*60)
# Also search for where the CS panel HTML template is built
# Look in the CS Widget script (720887-724962)
cs = t[720887:724962]
for line in cs.split('\n'):
    if 'textarea' in line or 'cs-input' in line or 'cs-send' in line or '<button' in line:
        print(line[:200])
