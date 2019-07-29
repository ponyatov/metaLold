## metaL/py : homoiconic metaprogramming system
## (c) Dmitry Ponyatov <dponyatov@gmail.com> CC BY-NC-ND
## wiki: https://github.com/ponyatov/metaL/wiki

import os,sys

############################################ extended Marvin Minsky frame model

class Frame:
    
    def __init__(self,V):
        self.type  = self.__class__.__name__.lower()
        self.val   = V
        self.slot  = {}
        self.nest  = []
        self.immed = False
        
    ################################ dump
        
    def __repr__(self):
        return self.dump()
    def dump(self, depth=0, prefix='', voc=True):
        tree = self._pad(depth) + self.head(prefix)
        if not depth: Frame._dumped = []
        if self in Frame._dumped: return tree + ' _/'
        else: Frame._dumped.append(self)
        if voc:
            for i in self.slot:
                tree += self.slot[i].dump(depth + 1, prefix= i + ' = ')
        for j in self.nest:
            tree += j.dump(depth + 1)
        return tree
    def head(self, prefix=''):
        return '%s<%s:%s> @%x' % (prefix, self.type, self._val(), id(self))
    def _pad(self, depth):
        return '\n' + ' '*4 * depth
    def _val(self):
        return str(self.val)
    
    ################################ operator

    ## ` that = this[key] `
    def __getitem__(self,key):
        return self.slot[key]
    ## ` this[key] = that ` 
    def __setitem__(self,key,that):
        self.slot[key] = that ; return self
    ## ` this << that `
    def __lshift__(self,that):
        self[that.val] = that ; return self
    ## ` this.has(key) `
    def has(self,key):
        return key in self.slot
    ## ` this // that `
    def __floordiv__(self,that):
        return self.push(that)
        
    ################################ stack
    
    ## ` ( ... -- ) ` clear
    def dropall(self):
        self.nest = [] ; return self
    ## ` ( -- a ) `
    def push(self,that):
        self.nest.append(that) ; return self
    ## ` ( a b -- a ) `
    def pop(self):
        return self.nest.pop(-1) # b
    ## ` ( a b -- b ) `
    def pip(self):
        return self.nest.pop(-2) # a
    ## ` ( a b -- a b ) `
    def top(self):
        return self.nest[-1] # b
    ## ` ( a b -- a b ) `
    def tip(self):
        return self.nest[-2] # a

    ## ` ( a - a a ) `
    def dup(self):
        return self // self.top()
    ## ` ( a b -- a ) `
    def drop(self):
        self.pop() ; return self
    ## ` ( a b -- b a ) `
    def swap(self):
        return self // self.pip()
    ## ` ( a b -- a b a ) `
    def over(self):
        return self // self.tip()
    ## ` ( a b -- b ) `
    def press(self):
        self.pip() ; return self
    
    ################################ execute & codegen
    
    def eval(self,ctx):
        return ctx // self
    
    ## in Python source code
    def py(self,parent):
        src = r"%s('%s')" % (self.__class__.__name__, self._val())
        for j in self.nest: src += r" // %s" % j.py(self)
        return src

    ################################ special dump form for tests
    
    def test(self,depth=0,prefix=''):
        tree = '\t' * depth + '%s<%s:%s>' % (prefix, self.type, self._val())
        if not depth: Frame._dumped = []
        if self in Frame._dumped: return tree + ' _/'
        else: Frame._dumped.append(self)
        for i in self.slot: tree += self.slot[i].test(depth+1,prefix=i+' ')
        for j in self.nest: tree += j.test(depth+1)
        return tree
    
##################################################################### primitive

class Primitive(Frame):
    def py(self,parent):
        return self._val()

class String(Primitive):
    def _val(self):
        s = ''
        for c in self.val:
            if   c == '\r': s += '\\r'
            elif c == '\n': s += '\\n'
            elif c == '\t': s += '\\t'
            else:           s += c
        return s
    def py(self,parent):
        return "'%s'" % self._val()

class Symbol(Primitive): pass

