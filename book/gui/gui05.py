if __name__ == '__main__':
    infiles = sys.argv[1:] ; print infiles
    for i in infiles:
        vm // String(open(i).read()) ; INTERPRET()
#     REPL(vm)
    vm['gui'] = GUI(
        re.sub(r'\.[a-z]+$',r'.ml',sys.argv[0]))
    vm['gui'].start()
