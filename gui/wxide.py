import sys,wx

ide = wx.App()

class ideWindow(wx.Frame):
    def __init__(self,V):
        wx.Frame.__init__(self,parent=None,title=V)
        self.initMenu()
    def initMenu(self):
        self.menu = wx.MenuBar() ; self.SetMenuBar(self.menu)
        
        self.file = wx.Menu() ; self.menu.Append(self.file,'&File')
        self.save = self.file.Append(wx.ID_SAVE,'&Save')
        self.quit = self.file.Append(wx.ID_EXIT,'&Quit')
        self.Bind(wx.EVT_MENU,self.onQuit,self.quit)
        
        self.debug = wx.Menu() ; self.menu.Append(self.debug,'&Debug')
        self.update = self.debug.Append(wx.ID_REFRESH,'&Update\tF12')
        
        self.help = wx.Menu() ; self.menu.Append(self.help,'&Help')
        self.about = self.help.Append(wx.ID_ABOUT,'&About\tF1')
        
    def onQuit(self,event):
        ideConsole.Close()

ideConsole = ideWindow(sys.argv[0]) ; ideConsole.Show()

ide.MainLoop()
