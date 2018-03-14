# -*- coding: utf-8 -*-
from models.user import UserModel
from dtos.user import UserDto
from werkzeug.security import check_password_hash


def authenticate(username, password):
    user = UserModel.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return UserDto(user)


def identity(payload):
    user_id = payload['identity']
    user = UserModel.get_user_by_id(user_id)
    return UserDto(user)
