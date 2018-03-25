# -*- coding: utf-8 -*
"""
This File contains the functions used by JWT

The are authenticate and identity.
"""
from werkzeug.security import check_password_hash

from models.user import UserModel
from dtos.user import UserDto


def authenticate(username, password):
    """
    This function is used by JWT when use got to the /login endpoint.
    :param username: The username value.
    :param password: The password value.
    :return: UserDTO: The dto that contains some user info.
    """
    user = UserModel.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return UserDto(user)

    return None


def identity(payload):
    """
    This function is used by JWT to validate with the token if hte user is the one that we send.
    :param payload:
    :return: UserDTO: The dto that contains some user info.
    """
    user_id = payload['identity']
    user = UserModel.get_user_by_id(user_id)

    if user:
        return UserDto(user)

    return None
