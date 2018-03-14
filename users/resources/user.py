# -*- coding: utf-8 -*-
from flask_restful import reqparse, fields, marshal_with, abort
from flask_restful_swagger_2 import swagger, Resource
from resources.base import Base
from models.user import UserModel
from dtos.user import UserDto
from swagger.schemas.user import UserSchema
from werkzeug.security import generate_password_hash

from flask_jwt import jwt_required


USER_FIELDS = {
    "_id": fields.Integer,
    "name": fields.String,
    "admin": fields.Boolean,
    "uri": fields.Url("user")
}


class UserResource(Base):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('_id', type=str, required=True,
                                   help='No user id provided', location='json')
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No user name provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                   help='No password provided',  location='json')
        self.reqparse.add_argument('isAdmin', type=bool, required=True,
                                   help='No isAdmin was provided', location='json')

        super(UserResource, self).__init__()

    @swagger.doc({
        'tags': ['users'],
        'description': 'Returns a user',
        'parameters': [
            {
                'name': '_id',
                'description': 'User identifier',
                'in': 'path',
                'type': 'integer'
            }
        ],
        'responses': {
            '200': {
                'description': 'User',
                'schema': UserSchema,
                'examples': {
                    'application/json': {
                        '_id': 1,
                        'name': 'somebody'
                    }
                }
            }
        }
    })
    @marshal_with(USER_FIELDS, envelope="user")
    @jwt_required()
    def get(self, _id):
        user = UserModel.get_user_by_id(_id)
        if user is None:
            abort(http_status_code=404)

        return UserDto(user), 200

    @swagger.doc({
        'tags': ['users'],
        'description': 'Deletes a user',
        'parameters': [
            {
                'name': 'id',
                'description': 'User id to be removed',
                'in': 'path',
                'type': "integer",
                'required': True
            }
        ],
        'responses': {
            '204': {
                'description': 'No content'
            }
        }
    })
    @jwt_required()
    def delete(self, _id):
        user = UserModel.get_user_by_id(_id)
        if user is None:
            abort(http_status_code=404)
        user.delete()
        return '', 204

    @swagger.doc({
        'tags': ['users'],
        'description': 'Updates a user',
        'parameters': [
            {
                'name': 'body',
                'description': 'Request body',
                'schema': UserSchema,
                'in': 'body',
                'required': True
            }
        ],
        'responses': {
            '201': {
                'description': 'User',
                'schema': UserSchema,
                'examples': {
                    'application/json': {
                        '_id': 1,
                        'name': 'somebody',
                        "admin": "false"
                    }
                }
            }
        }
    })
    @marshal_with(USER_FIELDS, envelope="user")
    @jwt_required()
    def put(self, _id):
        user = UserModel.get_user_by_id(_id)
        args = dict(self.reqparse.parse_args())
        user.name = args["name"]
        user.password = generate_password_hash(args["password"])
        user.isAdmin = args["isAdmin"]
        user.save()
        return UserDto(user), 200


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No user name provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                   help='No password provided',  location='json')
        super(UserList, self).__init__()

    @swagger.doc({
        'tags': ['users'],
        'description': 'Returns all users',
        'responses': {
            '200': {
                'description': 'Users',
                'schema': UserSchema,
                'examples': {
                    'application/json': {
                        'id': 1,
                        'name': 'somebody'
                    }
                }
            }
        }
    })
    @marshal_with(USER_FIELDS, envelope="users")
    @jwt_required()
    def get(self):
        users = UserModel.get_all()
        users = [UserDto(user) for user in users]
        return users

    @swagger.doc({
        'tags': ['users'],
        'description': 'Creates a user',
        'parameters': [
            {
                'name': 'body',
                'description': 'Request body',
                'schema': UserSchema,
                'in': 'body',
                'required': True
            }
        ],
        'responses': {
            '201': {
                'description': 'User',
                'schema': UserSchema,
                'examples': {
                    'application/json': {
                        '_id': 1,
                        'name': 'somebody',
                        "admin": "false"
                    }
                }
            }
        }
    })
    @marshal_with(USER_FIELDS, envelope="users")
    def post(self):
        args = dict(self.reqparse.parse_args())
        user = UserModel(name=args["name"], password=args["password"])
        user.save()
        return UserDto(user), 201
