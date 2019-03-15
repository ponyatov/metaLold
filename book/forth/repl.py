def REPL():
    while True:
        print S
        try: S // String(raw_input('hico> ')) ; INTERPRET()
        except EOFError: BYE()
        INTERPRET()
REPL()