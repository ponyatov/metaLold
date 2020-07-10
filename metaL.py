MODULE = 'metaL'
TITLE = '[meta]programming [L]anguage'
ABOUT = 'homoiconic metaprogramming system'
AUTHOR = 'Dmitry Ponyatov'
EMAIL = 'dponyatov@gmail.com'
YEAR = 2020
LICENSE = 'MIT'
GITHUB = 'https://github.com/ponyatov/'
LOGO = 'logo.png'

import os, sys, re, time
import config


## persistent storage

import redis

with redis.Redis(host=config.REDIS_IP, port=config.REDIS_PORT, db=0) as root:
    redis = redis.Redis(host=config.REDIS_IP, port=config.REDIS_PORT,
                        db=root[MODULE])

import json
from xxhash import xxh32
import threading, queue

storage = queue.Queue()#0x111)

def storage_daemon():
    time.sleep(2)
    while True:
        try:
            item = storage.get(timeout=1)
            if not item:
                break
            js = item.json()
            redis[item.gid] = js
            print(js)
            print(item.head())
        except queue.Empty:
            pass

# threading.Thread(target=storage_daemon).start()

# storage.put(None) ; exit()
# exit()


## graph

class Object:
    def __init__(self, V):
        if isinstance(V, Object):
            V = V.val
        # name / scalar value
        self.val = V
        # attributes = dict = env
        self.slot = {}
        # nested AST = vector = stack = queue
        self.nest = []
        # global storage id (unison hash)
        self.sync(self) # self.gid

    ## storage

    def sync(self, bypass):
        # update global hash
        self.gid = '%.8x' % hash(self)
        ## sync with storage
        storage.put(self)
        ## bypass object
        return bypass

    def __hash__(self):
        hsh = xxh32(self._type())
        hsh.update('%s' % self.val)
        for i in self.slot:
            hsh.update('%s=%s' % (i, self.slot[i].gid))
        for j in self.nest:
            hsh.update(j.gid)
        return hsh.intdigest()

    def json(self):
        js = {
            "gid": self.gid,
            "type": self._type(), "val": self.val,
            "slot": {},
            "nest": []
        }
        js["nest"] = [j.gid for j in self.nest]
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
            hdr += ' @%s' % self.gid
        return hdr

    def _type(self): return self.__class__.__name__.lower()
    def _val(self): return '%s' % self.val

    ## operator

    def __getitem__(self, key):
        if isinstance(key, Object):
            return self.nest[key.val]
        elif isinstance(key, int):
            return self.nest[key]
        else:
            return self.slot[key]

    def __setitem__(self, key, that):
        if isinstance(that, str):
            that = String(that)
        if isinstance(that, int):
            that = Integer(that)
        self.slot[key] = that
        return self.sync(self)

    def __lshift__(self, that):
        return self.__setitem__(that._type(), that)

    def __rshift__(self, that):
        return self.__setitem__(that.val, that)

    def __floordiv__(self, that):
        if isinstance(that, str):
            that = String(that)
        self.nest.append(that)
        return self.sync(self)

    ## stack

    def pop(self):
        return self.sync(self.nest.pop())

    ## evaluate

    def eval(self, ctx): raise Error((self))
    def apply(self, that, ctx): raise Error((self))

    ## codegen

    def file(self): return self.json()
    def py(self): return self.json()
    # def nim(self): return self.json()
    # def cxx(self): return self.json()
    # def cc(self): return self.json()

## error

class Error(Object, BaseException):
    pass

## primitive

class Primitive(Object):
    def eval(self, ctx): return self
    def file(self): return self.val

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
        self.sync(self)

class Integer(Number):
    def __init__(self, V):
        Primitive.__init__(self, int(V))
        self.sync(self)

    def add(self, that, ctx):
        assert isinstance(that, type(self))
        return Integer(self.val + that.val)

    def sub(self, that, ctx):
        assert isinstance(that, type(self))
        return Integer(self.val - that.val)

class Hex(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x10))
        self.sync(self)

    def _val(self):
        return hex(self.val)

