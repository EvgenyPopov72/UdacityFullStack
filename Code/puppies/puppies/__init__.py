from flask import Flask
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

import views

# @app.route('/hello')
# def index():
#     return 'Hello World!'
