import sys

if __name__ == '__main__':
    ini = sys.argv[0][:-3]+'.ini'
    for source in [ini] + sys.argv[1:]:
        with open(source) as SourceFile:
            S // SourceFile.read()
            INTERPRET()
    REPL()
