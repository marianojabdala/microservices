# -*- coding: utf-8 -*-
from db import db
from werkzeug.security import generate_password_hash


class UserModel(db.Model):
    """This class represents the User table."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    isAdmin = db.Column(db.Boolean(), unique=False, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name, password):
        """initialize with name."""
        self.username = name
        self.password = generate_password_hash(password)
        self.isAdmin = False

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_user_by_id(cls ,_id):
        return cls.query.filter_by(id=_id).first()

    def __repr__(self):
        return "<User: {},{}>".format(self.username, self.isAdmin)

