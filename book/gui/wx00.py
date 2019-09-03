import sys,wx

ide = wx.App()

class ideWindow(wx.Frame):
    def __init__(self,V):
        wx.Frame.__init__(self,parent=None,title=V)

ideConsole = ideWindow(sys.argv[0]) ; ideConsole.Show()

ide.MainLoop()
