# -*- coding: utf-8 -*-
r"""
This class is the one ths is send to the frontend.

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

"""


# pylint: disable=too-few-public-methods
class UserDto:
    """User Dto that is send back to the client of the api."""

    def __init__(self, user=None):
        """
        Construct method.

        :param user: The users to be used or none if we don't have one.
        """
        if user is not None:
            self._id = user.id
            self.id = self._id # pylint: disable=invalid-name
            self.name = user.username
            self.password = user.password
            self.created = user.date_created
            self.admin = user.is_admin
        else:
            self._id = -1
            self.id = self._id # pylint: disable=invalid-name
            self.name = ""
            self.password = ""
            self.created = ""
            self.admin = False

    def set_attributes(self, attr):
        """
        Set some other attributes to the Dto that could be create without any user.

        :param attr: Some user attributes
        :return: None
        """
        self._id = attr["_id"]
        self.name = attr["username"]
        self.password = attr["password"]

    def __repr__(self):
        """
        Return the user when we use print.

        :return: The user representation
        """
        return "User=[_id={},username={},admin={}]".format(self._id, self.name,
                                                           self.admin)
