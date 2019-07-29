
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
        assert hello._pad(2) == '\n' + ' '*4 *2
    
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

class TestInteger:
    
    def test_Integer(self):
        num = Integer('-01234')
        assert type(num.val) == int
        assert num.test() == '<integer:-1234>'
        
class TestHex:
    
    def test_hex(self):
        hex = Hex('0xDeadBeef')
        assert type(hex.val) == int
        assert hex.test() == '<hex:0xDEADBEEF>'
        
class TestBin:
    
    def test_bin(self):
        bin = Bin('0b1101')
        assert type(bin.val) == int
        assert bin.test() == '<bin:0b1101>'

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
        
        
