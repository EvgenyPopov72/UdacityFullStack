from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Shell, Manager
import os

# from models import Base

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
manager = Manager(app)

from models import Base

migrate = Migrate(app, Base)
manager.add_command('db', MigrateCommand)
Bootstrap(app)

import models
import views
