# -*- coding: utf-8 -*-
"""Fix: Insert wallet tab button after exchanges tab button, byte-level"""
filepath = 'index.html'
with open(filepath, 'rb') as f:
    raw = f.read()

# Find exchanges tab button end: </div>
# We know the exchanges tab div ends at 126963 range
marker = b"acc_tab_exchanges\">"
idx = raw.find(marker)
if idx < 0:
    print('ERROR: acc_tab_exchanges not found!')
    # Try without 
    idx = raw.find(b'acc_tab_exchanges')
    
print(f'Found acc_tab_exchanges at {idx}')
# The div closes at next </div> after this
div_end = raw.find(b'</div>', idx)
print(f'div end at {div_end}')
context = raw[div_end:div_end+30]
print(f'After div: {repr(context)}')

# We need to insert wallet button BEFORE the closing </div> of the tab button container
# Look for the pattern: </div>---whitespace---</div> after exchanges tab
close_div = raw.find(b'</div>', idx)
next_close = raw.find(b'</div>', close_div+6)
gap = raw[close_div:next_close+6]
print(f'Gap between closes: {repr(gap)}')

# Actually the pattern is: exchanges tab onclick ends with ...
# ...data-i18n="acc_tab_exchanges">BANK_EMOJI 交易所</div>
# Find the actual </div> that closes the exchange tab button
# Then </div>\n        </div>\n\n        <!-- ===== 标签页内容 ===== -->
# We want wallet button BEFORE the second </div> (or before the comment)

# Let's find: after the "</div>" that closes exchanges, then whitespace/newlines, then "</div>" closing the div container
ex_close = raw.find(b'</div>', idx+30)
# This is the exchanges tab closing </div>
print(f'Exchange button close at {ex_close}: {raw[ex_close-20:ex_close+30]}')

# Next </div> after that closes the container
container_close = raw.find(b'</div>', ex_close+6)
# Between them is whitespace + tab button container bottom
# Insert wallet button just before container_close
gap_text = raw[ex_close:container_close]
print(f'Gap ({len(gap_text)} bytes): {repr(gap_text)}')

# Insert wallet button after exchanges tab close (ex_close+6)
wallet_btn = b'\n          <div class="acc-tab" onclick="switchAccountTab(\'wallet\',this)" style="flex:1;text-align:center;padding:12px;font-size:13px;font-weight:600;color:var(--muted);cursor:pointer" data-i18n="acc_tab_wallet">\xf0\x9f\x92\xb3 \xe9\x92\xb1\xe5\x8c\x85</div>'

new_raw = raw[:ex_close+6] + wallet_btn + raw[ex_close+6:]
print(f'\nInserted wallet button, new size: {len(new_raw)}')

# Save
with open(filepath, 'wb') as f:
    f.write(new_raw)
print('Saved!')
