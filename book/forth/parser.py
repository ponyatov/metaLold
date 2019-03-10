import ply.lex as lex

tokens = ['symbol','number']

t_ignore = ' \t\r\n'

def t_number(t):
    r'[\+\-]?[0-9]+'
    return Number(t.value)

def t_symbol(t):
    r'[a-zA-Z0-9_.]+'
    return Symbol(t.value)

def t_error(t): return SyntaxError(t)