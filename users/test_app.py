# -*- coding: utf-8 -*-
from models import *
from db import db
from app import create_app

app = create_app(config_name="testing", db=db)

#binds the app to the current context
with app.app_context():

    db.init_app(app)
    # create all tables
    db.create_all()

