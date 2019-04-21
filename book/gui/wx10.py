  def initMenu(self):
    self.update = self.debug.Append(
        wx.ID_REFRESH,'&Update\tF12')
    self.Bind(wx.EVT_MENU,self.onUpdate,self.update)
    self.stack = self.debug.Append(
        wx.ID_ANY,'&Stack\tF11')
    self.words = self.debug.Append(
        wx.ID_ANY,'&Words\tF10')
  def onUpdate(self,event):
    ideStack.Show() ; ideWords.Show()
    ideStack.editor.SetValue(S.dump())
    ideWords.editor.SetValue(W.dump())

ideStack = ideWindow(autoloadFile+'.stack') # don't show
ideWords = ideWindow(autoloadFile+'.words') # on start
