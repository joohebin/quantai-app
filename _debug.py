import os
filepath = 'index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# Look at the acc-tab button area more broadly
acc_tab = raw.find(b'acc-tab active')
start = acc_tab
end = raw.find(b'<\!--', start)  # Next comment

# Show 4000 bytes around the tab buttons
area = raw[start:start+3000]
with open(os.devnull, 'w') as devnull:
    pass

# Print as repr
import sys
for i in range(0, len(area), 80):
    chunk = area[i:i+80]
    try:
        print(f'{start+i:6d}: {chunk.decode("utf-8", errors="replace")}')
    except:
        print(f'{start+i:6d}: {repr(chunk)}')
