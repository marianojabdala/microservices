# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema


class UserSchema(Schema):
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
