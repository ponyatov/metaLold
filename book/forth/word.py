def WORD():
    token = lexer.token()
    if not token: return False
    S // token ; return True
W << WORD
