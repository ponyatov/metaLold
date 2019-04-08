def onSave(self):
    with open(self.filename,'w') as F:
        F.write( self.editor.GetValue() ) ; F.close()
def initMenu(self):
    self.save = self.file.Append(wx.ID_SAVE,'&Save')
    self.Bind(wx.EVT_MENU,self.onSave,self.save)
