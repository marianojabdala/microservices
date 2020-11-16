# -*- coding: utf-8 -*-
"""
This config is used by gunicorn when run the tests on make ci.
"""
from multiprocessing import cpu_count
from socket import gethostname, gethostbyname
from os import environ, getuid, getgid

workers = cpu_count() + 1
threads = 1
daemon = environ.get("DAEMON")
certfile="microservice-example.org+4.pem"
keyfile="microservice-example.org+4-key.pem"
user=getuid()
group=getgid()
bind = f"{gethostbyname(gethostname())}:5000"
access_log_format='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s %(D)sµs"'
