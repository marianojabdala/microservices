# -*- coding: utf-8 -*-
"""
Generate the manager to be used to the database migrations.

Creates a new command line option 'db' for the migrate command.

Use:

python migrate.py db

"""
import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager  # class for handling a set of commands

from instance import create_app
from db import DB

from . import * # pylint: disable=wildcard-import

APP = create_app(config_name=os.getenv('APP_SETTINGS'), database=DB)
MIGRATE = Migrate(APP, DB)
MANAGER = Manager(APP)

MANAGER.add_command('db', MigrateCommand)

if __name__ == '__main__':
    MANAGER.run()
