import sys,wx,wx.stc

ide = wx.App()

class ideWindow(wx.Frame):
    def __init__(self,FileName):
        wx.Frame.__init__(self,parent=None,title=FileName)
        self.filename = FileName
        self.initMenu()
        self.initEditor()
        
    def initEditor(self):
        self.editor = wx.stc.StyledTextCtrl(self)
        self.onLoad()
        
    def onLoad(self,event=None):
        try:
            with open(self.filename) as F:
                self.editor.SetValue(F.read()) ; F.close()
        except IOError: # no file
            self.editor.SetValue('# %s\n\n' % self.filename)
            self.onSave()
            
    def onSave(self,event=None):
        with open(self.filename,'w') as F:
            F.write( self.editor.GetValue() ) ; F.close()
        
    def initMenu(self):
        self.menu = wx.MenuBar() ; self.SetMenuBar(self.menu)
        
        self.file = wx.Menu() ; self.menu.Append(self.file,'&File')
        self.save = self.file.Append(wx.ID_SAVE,'&Save\tCtrl+S')
        self.Bind(wx.EVT_MENU,self.onSave,self.save)
        self.quit = self.file.Append(wx.ID_EXIT,'&Quit\tCtrl+Q')
        self.Bind(wx.EVT_MENU,self.onQuit,self.quit)
        
        self.debug = wx.Menu() ; self.menu.Append(self.debug,'&Debug')
        self.update = self.debug.Append(wx.ID_REFRESH,'&Update\tF12')
        
        self.help = wx.Menu() ; self.menu.Append(self.help,'&Help')
        self.about = self.help.Append(wx.ID_ABOUT,'&About\tF1')
        
    def onQuit(self,event):
        ideConsole.onSave()
        ideConsole.Close()

try:
    autoloadFile = sys.argv[1]
except:
    autoloadFile = 'wxide.src'
    
ideConsole = ideWindow(autoloadFile) ; ideConsole.Show()

ide.MainLoop()
