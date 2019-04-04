import sys,wx

ide = wx.App()

class ideWindow(wx.Frame):
    def __init__(self,V):
        wx.Frame.__init__(self,parent=None,title=V)

ideMain = ideWindow(sys.argv[0]) ; ideMain.Show()

ide.MainLoop()
