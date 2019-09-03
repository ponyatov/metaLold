## metaL/py : homoiconic metaprogramming system
## (c) Dmitry Ponyatov <dponyatov@gmail.com> CC BY-NC-ND
## wiki: https://github.com/ponyatov/metaL/wiki

import os,sys

########################################## Marvin Minsky frame model /extended/

class Frame:
    
    def __init__(self, V, line=None):
        self.type  = self.__class__.__name__.lower()
        self.val   = V
        self.slot  = {}
        self.nest  = []
        self.immed = False
        if line: self.line = line
        
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
        return '\n' + '\t' * depth
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
        self.nest.append(that) ; return self
        
    ################################ stack
    
    ## ` ( ... -- ) ` clear
    def dropall(self):
        self.nest = [] ; return self
    ## ` ( -- a ) `
    def push(self,that):
        return self // that
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
    
    def test(self,depth=0,prefix='',voc=True):
        tree = '\t' * depth + '%s<%s:%s>' % (prefix, self.type, self._val())
        if not depth: Frame._dumped = []
        if self in Frame._dumped: return tree + ' _/'
        else: Frame._dumped.append(self)
        if voc:
            for i in self.slot: tree += self.slot[i].test(depth+1,prefix=i+' ')
        for j in self.nest: tree += j.test(depth+1)
        return tree
    
    ################################ plotting
    
    def plot(self,depth=0,parent=None,link=None):
        nodes = ''
        par = ''
        if parent: par = ', parent:0x%x ' % id(parent)
        if link: par += ', link:"%s" ' % link
        def key(what):
            return '\n{ key: 0x%x, head:"%s:%s" %s },' % \
                (id(what),what.type,what._val(),par) 
        nodes += key(self)
        if not depth: Frame._ploted = []
        if self in Frame._ploted: return nodes
        else: Frame._ploted.append(self)
        for i in self.slot:
            nodes += self.slot[i].plot(depth+1,parent=self,link=i)
        count = 0
        for j in self.nest:
            count += 1
            nodes += j.plot(depth+1,parent=self,link=count)
        return nodes
    
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
    def __add__(self,that):
        if isinstance(that,Number): return Number(self.val + that.val)
        else: raise TypeError(that)
    def __sub__(self,that):
        if isinstance(that,Number): return Number(self.val - that.val)
        else: raise TypeError(that)
    def __mul__(self,that):
        if isinstance(that,Number): return Number(self.val * that.val)
        else: raise TypeError(that)
    def __div__(self,that):
        return self.__truediv__(that)
    def __truediv__(self,that):
        if isinstance(that,Number): return Number(self.val / that.val)
        else: raise TypeError(that)
    def __mod__(self,that):
        if isinstance(that,Number): return Number(self.val % that.val)
        else: raise TypeError(that)
    def __neg__(self):
        return Number(-self.val)
    def __int__(self):
        return int(self.val)
    def toint(self):
        return Integer(int(self))

class Integer(Number):
    def __init__(self,V):
        Primitive.__init__(self, int(V))
    def __int__(self):
        return self.val
    def toint(self):
        return self

class Hex(Integer):
    def __init__(self,V):
        Integer.__init__(self, int(V[2:],0x10))
    def _val(self):
        return '0x{0:X}'.format(self.val)
    def __int__(self):
        return self.val
    def toint(self):
        return Integer(self.val)

class Bin(Integer):
    def __init__(self,V):
        Integer.__init__(self, int(V[2:],0x02))
    def _val(self):
        return '0b{0:b}'.format(self.val)
    def __int__(self):
        return self.val
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
    def __init__(self,V):
        Active.__init__(self, V)
        self.compile = []
        self.lexer = []
    def __setitem__(self,key,F):
        if callable(F): self[key] = Cmd(F)
        else: Active.__setitem__(self, key, F)
    def __lshift__(self,F):
        if callable(F): self << Cmd(F)
        else: Active.__lshift__(self, F)
        
class Seq(Active,Vector):
    def eval(self,ctx):
        for j in self.nest: j.eval(ctx)

################################################################## input/output

class IO(Frame): pass

class Dir(IO): pass

class File(IO):
    def gen(self):
        return self.head() + '\n\n' + Frame.gen(self)

####################################################################### network

class Net(IO): pass

class Protocol(Net): pass

class IP(Protocol): pass

class Port(Net,Integer): pass

class Email(Net): pass

class Url(Net): pass

############################################################### metaprogramming

class Meta(Frame): pass

class Group(Meta): pass

class Module(Meta): pass

class Compiler(Meta): pass

######################################################### Python code generator

class Python(Meta): pass

class Import(Python,Module):
    def __init__(self,V):
        Python.__init__(self,V)
        self.module = __import__(V)
        
################################################# embedded C/C++ code generator

class C(Meta): pass
class Cpp(C): pass

class CC(Compiler): pass

class GNU(CC): pass

class IAR(CC): pass

class cType(C): pass

class cInt(cType,Integer): pass

################################################### documenting & visualization

class Doc(Frame): pass

class Color(Doc): pass

class Font(Doc): pass

