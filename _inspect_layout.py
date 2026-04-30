"""Inspect QuantTalk page-square layout"""
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

idx = t.find('<div id="page-square"')
if idx < 0:
    # Try single quotes
    idx = t.find("id='page-square'")
print(f'page-square div at: {idx}')
if idx > 0:
    print(t[idx:idx+3000])
    print(f'\n--- End ---\n{t[idx:idx+8000][-500:]}')
