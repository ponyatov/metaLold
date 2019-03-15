## Python/FORTH metaprogramming language implementation
## (c) Dmitry Ponyatov <dponyatov@gmail.com> CC BY-NC-ND

import sys

######################################################################## FRAMES

class Frame:
    
    def __init__(self,V):
        self.type  = self.__class__.__name__.lower()
        self.value = V
        self.attr  = {}
        self.nest  = []
        
    ### dump
                
    def __repr__(self):
        return self.dump()
    dumped = []
    def dump(self, depth=0, prefix=''):
        S = self.pad(depth) + self.head(prefix)
        if not depth: Frame.dumped = []
        if self in Frame.dumped: return S + ' ...'
        else: Frame.dumped.append(self)
        for i in self.attr: S += self.attr[i].dump(depth+1,prefix='%s = '%i)
        for j in self.nest: S += j.dump(depth+1)
        return S
    def head(self,prefix=''):
        return '%s<%s:%s> @%x' % (prefix, self.type, self.str(), id(self))
    def str(self):
        return self.value
    def pad(self, N):
        return '\n' + '\t' * N
    
    ### operators override
    
    def __floordiv__(self,obj):
        if isinstance(obj,str): self.nest.append(String(obj))
        else: self.nest.append(obj)
        return self
    def __rshift__(self,obj):
        obj << self ; return self
    def __lshift__(self,obj):
        if callable(obj):
            return self << VM(obj)
        else:
            self.attr[obj.value] = obj ; return self
    def __getitem__(self,slot):
        return self.attr[slot]
    def __setitem__(self,slot,obj):
        self.attr[slot] = obj ; return self
        
    ## stack manipulations
        
    def top(self): return self.nest[-1]
    def pop(self): return self.nest.pop()
    def dropall(self): self.nest = []
    def push(self,obj): self.nest.append(obj) ; return self
    def dup(self): self.push(self.top()) ; return self
    def drop(self): self.pop() ; return self
    def press(self): del self.nest[-2] ; return self
    def swap(self):
        B = self.pop() ; A = self.pop() ; self // B // A ; return self
        
    ## processing
    
    def execute(self): S // self
    
    def gen(self):
        S = ''
        for i in self.nest: S += i.gen() + '\n'
        return S
        
class Primitive(Frame):
    def gen(self):
        return self.value

class Symbol(Primitive): pass

class String(Primitive):
    def str(self):
        S = ''
        for c in self.value:
            if    c == '\n': S += '\\n'
            elif  c == '\t': S += '\\t'
            else: S += c
        return S
    
class Number(Primitive):
	def add(self,obj):
		if isinstance(obj,Number): return Number(self.value + obj.value)
		else: raise TypeError(obj)
	def sub(self,obj):
		if isinstance(obj,Number): return Number(self.value - obj.value)
		else: raise TypeError(obj)
	def mul(self,obj):
		if isinstance(obj,Number): return Number(self.value * obj.value)
		else: raise TypeError(obj)
	def div(self,obj):
		if isinstance(obj,Number): return Number(self.value / obj.value)
		else: raise TypeError(obj)
	def mod(self,obj):
		if isinstance(obj,Number): return Number(self.value % obj.value)
		else: raise TypeError(obj)
	def neg(self):
		return Number(-self.value)

class Integer(Number): pass

class Hex(Integer):
	def str(self): return '0x%X' % self.value

class Bin(Integer):
	def str(self): return bin(self.value)
    
class Container(Frame): pass

class Group(Container): pass

class Stack(Container): pass

class Dict(Container):
    def __setitem__(self,slot,obj):
        if callable(obj): self[slot] = VM(obj) ; return self
        else: return Container.__setitem__(self, slot, obj)
    def __lshift__(self,obj):
        if callable(obj): self << VM(obj) ; return self
        else: return Container.__lshift__(self, obj)
        
class Active(Frame): pass

class VM(Active):
    def __init__(self,F):
        Active.__init__(self,F.__name__)
        self.fn = F
    def execute(self):
        self.fn()
    
class IO(Frame): pass
    
class Dir(IO): pass
class File(IO):
    def gen(self):
        return self.head() + '\n\n' + Frame.gen(self)

######################################################################### FORTH

W = Dict('FORTH') ; W['W'] = W

S = Stack('DATA') ; W['S'] = S

######################################################################### lexer

import ply.lex as lex

tokens = ['symbol','number','hex','bin']

t_ignore = ' \t\r\n'

t_ignore_comment = r'[\#\\].*'

def t_hex(t):
	r'0x[0-9a-fA-F]+'
	return Hex(int(t.value[2:],0x10))

def t_bin(t):
	r'0b[01]+'
	return Bin(int(t.value[2:],0x02))

def t_number(t):
    r'[\+\-]?[0-9]+'
    return Number(int(t.value))

