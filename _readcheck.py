import sys
sys.stdout.reconfigure(encoding='utf-8')
lines = open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\_check.js', encoding='utf-8', errors='replace').readlines()
for i, l in enumerate(lines[1155:1170], 1156):
    print(f'{i}: {l[:150]}', end='')
