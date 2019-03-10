def REPL():
    while True:
        print W ; print S ; print
        try: S // String(raw_input('hico> '))
        except EOFError: sys.exit()
        INTERPRET()
REPL()
