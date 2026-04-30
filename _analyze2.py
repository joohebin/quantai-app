import re

with open('index.html', 'rb') as f:
    content = f.read()

# Account page section
acc_page = content.find(b'page-account')
print(f'Account page at: {acc_page}')

# Find acc-tab-exchanges div
exc_div = content.find(b'acc-tab-exchanges')
print(f'Exc div at: {exc_div}')

# Print everything from just before the page wrapper to a bit after exc div
start = acc_page
end = exc_div + 100
chunk = content[start:end]
# Print with repr to see raw bytes
print(f'Chunk length: {len(chunk)}')
print('=== PRINTING CHUNK ===')
print(chunk.decode('utf-8', errors='replace'))
