# -*- coding: utf-8 -*-
"""Class used for Swagger documentation."""

from flask_restful_swagger_2 import Schema


class UserSchema(Schema):
    """User schema class to be used on swagger docs."""

    type = 'object'
    properties = {
        '_id': {
            'type': 'integer',
            'format': 'int64',
        },
        'name': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        },
        'admin': {
            'type': 'boolean',

        }
    }
    required = ['name', "password"]
