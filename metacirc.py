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
