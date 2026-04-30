"""Verify bot features were added"""
import os, sys
sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)

with open('index.html', 'rb') as f:
    d = f.read().decode('utf-8', errors='replace')

checks = [
    ('page-bot', 'id="page-bot"'),
    ('nav_bot i18n', 'nav_bot'),
    ('Bot CSS', 'Bot Page'),
    ('loadBots', 'loadBots'),
    ('createBotKey', 'createBotKey'),
    ('initBotPage', 'initBotPage'),
    ('_botOrders', '_botOrders'),
    ('botExecute', 'botExecute'),
    ('parseBotCommand', 'parseBotCommand'),
    ('bot nav item', 'data-page="bot"'),
]

all_ok = True
for name, keyword in checks:
    found = keyword in d
    if not found:
        print(f'  MISSING: {name}')
        all_ok = False

if all_ok:
    print('All Bot features verified ✓')
else:
    print('\nSome features were NOT added by the script. Need to fix.')
