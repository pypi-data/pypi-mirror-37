#!/usr/bin/python
###################################################################
#
#
#   RestServer
#
###################################################################
DEBUG = False

import logging
import urllib2 as _urllib2
import time 
import datetime
from time import gmtime, localtime, strftime
import datetime
import os
import threading
import signal
import getopt
import sys
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import jsonpickle  # For complex jsonfying our objects
import json

#from flask.logging import default_handler
import requests
import socket

filedir =  os.path.dirname ( os.path.realpath(__file__) )
flask = Flask('RestServer', template_folder = filedir + '/templates'  )
TOKEN=time.time()


import globals
import Service
import Container

@flask.route("/api")
def api():
  result = ' API call' 
  return result

@flask.route('/whoami')
def whoami():
    return 'I am docker register API Restful Server on ' + socket.gethostname()

@flask.route('/')
@flask.route('/index')
def index():
    return render_template ( 'index.html', title="Docker Register" )

@flask.route('/help')
def help():
    return render_template ( 'help.html', title="Docker Register - Help" )

@flask.route('/services')
def services():
    return render_template ( 'services.html', title="Docker Register - Services" , services = Service.services )

@flask.route('/service/<string:service_name>', methods=['GET']) 
def service(service_name):
    s = None
    for id, service in Service.services.items():
      if service.name == service_name:
        s = service
        break
#    jservice = jsonify ( service.__dict__ )
#    jservice = jsonpickle.encode ( service )
    temp_s = service
    jservice  = json.dumps(json.loads(jsonpickle.encode( temp_s )), indent=4) 
    return '<pre>' + jservice + '</pre>'

@flask.route('/containers')
def containers():
    return render_template ( 'containers.html', title="Docker Register - Containers" , containers = Container.containers )

@flask.route('/container/<string:container_name>', methods=['GET']) 
def container(container_name):
    c = None
    for id, container in Container.containers.items():
      if container.name == container_name:
        c = container
        break
#    jservice = jsonify ( service.__dict__ )
#    jservice = jsonpickle.encode ( service )
    temp_c = container
    jcontainer  = json.dumps(json.loads(jsonpickle.encode( temp_c )), indent=4) 
    return '<pre>' + jcontainer + '</pre>'

@flask.route('/quit')
def quit():
  token = request.args.get('token')
  if token == str(TOKEN):
    shutdown()
    return 'quiting ...'
  return 'no token given, not quiting ...'

def shutdown():
  func = request.environ.get('werkzeug.server.shutdown')
  if func is None:
      raise RuntimeError('Not running with the Werkzeug Server')
  func()



class RestServer(threading.Thread):

  count = 0
  name = 'RestServer'
  port = 0

  def __init__(self, port):
    threading.Thread.__init__(self)
    self.port = port

  def run (self):
    global flask

    flogger = logging.getLogger('werkzeug')
#    flogger.disabled = True
    if globals.fhdlr:
      flogger.addHandler(globals.fhdlr)
#    flogger.removeHandler(logging.StreamHandler)

#    flogger.setLevel(logging.ERROR)
#    flogger.setLevel(logging.DEBUG)
#    flask.logger.disabled = True

    globals.logger.info('Started thread ' + self.name + ' with token ' + str(TOKEN) + ' on port ' + str(self.port) )

    flask.run ( host='0.0.0.0' , port = self.port, debug = False , ssl_context=( filedir + '/ssl/cert.pem', filedir + '/ssl/key.pem') )
#    flask.run ( host='0.0.0.0' , port = self.port, debug = False )

  def quit(self):
      requests.get(url = "https://127.0.0.1:" + str(self.port) + "/quit" , params = 'token=' + str(TOKEN) , verify=False )
  
