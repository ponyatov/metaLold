def INTERPRET():
    lexer.input(S.pop().value)
    while True:
        if not WORD(): break;
        if isinstance(S.top(),Symbol):
            if FIND(): EXECUTE()
W << INTERPRET

def REPL():
    while True:
        print W ; print S ; print
        try: S // String(raw_input('hico> '))
        except EOFError: sys.exit()
        INTERPRET()
REPL()
