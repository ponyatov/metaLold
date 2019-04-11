class ideWindow(wx.Frame):
    def onQuit(self,event):
        ideConsole.onSave() ; ideConsole.Close()
        ideStack.Close() ; ideWords.Close()

ideStack = ideWindow(autoloadFile + '.stack')
ideStack.Show()
ideWords = ideWindow(autoloadFile + '.words')
ideWords.Show()
