# -*- coding: utf-8 -*-
"""
Remove OLD dupe functions that override our sim engine.

The file has TWO sets of arb functions:
1. Our sim engine (new, clean, inserted by _clean_rebuild.py) 
2. Original old version (leftover from d340005 base)

Both define: initArbitragePage, loadArbitragePrices, startArbitrageEngine, 
stopArbitrageEngine, renderArbPrices, scanArbitrage, syncArbToConsole,
renderArbHistory, syncExchangesToArbitrage, initExchangeUI, renderConnectedExchanges,
removeExchange, saveExchangeConfig, addArbRecord, selectAoMode, etc.

JS hoisting: last definition wins. We need to remove the OLD block (should be after our sim engine).
"""
filepath = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')

# Find all the OLD arb functions - they're a contiguous block
# The old block starts around function syncExchangesToArbitrage 
# (the one that's different from our sim engine version)

# Identify our sim engine end
# Our sim engine was inserted before "let _arbInterval = null;" 
# The original anchor variable declaration
anchor = 'let _arbInterval = null;'
anchor_pos = t.find(anchor)
print(f'Sim engine anchor at: {anchor_pos}')

# The old functions start AFTER our sim engine? Or before?
# From grep results: 
# Our sim engine functions start at ~619224 (getSimPrices)
# Old functions start at ~212349 (syncExchangesToArbitrage old)
# Wait - the old ones are BEFORE our sim engine!
# That means the old ones get overwritten by our sim engine.
# But initArbitragePage old is AFTER our sim engine!

# Let me trace: old initArbitragePage at 628234, our sim engine at 619224
print(f'\nOld initArbitragePage (second) at: {t.find("function initArbitragePage(){", 627500)}')

# The old block starts around: 621072 (syncExchangesToArbitrage old)
our_end = anchor_pos + len(anchor)

# Find old syncExchangesToArbitrage
old_sync = t.find("function syncExchangesToArbitrage() {", our_end)
print(f'Old syncExchangesToArbitrage at: {old_sync}')

if old_sync > 0:
    # Find where the OLD block ends — after the last old function
    # Old block has: syncExchangesToArbitrage, addExchange, removeExchange, 
    # loadArbitragePrices, renderArbPrices, updateArbFlow (our), addArbTradeLog (our),
    # startArbitrageEngine (our), stopArbitrageEngine (our), scanArbitrage (our),
    # initArbitragePage (our), saveArbitrageState, initExchangeUI (our),
    # renderArbHistory, syncArbToConsole, 
    # THEN the OLD: initArbitragePage, loadArbitragePrices, renderArbPrices,
    # startArbitrageEngine, stopArbitrageEngine, initExchangeUI, renderConnectedExchanges,
    # onExchangeSelected, saveExchangeConfig, cancelExchangeConfig, removeExchange,
    # quickLoginExchanges, logoutAllExchanges, toggleAITrading, stopAITrading,
    # aiArbitrageLoop, syncArbToConsole, scanArbitrage, addArbRecord, renderArbHistory,
    # selectAoMode, toggleAo, simulateAoFire, updateDcaProgress, addAoLiveFeed, addAoLog,

    # Find the end of the OLD block by looking for what comes after
    # The last old function before the next module is "addAoLog" -> "renderAoLog"
    # After that: drawdown charts etc
    old_block_end_marker = "function getSimPrice"
    end_marker_pos = t.find(old_block_end_marker, our_end)
    print(f'getSimPrice at: {end_marker_pos}')
    
    # Also check what's at the end
    # Last old func before our end: renderAoLog? clearAoLog?
    next_section = t.find("// ===== Drawdown", our_end)
    next_section2 = t.find("function upgradeToElite", our_end)
    print(f'Next section at: {next_section} or {next_section2}')
    
    if end_marker_pos > 0:
        # Remove everything from old syncExchangesToArbitrage to end_marker_pos
        # But keep our functions (they are before old_sync)
        print(f'\nRemoving old arb block: {old_sync} to {end_marker_pos}')
        before = t[:old_sync].rstrip()
        after = t[end_marker_pos:].lstrip()
        t = before + '\n\n' + after
        print(f'Removed {end_marker_pos - old_sync} bytes')
    else:
        print('Could not find end marker')
else:
    print('No old duplicate syncExchangesToArbitrage found')
    # Alternative: look for the old initArbitragePage block
    old_init_pos = t.find("function initArbitragePage(){", our_end)
    if old_init_pos > 0:
        print(f'Found old initArbitragePage at {old_init_pos}')
        # Find where it ends and what follows
        # After the old block we have getSimPrice or similar
        next_fn = t.find("function getSimPrice", old_init_pos)
        if next_fn < 0:
            next_fn = t.find("function upgradeToElite", old_init_pos)
        print(f'Next function after old block: {next_fn}')
        
        # Remove everything from old initArbitragePage to next_fn
        if next_fn > 0:
            before = t[:old_init_pos].rstrip()
            after = t[next_fn:].lstrip()
            t = before + '\n\n' + after
            print(f'Removed old init + followers: {next_fn - old_init_pos} bytes')

# Remove the old function block: from after our arbs to getSimPrice
# Let me also verify there's only one initArbitragePage now
with open(filepath, 'wb') as f:
    f.write(t.encode('utf-8'))

# Final verification
with open(filepath, 'rb') as f:
    data = f.read()
text = data.decode('utf-8')
print(f'\n=== Final ===')
print(f'Size: {len(data)/1024:.1f} KB')
for fn in ['initArbitragePage', 'loadArbitragePrices', 'startArbitrageEngine', 
           'stopArbitrageEngine', 'scanArbitrage', 'syncExchangesToArbitrage',
           'renderConnectedExchanges', 'renderArbPrices', 'getSimPrices',
           'updateArbFlow', 'addArbTradeLog']:
    cnt = text.count('function ' + fn + '(')
    if cnt > 1:
        print(f'⚠️  {fn}: {cnt} definitions')
    else:
        print(f'✅ {fn}: {cnt}')
