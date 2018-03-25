# -*- coding: utf-8 -*-
"""Class used as the model for the database."""
from werkzeug.security import generate_password_hash

from db import DB

class UserModel(DB.Model):
    """This class represents the User table."""

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(255))
    password = DB.Column(DB.String(255))
    is_admin = DB.Column(DB.Boolean(), unique=False, default=False)
    date_created = DB.Column(DB.DateTime, default=DB.func.current_timestamp())
    date_modified = DB.Column(
        DB.DateTime, default=DB.func.current_timestamp(),
        onupdate=DB.func.current_timestamp())

    def __init__(self, name, password):
        """
        Initialize with username and password.

        By default a new user is not admin.

        """
        self.username = name
        self.password = generate_password_hash(password)
        self.is_admin = False

    def save(self):
        """
        Save the new user.

        :return: None
        """
        DB.session.add(self)
        DB.session.commit()
        return None

    @classmethod
    def get_all(cls):
        """
        Return the collection of users.

        :return:All the users
        """
        return cls.query.all()

    def delete(self):
        """
        Remove the user from the database.

        :return: None
        """
        DB.session.delete(self)
        DB.session.commit()
        return None

    @classmethod
    def get_user_by_id(cls, _id):
        """
        Return the user that is get from the _id.

        :param _id: User id.
        :return: User.
        """
        return cls.query.filter_by(id=_id).first()

    def __repr__(self):
        """
        User representation when we use on a print method.

        :return: User info
        """
        return "<User: {},{}>".format(self.username, self.is_admin)
