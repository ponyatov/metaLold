from metaL import *


## lexer

import ply.lex as lex

tokens = ['symbol', 'string', 'integer', 'number',
          'add', 'sub', 'mul', 'div', 'pow',
          'colon', 'semicolon', 'tick',
          'push', 'lshift', 'rshift', 'eq', 'dot',
          'exit']

t_ignore = ' \t\r\n'
t_ignore_comment = r'\#.*'

states = (('str', 'exclusive'),)

states = (('str', 'exclusive'),)

t_str_ignore = ''

def t_str(t):
    r"\'\n*"
    t.lexer.push_state('str')
    t.lexer.string = ''
def t_str_string(t):
    r"\'"
    t.lexer.pop_state()
    t.value = String(t.lexer.string)
    return t
def t_str_any(t):
    r"."
    t.lexer.string += t.value
def t_str_nl(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    t.lexer.string += t.value

def t_ANY_error(t): raise SyntaxError(t)

def t_exit(t):
    r'exit\(\)'
    return t

def t_nl(t):
    r'\n'
    t.lexer.lineno += 1
def t_semicolon(t):
    r'\;'
    return t

def t_push(t):
    r'\/\/'
    t.value = Op(t.value)
    return t
def t_lshift(t):
    r'\<\<'
    t.value = Op(t.value)
    return t
def t_rshift(t):
    r'\>\>'
    t.value = Op(t.value)
    return t
def t_eq(t):
    r'\='
    t.value = Op(t.value)
    return t
def t_dot(t):
    r'\.'
    t.value = Op(t.value)
    return t

def t_colon(t):
    r'\:'
    t.value = Op(t.value)
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

def t_tick(t):
    r'\`'
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
    r'[^ \t\r\n\#\+\-\*\/\^\:\;\<\>\'\=\.]+'
    t.value = Symbol(t.value)
    return t


lexer = lex.lex()


## parser

import ply.yacc as yacc

precedence = (
    ('left', 'eq',),
    ('left', 'dot',),
    ('left', 'push', 'lshift', 'rshift',),
    ('left', 'add', 'sub'),
    ('left', 'mul', 'div'),
    ('left', 'pow', ),
    ('left', 'pfx', ),
    ('nonassoc', 'colon',),
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
def p_ex_string(p):
    ' ex : string '
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
def p_ex_tick(p):
    ' ex : tick ex %prec pfx '
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

def p_ex_colon(p):
    ' ex : ex colon ex '
    p[0] = p[2] // p[1] // p[3]
def p_ex_push(p):
    ' ex : ex push ex '
    p[0] = p[2] // p[1] // p[3]
def p_ex_lshift(p):
    ' ex : ex lshift ex '
    p[0] = p[2] // p[1] // p[3]
def p_ex_rshift(p):
    ' ex : ex rshift ex '
    p[0] = p[2] // p[1] // p[3]
def p_ex_eq(p):
    ' ex : ex eq ex '
    p[0] = p[2] // p[1] // p[3]
def p_ex_dot(p):
    ' ex : ex dot ex '
    p[0] = p[2] // p[1] // p[3]

def p_error(p): raise SyntaxError(p)


parser = yacc.yacc(debug=False, write_tables=False)


## interpreter

import traceback

def q(src, ctx=vm): # [q]uery
    parser.ctx = ctx
    for ast in parser.parse(src):
        print(ast)
        try:
            res = ast.eval(ctx)
            assert type(res) not in [Undef]
            print(res)
        except Exception as e:
            traceback.print_exc()
        print('-' * 66)

def repl(ctx=vm):
    while True:
        query = input("[sync:%i] %s " % (len(storage), ctx.head(test=True)))
        q(query, ctx)


if __name__ == '__main__':
    q(vm, """""")

    q(vm, """ AUTHOR """)

    q(vm, """ 2^10. """)

    repl()
