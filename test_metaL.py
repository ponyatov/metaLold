
from metaL import *

import re

########################################## Marvin Minsky frame model /extended/

class TestFrame:
    
    def test_empty(self):
        assert Frame('').test() == '<frame:>'

    def test_hello(self):
        hello = Frame('hello')
        assert hello.test() == '<frame:hello>'
        
    def test_dump_pad(self):
        hello = Frame('hello')
        assert hello._pad(2) == '\n' + '\t' * 2
    
    def test_dump_val(self):
        hello = Frame('hello')
        assert hello._val() == 'hello'
    
    def test_dump_head(self):
        hello = Frame('hello')
        assert re.match(r'<frame:hello> @[0-9a-f]+',hello.head())
    
    def test_dump(self):
        hello = Frame('hello')
        world = Frame('world')
        hello << world // world
        print(hello)
        h = r' @[0-9a-f]+'
        a = r'\n<frame:hello>'+h
        b = r'\n\s+world = <frame:world>'+h
        c = r'\n\s+<frame:world>'+h
        assert re.match(a+b+c,hello.__repr__())
        
    def test_operator_set(self):
        hello = Frame('hello')
        world = Frame('world')
        hello['key'] = world
        assert hello.test() == '<frame:hello>\tkey <frame:world>'

    def test_operator_get(self):
        hello = Frame('hello')
        world = Frame('world')
        hello['key'] = world
        assert hello['key'].test() == '<frame:world>'

    def test_operator_shift(self):
        hello = Frame('hello')
        world = Frame('world')
        hello << world
        assert hello.test() == '<frame:hello>\tworld <frame:world>'

    def test_operator_haskey(self):
        hello = Frame('hello')
        world = Frame('world')
        hello['key'] = world
        hello << world
        assert hello.has('key')
        assert hello.has('world')
        assert not hello.has('nothing')

    def test_operator_push(self):
        hello = Frame('hello')
        world = Frame('world')
        hello // hello // world 
        assert hello.test() == '<frame:hello>\t<frame:hello> _/\t<frame:world>'
    
    def test_stack_dropall(self):
        hello = Frame('hello')
        world = Frame('world')
        hello // hello // world 
        assert hello.dropall().test() == '<frame:hello>'
    
    def test_stack_push(self):
        hello = Frame('hello')
        world = Frame('world')
        hello.push(world) 
        assert hello.test() == '<frame:hello>\t<frame:world>'
    
    def test_stack_pop(self):
        hello = Frame('hello')
        a = Frame('a')
        b = Frame('b')
        hello // a // b
        assert hello.test() == '<frame:hello>\t<frame:a>\t<frame:b>' 
        assert hello.pop().test() == '<frame:b>'
        assert hello.test() == '<frame:hello>\t<frame:a>' 
    
    def test_stack_pip(self):
        hello = Frame('hello')
        a = Frame('a')
        b = Frame('b')
        hello // a // b
        assert hello.test() == '<frame:hello>\t<frame:a>\t<frame:b>' 
        assert hello.pip().test() == '<frame:a>'
        assert hello.test() == '<frame:hello>\t<frame:b>' 
    
    def test_stack_top(self):
        hello = Frame('hello')
        a = Frame('a')
        b = Frame('b')
        hello // a // b
        assert hello.test() == '<frame:hello>\t<frame:a>\t<frame:b>' 
        assert hello.top().test() == '<frame:b>'
        assert hello.test() == '<frame:hello>\t<frame:a>\t<frame:b>' 
    
    def test_stack_tip(self):
        hello = Frame('hello')
        a = Frame('a')
        b = Frame('b')
        hello // a // b
        assert hello.test() == '<frame:hello>\t<frame:a>\t<frame:b>' 
        assert hello.tip().test() == '<frame:a>'
        assert hello.test() == '<frame:hello>\t<frame:a>\t<frame:b>' 

    def test_stack_dup(self):
        hello = Frame('hello')
        a = Frame('a')
        hello // a
        assert hello.dup().test() == '<frame:hello>\t<frame:a>\t<frame:a> _/'
    
    def test_stack_drop(self):
        hello = Frame('hello')
        a = Frame('a')
        b = Frame('b')
        hello // a // b
        assert hello.drop().test() == '<frame:hello>\t<frame:a>'
    
    def test_stack_swap(self):
        hello = Frame('hello')
        a = Frame('a')
        b = Frame('b')
        hello // a // b
        assert hello.swap().test() == '<frame:hello>\t<frame:b>\t<frame:a>'
    
    def test_stack_over(self):
        hello = Frame('hello')
        a = Frame('a')
        b = Frame('b')
        hello // a // b
        assert hello.over().test() == '<frame:hello>\t<frame:a>\t<frame:b>\t<frame:a> _/'
    
    def test_stack_press(self):
        hello = Frame('hello')
        a = Frame('a')
        b = Frame('b')
        hello // a // b
        assert hello.press().test() == '<frame:hello>\t<frame:b>'
    
    def test_eval(self):
        hello = Frame('hello')
        assert hello.eval(hello).test() == '<frame:hello>\t<frame:hello> _/'


