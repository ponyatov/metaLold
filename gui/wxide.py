import sys,re
import wx,wx.stc,wx.lib.scrolledpanel
import pydot

sys.path += ['..']
from metaL import *

ide = wx.App()

class ideWindow(wx.Frame):
    
    icon = wx.Icon('logo.png')
    
    def __init__(self,FileName):
        wx.Frame.__init__(self,parent=None,title=FileName)
        self.filename = FileName
        self.initMenu()
        self.initEditor()
        self.SetIcon(self.icon)
        
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
        self.Bind(wx.EVT_MENU,self.onUpdate,self.update)
        self.stack = self.debug.Append(wx.ID_ANY,'&Stack\tF11')
        self.Bind(wx.EVT_MENU,self.onStack,self.stack)
        self.words = self.debug.Append(wx.ID_ANY,'&Words\tF10')
        self.Bind(wx.EVT_MENU,self.onWords,self.words)
        self.plot  = self.debug.Append(wx.ID_ANY,'&Plot\tCtrl+P')
        self.Bind(wx.EVT_MENU,self.onPlot,self.plot)
        
        self.help = wx.Menu() ; self.menu.Append(self.help,'&Help')
        self.about = self.help.Append(wx.ID_ABOUT,'&About\tF1')
        self.Bind(wx.EVT_MENU,self.onAbout,self.about)
        
    def onQuit(self,event):
        ideConsole.onSave()
        ideConsole.Close() ; ideStack.Close() ; ideWords.Close()
        ideGraph.Close()
        
    def onAbout(self,event):
        info = wx.AboutDialogInfo()
        info.Icon       = self.icon
        info.Name       = 'metaL/wx'
        info.License    = 'CC BY-NC-ND'
        info.WebSite    = 'https://github.com/ponyatov/metaL/releases'
        info.Developers = ['Dmitry Ponyatov <dponyatov@gmail.com>']
        info.Description = 'homoiconic metaprogramming language'
        wx.AboutBox(info)
        
    def onStack(self,event):
        if ideStack.IsShown(): ideStack.Hide()
        else:                  ideStack.Show() ; self.onUpdate(event)
        
    def onWords(self,event):
        if ideWords.IsShown(): ideWords.Hide()
        else:                  ideWords.Show() ; self.onUpdate(event)
        
    def onUpdate(self,event):
        if ideStack.IsShown():
            ideStack.editor.SetValue(S.dump())
        if ideWords.IsShown():
            ideWords.editor.SetValue(W.dump())
            
    def onPlot(self,event):
        if ideGraph.IsShown(): ideGraph.Hide()
        else:                  ideGraph.Show()
        
        
class idePlot(ideWindow):        
    def __init__(self,V):
        ideWindow.__init__(self,V)
        self.Bind(wx.EVT_SET_FOCUS, self.onFocus)
    def onFocus(self,event):
        ideConsole.SetFocus()
        
    def initEditor(self):
        # plot to file
        plot = pydot.Dot(graph_type='digraph') 
        for i in W.attr.keys():
            plot.add_edge(pydot.Edge(W.value,W.attr[i].value))
#         plot.write_png(self.filename)
        # file to GUI widget
        image = wx.Image(self.filename, wx.BITMAP_TYPE_ANY)
        self.panel = wx.lib.scrolledpanel.ScrolledPanel(self)
        self.panel.SetAutoLayout(True)
        self.panel.SetupScrolling()  
        self.editor = wx.StaticBitmap(
            self.panel,wx.ID_ANY,wx.BitmapFromImage(image))

try:
    autoloadFile = sys.argv[1]
except:
    autoloadFile = re.sub(r'\.py$',r'.src',sys.argv[0])
    
ideConsole = ideWindow(autoloadFile) ; ideConsole.Show()

ideStack   = ideWindow(autoloadFile + '.stack')
ideWords   = ideWindow(autoloadFile + '.words')
ideGraph   = idePlot  (autoloadFile + '.png' )

ide.MainLoop()
