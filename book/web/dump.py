def WEB():
    @web.route('/dump/<path:frame>')
    def dump(frame):
        return render_template('dump.html',
                               dump = W[frame].dump())