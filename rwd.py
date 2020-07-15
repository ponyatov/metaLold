from metaL import *
from nim import *

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
