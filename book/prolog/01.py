import time

def now():
    while True: 
        yield time.localtime()

var = now() ## get iterator

def main():
    for item in [1,2,3,4,5]:
        print item, var.next() ## lazy!
main()