from instance import create_app
from db import DB
import logging

def before_all(context):
    context.app = create_app(config_name="testing")
    context.client = context.app.test_client
    if not context.config.log_capture:
        logging.basicConfig(level=logging.DEBUG)

    # binds the app to the current context
    with context.app.app_context():
        DB.init_app(context.app)
        # create all tables
        DB.create_all()

def after_all(context):
    """Teardown all initialized variables."""
    with context.app.app_context():
        # drop all tables
        DB.session.remove()
        DB.drop_all()
