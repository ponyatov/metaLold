MODULE = 'metaL'
TITLE = '[meta]programming [L]anguage'
ABOUT = 'homoiconic metaprogramming system'
AUTHOR = 'Dmitry Ponyatov'
EMAIL = 'dponyatov@gmail.com'
YEAR = 2020
LICENSE = 'MIT'
GITHUB = 'https://github.com/ponyatov/metaL'
LOGO = 'logo.png'

import os, sys, re
import config


## persistent storage

import redis, json
from xxhash import xxh32
import threading, queue

storage = queue.Queue(0x11)


## graph

class Object:
    def __init__(self, V):
        # name / scalar value
        self.val = V
        # attributes = dict = env
        self.slot = {}
        # nested AST = vector = stack = queue
        self.nest = []
        # global storage id (unison hash)
        self.gid = self.sync()

    ## storage

    def sync(self):
        # update global hash
        self.gid = hash(self)
        ## sync with storage
        #storage.put(self)
        return self.gid

    def __hash__(self):
        hsh = xxh32(self._type())
        hsh.update('%s' % self.val)
        return hsh.intdigest()

    def json(self):
        js = {
            "type": self._type(), "val": self.val,
        }
        return json.dumps(js)

    ## dump

    def __repr__(self): return self.dump()

    def test(self): return self.dump(test=True, tab='\t')

    def html(self): return self.dump(test=False, tab=' ' * 2)

    def dump(self, cycle=None, depth=0, prefix='', test=False, tab='\t'):
        # header
        tree = self._pad(depth, tab) + self.head(prefix, test)
        # cycles
        if not depth:
            cycle = []
        if self in cycle:
            return tree + ' _/'
        else:
            cycle.append(self)
        # slot{}s
        for i in sorted(self.slot.keys()):
            tree += self.slot[i].dump(cycle, depth + 1, '%s = ' % i, test, tab)
        # nest[]ed
        idx = 0
        for j in self.nest:
            tree += j.dump(cycle, depth + 1, '%s: ' % idx, test, tab)
            idx += 1
        # subtree
        return tree

    def _pad(self, depth, tab='\t'): return '\n' + tab * depth

    def head(self, prefix='', test=False):
        hdr = '%s<%s:%s>' % (prefix, self._type(), self._val())
        if not test:
            hdr += ' @%.8x' % self.gid
        return hdr

    def _type(self): return self.__class__.__name__.lower()
    def _val(self): return '%s' % self.val

    ## operator

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.nest[key]
        else:
            return self.slot[key]

    def __setitem__(self, key, that):
        if isinstance(that, str):
            that = String(that)
        if isinstance(that, int):
            that = Integer(that)
        self.slot[key] = that
        self.sync()
        return self

    def __lshift__(self, that):
        return self.__setitem__(that._type(), that)

    def __rshift__(self, that):
        return self.__setitem__(that.val, that)

    def __floordiv__(self, that):
        if isinstance(that, str):
            that = String(that)
        self.nest.append(that)
        self.sync()
        return self

    ## evaluate

    def eval(self, ctx): raise Error((self))
    def apply(self, that, ctx): raise Error((self))

## error

class Error(Object, BaseException):
    pass

## primitive

class Primitive(Object):
    def eval(self, ctx): return self

class Symbol(Primitive):
    # special case: evaluates by name in context
    def eval(self, ctx):
        return ctx[self.val]

class String(Primitive):
    def _val(self):
        s = ''
        for c in self.val:
            if c == '\n':
                s += r'\n'
            elif c == '\t':
                s += r'\t'
            else:
                s += c
        return s

    def html(self): return self.val

class Number(Primitive):
    def __init__(self, V):
        Primitive.__init__(self, float(V))
        self.sync()

class Integer(Number):
    def __init__(self, V):
        Primitive.__init__(self, int(V))
        self.sync()

    def add(self, that, ctx):
        assert isinstance(that, type(self))
        return Integer(self.val + that.val)

    def sub(self, that, ctx):
        assert isinstance(that, type(self))
        return Integer(self.val - that.val)

class Hex(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x10))
        self.sync()

    def _val(self):
        return hex(self.val)

class Bin(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x02))
        self.sync()

    def _val(self):
        return bin(self.val)

# container

class Container(Object):
    pass
class Vector(Container):
    pass
class Dict(Container):
    pass
class Stack(Container):
    pass

## active

class Active(Object):
    pass

class Op(Active):
    def eval(self, ctx):
        # greedy computation for all subtrees
        greedy = list(map(lambda i: i.eval(ctx), self.nest))
        if self.val == '+':
            assert len(greedy) == 2
            return greedy[0].add(greedy[1], ctx)
        if self.val == '-':
            assert len(greedy) == 2
            return greedy[0].sub(greedy[1], ctx)
        raise Error((self))