def t_symbol(t):
    r'`|[^ \t\r\n\#\\]+'
    return Symbol(t.value)

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

################################################################### interpreter

def QUOTE():
    WORD()
W['`'] = VM(QUOTE)

def WORD():
    token = lexer.token()
    if not token: return False
    S // token ; return True
W << WORD
    
def FIND():
    token = S.pop()
    try: S // W[token.str()]             ; return True
    except KeyError:
        try: S // W[token.str().upper()] ; return True
        except KeyError: S // token      ; return False
W << FIND
    
def EXECUTE():
    S.pop().execute()
W << EXECUTE

def INTERPRET():
    lexer.input(S.pop().value)
    while True:
        if not WORD(): break;
        if isinstance(S.top(),Symbol):
            if FIND(): EXECUTE()
            else: raise SyntaxError(S.pop())
W << INTERPRET

def REPL():
    while True:
        print S
        try: S // String(raw_input('hico> ')) ; INTERPRET()
        except EOFError: BYE()
W << REPL
        
########################################################################## i/o
        
def FILE():
    WORD() ; S // File(S.pop().value) ; W << S.top() 
W << FILE

def DIR():
    WORD() ; S // Dir(S.pop().value) ; W << S.top() 
W << DIR

######################################################################### debug

def BYE():
    sys.exit(0)
W << BYE    

def Sdot():
    print S
W['?'] = VM(Sdot)

def WORDS():
    print W
W << WORDS

def DumpExit():
    WORDS() ; Sdot() ; BYE()
W['??'] = VM(DumpExit)

################################################################### stack fluff

def DUP(): S.dup()
W << DUP

def DROP(): S.drop()
W << DROP

def SWAP(): S.swap()
W << SWAP

def PRESS(): S.press()
W << PRESS

def DOT():
    S.dropall()
W['.'] = VM(DOT)

################################################################# manipulations

def PUSH():
    B = S.pop() ; S.top() // B
W['//'] = VM(PUSH)

def RSHIFT():
    WORD() ; FIND() ; B = S.pop() ; A = S.pop() ; A >> B
W['>>'] = VM(RSHIFT)

################################################################### definitions

def DEF():
    W << S.top()
W << DEF

########################################################################## math

def ADD():
	B = S.pop() ; A = S.pop() ; S // A.add(B)
W['+'] = VM(ADD)

def SUB():
	B = S.pop() ; A = S.pop() ; S // A.sub(B)
W['-'] = VM(SUB)

def MUL():
	B = S.pop() ; A = S.pop() ; S // A.mul(B)
W['*'] = VM(MUL)

def DIV():
	B = S.pop() ; A = S.pop() ; S // A.div(B)
W['/'] = VM(DIV)

def MOD():
	B = S.pop() ; A = S.pop() ; S // A.mod(B)
W['%'] = VM(MOD)

def NEG():
	B = S.pop() ; A = S.pop() ; S // A.neg()
W << NEG

############################################################### METAPROGRAMMING

class Meta(Frame): pass

class Class(Meta): pass

def CLASS():
    # forward symbol lookup
    WORD()
    # push new class created from top symbol
    S // Class(S.pop().str())
    # copy created class to global vocabulary
    W << S.top()
W << CLASS

def SUPER():
    # copy superclass from stack
    super = S.top()
    # create new class on stack
    CLASS()
    # create superclass slot
    S.top()['super'] = super 
W << SUPER

class Project(Meta): pass

# hico = W['META'] = Project('hico')
# 
# readme = File('README.md') ; hico // readme 
# readme // '# hico' // '## homoiconic Python bootstrap' // '' // '(c) Dmitry Ponyatov <<dponyatov@gmail.com>> CC BY-NC-ND' // '' // 'github: https://github.com/ponyatov/hico'
# 
# gitignore = File('.gitignore') ; hico // gitignore
# gitignore // '*~' // '*.swp' // '*.pyc' // '*.log'
# 
# eclipse = Group('Eclipse') ; hico // eclipse
# e_project = File('.project') ; eclipse // e_project
# e_project // '''<?xml version="1.0" encoding="UTF-8"?>
# <projectDescription>
#     <name>hico</name>
#     <comment></comment>
#     <projects>
#     </projects>
#     <buildSpec>
#         <buildCommand>
#             <name>org.python.pydev.PyDevBuilder</name>
#             <arguments>
#             </arguments>
#         </buildCommand>
#     </buildSpec>
#     <natures>
#         <nature>org.python.pydev.pythonNature</nature>
#     </natures>
# </projectDescription>'''
        
########################################################################## INIT

if __name__ == '__main__':
    ini = sys.argv[0][:-3]+'.ini'
    for source in [ini] + sys.argv[1:]:
        with open(source) as SourceFile:
            S // SourceFile.read()
            INTERPRET()
    REPL()
