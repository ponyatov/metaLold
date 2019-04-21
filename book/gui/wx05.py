def initEditor(self):
    self.editor = wx.stc.StyledTextCtrl(self)
    self.onLoad()
        
def onLoad(self):
    try:
        with open(self.filename) as F:
            self.editor.SetValue(F.read()) ; F.close()
    except IOError: # no file
        self.editor.SetValue('# %s\n\n' % self.filename)
        self.onSave()
