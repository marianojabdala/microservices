# -*- coding: utf-8 -*-
from users.models import *
import json
import unittest
from db import db
from app import create_app


class BaseTestCase(unittest.TestCase):
    """This class represents the Users test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing", db=db)
        self.client = self.app.test_client

        #binds the app to the current context
        with self.app.app_context():
            db.init_app(self.app)
            # create all tables
            db.create_all()


    def get_token(self, body):

        res = self.client().post('/login', data=body,
                                headers={"Content-Type": "application/json"})
        auth_token = json.loads(res.data)["access_token"]

        return {"Authorization": f"jahp {auth_token}"}
    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()