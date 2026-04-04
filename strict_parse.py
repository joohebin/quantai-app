#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
严格JS括号/字符串解析器，正确处理模板字符串嵌套
"""

with open('_test.js', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
total = len(lines)

# 用栈来跟踪状态
# 状态类型: 'normal', 'str_single', 'str_double', 'template', 'comment_line', 'comment_block'
# 模板字符串里的 ${...} 用栈跟踪

class Parser:
    def __init__(self):
        self.pos = 0
        self.line = 1
        self.col = 0
        self.src = content
        self.n = len(content)
        
        # 括号栈: 每个元素 (type, line)
        self.paren_stack = []   # ()
        self.bracket_stack = [] # []
        self.brace_stack = []   # {}
        
        # 上下文栈
        # 'N' = normal, 'S' = single-quote str, 'D' = double-quote str
        # 'T' = template str, 'B' = block comment
        # 'X' = template interpolation (${...} 里面)
        self.ctx_stack = ['N']
        
        self.errors = []
        self.warnings = []
    
    def cur(self):
        if self.pos < self.n:
            return self.src[self.pos]
        return ''
    
    def peek(self, offset=1):
        p = self.pos + offset
        if p < self.n:
            return self.src[p]
        return ''
    
    def adv(self, n=1):
        for _ in range(n):
            if self.pos < self.n:
                if self.src[self.pos] == '\n':
                    self.line += 1
                    self.col = 0
                else:
                    self.col += 1
                self.pos += 1
    
    def ctx(self):
        return self.ctx_stack[-1] if self.ctx_stack else 'N'
    
    def parse(self):
        while self.pos < self.n:
            c = self.cur()
            ctx = self.ctx()
            
            if ctx == 'B':  # block comment
                if c == '*' and self.peek() == '/':
                    self.adv(2)
                    self.ctx_stack.pop()
                else:
                    self.adv()
                continue
            
            if ctx == 'L':  # line comment
                if c == '\n':
                    self.ctx_stack.pop()
                self.adv()
                continue
            
            if ctx == 'S':  # single quote string
                if c == '\\':
                    self.adv(2)
                elif c == "'":
                    self.ctx_stack.pop()
                    self.adv()
                elif c == '\n':
                    self.errors.append(f'L{self.line}: 单引号字符串内换行（未闭合）')
                    self.ctx_stack.pop()
                    self.adv()
                else:
                    self.adv()
                continue
            
            if ctx == 'D':  # double quote string
                if c == '\\':
                    self.adv(2)
                elif c == '"':
                    self.ctx_stack.pop()
                    self.adv()
                elif c == '\n':
                    self.errors.append(f'L{self.line}: 双引号字符串内换行（未闭合）')
                    self.ctx_stack.pop()
                    self.adv()
                else:
                    self.adv()
                continue
            
            if ctx == 'T':  # template string
                if c == '\\':
                    self.adv(2)
                elif c == '`':
                    self.ctx_stack.pop()
                    self.adv()
                elif c == '$' and self.peek() == '{':
                    # 进入模板插值，作为普通N上下文处理，但要用特殊brace追踪
                    self.ctx_stack.append('X')
                    self.brace_stack.append(('X', self.line))
                    self.adv(2)
                else:
                    self.adv()
                continue
            
            if ctx == 'X':  # 模板插值内部 ${ ... }
                # 和 N 一样处理，但 } 会关闭这个 X 上下文
                pass  # fall through to normal handling below
            
            # Normal / X context
            if c == '/' and self.peek() == '/':
                self.ctx_stack.append('L')
                self.adv(2)
            elif c == '/' and self.peek() == '*':
                self.ctx_stack.append('B')
                self.adv(2)
            elif c == "'":
                self.ctx_stack.append('S')
                self.adv()
            elif c == '"':
                self.ctx_stack.append('D')
                self.adv()
            elif c == '`':
                self.ctx_stack.append('T')
                self.adv()
            elif c == '(':
                self.paren_stack.append(self.line)
                self.adv()
            elif c == ')':
                if not self.paren_stack:
                    self.errors.append(f'L{self.line}: 多余的 ) [col {self.col}]')
                    snippet = content[max(0,self.pos-30):self.pos+30].replace('\n','↵')
                    self.errors.append(f'  上下文: ...{snippet}...')
                else:
                    self.paren_stack.pop()
                self.adv()
            elif c == '[':
                self.bracket_stack.append(self.line)
                self.adv()
            elif c == ']':
                if not self.bracket_stack:
                    self.errors.append(f'L{self.line}: 多余的 ]')
                else:
                    self.bracket_stack.pop()
                self.adv()
            elif c == '{':
                if ctx == 'X':
                    # 嵌套在模板插值里的 {
                    self.brace_stack.append(('X_inner', self.line))
                else:
                    self.brace_stack.append(('N', self.line))
                self.adv()
            elif c == '}':
                if not self.brace_stack:
                    self.errors.append(f'L{self.line}: 多余的 }}')
                else:
                    top_type, top_line = self.brace_stack[-1]
                    if top_type == 'X':
                        # 关闭模板插值
                        self.brace_stack.pop()
                        self.ctx_stack.pop()  # 弹出 'X'，回到 T
                    else:
                        self.brace_stack.pop()
                self.adv()
            else:
                self.adv()
    
    def report(self):
        print(f'=== 解析完成，共 {total} 行 ===')
        print(f'错误数: {len(self.errors)}')
        if self.errors:
            for e in self.errors[:30]:
                print(f'  {e}')
        
        print(f'\n最终栈状态:')
        print(f'  未闭合的 ( 共 {len(self.paren_stack)} 个，开于行: {self.paren_stack[:10]}')
        print(f'  未闭合的 [ 共 {len(self.bracket_stack)} 个，开于行: {self.bracket_stack[:10]}')
        
        # 过滤掉X类型的brace（模板插值应该已经关闭了）
        real_braces = [(t,l) for t,l in self.brace_stack if t == 'N']
        x_braces = [(t,l) for t,l in self.brace_stack if t != 'N']
        print(f'  未闭合的 {{ 共 {len(real_braces)} 个（正常），开于行: {[l for t,l in real_braces[:10]]}')
        if x_braces:
            print(f'  未闭合的 {{ 共 {len(x_braces)} 个（模板插值类型: {[t for t,l in x_braces[:5]]}），开于行: {[l for t,l in x_braces[:5]]}')
        
        ctx_remaining = [c for c in self.ctx_stack if c not in ('N',)]
        print(f'  上下文栈: {self.ctx_stack[-10:]}')
        if ctx_remaining:
            print(f'  !! 未关闭的上下文: {ctx_remaining}')

p = Parser()
p.parse()
p.report()
