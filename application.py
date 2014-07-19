import os
import utility
from flask import Flask 
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/background/')
@app.route('/background/<int:test_variable>')
def background(test_variable=None):
    #test_variable = utility.return_file_years()
    return render_template('background.html', test=test_variable)

if __name__ == '__main__':
    app.run(debug=True)