class Bin(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x02))
        self.sync(self)

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

## metainfo

vm['TITLE'] = '[meta]programming [L]anguage'
vm['ABOUT'] = '''homoiconic metaprogramming system
* specialized language for generative (meta)programming
* web application engine over Flask (mostly for prototyping)
* self-transformational knowledge base'''
vm['AUTHOR'] = 'Dmitry Ponyatov'
vm['LICENSE'] = 'MIT'
vm['YEAR'] = 2020


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
        if isinstance(C, str):
            Meta.__init__(self, C)
        else:
            Meta.__init__(self, C.__name__.lower())
        self.cls = C

    def apply(self, that, ctx):
        return self.cls(that.val)

    def py(self):
        p = '\nclass %s' % self.val
        p += ':\n'
        if self.nest:
            for i in self.nest:
                p += i.py()
        else:
            p += '\tpass'
        return p + '\n'

class Module(Meta):
    def __init__(self, V):
        Meta.__init__(self, V)
        self['MODULE'] = self
        self['AUTHOR'] = AUTHOR
        self['EMAIL'] = EMAIL
        self['AUTHOR'] // self['EMAIL']
        self['YEAR'] = YEAR
        self['LICENSE'] = LICENSE
        self['GITHUB'] = GITHUB + self.val
        self['LOGO'] = LOGO
        self['dir'] = Dir(self.val)
        self['readme'] = File('README.md')
        self['dir'] // self['readme']


class Section(Meta):
    def py(self):
        p = '\n## \\ %s\n' % self.val
        for i in self.nest:
            p += i.py()
        p += '\n## / %s\n' % self.val
        return p

class Fn(Meta):
    pass

class Method(Meta):
    pass


## I/O

class IO(Object):
    pass

class Dir(IO):
    def __init__(self, V):
        if isinstance(V, Object):
            V = V.val
        IO.__init__(self, V)
        try:
            os.mkdir(self.val)
        except FileExistsError:
            pass

    def __floordiv__(self, that):
        if isinstance(that, str):
            that = File(that)
        if isinstance(that, File):
            filename = '%s/%s' % (self.val, that.val)
            that.fh = open(filename, 'w')
            that.sync(self)
            return IO.__floordiv__(self, that)
        if isinstance(that, Dir):
            that.val = '%s/%s' % (self.val, that.val)
            try:
                os.mkdir('%s' % (that.val))
            except FileExistsError:
                pass
            return IO.__floordiv__(self, that)
        # if no dir/file
        raise Error((that))

class BinFile(IO):
    pass

class Png(BinFile):
    pass


vm['LOGO'] = Png(LOGO)

class File(BinFile):

    def __init__(self, V):
        IO.__init__(self, V)
        self >> Vector('head')
        self >> Vector('tail')
        self.sync(self)

    def sync(self, bypass):
        if hasattr(self, 'fh'):
            self.fh.seek(0)
            for i in self['head']:
                self.fh.write('%s\n' % i.file())
            for j in self.nest:
                self.fh.write('%s\n' % j.file())
            for i in self['tail']:
                self.fh.write('%s\n' % i.file())
            self.fh.flush()
        return IO.sync(self, bypass)

class PFile(File):

    def sync(self, bypass):
        if hasattr(self, 'fh'):
            self.fh.seek(0)
            for i in self.nest:
                self.fh.write('%s\n' % i.py())
            self.fh.flush()
        return IO.sync(self, bypass)

class Makefile(File):
    def __init__(self, V='Makefile'):
        File.__init__(self, V)
        # head
        self['head'] // '''
CWD     = $(CURDIR)
MODULE  = $(notdir $(CWD))
OS     ?= $(shell uname -s)'''
        self['head'] // '''
NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)'''
        self['head'] // '''
.PHONY: install update'''
        self['head'] // '''
MERGE   = Makefile README.md .gitignore .vscode apt.txt'''
        # tail
        self['tail'] // '''\n
