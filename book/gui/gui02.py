class Editor(GUI,wx.Frame):
    def __init__(self,V):
        Frame.__init__(self, V)
        wx.Frame.__init__(self,parent=None,title=V)
        self.initMenu()
        self.initEditor()
