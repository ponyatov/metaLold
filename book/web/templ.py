def WEB():
  from flask import Flask,render_template
    
  @web.route('/')
  def index(): return render_template('index.html',W = W)

  @web.route('/css/<path:path>')
  def css(path): return web.send_static_file(path)