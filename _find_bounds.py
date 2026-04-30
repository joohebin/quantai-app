# -*- coding: utf-8 -*-
"""Find page-arbitrage boundaries properly"""
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
arb_pos = t.find('id="page-arbitrage"')
next_page = t.find('id="page-', arb_pos + 50)
print(f'page-arbitrage at {arb_pos}')
print(f'Next page at {next_page}')
print(f'Block size: {next_page - arb_pos} bytes')
end_block = t[next_page-200:next_page+50]
print(repr(end_block))
