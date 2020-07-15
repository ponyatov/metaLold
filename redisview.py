from metaL import *
from nim import *

# threading.Thread(target=storage_daemon).start()


MODULE = 'redisview'
TITLE = 'async Redis browser'

module = vm['MODULE'] = nModule(MODULE)
title = module['TITLE'] = TITLE
readme = module['readme']

readme // ('#  `%s`' % MODULE)
readme // ('## %s' % TITLE)


readme.fh.flush()

module
