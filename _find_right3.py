"""Find the exact right panel div position"""
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

idx = t.find('<!-- Right: Post Feed -->')
print(f'Comment at: {idx}')

# Go backwards from comment to find the opening <div of the right panel
# The right panel's <div is right before or at the comment position.
# Actually, looking at the structure:
# ...</div>    (closes middle panel)
# <div style="width:280px...  (right panel starts)
# <!-- Right: Post Feed -->
# ...
# The <div should be right BEFORE the comment

# Find the last <div before the comment
prev = max(0, idx - 300)
for i in range(idx - 1, prev, -1):
    if t[i:i+4] == '<div':
        print(f'Last <div before comment at: {i}')
        print(f'Content: {t[i:i+130]}')
        break
else:
    print('No <div found before comment')
    # Check if right panel <div is AFTER the comment
    after = t[idx:idx+200]
    print(f'After comment: {after[:150]}')
