# -*- coding: utf-8 -*-
import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager  # class for handling a set of commands

from . import *
from instance import create_app
from db import db

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
