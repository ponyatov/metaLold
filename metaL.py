## metaL/Python: FORTH-like metaprogramming language implementation
## (c) Dmitry Ponyatov <dponyatov@gmail.com> CC BY-NC-ND
 
import os,sys,re
 
################################################# extended Marvin Minsky frames
 
class Frame:
    def __init__(self,V):
        self.type  = self.__class__.__name__.lower()
        self.val   = V
        self.slot  = {}
        self.nest  = []
        self.immed = False

    ################################################################## printing
 
    def __repr__(self):
        return self.dump()

    def dump(self, depth=0, prefix='', voc=True):
        tree = self._pad(depth) + self.head(prefix)
        if not depth: Frame._dumped = []
        if self in Frame._dumped: return tree + ' _/'
        else: Frame._dumped.append(self)
        if voc:
            for i in self.slot:
                tree += self.slot[i].dump(depth + 1, prefix=i + ' = ')
        for j in self.nest:
            tree += j.dump(depth + 1)
        return tree
    def head(self, prefix=''):
        return '%s<%s:%s> @%x' % (prefix, self.type, self.valdump(), id(self))
    def valdump(self):
        return str(self.val)
    def _pad(self, depth):
        return '\n' + '\t' * depth
    
    ############################################### slot manipulation operators
    
    def __getitem__(self,key):
        return self.slot[key]
    def __setitem__(self,key,that):
        self.slot[key] = that ; return self
    def __lshift__(self,that):
        self[that.val] = that ; return self
    def __floordiv__(self,that):
        return self.push(that)
        
    ############################################## stack operations over nest[]

    def push(self,that):
        self.nest.append(that) ; return self
    def pop(self):
        return self.nest.pop(-1)
    def pip(self):
        return self.nest.pop(-2)
    def top(self):
        return self.nest[-1]
    def tip(self):
        return self.nest[-2]
    def dropall(self):
        self.nest = []
    def dup(self):
        return self // self.top()
    def drop(self):
        self.pop() ; return self
    def swap(self):
        return self // self.pip()
    def over(self):
        return self // self.tip()
    def press(self):
        self.pip() ; return self
        
#     ################################################################# plotting
#     
#     graphed = []
#     def graph(self,kxgraph,depth=0):
#         if not depth: Frame.graphed = []
#         if self not in Frame.graphed:
#             Frame.graphed.append(self)
#             for i in self.attr:
#                 kxgraph.add_edge(self.value,i)
#                 self.attr[i].graph(kxgraph,depth+1)
# 
    ################################### execution, conversion & code generation
    
    def eval(self,vm):
        return vm // self
        
    def str(self):
        return str(self.val)
    
    def gen(self):
        src = self.val
        for i in self.nest: src += i.gen() + '\n'
        return src

##################################################################### primitive

class Primitive(Frame):
    def gen(self):
        return self.str()
        
class Symbol(Primitive): pass

class String(Primitive):
    def valdump(self):
        S = ''
        for c in self.value:
            if    c == '\n': S += '\\n'
            elif  c == '\t': S += '\\t'
            else: S += c
        return S

class Number(Primitive):
    
    def add(self,obj):
        if isinstance(obj,Number): return Number(self.val + obj.val)
        else: raise TypeError(obj)
    def sub(self,obj):
        if isinstance(obj,Number): return Number(self.val - obj.val)
        else: raise TypeError(obj)
    def mul(self,obj):
        if isinstance(obj,Number): return Number(self.val * obj.val)
        else: raise TypeError(obj)
    def div(self,obj):
        if isinstance(obj,Number): return Number(self.val / obj.val)
        else: raise TypeError(obj)
    def mod(self,obj):
        if isinstance(obj,Number): return Number(self.val % obj.val)
        else: raise TypeError(obj)
    def neg(self):
        return Number(-self.val)
    
    def toint(self):
        return Integer(self.val)

class Integer(Number):
    def toint(self):
        return self
    def tohex(self):
        return Hex(self.val)
    def tobin(self):
        return Bin(self.val)

class Hex(Integer):
    def valdump(self):
        return hex(self.val)
    def toint(self):
        return Integer(self.val)
    
