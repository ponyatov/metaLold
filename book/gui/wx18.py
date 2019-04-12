class idePlot(ideWindow):
  def initEditor(self):
    self.figure = Figure()
    self.canvas = FigureCanvas(self, -1, self.figure)
    self.axes = self.figure.add_subplot(111)
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.sizer.Add(self.canvas, 1,
                            wx.LEFT | wx.TOP | wx.GROW)
    self.SetSizer(self.sizer)
    
  def onUpdate(self,event):
    graph = nx.DiGraph()
    for i in W.keys(): graph.add_edge(W, W[i])
    nx.draw(graph,ax=self.axes)
    self.Fit()
