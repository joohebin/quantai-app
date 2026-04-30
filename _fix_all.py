f=open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','rb')
c=f.read()
f.close()
t=c.decode('utf-8')

# Step 1: Normalize ALL line endings (\r\r\n -> \r\n, \r\n -> \n)
# This fixes the triple-CRLF issue
import re
# Replace \r\r\n with \r\n, then \r\n with \n
t = re.sub(r'\r+', '\r', t)  # Multiple CR -> single CR
t = t.replace('\r\n', '\n')  # CRLF -> LF
t = t.replace('\r', '\n')    # Any remaining CR -> LF

print('Normalized line endings')

# Step 2: Fix ALL corrupted/escaped unicode issues
# Pattern 1: literal \uXXXX in HTML (outside <script>)
def fix_escapes(text):
    """Fix backslash-u and backslash-U escapes in HTML, JS can keep them"""
    # Fix escaped unicode sequences that became literal '\\u' in file
    # These appear as the actual chars \ u X X X X 
    # Simple approach: replace common escaped sequences
    replacements = {
        '\\u514d\\u8d39': '\u514d\u8d39',
        '\\u514d\u8d39': '\u514d\u8d39',
        '\\u65d7\\u8230\\u5957\\u9910': '\u65d7\u8230\u5957\u9910',
        '\\u57fa\\u7840\\u5957\\u9910': '\u57fa\u7840\u5957\u9910',
        '\\u4e13\\u4e1a\\u5957\\u9910': '\u4e13\u4e1a\u5957\u9910',
        '\\u514d\\u8d39\\u8bd5\\u7528': '\u514d\u8d39\u8bd5\u7528',
        '\\U0001f451': '\U0001f451',  # crown
        '\\U0001f949': '\U0001f949',  # bronze
        '\\U0001f948': '\U0001f948',  # silver
        '\\U0001f513': '\U0001f513',  # unlock
    }
    for old, new in replacements.items():
        if old in text:
            text = text.replace(old, new)
            print(f'Fixed escape: {repr(old.encode("ascii","backslashreplace"))} -> {repr(new.encode("ascii","backslashreplace"))}')
    return text

t = fix_escapes(t)

# Step 3: Fix corrupted '免费' (shows as '��')
i = t.find('return p.price === 0 ?')
if i >= 0:
    before = t[i:i+50]
    print(f'Before fix: {repr(before)}')
    t = t[:i] + "return p.price === 0 ? '\u514d\u8d39' : '$' + p.price + '/' + p.period;" + t[i+len("return p.price === 0 ? ''' : '$' + p.price + '/' + p.period;"):]
    
# Actually let me just find and fix the specific corrupted chars
# The '免费' became something else. Find getPlanPrice function
i = t.find('function(planId)')
j = t.find('window.canUseNode', i)
old_func = t[i:j]
print(f'Old func: {repr(old_func[:120])}')
# Just rebuild it from scratch  
new_get_price = """function(planId){
  var p = window.getPlanInfo(planId);
  return p.price === 0 ? '\u514d\u8d39' : '$' + p.price + '/' + p.period;
};
"""
t = t[:i] + new_get_price + t[j:]
print('getPlanPrice rebuilt')

# Step 4: Fix REVENUE_SHARE
i = t.find('window.REVENUE_SHARE = [')
j = t.find('];', i) + 2
new_rs = """window.REVENUE_SHARE = [
  { min: 0,      max: 500,    rate: 0,   label: '\u2264$500' },
  { min: 501,    max: 3000,   rate: 0.05,label: '$501~$3,000' },
  { min: 3001,   max: 10000,  rate: 0.08,label: '$3,001~$10,000' },
  { min: 10001,  max: Infinity,rate: 0.10,label: '>$10,000' }
];"""
t = t[:i] + new_rs + t[j:]
print('REVENUE_SHARE rebuilt')

# Step 5: Fix calcRevenueShare thresholds
old_calc = t.find('<= 1000')
while old_calc >= 0:
    t = t[:old_calc] + '<= 500' + t[old_calc+7:]
    old_calc = t.find('<= 1000', old_calc+6)
    
old_calc2 = t.find('first $1000')
if old_calc2 >= 0:
    t = t[:old_calc2] + 'first $500' + t[old_calc2+11:]
    
old_calc3 = t.find('1000)')
# Be careful - only the return statement
old_calc_ret = t.find('<= 1000) return', 0, 20000)
if old_calc_ret >= 0:
    t = t[:old_calc_ret] + '<= 500) return' + t[old_calc_ret+12:]
    
# Fix 1001 -> 501 references in calcRevenueShare
old_1001 = t.find('1001,', 15000, 17000)
if old_1001 >= 0:
    t = t[:old_1001] + '501,' + t[old_1001+5:]
    print('Fixed 1001 -> 501')
old_1001b = t.find('1001.', 15000, 17000)
if old_1001b >= 0:
    t = t[:old_1001b] + '501.' + t[old_1001b+5:]
    print('Fixed 1001. -> 501.')

# Fix billing tab rendering thresholds
old_bill_label = t.find('<=$1,000')
if old_bill_label >= 0:
    t = t[:old_bill_label] + '\u2264$500' + t[old_bill_label+9:]
    print('Fixed billing label $1k -> $500')

# Step 6: Fix the PLANS price
old_29 = t.find("basic: {\n    id: 'basic',")
if old_29 >= 0:
    t = t[:old_29+40] + '39' + t[old_29+42:]
    print('Basic price updated to 39')
    
old_99 = t.find("pro: {\n    id: 'pro',")
if old_99 >= 0:
    t = t[:old_99+38] + '79' + t[old_99+40:]
    print('Pro price updated to 79')
    
old_149 = t.find("flagship: {\n    id: 'flagship',")
if old_149 >= 0:
    t = t[:old_149+44] + '199' + t[old_149+47:]
    print('Flagship price updated to 199')

# Add autoEngine feature to PLANS  
if "autoTrade: true, liveTrade: true" in t:
    t = t.replace("autoTrade: true, liveTrade: true,\n      advancedBacktest: true, factorAnalysis: true, copyTrade: true, hft: false, tvUltimate: false,\n      multiRegion: false, nodeSelectable: true }",
                  "autoTrade: true, liveTrade: true,\n      advancedBacktest: true, factorAnalysis: true, copyTrade: true, hft: false, tvUltimate: false,\n      multiRegion: false, nodeSelectable: true, autoEngine: true }")
    # Flagship already has autoEngine: true

with open(r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','w',encoding='utf-8') as f:
    f.write(t)
print('All fixes applied!')
