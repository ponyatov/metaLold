## Nim lang target compiling

from metaL import *

class nModule(Module):
    def __init__(self, V):
        Module.__init__(self, V)
        self['src'] = Dir('src')
        self['dir'] // self['src']
        self['nimble'] = File('%s.nimble' % self.val)
        self['dir'] // self['nimble']
