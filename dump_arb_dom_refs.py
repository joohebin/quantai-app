# -*- coding: utf-8 -*-
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

import re
fns = ['syncExchangesToArbitrage', 'loadArbitragePrices', 'renderArbPrices', 
       'startArbitrageEngine', 'aiArbitrageLoop', 'scanArbitrage', 
       'addArbRecord', 'renderArbHistory', 'initExchangeUI', 'syncArbToConsole',
       'initExchangeUI']

for fn in fns:
    i = t.find('function ' + fn)
    if i < 0:
        print(f'{fn}: NOT FOUND')
        continue
    end = t.find('\nfunction ', i + 1)
    if end < 0:
        end = t.find('</script>', i)
    code = t[i:end]
    refs = re.findall(r"(getElementById|querySelector|getElementByClassName)\(['\"]([^'\"]+)['\"]", code)
    print(f'{fn}:')
    for ref in refs:
        print(f'  {ref[0]}("{ref[1]}")')
    print()
