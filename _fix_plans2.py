f=open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','rb')
c=f.read()
f.close()
t=c.decode('utf-8')

# Fix 1: REVENUE_SHARE - old thresholds with corruption
i=t.find('window.REVENUE_SHARE = [')
j=t.find('];',i)+2
new_rs = """window.REVENUE_SHARE = [
  { min: 0,      max: 500,    rate: 0,   label: '\u2264$500' },
  { min: 501,    max: 3000,   rate: 0.05,label: '$501~$3,000' },
  { min: 3001,   max: 10000,  rate: 0.08,label: '$3,001~$10,000' },
  { min: 10001,  max: Infinity,rate: 0.10,label: '>$10,000' }
];"""
t = t[:i] + new_rs + t[j:]
print('REVENUE_SHARE fixed')

# Fix 2: Check renderBillingTab's billing tier rendering uses 500
# Find "<= $1,000" text
if '\u2264$1,000' in t:
    t = t.replace('\u2264$1,000', '$0~$500')
    print('Billing label fixed')
# Fix ">"
if '>\\$20,000' in t:
    t = t.replace('>$20,000', '>$10,000')
    print('Billing max label fixed')

# Fix 3: Any corrupted unicode shortcuts like '免��' (shows 3 chars)
# Check for corruption pattern
bad = t.find('\u514d\u0000')
if bad < 0:
    # Check for the specific corrupt pattern in the file
    pass

# Fix 4: Check PLANS object for corruption
i2=t.find('window.PLANS = {')
j2=t.find('window.NODES',i2)
plans_section = t[i2:j2]
# Check if free text is corrupted
if '\u514d\u8d39\u8bd5\u7528' not in plans_section:
    print('WARN: PLANS section has corruption')
    # It might have been corrupted to raw chars
    print('Plans first 200:', repr(plans_section[:200])[:300])
else:
    print('PLANS section OK')

# Fix 5: Check sidebar corrupted chars
s='sidebar-plan-icon'
i3=t.find(s)
if i3>=0:
    context = t[i3-5:i3+80]
    print('Sidebar plan:', repr(context))

with open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','w',encoding='utf-8') as f:
    f.write(t)
print('All fixes applied')
