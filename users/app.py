# -*- coding: utf-8 -*-
"""
Create the main application.

Create the main application using the development setting as default also
initialize the database. The database is populated on the endpoint _init_db
that is used with a POST to the proper url and with the header Authorization
Bearer base64(username + password)

"""

import os

from flask_cors import CORS

from db import DB
from instance import create_app

APP = create_app(os.getenv("APP_SETTINGS"), database=DB)

CORS(APP)

DB.init_app(APP)

if __name__ == '__main__':
    APP.run()
