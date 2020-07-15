
import pytest

from parser import parser

class TestParser:

    def test_empty(self):
        assert parser.parse('').test() ==\
            '\n<ast:>'

    def test_integer(self):
        assert parser.parse('-01').test() ==\
            '\n<ast:>' +\
            '\n\t0: <op:->' +\
            '\n\t\t0: <integer:1>'

    def test_semicolon(Self):
        assert parser.parse('1;2;3').test() ==\
            '\n<ast:>' +\
            '\n\t0: <integer:1>' +\
            '\n\t1: <integer:2>' +\
            '\n\t2: <integer:3>'
