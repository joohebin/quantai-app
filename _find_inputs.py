"""Find all chat input areas in index.html - safe print version"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'rb') as f:
    r = f.read()
t = r.decode('utf-8')

def safe(s):
    # replace surrogates
    return s.encode('utf-8', errors='replace').decode('utf-8', errors='replace')

# Find CS Widget chat input area
print('=== CS Widget Chat Input Area ===')
for kw in ['cs-msg-area', 'cs-input', 'cs-chat-input', 'cs-textarea']:
    idx = t.find(kw)
    if idx >= 0:
        print(f'{kw}:')
        start = max(0, idx-300)
        end = min(len(t), idx+200)
        print(safe(t[start:end]))
        print('---')
        break

# Find QuantTalk msg input
print('\n=== QuantTalk Message Input ===')
for kw in ['sendMsg', 'msg-input', 'sq-input', 'sq-msg-input']:
    idx = t.find(kw)
    if idx >= 0 and t[idx:idx+100].find('onclick') >= 0 or kw in ['msg-input', 'sq-input', 'sq-msg-input']:
        idx = t.find(kw)
        if idx >= 0:
            start = max(0, idx-400)
            end = min(len(t), idx+300)
            print(f'{kw} at {idx}:')
            print(safe(t[start:end]))
            print('---')

# AI advisor chat input
print('\n=== AI Advisor Chat Input ===')
for kw in ['ai-advisor', 'ai_advisor', 'advisor-input', 'advisor-chat']:
    idx = t.find(kw)
    if idx >= 0:
        start = max(0, idx-1200)
        end = min(len(t), idx+200)
        print(f'{kw} at {idx}:')
        print(safe(t[start:end]))
        print('---')

# All textareas
print('\n=== All textareas ===')
i = 0
while True:
    idx = t.find('<textarea', i)
    if idx < 0: break
    end = t.index('>', idx)
    print(f'  textarea at {idx}: {safe(t[idx:end+80])}')
    i = idx + 1
