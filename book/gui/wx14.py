    def onUpdate(self,event):
        if ideStack.IsShown():
            ideStack.editor.SetValue(S.dump())
        if ideWords.IsShown():
            ideWords.editor.SetValue(W.dump())
