def WEB():
    from flask import Flask
    # ...
    web.run(
        host = W['WEB']['IP'].value   ,
        port = W['WEB']['PORT'].value ,
        debug=True)
W << WEB
W['WEB']['IP']   = String('127.0.0.1')
W['WEB']['PORT'] = Integer(8888)