
import sys

class Frame:
    def __init__(self,V):
        self.type  = self.__class__.__name__.lower()
        self.value = V
        self.attr  = {}
        self.nest  = []
    def __repr__(self):
        return self.dump()
    dumped = []
    def dump(self,depth=0,prefix=''):
        S = self.pad(depth) + self.head(prefix)
        if not depth: Frame.dumped = []
        if self in Frame.dumped: return S + ' ...'
        else: Frame.dumped.append(self)
        for i in self.attr: S += self.attr[i].dump(depth+1,prefix='%s = '%i)
        for j in self.nest: S += j.dump(depth+1)
        return S
    def head(self,prefix=''):
        return '%s<%s:%s> @%x' % (prefix, self.type, self.value, id(self))
    def pad(self,padding):
        return '\n'+'\t'*padding
    
    def __floordiv__(self,obj):
        if isinstance(obj,str): self.nest.append(String(obj))
        else: self.nest.append(obj)
        return self
    def __lshift__(self,obj):
        self.attr[obj.value] = obj ; return self
    def __getitem__(self,slot):
        return self.attr[slot]
    def __setitem__(self,slot,obj):
        self.attr[slot] = obj ; return self
        
    def top(self): return self.nest[-1]
    def pop(self): return self.nest.pop()
    def dropall(self): self.nest = []
    
    def gen(self):
        S = ''
        for i in self.nest: S += i.gen() + '\n'
        return S
        
class Primitive(Frame):
    def gen(self):
        return self.value

class Symbol(Primitive): pass

class String(Primitive): pass
    
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
    
class File(IO):
    def gen(self):
        return self.head() + '\n\n' + Frame.gen(self)
    
class Meta(Frame): pass

class Project(Meta): pass

hico = Project('hico')
readme = File('README.md') ; hico // readme 
readme // '# hico' // '## homoiconic Python bootstrap' // '' // '(c) Dmitry Ponyatov <<dponyatov@gmail.com>> CC BY-NC-ND' // '' // 'github: https://github.com/ponyatov/hico'

gitignore = File('.gitignore') ; hico // gitignore
gitignore // '*~' // '*.swp' // '*.pyc' // '*.log'

eclipse = Group('Eclipse') ; hico // eclipse
e_project = File('.project') ; eclipse // e_project
e_project // '''<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
    <name>hico</name>
    <comment></comment>
    <projects>
    </projects>
    <buildSpec>
        <buildCommand>
            <name>org.python.pydev.PyDevBuilder</name>
            <arguments>
            </arguments>
        </buildCommand>
    </buildSpec>
    <natures>
        <nature>org.python.pydev.pythonNature</nature>
    </natures>
</projectDescription>'''

import ply.lex as lex

tokens = ['symbol']

t_ignore = ' \t\r\n'

def t_symbol(t):
    r'[a-zA-Z0-9_.]+'
    return Symbol(t.value)

def t_error(t): return SyntaxError(t)

lexer = lex.lex()

S = Stack('DATA')
W = Dict('WORDS') ; W['W'] = W

def DROPALL(): S.dropall()
W['.'] = DROPALL

def WORD():
    token = lexer.token()
    if not token: return False
    S // token ; return True
W << WORD
    
def FIND():
    T = S.pop()
    try: S // W[T.value] ; return True
    except KeyError: S // T ; return False
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
W << INTERPRET

def REPL():
    while True:
        print W ; print S ; print
        try: S // String(raw_input('hico> '))
        except EOFError: sys.exit()
        INTERPRET()
REPL()