.PHONY: Linux_install Linux_update\n
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`'''
        self['tail'] // '''\n\n
.PHONY: master shadow release

master:
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)

shadow:
	git checkout $@
	git pull -v

release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) shadow
'''

class NMakefile(Makefile):
    def __init__(self, V='Makefile'):
        Makefile.__init__(self, V)
        self['head'] // '''
NIMBLE  = $(HOME)/.nimble/bin/nimble
NIM     = $(HOME)/.nimble/bin/nim'''
        self // '\n\n.PHONY: all nim\nall: nim'
        self // 'nim: $(MODULE) $(MODULE).ini\n\t./$^'
        self // '''
SRC = $(shell find $(CWD)/src -type f -regex ".+\\.nim$$")'''
        self // '''
$(MODULE): $(SRC) $(MODULE).nimble Makefile
\techo $(SRC) | xargs -n1 -P0 nimpretty --indent:2
\tnimble build
'''
        self // '''
install: $(OS)_install $(NIMBLE)
update:  $(OS)_update  $(NIMBLE)
\tchoosenim update self
\tchoosenim update stable'''
        self // '''
$(NIMBLE):
	curl https://nim-lang.org/choosenim/init.sh -sSf | sh'''

class NimbleFile(File):
    pass

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


vm['EMAIL'] = Email('dponyatov@gmail.com')

class Url(Net):
    def html(self):
        return '<a href="%s">%s</a>' % (self.val, self.val)


vm['GITHUB'] = Url(GITHUB + MODULE)

## web

class Web(Net):
    def __init__(self, V):
        Net.__init__(self, V.val)
        self['ip'] = IP(config.HTTP_IP)
        self['port'] = IP(config.HTTP_PORT)
        self.sync(self)


web = vm['web'] = Web(vm)

## database

class DB(Object):
    pass

class Redis(DB):
    def __init__(self, V):
        DB.__init__(self, V)
        self['ip'] = IP(config.REDIS_IP)
        self['port'] = IP(config.REDIS_PORT)
        self.sync(self)


vm['redis'] = Redis(config.REDIS_IP)


##################################################
## metacircular
##################################################

metaL = vm['metaL'] = vm['MODULE'] = Module(MODULE)

metaL['TITLE'] = vm['TITLE']
metaL['ABOUT'] = vm['ABOUT']

dir = metaL['dir']

# readme = File('README.md')
# dir // readme
readme = metaL['readme']
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
readme // '''
### Links

* https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book.html
* https://github.com/ponyatov/OGP/blob/master/OGP.ipynb
'''

mk = File('Makefile')
dir // mk

ini = File('metaL.ini')
dir // ini

giti = File('.gitignore')
dir // giti

py = metaL['py'] = PFile('metaL.py')
dir // py

graph = Section('graph')

obj = Class('Object')
graph // obj

py // graph

dir

##################################################

ctx

# x = Vector('x')
# x // Symbol('y')
# x.pop()

# redis.keys()

# threading.Thread(target=storage_daemon).start()

# storage.put(None) ; exit()
# exit()

rwd = Module('rwd')
rwd['TITLE'] = 'Redis Web daemon /Nim/'
rwdir = rwd['dir'] = Dir(rwd)
rwmk = NMakefile()
rwdir // rwmk
rwsrc = Dir('src')
rwdir // rwsrc
nim = File(rwd.val + '.nim')
rwsrc // nim
nimble = NimbleFile(rwd.val + '.nimble')
rwdir // nimble
apt = File('apt.txt')
rwdir // apt
apt // 'git make tcc'
rwrd = File('README.md')
rwdir // rwrd
rwrd // ('#  `%s`' % rwd['MODULE'].val)
rwrd // ('## %s' % rwd['TITLE'].val)
rwrd // ('\n(c) %s <<%s>> 2020 MIT' % (rwd['AUTHOR'].val, rwd['EMAIL'].val))
rwrd // ('\ngithub: %s' % rwd['GITHUB'].val)
rwrd // '\nwiki/ru: https://github.com/ponyatov/nimbook/wiki/rwd'

vm
