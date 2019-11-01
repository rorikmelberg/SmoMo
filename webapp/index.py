@app.route('/index', methods=('GET'))
def index():
    return render_template('index.html')