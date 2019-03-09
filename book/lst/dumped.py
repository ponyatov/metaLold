class Frame:
  dumped = []
  def dump(self,depth=0,prefix=''):
    # header
    S = self.pad(depth) + self.head(prefix)
    # block infty dump
    ## root element
    if depth == 0: Frame.dumped = []
    ## frame was dumped. return short form only
    if self in Frame.dumped: return S + ' ...'
    ## dump in full form
    else: Frame.dumped.append(self)
    for i in self.attr: ...
    for j in self.nest: ...
    return S