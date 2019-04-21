    def initMenu(self):
        self.save = self.file.Append(wx.ID_SAVE,'&Save')
        self.quit = self.file.Append(wx.ID_EXIT,'&Quit')
        self.Bind(wx.EVT_MENU,self.onQuit,self.quit)
    def onQuit(self,event):
        ideConsole.Close()
