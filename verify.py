
# -*- coding: utf-8 -*-
with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html','r',encoding='utf-8') as f:
    content = f.read()

funcs = [
    'switchLbTab', 'renderLbList', 'openTraderDetail', 'closeTraderDetail', 'initLbPage',
    'renderSquare', 'filterSquare', 'postSquare', 'sqLike', 'selectSqSentiment',
    'renderStratMarket', 'filterStratMarket', 'toggleSmUpload', 'submitStrategy',
    'openStratDetail', 'backtestStrat', 'copyStrat',
    'renderSignalsPage', 'switchSigTab', 'filterSignals', 'renderLiveSignals',
    'renderBroadcasters', 'renderSigHistory', 'publishSignal', 'followSignal', 'toggleBcSubscribe',
]

print('=== Function Check ===')
all_ok = True
for fn in funcs:
    found = ('function ' + fn + '(') in content
    status = 'OK' if found else 'MISSING!'
    if not found: all_ok = False
    print('  ' + status + '  ' + fn)

print()
print('=== i18n Key Check (expect 4 each) ===')
keys = ['nav_square','nav_stratmarket','nav_signals','sq_title','sm_title','sig_title','lb_tab_roi']
for k in keys:
    cnt = content.count(k)
    ok = 'OK' if cnt >= 4 else 'LOW:'+str(cnt)
    print('  ' + ok + '  ' + k)

print()
print('=== Page HTML Check ===')
pages = ['page-square','page-stratmarket','page-signals','trader-detail-panel','tdp-overlay','sm-detail-modal']
for p in pages:
    found = p in content
    status = 'OK' if found else 'MISSING!'
    print('  ' + status + '  #' + p)

print()
print('ALL FUNCS OK:', all_ok)
print('Total chars:', len(content))
print('Total lines:', content.count(chr(10)))
