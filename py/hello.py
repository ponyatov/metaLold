import sys

def main(argv):
    print 'hello'

def target(*args):
    return main,None

if __name__ == '__main__': main(sys.argv)
