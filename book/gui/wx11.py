def initMenu(self):
  self.stack = self.debug.Append(wx.ID_ANY,'&Stack\tF11')
  self.Bind(wx.EVT_MENU,self.onStack,self.stack)
  self.words = self.debug.Append(wx.ID_ANY,'&Words\tF10')
  self.Bind(wx.EVT_MENU,self.onWords,self.words)
