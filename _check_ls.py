import re
f=open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','rb')
c=f.read()
f.close()
t=c.decode('utf-8')

# Find localStorage methods
uses = set()
for m in re.finditer(r'localStorage\.\w+', t):
    uses.add(m.group())
uses = sorted(uses)
print('localStorage methods:')
for u in uses:
    print(f'  {u}')

# Find keys
keys = set()
for m in re.finditer(r"localStorage\.getItem\([\"'](\w+)[\"']\)", t):
    keys.add(m.group(1))
for m in re.finditer(r"localStorage\.setItem\([\"'](\w+)[\"']", t):
    keys.add(m.group(1))
for m in re.finditer(r"localStorage\.removeItem\([\"'](\w+)[\"']", t):
    keys.add(m.group(1))
keys = sorted(keys)
print('\nlocalStorage keys:')
for k in keys:
    print(f'  {k}')
print(f'\nTotal unique keys: {len(keys)}')

# Find count of localStorage references
all_refs = list(re.finditer(r'localStorage', t))
print(f'Total localStorage references: {len(all_refs)}')
