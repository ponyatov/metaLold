
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
        for i in self.attr: S += self.attr[i].dump(depth+1,prefix='%s = '%i)
        for j in self.nest: S += j.dump(depth+1)
        return S
    def head(self,prefix=''):
        return '%s<%s:%s> @%x' % (prefix, self.type, self.value, id(self))
    def pad(self,padding):
        return '\n'+'\t'*padding
    
    def __floordiv__(self,obj):
        if isinstance(obj,str): self.nest.append(String(obj))
        else: self.nest.append(obj)
        return self
    
    def gen(self):
        S = ''
        for i in self.nest: S += i.gen() + '\n'
        return S

        
class Primitive(Frame): pass

class String(Primitive):
    def gen(self):
        return self.value
    
class IO(Frame): pass
    
class File(IO):
    def gen(self):
        return self.head() + '\n\n' + Frame.gen(self)

class Project(Frame): pass

hico = Project('hico')
readme = File('README.md') ; hico // readme 
readme // '# hico' // '## homoiconic Python bootstrap' // '' // '(c) Dmitry Ponyatov <dponyatov@gmail.com> CC BY-NC-ND' // '' // 'github: https://github.com/ponyatov/hico'

gitignore = File('.gitignore') ; hico // gitignore
gitignore // '*~' // '*.swp' // '*.pyc' // '*.log'

print hico.gen()

print hico