##################################################################### primitive

class TestString:
    
    def test_String(self):
        str = String("hello\n\tworld")
        h = r' @[0-9a-f]+'
        assert re.match(r'<string:hello\\n\\tworld>'+h,str.head())
        
        
class TestSymbol:
    
    def test_Symbol(self):
        assert True

class TestNumber:
    
    def test_Number(self):
        num = Number('-012.340')
        assert type(num.val) == float
        assert num.test() == '<number:-12.34>'
        
    def test_add(self):
        a = Number(-12.34)
        b = Number(+56.78)
        c = String('')
        assert (a+b).test() == '<number:44.44>'
        try: a+c ; assert False
        except TypeError: assert True

    def test_sub(self):
        a = Number(-12.34)
        b = Number(+56.78)
        c = String('')
        assert (a-b).test() == '<number:-69.12>'
        try: a-c ; assert False
        except TypeError: assert True

    def test_mul(self):
        a = Number(-12.34)
        b = Number(+56.78)
        c = String('')
        assert (a*b).test() == '<number:-700.6652>'
        try: a*c ; assert False
        except TypeError: assert True

    def test_div(self):
        a = Number(-12.34)
        b = Number(+56.78)
        c = String('')
        assert (a/b).test() == '<number:-0.2173300457907714>'
        assert (a.__div__(b)).test() == '<number:-0.2173300457907714>'
        try: a/c ; assert False
        except TypeError: assert True

    def test_mod(self):
        a = Number(-12.34)
        b = Number(+56.78)
        c = String('')
        assert (a%b).test() == '<number:44.44>'
        try: a%c ; assert False
        except TypeError: assert True

    def test_neg(self):
        a = Number(-12.34)
        assert (-a).test() == '<number:12.34>'
        
    def test_int(self):
        a = Number(-12.34)
        b = int(a)
        assert b == -12

    def test_toint(self):
        a = Number(-12.34)
        b = a.toint()
        assert b.test() == '<integer:-12>'

class TestInteger:
    
    def test_Integer(self):
        num = Integer('-01234')
        assert type(num.val) == int
        assert num.test() == '<integer:-1234>'
        
    def test_int(self):
        a = Integer(-12.34)
        b = int(a)
        assert b == -12

    def test_toint(self):
        a = Integer(-12.34)
        b = a.toint()
        assert b.test() == '<integer:-12>'

class TestHex:
    
    def test_hex(self):
        hex = Hex('0xDeadBeef')
        assert type(hex.val) == int
        assert hex.test() == '<hex:0xDEADBEEF>'
        
    def test_int(self):
        a = Hex('0xDeadBeef')
        b = int(a)
        assert b == 3735928559

    def test_toint(self):
        a = Hex('0xDeadBeef')
        b = a.toint()
        assert b.test() == '<integer:3735928559>'

class TestBin:
    
    def test_bin(self):
        bin = Bin('0b1101')
        assert type(bin.val) == int
        assert bin.test() == '<bin:0b1101>'

    def test_int(self):
        a = Bin('0b1101')
        b = int(a)
        assert b == 13

    def test_toint(self):
        a = Bin('0b1101')
        b = a.toint()
        assert b.test() == '<integer:13>'

############################################################## no-syntax parser

class TestPLY:
    
    def test_eol(self):
        lexer = lex.lex()
        lexer.input("'\\t\\r\nx'")
        assert lexer.token().test() == r'<string:\t\r\nx>'
        
    def test_inc(self):
        vm // String('.inc /dev/null') ; INTERPRET(vm)
        assert vm.test(voc=False) == '<vm:metaL>'

