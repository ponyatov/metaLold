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

with redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0) as root:
    redis = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT,
                        db=root[MODULE])

from xxhash import xxh32
import json, queue, threading

class Storage:

    def __init__(self, queue_size):
        self.storage = queue.Queue(queue_size)
        self.thread = None

    def __len__(self):
        return self.storage.qsize()

    def start(self):
        self.thread = threading.Thread(target=storage_daemon)
        self.thread.start()

    def stop(self):
        if self.thread:
            self.put(None)
            self.thread.join()

    def get(self, timeout=1):
        return self.storage.get(timeout)

    def put(self, item, timeout=1):
        return self.storage.put(item, timeout)

    def send(self, item):
        js = item.json()
        redis[item.gid] = js
        print(js)
        print(item.head())

    def daemon(self):#, threaded=True):
        while True:
            try:
                item = self.get(timeout=1)
                if not item: # stop system marker
                    self.put(item) # forward to other daemons
                    break
                self.send(item)
            except queue.Empty:
                if not self.threaded: # don't loop in emergency flush
                    break


storage = Storage(0x111)

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
        while True:
            try:
                storage.put(self, timeout=1)
                break
            except queue.Full:
                storage.flush()
                continue
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
        if isinstance(key,str):
            return self.slot[key]
        elif isinstance(key,int):
            return self.nest[key]
        else:
            raise TypeError(key)

    def __setitem__(self, key, that):
        if isinstance(that, str):
            that = String(that)
        if isinstance(that, int):
            that = Integer(that)
        assert isinstance(key, str)
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

    def push(self, that, ctx):
        return self // that

    def lshift(self, that, ctx):
        return self << that

    def rshift(self, that, ctx):
        return self >> that

    def eq(self, that, ctx):
        ctx['%s' % self.val] = that
        return that

    def dot(self, that, ctx):
        try:
            return self[that.val]
        except KeyError:
            return Undef(that.val) // self

    ## codegen

    def file(self): return self.json()
    def py(self): return self.json()
    # def nim(self): return self.json()
    # def cxx(self): return self.json()
    # def cc(self): return self.json()

## error

class Error(Object, BaseException):
    pass

class Undef(Object):
    def eq(self, that, ctx):
        return self.nest[0].__setitem__(self.val, that)

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

    def plus(self, ctx):
        return self.__class__(+self.val)

    def minus(self, ctx):
        return self.__class__(-self.val)

    def add(self, that, ctx):
        assert type(self) == type(that)
        return self.__class__(self.val + that.val)

    def sub(self, that, ctx):
        assert type(self) == type(that)
        return self.__class__(self.val - that.val)

    def mul(self, that, ctx):
        assert type(self) == type(that)
        return self.__class__(self.val * that.val)

    def div(self, that, ctx):
        assert type(self) == type(that)
        return self.__class__(self.val / that.val)

    def pow(self, that, ctx):
        assert type(self) == type(that)
        return self.__class__(self.val ** that.val)

class Integer(Number):
    def __init__(self, V):
        Primitive.__init__(self, int(V))
        self.sync(self)

    # def add(self, that, ctx):
    #     assert type(self) == type(that)
    #     return Integer(self.val + that.val)

    # def sub(self, that, ctx):
    #     assert type(self) == type(that)
    #     return Integer(self.val - that.val)

    # def pow(self, that, ctx):
    #     assert type(self) == type(that)
    #     return Number(self.val ** that.val)

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
        # quote
        if self.val == '`':
            return self.nest[0]
        # a.b operator without b.eval
        if self.val == '.':
            assert len(self.nest) == 2
            lval = self.nest[0].eval(ctx)
            rval = self.nest[1]
            return lval.dot(rval, ctx)
        # greedy computation for all subtrees
        greedy = list(map(lambda i: i.eval(ctx), self.nest))
        # unary
        if len(greedy) == 1:
            if self.val == '+':
                return greedy[0].plus(ctx)
            if self.val == '-':
                return greedy[0].minus(ctx)
        # binary
        if len(greedy) == 2:
            if self.val == '//':
                return greedy[0].push(greedy[1], ctx)
            if self.val == '<<':
                return greedy[0].lshift(greedy[1], ctx)
            if self.val == '>>':
                return greedy[0].rshift(greedy[1], ctx)
            if self.val == '=':
                return greedy[0].eq(greedy[1], ctx)
            if self.val == '+':
                return greedy[0].add(greedy[1], ctx)
            if self.val == '-':
                return greedy[0].sub(greedy[1], ctx)
            if self.val == '*':
                return greedy[0].mul(greedy[1], ctx)
            if self.val == '/':
                return greedy[0].div(greedy[1], ctx)
            if self.val == '^':
                return greedy[0].pow(greedy[1], ctx)
            if self.val == ':':
                return greedy[0].colon(greedy[1], ctx)
        raise Error((self))

class VM(Active):
    pass


ctx = vm = VM(MODULE)
vm << vm

## debug/control

def BYE(ctx=vm):
    storage.stop()
    os._exit(0)
    # sys.exit(0)

## metainfo


vm['MODULE'] = MODULE
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

    def colon(self, that, ctx):
        return self.apply(that, ctx)

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


vm >> Class(Module)

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
        self['host'] = IP(config.HTTP_HOST)
        self['port'] = IP(config.HTTP_PORT)
        self.sync(self)


web = vm['web'] = Web(vm)

## database

class DB(Object):
    pass

class Redis(DB):
    def __init__(self, V):
        DB.__init__(self, V)
        self['host'] = IP(config.REDIS_HOST)
        self['port'] = IP(config.REDIS_PORT)
        self.sync(self)


vm['redis'] = Redis(config.REDIS_HOST)


##################################################

ctx

# x = Vector('x')
# x // Symbol('y')
# x.pop()

# redis.keys()

# threading.Thread(target=storage_daemon).start()

# storage.put(None) ; exit()
# exit()
