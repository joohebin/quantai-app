import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('_check.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# L1709-1714 完整内容
print('=== L1709-1714 完整内容 ===')
for i in range(1707, 1715):
    line = lines[i].rstrip('\n')
    print(f'L{i+1} [{len(line)}]: {repr(line)}')

# 将L1710-1712单独拎出来，测试三元表达式
snippet = '\n'.join(l.rstrip('\n') for l in lines[1707:1714])
print('\n=== Snippet ===')
print(snippet)

import subprocess, json, tempfile, os

# 写一个mini测试
test_code = """
var tr = {id:'x', monthly:1, wr:50, dd:5, av:'A', followers:100, tagKey:'t1'};
var isFollowing = true;
function t(k){ return ''; }
function unfollowTrader(){}
function showFollowModal(){}
function openTraderDetail(){}
""" + snippet

with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.js', delete=False) as tf:
    tf.write(test_code)
    tmpname = tf.name

print(f'\nTest file: {tmpname}')

# Run node check
node = r"C:\Users\Administrator\.workbuddy\binaries\node\versions\22.12.0.installing.47708.__extract_temp__\node-v22.12.0-win-x64\node.exe"
result = subprocess.run([node, '--check', tmpname], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('STDOUT:', result.stdout)
print('STDERR:', result.stderr)
os.unlink(tmpname)