class Size(Doc): pass

################################################################## web platform

class Web(Net):
    
    def __init__(self,V):
        Net.__init__(self, V)
        self['IP'  ] = IP('127.0.0.1')
        self['PORT'] = Port(8888)
        self['font'] = Font('monospace')
        self['font']['size'] = Size('3mm')
        self['back']  = Color('black')
        self['color'] = Color('lightgreen')

    def eval(self,ctx):
        from flask     import Flask,render_template,escape
        from flask_wtf import FlaskForm
        from wtforms   import TextAreaField,SubmitField
        
        app = Flask(self.val)
        app.config['SECRET_KEY'] = os.urandom(32)

        class CLI(FlaskForm):
            pad = TextAreaField('pad',
                                render_kw={'rows':5,'autofocus':'true'},
                                default='# put your commands here')
            go = SubmitField('go')
    
        @app.route('/', methods=['GET', 'POST'])
        def index():
            form = CLI()
            if form.validate_on_submit():
                S // String(form.pad.data) ; INTERPRET()
            return render_template('index.html',ctx=ctx,web=self)

#    @web.route('/viz/<path:frame>')
#    def viz(frame):
#        S='"%s"' % frame
#        for i in W[frame].attr.keys():
#            S += ',"%s"'%i
#        return render_template('viz.html',dump=S)
        
        @app.route('/favicon.ico')
        @app.route('/logo.png')
        def logo():
            return self.app.send_static_file('logo.png')
        
        @app.route('/<path>.css')
        def css(path):
            return flask.Response(\
                    flask.render_template(path+'.css',ctx=ctx,web=self),\
                    mimetype='text/css')
            
        @app.route('/<path:path>')
        def console(path):
            frame = ctx
            for i in path.split('/'): frame = frame[i]
            return flask.render_template('index.html',ctx=frame,web=self)
        
        @app.route('/dump/<path:path>')
        def dump(path):
            frame = ctx
            for i in path.split('/'): frame = frame[i]
            return flask.render_template('dump.html',ctx=frame,web=self)
        
        @app.route('/<path>.js')
        def jslib(path):
            return self.app.send_static_file(path + '.js')
        
        @app.route('/plot/<path:path>')
        def plot(path):
            frame = ctx
            for i in path.split('/'): frame = frame[i]
            return flask.render_template('plot.html',ctx=frame,web=self)
        
        @app.route('/icon/<path>.png')
        def icon(path):
            return self.app.send_static_file('icon/%s.png' % path )
        
        self.app.run(host=self['IP'].val, port=self['PORT'].val,\
                     debug=True, extra_files='metaL.ini')

############################################################### virtual machine

vm = VM('metaL') ; vm['vm'] = vm

######################################################################### debug

def BYE(ctx): sys.exit(0)
vm << BYE

def Q(ctx): print(ctx.dump(voc=True)) ; BYE(ctx)
vm['?'] = Cmd(Q,I=True)

def QS(ctx): print(ctx.dump(voc=False))
vm['?s'] = Cmd(QS,I=True)

def QW(ctx): print(ctx.dump(voc=True)) ; BYE(ctx)
vm['?w'] = Cmd(QW,I=True)

def QC(ctx): print(ctx.compile)
vm['?c'] = Cmd(QC,I=True)

################################################################### stack fluff

def DUP(ctx): ctx.dup()
vm << DUP

def DROP(ctx): ctx.drop()
vm << DROP

def SWAP(ctx): ctx.swap()
vm << SWAP

def PRESS(ctx): ctx.press()
vm << PRESS

# ( ... -- )
def DOT(ctx): ctx.dropall()
vm['.'] = DOT

# ( a b -- a ) ctx[b] = a
def EQ(ctx):
    where = ctx.pop() ; what = ctx.top() ; ctx[where.val] = what
vm['='] = EQ

# ( a b -- a ) a // b
def PUSH(ctx):
    what = ctx.pop() ; where = ctx.top() ; where // what
vm['//'] = PUSH

# ( a b c -- a ) b[c] = b
def STOR(ctx):
    where = ctx.pop() ; what = ctx.pop() ; ctx.top()[where.val] = what
vm['/='] = STOR

########################################################################## math

def ADD(ctx):
	B = ctx.pop() ; A = ctx.pop() ; ctx // A.add(B)
vm['+'] = ADD

def SUB(ctx):
	B = ctx.pop() ; A = ctx.pop() ; ctx // A.sub(B)
vm['-'] = SUB

def MUL(ctx):
	B = ctx.pop() ; A = ctx.pop() ; ctx // A.mul(B)
vm['*'] = MUL

def DIV(ctx):
	B = ctx.pop() ; A = ctx.pop() ; ctx // A.div(B)
vm['/'] = DIV

def MOD(ctx):
	B = ctx.pop() ; A = ctx.pop() ; ctx // A.mod(B)
vm['%'] = MOD

def NEG(ctx):
	B = ctx.pop() ; A = ctx.pop() ; ctx // A.neg()
vm << NEG

################################################################## input/output

def DIR(ctx): ctx // Dir(ctx.pop().val)
vm << DIR