class VM(Active):
    pass


ctx = vm = VM(MODULE)
vm << vm


class Env(Active, Vector):
    pass


env = Env('ironment')
vm << env
for i in os.environ:
    var = os.environ[i]
    if re.match(r'^[+\-]?\d+$', var):
        env[i] = Integer(var)
    else:
        env[i] = String(var)

## meta

class Meta(Object):
    pass

class Class(Meta):
    def __init__(self, C):
        Meta.__init__(self, C.__name__.lower())
        self.cls = C

    def apply(self, that, ctx):
        return self.cls(that.val)

class Module(Meta):
    pass

class Section(Meta):
    pass

class Fn(Meta):
    pass

class Method(Meta):
    pass


## I/O

class IO(Object):
    pass

class Dir(IO):
    def __init__(self, V):
        IO.__init__(self, V)
        try:
            os.mkdir(self.val)
        except FileExistsError:
            pass

    def __floordiv__(self, that):
        if isinstance(that, str):
            that = File(that)
        assert isinstance(that, File)
        filename = '%s/%s' % (self.val, that.val)
        that.fh = open(filename, 'w')
        return IO.__floordiv__(self, that)

class File(IO):
    def __init__(self, V):
        IO.__init__(self, V)
        self.fh = None

    def __floordiv__(self, that):
        if isinstance(that, str):
            that = String(that)
        if self.fh:
            self.fh.write('%s\n' % that.val)
            self.fh.flush()
        return IO.__floordiv__(self, that)

class Png(File):
    pass

class Makefile(File):
    def __init__(self, V='Makefile'):
        File.__init__(self, V)

## network

class Net(IO):
    pass

class IP(Net, Primitive):
    pass

class Port(Net, Integer):
    def __init__(self, V):
        Integer.__init__(self, V)

class Email(Net):
    def html(self):
        return '&lt;<a href="mailto:%s">%s</a>&gt;' % (self.val, self.val)

class Url(Net):
    def html(self):
        return '<a href="%s">%s</a>' % (self.val, self.val)

## web

class Web(Net):
    def __init__(self, V):
        Net.__init__(self, V.val)
        self['ip'] = IP(config.HTTP_IP)
        self['port'] = IP(config.HTTP_PORT)
        self.sync()


web = vm['web'] = Web(vm)

## database

class DB(Object):
    pass

class Redis(DB):
    def __init__(self, V):
        DB.__init__(self, V)
        self['ip'] = IP(config.REDIS_IP)
        self['port'] = IP(config.REDIS_PORT)
        self.sync()


vm['redis'] = Redis(config.REDIS_IP)

## metainfo


vm['MODULE'] = Module(MODULE)
vm['TITLE'] = '[meta]programming [L]anguage'
vm['ABOUT'] = '''homoiconic metaprogramming system
* specialized language for generative (meta)programming
* web application engine over Flask (mostly for prototyping)
* self-transformational knowledge base'''
vm['AUTHOR'] = 'Dmitry Ponyatov'
vm['EMAIL'] = Email('dponyatov@gmail.com')
vm['LICENSE'] = 'MIT'
vm['YEAR'] = 2020
vm['GITHUB'] = Url(GITHUB)
vm['LOGO'] = Png(LOGO)


##################################################
## metacircular
##################################################

metaL = vm['metaL'] = Module(MODULE)

metaL['MODULE'] = vm['MODULE']
metaL['TITLE'] = vm['TITLE']
metaL['ABOUT'] = vm['ABOUT']
metaL['AUTHOR'] = vm['AUTHOR'] // vm['EMAIL']
metaL['EMAIL'] = vm['EMAIL']
metaL['LICENSE'] = vm['LICENSE']
metaL['YEAR'] = vm['YEAR']
metaL['GITHUB'] = vm['GITHUB']
metaL['LOGO'] = vm['LOGO']

dir = Dir(metaL.val)
metaL << dir

readme = File('README.md')
dir // readme
readme // ('#  `%s`' % metaL.val)
readme // ('## %s' % metaL['TITLE'].val)
readme // ''
readme // vm['ABOUT']
readme // ''
readme // ('(c) %s <<%s>> %s %s' %
           (metaL['AUTHOR'].val, metaL['EMAIL'].val, metaL['YEAR'].val, metaL['LICENSE'].val))
readme // ''
readme // ('github: %s\n\nwiki: %s/wiki' %
           (metaL['GITHUB'].val, metaL['GITHUB'].val))

##################################################

ctx
