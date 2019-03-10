# ( string: -- )
def INTERPRET():
    lexer.input(S.pop().value)
    while True:
        if not WORD(): break;
        if isinstance(S.top(),Symbol):
            if FIND(): EXECUTE()
W << INTERPRET
