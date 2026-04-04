#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更严格的JS解析器：增加正则字面量检测
策略：如果在 = / ( [ , ; ! & | ? : return new 后面跟着 / 就是正则
"""

with open('_test.js', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
total = len(lines)

# 简单方法：用 esprima-style heuristic
# 前置词 + / 开头 = 正则
REGEX_PRECEDE = set(['=', '(', '[', ',', ';', '!', '&', '|', '?', ':', 
                      'return', 'new', 'typeof', 'instanceof', 'in', 'of',
                      'delete', 'throw', 'void', 'case'])

class Parser:
    def __init__(self):
        self.pos = 0
        self.line = 1
        self.col = 0
        self.src = content
        self.n = len(content)
        
        # 括号栈
        self.paren_stack = []   # ()
        self.bracket_stack = [] # []
        self.brace_stack = []   # {}
        
        # 上下文栈
        self.ctx_stack = ['N']
        
        # 上一个有效token（用于判断 / 是除法还是正则）
        self.last_token = ''
        
        self.errors = []
    
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
    
    def skip_regex(self):
        """跳过正则字面量 /.../ 内容（包括字符类 [...]）"""
        # 当前位置是第一个 /
        self.adv()  # skip opening /
        in_class = False
        while self.pos < self.n:
            c = self.cur()
            if c == '\\':
                self.adv(2)
                continue
            if c == '[':
                in_class = True
                self.adv()
                continue
            if c == ']':
                in_class = False
                self.adv()
                continue
            if c == '/' and not in_class:
                self.adv()  # skip closing /
                # skip flags: g, i, m, s, u, y
                while self.pos < self.n and self.cur() in 'gimsuy':
                    self.adv()
                self.last_token = 'regex'
                return
            if c == '\n':
                self.errors.append(f'L{self.line}: 正则表达式内换行（疑似问题）')
                return
            self.adv()
    
    def is_after_operator(self):
        """判断当前 / 前是否是操作符（即这是正则开始而不是除法）"""
        t = self.last_token
        return (t in REGEX_PRECEDE or t == '' or 
                t in ('{', '}', '(', '[', ';', ',', '!', '~', '+', '-', '*', '%', '**',
                      '&&', '||', '??', '=', '+=', '-=', '==', '===', '!=', '!==',
                      '>=', '<=', '>', '<', '=>'))
    
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
                    self.last_token = 'str'
                    self.adv()
                elif c == '\n':
                    self.errors.append(f'L{self.line}: 单引号字符串内换行（col {self.col}）')
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
                    self.last_token = 'str'
                    self.adv()
                elif c == '\n':
                    self.errors.append(f'L{self.line}: 双引号字符串内换行（col {self.col}）')
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
                    self.last_token = 'str'
                    self.adv()
                elif c == '$' and self.peek() == '{':
                    self.ctx_stack.append('X')
                    self.brace_stack.append(('X', self.line))
                    self.adv(2)
                else:
                    self.adv()
                continue
            
            # Normal / X context
            if c == '/' and self.peek() == '/':
                self.ctx_stack.append('L')
                self.adv(2)
                continue
            if c == '/' and self.peek() == '*':
                self.ctx_stack.append('B')
                self.adv(2)
                continue
            
            # 正则检测
            if c == '/':
                if self.is_after_operator():
                    self.skip_regex()
                    continue
                else:
                    # 除法运算符
                    self.last_token = '/'
                    self.adv()
                    continue
            
            if c == "'":
                self.ctx_stack.append('S')
                self.last_token = ''
                self.adv()
            elif c == '"':
                self.ctx_stack.append('D')
                self.last_token = ''
                self.adv()
            elif c == '`':
                self.ctx_stack.append('T')
                self.last_token = ''
                self.adv()
            elif c == '(':
                self.paren_stack.append(self.line)
                self.last_token = '('
                self.adv()
            elif c == ')':
                if not self.paren_stack:
                    snippet_start = max(0, self.pos-50)
                    snippet = content[snippet_start:self.pos+50].replace('\n', '↵')
                    self.errors.append(f'L{self.line}: 多余的 ) → ...{snippet}...')
                else:
                    self.paren_stack.pop()
                self.last_token = ')'
                self.adv()
            elif c == '[':
                self.bracket_stack.append(self.line)
                self.last_token = '['
                self.adv()
            elif c == ']':
                if not self.bracket_stack:
                    self.errors.append(f'L{self.line}: 多余的 ]')
                else:
                    self.bracket_stack.pop()
                self.last_token = ']'
                self.adv()
            elif c == '{':
                if ctx == 'X':
                    self.brace_stack.append(('X_inner', self.line))
                else:
                    self.brace_stack.append(('N', self.line))
                self.last_token = '{'
                self.adv()
            elif c == '}':
                if not self.brace_stack:
                    self.errors.append(f'L{self.line}: 多余的 }}')
                else:
                    top_type, top_line = self.brace_stack[-1]
                    if top_type == 'X':
                        self.brace_stack.pop()
                        if self.ctx_stack and self.ctx_stack[-1] == 'X':
                            self.ctx_stack.pop()
                    else:
                        self.brace_stack.pop()
                self.last_token = '}'
                self.adv()
            elif c in ' \t\n\r':
                self.adv()
            else:
                # 收集标识符/关键字/运算符作为 last_token
                if c.isalpha() or c == '_' or c == '$':
                    start = self.pos
                    while self.pos < self.n and (self.src[self.pos].isalnum() or self.src[self.pos] in '_$'):
                        self.adv()
                    self.last_token = content[start:self.pos]
                elif c in '=!<>&|?+-%*~^':
                    start = self.pos
                    while self.pos < self.n and self.src[self.pos] in '=!<>&|?+-%*~^':
                        self.adv()
                    self.last_token = content[start:self.pos]
                elif c in ';,':
                    self.last_token = c
                    self.adv()
                else:
                    self.adv()
    
    def report(self):
        print(f'=== 解析完成，共 {total} 行 ===')
        print(f'错误数: {len(self.errors)}')
        if self.errors:
            for e in self.errors[:30]:
                print(f'  {e}')
        else:
            print('  无语法错误！')
        
        print(f'\n最终栈状态:')
        print(f'  未闭合的 ( 共 {len(self.paren_stack)} 个，开于JS行: {self.paren_stack[:20]}')
        print(f'  未闭合的 [ 共 {len(self.bracket_stack)} 个，开于JS行: {self.bracket_stack[:20]}')
        
        real_braces = [(t,l) for t,l in self.brace_stack if t == 'N']
        x_braces = [(t,l) for t,l in self.brace_stack if t != 'N']
        print(f'  未闭合的 {{ 共 {len(real_braces)} 个（正常），开于JS行: {[l for t,l in real_braces[:20]]}')
        if x_braces:
            print(f'  模板插值未闭合: {len(x_braces)} 个，开于: {[l for t,l in x_braces[:5]]}')
        
        print(f'  上下文栈末端: {self.ctx_stack[-5:]}')

p = Parser()
p.parse()
p.report()
