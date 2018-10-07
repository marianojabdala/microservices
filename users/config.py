# -*- coding: utf-8 -*-
import multiprocessing
from os import environ, getuid, getgid


workers=multiprocessing.cpu_count() * 2 + 1
threads=1
errorlog='-'
loglevel='info'
accesslog='-'
port=5000 if environ.get("APP_SETTINGS").upper()=="DEVELOPMENT" else 80
bind="0.0.0.0:" + str(port)
certfile="microservice-example.org+4.pem"
keyfile="microservice-example.org+4-key.pem"
user=getuid()
group=getgid()
daemon=False if environ.get("DAEMON") is None else True
access_log_format='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s %(D)sµs"'


def when_ready(server):
    server.log.info("Server is ready. Spawning workers")
