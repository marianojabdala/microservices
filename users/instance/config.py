# -*- codi$ContentRoot$ng: utf-8 -*-
"""Config Objects used to get all the environment variables."""
import os
import datetime
import socket

class Config(object):
    """Parent configuration class."""

    DEBUG = False
    CSRF_ENABLED = True
    PATH = os.getcwd()
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD= os.getenv("DB_PASSWORD")
    CREATE_INITIAL_DB = os.getenv("DB_INIT")
    DB_DEFAULT = os.getenv("DB_DEFAULT")
    DATABASE = DB_DEFAULT if CREATE_INITIAL_DB else os.getenv('DATABASE')
    DB_USER_PASS = DB_USER + ":" + DB_PASSWORD if DB_USER is not None else ""
    DB_HOST = f"{DB_USER_PASS}{'@'}{os.getenv('DB_HOST')}" if DB_USER_PASS else None
    SQLALCHEMY_DATABASE_URI = f"{os.getenv('DB_PREFIX')}{DB_HOST if DB_HOST is not None else PATH}/" \
                              f"{DATABASE}{os.getenv('DB_SUFFIX')}"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_AUTH_HEADER_PREFIX = os.getenv("JWT_AUTH_HEADER_PREFIX")
    JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=30)
    JWT_AUTH_URL_RULE = os.getenv("JWT_AUTH_URL_RULE")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ENVIRONMENT = os.getenv("APP_SETTINGS")
    HOST = socket.getfqdn()
    BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
    BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD")


    def to_json(self):
        """Return a json object with the used environment variables."""
        return {
            "DEBUG": self.DEBUG,
            "CSRF_ENABLED": self.CSRF_ENABLED,
            "SQLALCHEMY_DATABASE_URI": self.SQLALCHEMY_DATABASE_URI,
            "JWT_AUTH_HEADER_PREFIX": self.JWT_AUTH_HEADER_PREFIX,
            "JWT_AUTH_URL_RULE": self.JWT_AUTH_URL_RULE,
            "JWT_EXPIRATION_DELTA(seconds)": self.JWT_EXPIRATION_DELTA.seconds,
            "ENVIRONMENT": self.ENVIRONMENT,
            "DB_HOST": self.DB_HOST,
            "PWD": self.PATH,
            "HOST": self.HOST,
            "CREATE_DB": "Yes" if self.CREATE_INITIAL_DB else "No"
        }

class DevelopmentConfig(Config):
    """Configurations for Development."""

    SQLALCHEMY_DATABASE_URI = f"{os.getenv('DB_PREFIX')}{Config.DB_HOST if Config.DB_HOST else Config.PATH }/" \
                              f"{os.getenv('DATABASE')}{os.getenv('DB_SUFFIX')}"

    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"{os.getenv('DB_PREFFIX_TEST')}{os.getenv('TMP_DIR')}/" \
                              f"{os.getenv('TEST_DATABASE')}{os.getenv('DB_SUFIX_TEST')}"

    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""

    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""

    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
