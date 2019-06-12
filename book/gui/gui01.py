class GUI(Frame):
    def __init__(self,V):
        Frame.__init__(self, V)
        self.app = wx.App()
        self['main' ] = self.main  = Editor(V)
        self['stack'] = self.stack = Editor(V+'.stack')
        self['words'] = self.words = Editor(V+'.words')
    def start(self):
        self.main.Show()
        self.main.onUpdate(None)
        self.app.MainLoop()
