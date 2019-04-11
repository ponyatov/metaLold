class ideWindow(wx.Frame):
    def onQuit(self,event):
        ideConsole.onSave()
        ideConsole.Close() ; ideStack.Close() ; ideWords.Close()
        
ideConsole = ideWindow(autoloadFile)          ; ideConsole.Show()
ideStack   = ideWindow(autoloadFile+'.stack') ; ideStack.Show()
ideWords   = ideWindow(autoloadFile+'.words') ; ideWords.Show()
