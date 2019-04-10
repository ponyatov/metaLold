class ideWindow(wx.Frame):
  def __init__(self,FileName):
    wx.Frame.__init__(self,parent=None,title=FileName)
    self.filename = FileName
    self.initMenu()
    self.initEditor()
