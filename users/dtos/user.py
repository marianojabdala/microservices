# -*- coding: utf-8 -*-
"""This class is the one ths is send to the frontent.

Example:
    This could be a postman request or a curl request and will return this dto object as json::

        $ curl -X POST \
              http://localhost:8000/users \
              -H 'Cache-Control: no-cache' \
              -H 'Content-Type: application/json' \
              -H 'Postman-Token: 004ac1c8-69ee-275b-7b23-30cdbee5e02e' \
              -d '{
                "name": "Test User-0",
                "password": "my secret password"
            }'
            response :




Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

class UserDto:

    def __init__(self, user=None):
        if user is not None:
            self.id = user.id
            self._id = user.id
            self.name = user.username
            self.password = user.password
            self.created = user.date_created
            self.admin = user.isAdmin
        else:
            self.id = -1
            self.name = ""
            self.password =""
            self.created =""
            self.admin = False

    def set_attributes(self, attr):
        self._id = attr["_id"]
        self.id = attr["_id"]
        self.name = attr["username"]
        self.password = attr["password"]

    def __repr__(self):
        return "User=[_id={},username={},password={},admin={}]".format(self._id, self.name, self.password,
                                                                       self.admin)
