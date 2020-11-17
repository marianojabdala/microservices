# -*- coding: utf-8 -*-
"""Create the application and other endpoints."""
from os import path

from dotenv import load_dotenv, find_dotenv

from flask import Flask, json
from flask_restful_swagger_2 import Api
from flask_jwt import JWT
from flask_basicauth import BasicAuth

import psutil

from resources.user import UserResource, UserList
from security import authenticate, identity

load_dotenv(find_dotenv(".env", raise_error_if_not_found=True), verbose=True)

from instance.config import app_config #pylint: disable=wrong-import-position


def create_app(config_name, database=None):
    """
    Create the api application with the proper configurations.

    :param config_name: The name of the configuration to load, eg: development, production
    :param database: The database object
    :return the app object whit the Flask app in it.
    """
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object(app_config[config_name])
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    a_p_i = Api(application, api_version='1.0',
                api_spec_url='/api/swagger')

    a_p_i.add_resource(UserList, "/users", endpoint="users")
    a_p_i.add_resource(UserResource, "/users/<_id>", endpoint="user")

    JWT(application, authenticate, identity) # pylint: disable=unused-variable

    add_index_endpoint(application)

    add_health_endpoint(application)

    add_environment_endpoint(application, app_config[config_name])

    if database is not None:
        add_database_creation_endpoint(application, database)

    return application


def add_health_endpoint(app):
    """
    Add /_health endpoint.

    :param app: The application to add the endpoint
    :return: A json object that shows metrics about the application and the system.
    """
    @app.route("/_health", methods=["GET"])
    def health(): # pylint: disable=unused-variable
        """
        Create the /_health endpoint for the app and the system.

        :param app: The application to add the endpoint
        :return: A json object that shows metrics about the application and the system.
        """
        process = psutil.Process()
        with process.oneshot():
            current_pid = process.ppid()
            cpu_num = process.cpu_num() + 1  # return cached values
            cpu_percent = process.cpu_percent()  # return cached value

        process = psutil.Process(current_pid)

        full_memory_info = process.memory_full_info()
        rss = full_memory_info[0]
        vms = full_memory_info[1]
        shared = full_memory_info[2]
        uss = full_memory_info[7]
        pss = full_memory_info[8]

        system_memory = psutil.virtual_memory()
        process_memory = process.memory_percent()
        environ = process.environ()

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
    Create a /_environ endpoint.

    This creates a /_environ endpoint where expose some variables used in the
    application to verify if they are ok.

    :param app:
    :param config:
    :return: A json file that expose the configuration variables loaded on the environment.
    """
    @app.route("/_environ", methods=["GET"])
    def environment(): # pylint: disable=unused-variable
        """
        Create a /_environ endpoint.

        This endpoint will expose some variables used in the application
        to verify if they are ok.

        :param app:
        :param config:
        :return: A json file that expose the configuration variables loaded on the environment.
        """
        return json.dumps(
            {
                "app":
                    {
                        "environ": config.to_json(config)
                    }
            }
        )


def add_database_creation_endpoint(app, database):
    """
    Initialize the dabase.

    This endpoint allow us to initialize the database in case it is not already,
    useful when deployed into kubernetes or docker-compose
    :param app:
    :param database:
    """
    basic_auth = BasicAuth(app)

    # Create a unique endpoint that will be used to initialze the database with the proper tables.
    @app.route("/_init_db", methods=["POST"])
    @basic_auth.required
    def init_db(): # pylint: disable=unused-variable
        """
        Endpoint that Initialize the database.

        :return: json message.
        """
        try:
            database.create_all()
        except ConnectionError:
            # if the database doesn't exist we create it.
            _create_database(app.config, database)

        return json.dumps(("Database Initialized!!!"))


def _create_database(config, database):
    """
    Create the tables if it doesn't exists.

    :param config: configuration object
    :param database: the database object to be used
    :return: None
    """
    engine = database.create_engine(config["SQLALCHEMY_DATABASE_URI"])
    conn = engine.connect()
    conn.execute("commit")
    conn.execute(f"create database{config['DATABASE']}")
    conn.close()


def add_index_endpoint(app):
    """
    Add the /index endpoint.

    :param app:
    :return: None
    """
    @app.route("/")
    def index():    # pylint: disable=unused-variable
        """
        Index endopoint.

        :return: the content of the index.html file to be used on the index of the project.
        """
        return open(path.join(path.dirname(__file__), "index.html")).read()


def format_value(number):
    """
    Format the value with  ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y').

    Defines the format of the value that will be shown on the /_health endpoint,
    this could be K, M, G ,etc

    :param number: The value to be use.
    :return: Formatted value.
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for index, symbol in enumerate(symbols):
        prefix[symbol] = 1 << (index + 1) * 10
    for symbol in reversed(symbols):
        if number >= prefix[symbol]:
            value = float(number) / prefix[symbol]
            return '%.1f%s' % (value, symbol)
    return "%sB" % number
