def REPL():
    while True:
        print S
        try: S // String(raw_input('ok> ')) ; INTERPRET()
        except EOFError: BYE()
        INTERPRET()
REPL()