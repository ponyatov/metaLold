import pydot
class ideWindow(wx.Frame):
    def initMenu(self):
        self.plot  = self.debug.Append(
            wx.ID_ANY,'&Plot\tCtrl+P')
        self.Bind(wx.EVT_MENU,self.onPlot,self.plot)
    def onPlot(self,event):
        ideGraph.Show()

class idePlot(ideWindow):        
    def initEditor(self): pass

ideGraph   = idePlot(autoloadFile + '.dot')
