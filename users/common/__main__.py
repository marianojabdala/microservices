# -*- coding: utf-8 -*-

"""
Create an initial application.

This will be usedon when it's installed with pip install.
"""
import os

from flask_cors import CORS
from users.db import DB
from users.instance import create_app

APP = create_app(os.getenv("APP_SETTINGS"), database=DB)

CORS(APP)

DB.init_app(APP)

if __name__ == '__main__':
    APP.run()
