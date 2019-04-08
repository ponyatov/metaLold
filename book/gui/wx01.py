class ideWindow(wx.Frame):
    def __init__(self,V):
        wx.Frame.__init__(self,parent=None,title=V)
        self.initMenu()
    def initMenu(self):
        self.menu = wx.MenuBar()
        self.SetMenuBar(self.menu)
        self.file = wx.Menu()
        self.menu.Append(self.file,'&File')
        
        self.debug = wx.Menu()
        self.menu.Append(self.debug,'&Debug')
        
        self.help = wx.Menu()
        self.menu.Append(self.help,'&Help')
