# -*- coding: utf-8 -*-
"""
Create the application that will be used on the tests.

Create the application with the testing environment and also
initialize the database with the proper tables.

"""
from models import user  #pylint: disable=W0611
from db import DB
from app import create_app

APP = create_app(config_name="testing")

#binds the app to the current context
with APP.app_context():

    DB.init_app(APP)
    # create all tables
    DB.create_all()
