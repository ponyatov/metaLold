def WEB():
    IP   = '127.0.0.1'
    PORT = 8888
    from flask import Flask
    web = Flask(__name__)
    web.config['SECRET_KEY'] = os.urandom(32)
    
    @web.route('/')
    def index(): return '<pre>' + W.dump()
    
    web.run(host = IP, port = PORT, debug=True)
W << WEB
