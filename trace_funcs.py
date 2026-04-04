import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('main.js', 'r', encoding='utf-8') as f:
    src = f.read()

lines = src.split('\n')

def parse_range(src):
    results = []
    i = 0; n = len(src); line = 1
    while i < n:
        c = src[i]
        if c == '/' and i+1 < n and src[i+1] == '/':
            while i < n and src[i] != '\n': i += 1
            continue
        if c == '/' and i+1 < n and src[i+1] == '*':
            i += 2
            while i < n:
                if src[i] == '*' and i+1 < n and src[i+1] == '/': i += 2; break
                if src[i] == '\n': line += 1
                i += 1
            continue
        if c in ('"', "'"):
            q = c; i += 1
            while i < n:
                ch = src[i]
                if ch == '\\': i += 2; continue
                if ch == '\n': line += 1
                if ch == q: i += 1; break
                i += 1
            continue
        if c == '`':
            i += 1
            while i < n:
                ch = src[i]
                if ch == '\\': i += 2; continue
                if ch == '\n': line += 1
                if ch == '`': i += 1; break
                i += 1
            continue
        if c == '\n': line += 1; i += 1; continue
        if c in '{}': results.append((line, c)); i += 1; continue
        i += 1
    return results

tokens = parse_range(src)

# 只看前100行
print("前100行的所有括号:")
depth = 0
for ln, c in tokens:
    if ln > 100: break
    if c == '{': depth += 1
    else: depth -= 1
    ctx = lines[ln-1].strip()[:80]
    print(f"  L{ln}: {c} depth={depth} | {ctx}")

print(f"\nL100时的深度: {depth}")
