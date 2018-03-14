# -*- coding: utf-8 -*-
import os

from flask_cors import CORS

from db import db
from instance import create_app

app = create_app(os.getenv("APP_SETTINGS"), db)

CORS(app)

db.init_app(app)

if __name__ == '__main__':
    app.run()