class Number(Primitive):
    def __init__(self,V):
        Primitive.__init__(self, float(V))
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

class Integer(Number):
    def __init__(self,V):
        Primitive.__init__(self, int(V))

class Hex(Integer):
    def __init__(self,V):
        Integer.__init__(self, int(V[2:],0x10))
    def _val(self):
        return '0x{0:X}'.format(self.val)
    def toint(self):
        return Integer(self.val)

class Bin(Integer):
    def __init__(self,V):
        Integer.__init__(self, int(V[2:],0x02))
    def _val(self):
        return '0b{0:b}'.format(self.val)
    def toint(self):
        return Integer(self.val)

##################################################################### container

class Container(Frame): pass

class Vector(Container): pass
class Stack(Container): pass
class Dict(Container): pass
class Queue(Container): pass

######################################################################## active

class Active(Frame): pass

class Cmd(Active):
    def __init__(self,F,I=False):
        Active.__init__(self, F.__name__)
        self.fn = F
        self.immed = I
    def eval(self,ctx):
        self.fn(ctx)

class VM(Active):
    def __init__(self,F):
        Active.__init__(self,F.__name__)
        self.fn = F
    def execute(self):
        self.fn()
        
################################################################## input/output
    
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

tokens = ['symbol','number','integer','hex','bin']

t_ignore = ' \t\r\n'

t_ignore_comment = r'[\#\\].*'

def t_hex(t):
	r'0x[0-9a-fA-F]+'
	return Hex(int(t.value[2:],0x10))

def t_bin(t):
	r'0b[01]+'
	return Bin(int(t.value[2:],0x02))

def t_number(t):
    r'[\+\-]?[0-9]+\.[0-9]*([eE][]?[0-9]+)?'
    return Number(float(t.value))

def t_integer(t):
    r'[\+\-]?[0-9]+'
    return Integer(int(t.value))

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

def INTERPRET(ctx):
    lexer.input(ctx.pop().value)
    while True:
        if not WORD(): break;
        if isinstance(ctx.top(),Symbol):
            if FIND(): EXECUTE()
            else: raise SyntaxError(ctx.pop())
W << INTERPRET

def REPL():
    while True:
        print(S)
        try: S // String(raw_input('ok> ')) ; INTERPRET()
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
    print(S)
W['?'] = VM(Sdot)

def WORDS(ctx):
    print(ctx.dump())
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
    # register created class in global vocabulary
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

########################################################################### WEB

def WEB():
    from flask     import Flask,render_template,escape
    from flask_wtf import FlaskForm
    from wtforms   import TextAreaField,SubmitField
    
    web = Flask(__name__)
    web.config['SECRET_KEY'] = os.urandom(32)
    
    class CLI(FlaskForm):
        pad = TextAreaField('pad',
                            render_kw={'rows':5,'autofocus':'true'},
                            default='# put your commands here')
        go = SubmitField('go')
    
    @web.route('/', methods=['GET', 'POST'])
    def index():
        form = CLI()
        if form.validate_on_submit():
            S // String(form.pad.data) ; INTERPRET()
        return render_template('index.html',W=W,form=form)
    
    @web.route('/css/<path:path>')
    def css(path): return web.send_static_file(path)
    
    @web.route('/dump/<path:frame>')
    def dump(frame): return render_template('dump.html',dump=W[frame].dump())
    
    @web.route('/viz/<path:frame>')
    def viz(frame):
        S='"%s"' % frame
        for i in W[frame].attr.keys():
            S += ',"%s"'%i
        return render_template('viz.html',dump=S)
    
    web.run(host=W['WEB']['IP'].value,port=W['WEB']['PORT'].value,debug=True)
W << WEB
W['WEB']['IP']   = String('127.0.0.1')
W['WEB']['PORT'] = Integer(8888)

########################################################################## INIT

if __name__ == '__main__':
    ini = sys.argv[0][:-3]+'.ini'
    for source in [ini] + sys.argv[1:]:
        with open(source) as SourceFile:
            vm // SourceFile.read()
            INTERPRET(vm)
#     REPL()
#     WEB()
