import os
from flask import Flask 
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/background/')
@app.route('/background/<test_variable>')
def background(test_variable=None):
    return render_template('background.html', test=test_variable)

if __name__ == '__main__':
    app.run(debug=True)
