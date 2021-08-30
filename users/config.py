# -*- coding: utf-8 -*-
import multiprocessing
from os import environ, getuid, getgid


workers=multiprocessing.cpu_count() * 2 + 1
threads=1
errorlog='-'
loglevel='info'
accesslog='-'
port= environ.get("APP_PORT", 8000)
bind = f'0.0.0.0:{port}'
user=getuid()
group=getgid()
access_log_format='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s %(D)sµs"'


def when_ready(server):
    server.log.info("Server is ready. Spawning workers")
