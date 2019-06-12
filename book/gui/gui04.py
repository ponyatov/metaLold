class Editor(GUI,wx.Frame):
    def __init__(self,V):
        ...
        self.initEditor()

    def initEditor(self):
        self.editor = wx.stc.StyledTextCtrl(self)
        self.font = wx.Font(14,
                    wx.FONTFAMILY_MODERN,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_BOLD)
        self.editor.StyleSetSpec(
            wx.stc.STC_STYLE_DEFAULT,
            "face:%s,size:%d" % (
                self.font.GetFaceName(),
                self.font.GetPointSize()
            ))
        try:
            with open(self.val,'r') as file:
                self.editor.SetValue(file.read())
        except IOError: pass
