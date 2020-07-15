from metaL import *


## lexer

import ply.lex as lex

tokens = ['symbol', 'exit', 'integer', 'number',
          'add', 'sub', 'mul', 'div', 'pow',
          'semicolon']

t_ignore = ' \t\r\n'
t_ignore_comment = r'\#.*'

def t_ANY_error(t): raise SyntaxError(t)

def t_exit(t):
    r'BYE\(\)'
    return t

def t_nl(t):
    r'\n'
    t.lexer.lineno += 1
def t_semicolon(t):
    r'\;'
    return t

def t_add(t):
    r'\+'
    t.value = Op(t.value)
    return t
def t_sub(t):
    r'\-'
    t.value = Op(t.value)
    return t
def t_mul(t):
    r'\*'
    t.value = Op(t.value)
    return t
def t_div(t):
    r'\/'
    t.value = Op(t.value)
    return t
def t_pow(t):
    r'\^'
    t.value = Op(t.value)
    return t

def t_number(t):
    r'[0-9]+(\.[0-9]*)'
    t.value = Number(t.value)
    return t
def t_integer(t):
    r'[0-9]+'
    t.value = Integer(t.value)
    return t

def t_symbol(t):
    r'[^ \t\r\n\#\+\-\*\/\^\;]+'
    t.value = Symbol(t.value)
    return t


lexer = lex.lex()


## parser

import ply.yacc as yacc

precedence = (
    ('left', 'add', 'sub'),
    ('left', 'mul', 'div'),
    ('left', 'pow', ),
    ('left', 'pfx', ),
)

class AST(Vector):
    pass

def p_REPL_exit(p):
    ' REPL : exit '
    BYE()
def p_REPL_none(p):
    ' REPL : '
    p[0] = AST('')
def p_REPL_recursion(p):
    ' REPL : REPL ex '
    p[0] = p[1] // p[2]
def p_REPL_semicolon(p):
    ' REPL : REPL semicolon ex '
    p[0] = p[1] // p[3]

def p_ex_symbol(p):
    ' ex : symbol '
    p[0] = p[1]
def p_ex_number(p):
    ' ex : number '
    p[0] = p[1]
def p_ex_integer(p):
    ' ex : integer '
    p[0] = p[1]

def p_ex_plus(p):
    ' ex : add ex %prec pfx '
    p[0] = p[1] // p[2]
def p_ex_minus(p):
    ' ex : sub ex %prec pfx '
    p[0] = p[1] // p[2]
def p_ex_add(p):
    ' ex : ex add ex '
    p[0] = p[2] // p[1] // p[3]
def p_ex_sub(p):
    ' ex : ex sub ex '
    p[0] = p[2] // p[1] // p[3]
def p_ex_mul(p):
    ' ex : ex mul ex '
    p[0] = p[2] // p[1] // p[3]
def p_ex_div(p):
    ' ex : ex div ex '
    p[0] = p[2] // p[1] // p[3]
def p_ex_pow(p):
    ' ex : ex pow ex '
    p[0] = p[2] // p[1] // p[3]

def p_error(p): raise SyntaxError(p)


parser = yacc.yacc(debug=False, write_tables=False)


## interpreter

def q(ctx, src): # [q]uery
    parser.ctx = ctx
    parser.parse(src)


import traceback

def repl(ctx=vm):
    while True:
        query = input("[sync:%i] %s " % (len(storage), ctx.head(test=True)))
        ast = parser.parse(query)
        print(ast)
        for expr in ast:
            try:
                print(expr.eval(ctx))
            except Exception as e:
                traceback.print_exc()
            print('-' * 88)


if __name__ == '__main__':
    q(vm, """""")

    q(vm, """ AUTHOR """)

    q(vm, """ 2^10. """)

    repl()
