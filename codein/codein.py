import sys

class Source:
	def __init__(self,t):
		self.file  = t.lexer.file
		self.type  = self.__class__.__name__.lower()
		self.value = t.value
		self.line  = t.lineno
		self.pos   = t.lexpos
		self.nest  = []
	def __repr__(self):
		return self.dump()
	def dump(self,depth=0):
		S = self.pad(depth) + self.head()
		for j in self.nest: S += i.dump(depth+1)
		return S
	def head(self):
		return '<%s:%s>' % (self.type, self.value)
	def pad(self,N):
		return '\n' + '\t'*N

import ply.lex  as lex
import ply.yacc as yacc

tokens = ['comment','ppinclude','ppifdef','ppifndef','ppif','ppendif',
			'string','symbol','number','semicolon',
			'comma','star','plus','minus','great',
			'and','or','xor','exclam','eq',
			'lq','rq','lp','rp','lb','rb']

t_ignore = '[ \t\r]+'

def t_newline(t):
	r'\n'
	t.lexer.lineno += 1

class Comment(Source): pass
def t_comment(t):
	r'//[^\n]*|\/\*.*?\*\/'
	return Comment(t)

class ppInclude(Source): pass
def t_ppinclude(t):
	r'\#include'
	return ppInclude(t)

class ppIfdef(Source): pass
def t_ppifdef(t):
	r'\#ifdef'
	return ppIfdef(t)

class ppIfndef(Source): pass
def t_ppifndef(t):
	r'\#ifndef'
	return ppIfdef(t)

class ppIf(Source): pass
def t_ppif(t):
	r'\#if'
	return ppIf(t)

class ppEndif(Source): pass
def t_ppendif(t):
	r'\#endif'
	return ppEndif(t)

class String(Source): pass
def t_string(t):
	r'\".*?\"'
	return String(t)

class Number(Source): pass
def t_number(t):
	r'[0-9]+'
	return Number(t)

class Symbol(Source): pass
def t_symbol(t):
	r'[a-zA-Z0-9_]+'
	return Symbol(t)

class Semicolon(Source): pass
def t_semicolon(t):
	r';'
	return Semicolon(t)

class Comma(Source): pass
def t_comma(t):
	r','
	return Comma(t)

class Star(Source): pass
def t_star(t):
	r'\*'
	return Star(t)

class Plus(Source): pass
def t_plus(t):
	r'\+'
	return Plus(t)

class Minus(Source): pass
def t_minus(t):
	r'\-'
	return Minus(t)

class Great(Source): pass
def t_great(t):
	r'\>'
	return Great(t)

class And(Source): pass
def t_and(t):
	r'&'
	return And(t)

class Or(Source): pass
def t_or(t):
	r'\|'
	return Or(t)

class Xor(Source): pass
def t_xor(t):
	r'\^'
	return Xor(t)

class Exclam(Source): pass
def t_exclam(t):
	r'!'
	return Exclam(t)

class Eq(Source): pass
def t_eq(t):
	r'='
	return Eq(t)

class Lq(Source): pass
def t_lq(t):
	r'\['
	return Lq(t)

class Rq(Source): pass
def t_rq(t):
	r'\]'
	return Rq(t)

class Lp(Source): pass
def t_lp(t):
	r'\('
	return Lq(t)

class Rp(Source): pass
def t_rp(t):
	r'\)'
	return Rq(t)

class Lb(Source): pass
def t_lb(t):
	r'\{'
	return Lq(t)

class Rb(Source): pass
def t_rb(t):
	r'\}'
	return Rq(t)

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()
lexer.linepos = 0

#parser = yacc.yacc()

def LOAD(FILE,SRC):
	lexer.input(SRC)
	lexer.file = FILE
#	parser.parse('')
	while True:
		token = lexer.token()
		if not token: break
		print token

for i in sys.argv[1:]:
	with open(i) as F : LOAD(i,F.read()) ; F.close()

