import sys

def main(argv):
    print 'hello'

def target(*args):
    return main,None

# this will run main() in interpreter mode (CPython/pypy)
if __name__ == '__main__':
    main(sys.argv)