class Bin(Integer):
    def valdump(self):
        return bin(self.val)
    def toint(self):
        return Integer(self.val)

##################################################################### container
        
class Container(Frame): pass

class Group(Container): pass
 
class Vector(Container): pass        

class Stack(Container): pass

class Queue(Container): pass        

class Dict(Container): pass

######################################################################## active

class Active(Frame): pass

class VM(Active):
    def __lshift__(self,F):
        if callable(F): return self << Cmd(F)
        else: return Active.__lshift__(self, F)

class Cmd(Active):
    def __init__(self,F,I=False):
        Frame.__init__(self, F.__name__)
        self.fn = F
        self.immed = I
    def eval(self,vm):
        for i in self.nest: vm // i
        self.fn(vm)
    def cp(self):
        return Cmd(self.fn)
        
class Seq(Active): pass

########################################################################## meta
 
class Meta(Frame): pass

class Var(Meta): pass

class Type(Meta): pass

class Fn(Meta): pass
 
# ############################################################################ io
#     
# class IO(Frame): pass
#     
# class Dir(IO): pass
# class File(IO):
#     def gen(self):
#         return self.head() + '\n\n' + Frame.gen(self)
#

######################################################### virtual FORTH machine

vm = VM('metaL')

######################################################################### debug

def BYE(vm): sys.exit(0)
vm << BYE

def Q(vm): print(vm.dump(voc=False))
vm['?'] = Cmd(Q,I=True)

def QQ(vm): print(vm.dump(voc=True))
vm['??'] = Cmd(QQ,I=True)

######################################################################### stack

def DROPALL(vm): vm.dropall()
vm['.'] = Cmd(DROPALL)

def DUP(vm): vm.dup()
vm << DUP

def DROP(vm): vm.drop()
vm << DROP

def SWAP(vm): vm.swap()
vm << SWAP

def OVER(vm): vm.over()
vm << OVER
 
def PRESS(vm): vm.press()
vm << PRESS

########################################################################## math
 
def ADD(vm):
    B = vm.pop() ; A = vm.pop() ; vm // A.add(B)
vm['+'] = Cmd(ADD)
 
def SUB(vm):
    B = vm.pop() ; A = vm.pop() ; vm // A.sub(B)
vm['-'] = Cmd(SUB)
 
def MUL(vm):
    B = vm.pop() ; A = vm.pop() ; vm // A.mul(B)
vm['*'] = Cmd(MUL)
 
def DIV(vm):
    B = vm.pop() ; A = vm.pop() ; vm // A.div(B)
vm['/'] = Cmd(DIV)
 
def MOD(vm):
    B = vm.pop() ; A = vm.pop() ; vm // A.mod(B)
vm['%'] = Cmd(MOD)
 
def NEG(vm):
    B = vm.pop() ; A = vm.pop() ; vm // A.neg()
vm << NEG

#################################################################### converting

def toINT(vm):
    vm // vm.pop().toint()
vm['>INT'] = Cmd(toINT)

def toHEX(vm):
    vm // vm.pop().tohex()
vm['>HEX'] = Cmd(toHEX)

def toBIN(vm):
    vm // vm.pop().tobin()
vm['>BIN'] = Cmd(toBIN)
 
# ########################################################################## i/o

#         
# def FILE():
#     WORD() ; S // File(S.pop().value) ; W << S.top() 
# W << FILE
# 
# def DIR():
#     WORD() ; S // Dir(S.pop().value) ; W << S.top() 
# W << DIR
# 

