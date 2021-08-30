# -*- coding: utf-8 -*-
"""
Create the application that will be used on the tests.

Create the application with the testing environment and also
initialize the database with the proper tables.

"""
from users.models import user  #pylint: disable=W0611:
from users.db import DB
from users.app import create_app

APP = create_app(config_name="testing", database=DB)

# binds the app to the current context
with APP.app_context():
    DB.init_app(APP)
    # create all tables
    DB.create_all()