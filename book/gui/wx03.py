try:
    autoloadFile = sys.argv[1]
except:
    autoloadFile = 'wxide.src'
    
ideConsole = ideWindow(autoloadFile) ; ideConsole.Show()