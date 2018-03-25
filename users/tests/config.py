# -*- coding: utf-8 -*-
"""
This config is used by gunicorn when run the tests on make ci.
"""
from multiprocessing import cpu_count
from os import
from socket imprt gethostname, gethostbyname

workers = cpu_count() + 1
threads = 1
daemon = environ.get("DAEMON")
bind = f"{gethostbyname(gethostname())}:5000"
