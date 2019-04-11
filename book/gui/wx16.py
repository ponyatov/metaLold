class idePlot(ideWindow):        
    def initEditor(self):
        # plot to file
        plot = pydot.Dot(graph_type='digraph',rankdir='TD') 
        for i in W.attr.keys():
            plot.add_edge(pydot.Edge(W.value,W.attr[i].value))
        plot.write_png(self.filename)
        # file to GUI widget
        image = wx.Image(self.filename, wx.BITMAP_TYPE_ANY)
        self.editor = wx.StaticBitmap(
            self,wx.ID_ANY,wx.BitmapFromImage(image))

ideGraph   = idePlot  (autoloadFile + '.png' )
