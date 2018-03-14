# -*- coding: utf-8 -*-
from flask_restful import abort, Resource

class Base(Resource):

    @staticmethod
    def abort_if_object_doesnt_exist(obj_property, id_obj, objects):
        obj = [obj for obj in objects if obj[obj_property] == id_obj]
        if obj is None:
            abort(404, message="Object {} doesn't exist".format(id_obj))
