from metaL import *
from nim import *

# threading.Thread(target=storage_daemon).start()

MODULE = 'nimde'
TITLE = 'generic text console IDE'
ABOUT = '''
* written in Nim language
* friendly for embedded Linux and IoT devices
* works in the console over serial, SSH, `screen` sessions,
  and locally with tiling window managers (i3-wm) in multiple terminal windows
'''

module = vm['MODULE'] = Module(MODULE)
title = module['TITLE'] = TITLE
about = module['ABOUT'] = ABOUT

module

