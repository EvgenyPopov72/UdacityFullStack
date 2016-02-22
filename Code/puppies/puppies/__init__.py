from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Shell, Manager
import os

from models import Base


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
manager = Manager(app)
migrate = Migrate(app, Base)
manager.add_command('db', MigrateCommand)
Bootstrap(app)

import views

