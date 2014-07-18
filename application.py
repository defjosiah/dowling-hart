import os
from flask import Flask 

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/background/')
def background():
    return "Empty String"
