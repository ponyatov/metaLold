
class Frame:
    def __init__(self,V):
        self.type  = self.__class__.__name__.lower()
        self.value = V
        self.attr  = {}
        self.nest  = []
    def __repr__(self):
        return self.dump()
    def dump(self,depth=0,prefix=''):
        S = self.pad(depth) + self.head(prefix)
        return S
    def head(self,prefix=''):
        return '%s<%s:%s> @%x' % (prefix, self.type, self.value, id(self))
    def pad(self,padding):
        return '\n'+'\t'*padding

print Frame('hico')
