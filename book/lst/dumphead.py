class Frame:
  def head(self,prefix=''):
    return '%s<%s:%s> @%x' % \
      (prefix, self.type, self.str(), id(self))