# ################################################################# manipulations
# 
# def PUSH():
#     B = S.pop() ; S.top() // B
# W['//'] = CMD(PUSH)
# 
# def RSHIFT():
#     WORD() ; FIND() ; B = S.pop() ; A = S.pop() ; A >> B
# W['>>'] = CMD(RSHIFT)
# 
# ############################################################### METAPROGRAMMING
# 
# class Meta(Frame): pass
# 
# class Class(Meta): pass
# 
# def CLASS():
#     # forward symbol lookup
#     WORD()
#     # push new class created from top symbol
#     S // Class(S.pop().str())
#     # register created class in global vocabulary
#     W << S.top()
# W << CLASS
# 
# def SUPER():
#     # copy superclass from stack
#     super = S.top()
#     # create new class on stack
#     CLASS()
#     # create superclass slot
#     S.top()['super'] = super 
# W << SUPER
# 
# class Project(Meta): pass
# 
# ########################################################################### WEB
# 
# def WEB():
#     from flask     import Flask,render_template,escape
#     from flask_wtf import FlaskForm
#     from wtforms   import TextAreaField,SubmitField
#     
#     web = Flask(__name__)
#     web.config['SECRET_KEY'] = os.urandom(32)
#     
#     class CLI(FlaskForm):
#         pad = TextAreaField('pad',
#                             render_kw={'rows':5,'autofocus':'true'},
#                             default='# put your commands here')
#         go = SubmitField('go')
#     
#     @web.route('/', methods=['GET', 'POST'])
#     def index():
#         form = CLI()
#         if form.validate_on_submit():
#             S // String(form.pad.data) ; INTERPRET()
#         return render_template('index.html',W=W,form=form)
#     
#     @web.route('/css/<path:path>')
#     def css(path): return web.send_static_file(path)
#     
#     @web.route('/dump/<path:frame>')
#     def dump(frame): return render_template('dump.html',dump=W[frame].dump())
#     
#     @web.route('/viz/<path:frame>')
#     def viz(frame):
#         S='"%s"' % frame
#         for i in W[frame].attr.keys():
#             S += ',"%s"'%i
#         return render_template('viz.html',dump=S)
#     
#     web.run(host=W['WEB']['IP'].value,port=W['WEB']['PORT'].value,debug=True)
# W << WEB
# W['WEB']['IP']   = String('127.0.0.1')
# W['WEB']['PORT'] = Integer(8888)

###################################################################### compiler

vm.COMPILE = []

# def COMMA(vm): vm.COMPILE[-1] // vm.pop()

def LC(vm): vm.COMPILE.append( Seq('') ) 
vm['{'] = Cmd(LC,I=True)

def LQ(vm): vm.COMPILE.append( Vector('') )
vm['['] = Cmd(LQ,I=True)

def RC(vm):
    vm // vm.COMPILE.pop()
#     if vm.COMPILE: COMMA()
vm['}'] = Cmd(RC,I=True)

def RQ(vm): RC(vm)
vm[']'] = Cmd(RQ,I=True)

def TILD(vm):
    WORD(vm) ; sym = vm.pop() ; vm // ( vm['FIND'].copy() // sym )
#     if COMPILE: COMMA()
#     else:       EXECUTE()
vm['~'] = Cmd(TILD,I=True)

def DEF(vm):
    vm << vm.top()
vm << DEF

############################################################# PLY powered lexer

import ply.lex as lex

tokens = ['symbol','string','hex','bin','integer']

t_ignore = ' \t\r\n'

def t_comment(t): r'[\#\\].*'

states = (('str','exclusive'),)
t_str_ignore = ''

def t_string(t):
    r'\''
    t.lexer.lexstring=''
    t.lexer.push_state('str')
def t_str_string(t):
    r'\''
    t.lexer.pop_state()
    return String(t.lexer.lexstring)
def t_str_char(t):
    r'.'
    t.lexer.lexstring += t.value

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
    r'[`~]|[^ \t\r\n]+'
    return Symbol(t.value)

def t_ANY_error(t): raise SyntaxError(t)

vm.lexer = lex.lex()

################################################################### interpreter

def QUOTE(vm):
    WORD(vm)
vm['`'] = Cmd(QUOTE,I=True)

def WORD(vm):
    token = vm.lexer.token()
    if not token: return False
    vm // token  ; return True
vm << WORD

def FIND(vm):
    token = vm.pop().str()
    try: vm // vm[token]
    except KeyError:
        try: vm // vm[token.upper()]
        except KeyError:
            raise SyntaxError(token)
vm << FIND

def EVAL(vm):
    vm.pop().eval(vm)    

def INTERPRET(vm):
    vm.lexer.input(vm.pop().val)
    while True:
        if not WORD(vm): break
        if isinstance(vm.top(), Symbol):
            FIND(vm)
        if not vm.COMPILE or vm.top().immed:
            EVAL(vm)
        else:
            COMMA(vm)
