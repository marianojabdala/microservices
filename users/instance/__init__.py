# -*- coding: utf-8 -*-
from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_restful_swagger_2 import Api
from flask_jwt import JWT

from resources.user import UserResource, UserList
from security import authenticate, identity
import json
import psutil

load_dotenv(find_dotenv(".env", raise_error_if_not_found=True), verbose=True)

from instance.config import app_config

from flask import json
from flask_basicauth import BasicAuth


def create_app(config_name, db):
    """
        Creates the api application with the proper configurations.
        :param config_name: The name of the configuration to load, eg: development, production
        :param db: The database object
        :return the api object whit the Flask app in it.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    api = Api(app, api_version='1.0',
              api_spec_url='/api/swagger')

    api.add_resource(UserList, "/users", endpoint="users")
    api.add_resource(UserResource, "/users/<_id>", endpoint="user")

    jwt = JWT(app, authenticate, identity)

    add_index_endpoint(app)

    add_health_endpoint(app)

    add_environment_endpoint(app, app_config[config_name])

    add_database_creation_endpoint(app, db)

    return app


def add_health_endpoint(app):
    """
    Creates and endpoint to know the health of the application and also of the system where it is running.
    :param app: The application to add the endpoint
    """

    @app.route("/_health", methods=["GET"])
    def health():
        p = psutil.Process()
        with p.oneshot():
            current_pid = p.ppid()
            cpu_num = p.cpu_num() + 1  # return cached values
            cpu_percent = p.cpu_percent()  # return cached value

        p = psutil.Process(current_pid)

        full_memory_info = p.memory_full_info()
        rss = full_memory_info[0]
        vms = full_memory_info[1]
        shared = full_memory_info[2]
        uss = full_memory_info[7]
        pss = full_memory_info[8]

        system_memory = psutil.virtual_memory()
        process_memory = p.memory_percent()
        environ = p.environ()

        return json.dumps(
            {
                "app": {
                    "process memory used %": round(process_memory, 2),
                    "rss": format_value(rss),
                    "vms": format_value(vms),
                    "uss": format_value(uss),
                    "pss": format_value(pss),
                    "shared": format_value(shared),
                    "running on cpu N°": cpu_num,
                    "cpu used in %": cpu_percent
                }, "system": {
                        "environ": environ,
                        "total memory": format_value(system_memory[0]),
                        "available memory": format_value(system_memory[1]),
                        "percent total memory": system_memory[2],
                        "used memory": format_value(system_memory[3])
            }
        })


def add_environment_endpoint(app, config):
    """
    This creates a /_environ endpoint where expose some variables used in the application to verify if they are rigth.
    :param app:
    :param config:
    """
    @app.route("/_environ", methods=["GET"])
    def environment():
        return json.dumps(
        {
            "app": {
                "environ": config.to_json(config),
            }
        })


def add_database_creation_endpoint(app, db):
    """
    This endpoint allow us to initialize the database in case it is not already, usefull when deployed into
    kubernetes or docker-compose
    :param app:
    :param db:
    """
    basic_auth = BasicAuth(app)

    # Create a unique endpoint that will be used to initialze the database with the proper tables.
    @app.route("/_init_db", methods=["POST"])
    @basic_auth.required
    def init_db():
        try:
            db.create_all()
        except:
            # if the database doesn't exist we create it.
            _create_database(app.config, db)

        return json.dumps(("Database Initialized!!!"))


def _create_database(config, db):
    engine = db.create_engine(config["SQLALCHEMY_DATABASE_URI"])
    conn = engine.connect()
    conn.execute("commit")
    conn.execute(f"create database{config['DATABASE']}")
    conn.close()


def add_index_endpoint(app):
    @app.route("/")
    def index():
        from os import path
        return open(path.join(path.dirname(__file__), "index.html")).read()


def format_value(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


