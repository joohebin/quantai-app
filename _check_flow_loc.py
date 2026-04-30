# -*- coding: utf-8 -*-
filepath = r'index.html'
with open(filepath, 'rb') as f:
    t = f.read().decode('utf-8')
arb_start = t.find('id="page-arbitrage"')
print(f'page-arbitrage at: {arb_start}')
open_tag_start = t.rfind('<div', arb_start-20, arb_start)
open_tag_end = t.find('>', open_tag_start) + 1
depth = 1; i = open_tag_end
while depth > 0 and i < len(t):
    i = t.find('</', i)
    if i < 0: break
    end_tag_end = t.find('>', i)
    tag_name = t[i+2:end_tag_end].strip()
    if tag_name == 'div':
        depth -= 1
    i = end_tag_end + 1
close_div = i if depth == 0 else len(t)
print(f'page-arbitrage: {open_tag_start} to {close_div}')
print(f'Inside div: {open_tag_end} to {close_div-6}')
# Find flow/log inside page div
flow_in = t.find('arb-flow-container', open_tag_end, close_div)
log_in = t.find('arb-trade-log', open_tag_end, close_div)
print(f'Flow in page div: {flow_in >= 0}, Log in page div: {log_in >= 0}')
# Find them globally
flow_global = t.find('arb-flow-container')
log_global = t.find('arb-trade-log')
print(f'Flow global: {flow_global}, Log global: {log_global}')
print(f'Are they before page div? Flow: {flow_global < open_tag_start}, Log: {log_global < open_tag_start}')
