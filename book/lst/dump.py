class Frame:
  # print frame
  def __repr__(self):
    return self.dump()
  # tree form dump
  def dump(self,depth=0,prefix=''):
    S = self.pad(depth) + self.head(prefix)
    for i in self.attr:
        S += self.attr[i].dump(depth+1,prefix='%s = '%i)
    for j in self.nest:
        S += j.dump(depth+1)
    return S