# -*- coding: utf-8 -*-
"""
This config is used by gunicorn when run the tests on make ci.
"""

workers = 1
threads = 1
daemon = False
bind = "127.0.0.1:5000"
access_log_format='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s %(D)sµs"'
