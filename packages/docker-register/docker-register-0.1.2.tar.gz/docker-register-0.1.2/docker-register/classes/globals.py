#!/usr/bin/env python
import sys
import logging
import threading
from  Service import Service
from  RestServer import RestServer


LOG_FILE=''
logger = logging.getLogger ( __name__ )
fhdlr = None
pversion_major = sys.version_info[0]
pversion_minor = sys.version_info[1]
DEBUG = False
PORT = 8000
restServer = RestServer(PORT)
call_backs = []
BASE=''


def init_logger ():
    global fhdlr
    formatter = logging.Formatter('%(asctime)s ; %(filename)s:%(funcName)s() ; %(levelname)s ; %(message)s')
    if LOG_FILE != '':
      fhdlr = logging.FileHandler(LOG_FILE) 
      fhdlr.setFormatter(formatter)
      logger.addHandler(fhdlr)
    else:
      hdlr = logging.StreamHandler( sys.stdout )
      hdlr.setFormatter(formatter)
      logger.addHandler(hdlr)
    logger.setLevel(logging.CRITICAL)
    logger.setLevel(logging.ERROR)
    logger.setLevel(logging.WARNING)
    logger.setLevel(logging.INFO)
    if DEBUG:
      logger.setLevel(logging.DEBUG)

def init_globals (**kwargs):
  global DEBUG, LOG_FILE, call_backs, PORT, restServer, BASE

  if kwargs:
    for key, value in kwargs.items():
      if key == 'BASE':
        BASE = value
      if key == 'DEBUG':
        DEBUG = value
      if key == 'LOG_FILE':
        LOG_FILE = value
      if key == 'PORT':
        PORT = value
        restServer.port =  PORT
      if key == 'CALL_BACK':
        call_backs.append (value)

def init (**kwargs):

  init_globals (**kwargs)
  init_logger()
  

