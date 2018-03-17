# -*- coding: utf-8 -*-
import os

from flask_cors import CORS
from users.db import db
from users.instance import create_app

app = create_app(os.getenv("APP_SETTINGS"))

CORS(app)

db.init_app(app)

if __name__ == '__main__':
    app.run()