# -*- coding: utf-8 -*-
"""User Resource that will be use on the api."""
from flask_restful import reqparse, fields, marshal_with, abort
from flask_restful_swagger_2 import swagger, Resource
from flask_jwt import jwt_required

from werkzeug.security import generate_password_hash

from swagger.schemas.user import UserSchema
from resources.base import Base
from models.user import UserModel
from dtos.user import UserDto

USER_FIELDS = {
    "_id": fields.Integer,
    "name": fields.String,
    "admin": fields.Boolean,
    "uri": fields.Url("user")
}


class UserResource(Base):
    """User list resource used by /users<id> with GET, POST ,PUT ,DELETE."""

    def __init__(self):
        """Construct."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('_id', type=str, required=True,
                                   help='No user id provided', location='json')
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No user name provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                   help='No password provided', location='json')
        self.reqparse.add_argument('isAdmin', type=bool, required=True,
                                   help='No is_admin was provided', location='json')

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
    # pylint: disable=no-self-use
    def get(self, _id):
        """
        Get method that will retrieve a user from the _id.

        :param _id: The user id
        :return: UserDto
        """
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
    # pylint: disable=no-self-use
    def delete(self, _id):
        """
        Delete method that will remove a user from the database using the _id.

        :param _id: The user id
        :return: HTTP code. 204
        """
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
        """
        Update a user from the id and the arguments that came from the body.

        :param _id: user id.
        :return: UserDto
        """
        user = UserModel.get_user_by_id(_id)
        args = dict(self.reqparse.parse_args())
        user.name = args["name"]
        user.password = generate_password_hash(args["password"])
        user.is_admin = args["isAdmin"]
        user.save()
        return UserDto(user), 200


class UserList(Resource):
    """
    User list resource.

    Used by /users GET(all the users) and POST(to create a user).

    """

    def __init__(self):
        """Construct."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No user name provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                   help='No password provided', location='json')
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
    # pylint: disable=no-self-use
    def get(self):
        """
        Return the collection of users.

        :return: collection of users mapped by the UserDto
        """
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
        """
        User creation.

        :return: UserDto.
        """
        args = dict(self.reqparse.parse_args())
        user = UserModel(name=args["name"], password=args["password"])
        user.save()
        return UserDto(user), 201