################################################################### interpreter

class TestInterpreter:
    
    def test_empty(self):
        DOT(vm)
        assert vm.test(voc=False) == '<vm:metaL>'
        vm // String('')
        assert vm.test(voc=False) == '<vm:metaL>\t<string:>'
        INTERPRET(vm)
        assert vm.test(voc=False) == '<vm:metaL>'
        
    def test_symbol(self):
        DOT(vm)
        assert vm.test(voc=False) == '<vm:metaL>'
        vm // String('`quoted')
        assert vm.test(voc=False) == '<vm:metaL>\t<string:`quoted>'
        INTERPRET(vm)
        assert vm.test(voc=False) == '<vm:metaL>\t<symbol:quoted>'
        
    def test_string(self):
        DOT(vm)
        assert vm.test(voc=False) == '<vm:metaL>'
        vm // String("\t\r\n'test\\t\\r\\nstring'\n")
        assert vm.test(voc=False) == \
                        "<vm:metaL>\t<string:\\t\\r\\n'test\\t\\r\\nstring'\\n>"
        INTERPRET(vm)
        assert vm.test(voc=False) == '<vm:metaL>\t<string:test\\t\\r\\nstring>'
        
    def test_numbers(self):
        DOT(vm)
        assert vm.test(voc=False) == '<vm:metaL>'
        vm // String('-01 +02.30 -04e+5 0xDeadBeef 0b1101')
        assert vm.test(voc=False) == \
            '<vm:metaL>\t<string:-01 +02.30 -04e+5 0xDeadBeef 0b1101>'
        INTERPRET(vm)
        assert vm.test(voc=False) == \
            '<vm:metaL>\t<integer:-1>\t<number:2.3>\t<number:-400000.0>'+\
            '\t<hex:0xDEADBEEF>\t<bin:0b1101>'
        
        
###################################################################### compiler
        
class TestCompiler:
    
    def no_test_compile(self):
        DOT(vm)
        assert vm.test(voc=False) == '<vm:metaL>'
        vm // String('[ ] { }')
        assert vm.test(voc=False) == '<vm:metaL>\t<string:[ ] { }>'
        INTERPRET(vm)
        assert vm.test(voc=False) == '<vm:metaL>\t<symbol:quoted>'

################################################################## web platform

class TestWeb:
    
    def test_create(self):
        web = Web('test')
        assert web.test(voc=False) == '<web:test>'
        assert web['IP'].test() == '<ip:127.0.0.1>'
        assert web['PORT'].test() == '<port:8888>'
        assert web['font'].test() == '<font:monospace>\tsize <size:3mm>'
        assert web['back'].test() == '<color:black>'
        assert web['color'].test() == '<color:lightgreen>'

################################################################### system init

class TestInit:
    
    def test_init(self):
        sys.argv = [sys.argv[0],'/dev/null']
        INIT(vm) 

######################################################## Python code generation

class TestPython:
    
    def test_Frame(self):
        hello = Frame('hello')
        a = Frame('a')
        b = Frame('b')
        hello // a // b
        assert hello.py(None) == r"Frame('hello') // Frame('a') // Frame('b')"
        
    def test_Primitive(self):
        hello = Primitive('prim')
        a = Frame('a')
        b = Frame('b')
        hello // a // b
        assert hello.py(hello) == r"prim"
        
    def test_String(self):
        str = String("hello\n\tworld")
        assert str.py(None) == r"'hello\n\tworld'"
        
    def test_Integer(self):
        num = Integer('-01234')
        assert num.py(None) == r"-1234"
        
    def test_Hex(self):
        hex = Hex('0xDeadBeef')
        assert hex.py(None) == r"0xDEADBEEF"
        
    def test_Bin(self):
        bin = Bin('0b1101')
        assert bin.py(None) == r"0b1101"
        
    def test_import(self):
        os = Import('os')
        assert os.test() == '<import:os>'
        assert 'sys' in os.module.__dict__
        
################################################# embedded C/C++ code generator

class TestCpp:
    
    def test_frame(self):
        assert C('C99').test() == '<c:C99>'
        assert Cpp('C++03').test() == '<cpp:C++03>'

