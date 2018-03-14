# -*- coding: utf-8 -*-
# import sys
# def main(args=None):
#     """The main routine."""
#     if args is None:
#         args = sys.argv[1:]
    # print("This is the main routine.")
    # print("It should do something interesting.")

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.

import os

from flask_cors import CORS
from users.db import db
from users.instance import create_app

app = create_app(os.getenv("APP_SETTINGS"))

CORS(app)

db.init_app(app)

if __name__ == '__main__':
    app.run()


# if __name__ == "__main__":
#     main()