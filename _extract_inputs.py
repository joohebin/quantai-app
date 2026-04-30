"""Extract the exact HTML of CS and QT input areas for modification"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

# CS Widget input area (textarea at 735941)
print('=== CS Widget input section ===')
idx = t.rfind('<textarea', 735000, 736000)
if idx >= 0:
    # Go back to find the containing div
    start = t.rfind('<div', max(0, idx-100), idx)
    end = t.find('</div>', idx)
    # Find the end div that closes this section - 3 divs close
    end2 = t.find('</div>', end+6)
    end3 = t.find('</div>', end2+6)
    for epos in [end, end2, end3]:
        if t[idx:epos+6].count('<div') == t[idx:epos+6].count('</div>'):
            end = epos + 6
            break
    print(f'Start: {start}, End: {end}')
    section = t[start:end]
    print(section)
    print()

# QuantTalk input section
print('\n=== QuantTalk Input Section ===')
idx = t.find('<input id="sq-input"')
if idx >= 0:
    start = t.rfind('<div', max(0, idx-50), idx)
    # Find the enclosing div that contains the whole input bar
    end = t.find('</div>', idx)
    # Look for a few more closes
    end2 = t.find('</div>', end+6)
    end3 = t.find('</div>', end2+6)
    for epos in [end, end2, end3]:
        if t[start:epos+6].count('<div') == t[start:epos+6].count('</div>'):
            end = epos + 6
            break
    section = t[start:end]
    print(f'Start: {start}, End: {end}')
    print(section)

# Also find the CS Widget fab button area
print('\n=== CS Fab HTML ===')
idx = t.find('cs-fab')
if idx >= 0:
    start = idx
    end = t.find('</div>', idx)
    section = t[start:end+6]
    print(section)
