import sys,wx

ide = wx.App()

class GUI_window(wx.Frame):
    def __init__(self,V):
        wx.Frame.__init__(self,parent=None,title=V)

ideMain = GUI_window(sys.argv[0]) ; ideMain.Show()

ide.MainLoop()
