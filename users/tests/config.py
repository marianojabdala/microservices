# -*- coding: utf-8 -*-
import multiprocessing
from os import environ

workers = multiprocessing.cpu_count() + 1
threads = 1
daemon = environ.get("DAEMON")
bind = "127.0.0.1:5000"

