from flask import Flask
from flask import render_template

print("start")

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')


@app.route('/admin')

def admin():
    currentDate = 'this is the date'
    return render_template('admin.html')
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