vm << INTERPRET

def REPL(vm):
    while True:
        Q(vm)
        try: vm // String(raw_input('-'*40 + '\nok> '))
        except EOFError: BYE(vm)
        INTERPRET(vm)
vm << REPL

########################################################################### GUI

import wx,wx.stc

class GUI(Frame):
    def __init__(self,V):
        Frame.__init__(self, V)
        self.app = wx.App()
        self['main' ] = self.main  = Editor(V)
        self['stack'] = self.stack = Editor(V+'.stack')
        self['words'] = self.words = Editor(V+'.words')
    def start(self):
        self.main.Show()
        self.main.onUpdate(None)
        self.app.MainLoop()

## https://github.com/ponyatov/orth/blob/master/ORTH.py
class Editor(GUI,wx.Frame):
    def __init__(self,V):
        Frame.__init__(self, V)
        wx.Frame.__init__(self,parent=None,title=V)
        self.initMenu()
        self.initEditor()

    def initMenu(self):
        self.menubar = wx.MenuBar()
        self.SetMenuBar(self.menubar)
        # file
        self.file = wx.Menu() ; self.menubar.Append(self.file,'&File')
        # file/save
        self.file.save = self.file.Append(wx.ID_SAVE,'&Save')
        self.Bind(wx.EVT_MENU,self.onSave,self.file.save)
        # file/quit
        self.file.quit = self.file.Append(wx.ID_EXIT,'&Quit')
        self.Bind(wx.EVT_MENU,self.onQuit,self.file.quit)
        # debug
        self.debug = wx.Menu() ; self.menubar.Append(self.debug,'&Debug')
        self.debug.update = self.debug.Append(wx.ID_REFRESH,'&Update\tF12')
        self.Bind(wx.EVT_MENU,self.onUpdate,self.debug.update)
        # debug/stack
        self.debug.stack = self.debug.Append(wx.ID_ANY,'&Stack\tF9',kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU,self.onStack,self.debug.stack)
        # debug/words
        self.debug.words = self.debug.Append(wx.ID_ANY,'&Words\tF8',kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU,self.onWords,self.debug.words)
        # help
        self.help = wx.Menu() ; self.menubar.Append(self.help,'&Help')
        self.help.about = self.help.Append(wx.ID_ABOUT,'&About\tF1')
        self.Bind(wx.EVT_MENU,self.onAbout,self.help.about)
    def onSave(self,e):
        with open(self.val,'w') as file:
            file.write(self.editor.GetValue())
    def onQuit(self,e):
        vm['gui'].stack.Close()
        vm['gui'].words.Close()
        vm['gui'].main.Close()
    def onUpdate(self,e):
        vm['gui'].stack.editor.SetValue(vm.dump(voc=False))
        vm['gui'].words.editor.SetValue(vm.dump(voc=True ))
    def onAbout(self,e):
        with open('README.md') as file: info = file.read()
        wx.MessageBox(info,'About',wx.OK|wx.ICON_INFORMATION)
        
    def onStack(self,event):
        if vm['gui'].stack.IsShown(): vm['gui'].stack.Hide()
        else:                         vm['gui'].stack.Show() ; self.onUpdate(event)        
    def onWords(self,event):
        if vm['gui'].words.IsShown(): vm['gui'].words.Hide()
        else:                         vm['gui'].words.Show() ; self.onUpdate(event)        

    def initEditor(self):
        self.editor = wx.stc.StyledTextCtrl(self)
        self.font = wx.Font(14, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.editor.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,
            "face:%s,size:%d" % (
                self.font.GetFaceName(), self.font.GetPointSize()
            ))
        try:
            with open(self.val,'r') as file:
                self.editor.SetValue(file.read())
        except IOError: pass
        
################################################################### system init

if __name__ == '__main__':
    infiles = sys.argv[1:] ; print infiles
    for i in infiles:
        vm // String(open(i).read()) ; INTERPRET()
#     REPL(vm)
    vm['gui'] = GUI(re.sub(r'\.[a-z]+$',r'.ml',sys.argv[0])) ; vm['gui'].start()
