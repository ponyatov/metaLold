    def initMenu(self):
        self.menubar = wx.MenuBar()
        self.SetMenuBar(self.menubar)
        # file
        self.file = wx.Menu()
        self.menubar.Append(self.file,'&File')
        # file/save
        self.file.save = self.file.Append(\
                            wx.ID_SAVE,'&Save')
        self.Bind(wx.EVT_MENU,self.onSave,self.file.save)
        # file/quit
        self.file.quit = self.file.Append(\
                            wx.ID_EXIT,'&Quit')
        self.Bind(wx.EVT_MENU,self.onQuit,self.file.quit)
        # debug
        self.debug = wx.Menu()
        self.menubar.Append(self.debug,'&Debug')
        self.debug.update = self.debug.Append(\
                            wx.ID_REFRESH,'&Update\tF12')
        self.Bind(wx.EVT_MENU,\
                        self.onUpdate,self.debug.update)
        # debug/stack
        self.debug.stack = self.debug.Append(\
                wx.ID_ANY,'&Stack\tF9',kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU,\
                  self.onStack,self.debug.stack)
        # debug/words
        self.debug.words = self.debug.Append(\
                wx.ID_ANY,'&Words\tF8',kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU,\
                  self.onWords,self.debug.words)
        # help
        self.help = wx.Menu()
        self.menubar.Append(self.help,'&Help')
        self.help.about = self.help.Append(\
                            wx.ID_ABOUT,'&About\tF1')
        self.Bind(wx.EVT_MENU,\
                  self.onAbout,self.help.about)
    def onSave(self,e):
        with open(self.val,'w') as file:
            file.write(self.editor.GetValue())
    def onQuit(self,e):
        vm['gui'].stack.Close()
        vm['gui'].words.Close()
        vm['gui'].main.Close()
    def onUpdate(self,e):
        vm['gui'].stack.editor.SetValue(\
                                vm.dump(voc=False))
        vm['gui'].words.editor.SetValue(\
                                vm.dump(voc=True ))
    def onAbout(self,e):
        with open('README.md') as file:
            info = file.read()
        wx.MessageBox(info,'About',\
                            wx.OK|wx.ICON_INFORMATION)