def FILE(ctx): ctx // File(ctx.pop().val)
vm << FILE

####################################################################### network

def EMAIL(ctx): ctx // Email(ctx.pop().val)
vm << EMAIL

################################################# embedded C/C++ code generator

vm << GNU('gcc')
vm << GNU('g++')
vm << IAR('msp430')

############################################################## no-syntax parser

import ply.lex as lex

tokens = ['symbol','string','number','integer','hex','bin']

states = (('str','exclusive'),)

t_str_ignore = ''
def t_str(t):
    r'\'[\r\n]?'
    t.lexer.push_state('str')
    t.lexer.string = ''
def t_str_str(t):
    r'[\r\n]?\''
    t.lexer.pop_state()
    return String(t.lexer.string)
def t_str_tab(t):
    r'\\t'
    t.lexer.string += '\t'
def t_str_lf(t):
    r'\\n'
    t.lexer.string += '\n'
def t_str_eol(t):
    r'\n'
    t.lexer.string += t.value
def t_str_char(t):
    r'.'
    t.lexer.string += t.value

t_ignore = ' \t\r\n'

t_ignore_comment = r'[\#\\].*'

def t_hex(t):
    r'0x[0-9a-fA-F]+'
    return Hex(t.value)

def t_bin(t):
    r'0b[01]+'
    return Bin(t.value)

def t_number_dot(t):
    r'[+\-]?[0-9]+\.[0-9]*'
    return Number(t.value)

def t_number_exp(t):
    r'[+\-]?[0-9]+(\.[0-9]*)?[eE][+\-]?[0-9]+'
    return Number(t.value)

def t_integer(t):
    r'[+\-]?[0-9]+'
    return Integer(t.value)

def t_symbol(t):
    r'`|[^ \t\r\n\#\\]+'
    return Symbol(t.value)

def t_ANY_error(t): raise SyntaxError(t)

def INC(ctx):
    WORD(ctx) ; file = ctx.pop().val
    lexer = lex.lex() ; ctx.lexer += [lexer]
    with open(file) as F: lexer.input(F.read())
vm['.inc'] = INC

################################################################### interpreter

def QUOTE(ctx):
    WORD(ctx)
    if ctx.compile: COMPILE(ctx)
vm['`'] = Cmd(QUOTE,I=True)

def WORD(ctx):
    token = ctx.lexer[-1].token()
    if token: ctx // token
    if not token:                       # on EOF using .inc
        ctx.lexer.pop()                 # drop finished lexer
        if ctx.lexer: return WORD(ctx)  # recurse if nested
    return token

def FIND(ctx):
    token = ctx.pop()
    try: ctx // ctx[token.val] ; return True
    except KeyError:
        try: ctx // ctx[token.val.upper()] ; return True
        except KeyError:
            ctx // token ; return False
    
def EVAL(ctx):
    ctx.pop().eval(ctx)

def INTERPRET(ctx):
    ctx.lexer.append(lex.lex())
    ctx.lexer[-1].input(ctx.pop().val)
    while True:
        if not WORD(ctx): break
        if isinstance(ctx.top(), Symbol):
            if not FIND(ctx): raise SyntaxError(ctx.pop())
        if not ctx.compile or ctx.top().immed:
            EVAL(ctx)
        else:
            COMPILE(ctx)
        
def REPL(ctx):
    while True:
        print(S)
        try: S // String(raw_input('ok> ')) ; INTERPRET(ctx)
        except EOFError: BYE()
vm << REPL
        
###################################################################### compiler

# ( any -- ) add object to current compilation block
def COMPILE(ctx): ctx.compile[-1] // ctx.pop()

def LQ(ctx): ctx.compile.append(Vector(''))
vm['['] = Cmd(LQ,I=True)

def LC(ctx): ctx.compile.append(Seq(''))
vm['{'] = Cmd(LC,I=True)

def RQC(ctx):
    block = ctx.compile.pop()
    try: ctx.compile[-1] // block
    except IndexError: ctx // block 
vm[']'] = Cmd(RQC,I=True)
vm['}'] = Cmd(RQC,I=True)

# [ 1 $ 2 3 + $ 4 ] -> [ 1 5 4] execute code in compile mode
def INLINE(ctx):
    if ctx.compile:
        ctx.inline = ctx.compile ; ctx.compile = []
    else:
        ctx.compile = ctx.inline ; COMPILE(ctx)
vm['$'] = Cmd(INLINE,I=True)

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
vm << CLASS

def SUPER():
    # copy superclass from stack
    super = S.top()
    # create new class on stack
    CLASS()
    # create superclass slot
    S.top()['super'] = super 
vm << SUPER

class Project(Meta): pass

################################################################## web platform

def WEB(ctx): ctx['WEB'] = Web('metaL') ; ctx['WEB'].eval(ctx)
vm << WEB

################################################################### system init

def INIT(ctx):
    files = sys.argv[1:]
    if not files: files = [ 'metaL.ini' ]
    for file in files:
        ctx // String(open(file).read()) ; INTERPRET(ctx)

if __name__ == '__main__': INIT(vm)
