# -*- coding: utf-8 -*-
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8')
lines = text.split('\n')

# Print lines 3580-3620
for i in range(3580, min(3620, len(lines))):
    line = lines[i]
    if line.strip():
        print(f"{i:4d}: {line[:90]}")
    else:
        print(f"{i:4d}: [空行]")
