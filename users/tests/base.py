# -*- coding: utf-8 -*-
"""Base test class."""
import json
import unittest
from users.db import DB
from users.instance import create_app


class BaseTestCase(unittest.TestCase):
    """This class represents the Users test case."""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            DB.init_app(self.app)
            # create all tables
            DB.create_all()

    def get_token(self, body):
        """
        Get the jwt token to continue other tests.

        :param body: the username and password to be used.
        :return:  json: the authorization header to be used.
        """
        res = self.client().post('/login', data=body,
                                 headers={"Content-Type": "application/json"})
        auth_token = json.loads(res.data)["access_token"]

        return {"Authorization": f"jahp {auth_token}"}

    def tearDown(self):
        """Teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            DB.session.remove()
            DB.drop_all()
