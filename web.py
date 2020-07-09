# web client (async viever)

import os, sys
import config

from metaL import *

import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html', vm=vm, ctx=vm)

@app.route('/<path:path>.png')
def png(path):
    return app.send_static_file(path + '.png')
@app.route('/<path:path>.jpg')
def jpg(path):
    return app.send_static_file(path + '.jpg')

@app.route('/<path:path>.css')
def css(path):
    return app.send_static_file(path + '.css')
@app.route('/<path:path>.js')
def js(path):
    return app.send_static_file(path + '.js')

@app.route('/<path:path>')
def path(path):
    ctx = vm
    for i in path.split('/'):
        ctx = ctx[i]
    return flask.render_template('index.html', vm=vm, ctx=ctx)


app.run(host=config.HTTP_IP, port=config.HTTP_PORT,
        debug=True, extra_files=sys.argv)
