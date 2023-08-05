#!/usr/bin/env python
"""
Description: Implements a register of docker objects
"""
import os
import sys
import getopt
from classes import globals
from version import *
from  classes.Service import Service
from  classes.Container import Container
import monitor

DEBUG = False
USAGE=__file__ + ' [-h] [-d] [-c cb1 .. -c cbN] [-l logfile ] [-p port] [-v] [-R]' + __doc__
BASE = os.path.dirname ( os.path.realpath(__file__) )


def usage ():
  print ( 'Usage: ' + USAGE + "\n\
   -h|--help  : this help\n\
   -d|--debug : debug on\n\
   -l|--logfile FILE : FILE the path to the log file \n\
   -p|--port port : port to run restful server (default: " + str(globals.PORT) + ") \n\
   -c|--callback PROG : script or executable to callback \n\
   -v|--version : shows version  \n\
   -R|--README : shows the README file \n\n\
   E.g.   " + __file__ + " -c jq\n\
          " + __file__ + " -c jq -p 9000 \n\
          " + __file__ + " -c jq -p 9000 -l /var/log/register.log \n\
\n"
  )


def  getopts():
  global USAGE
  global DEBUG

  try:
    opts, args = getopt.getopt(sys.argv[1:],"hdl:c:p:vR",["help","debug","logfile","callback","port","version", "README"])
  except getopt.GetoptError:
    usage('Error:')
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      usage()
      sys.exit(0)
    if opt in ( '-d', '--debug' ):
      globals.init_globals (DEBUG=True)
    if opt in ( '-l', '--logfile' ):
      globals.init_globals (LOG_FILE=arg)
    if opt in ( '-c', '--callback' ):
      globals.init_globals (CALL_BACK=arg)
    if opt in ( '-p', '--port' ):
      globals.init_globals (PORT=arg)
    if opt in ( '-v', '--version' ):
      print("version: " + VERSION)
      sys.exit(0)
    if opt in ( '-R', '--README' ):
      filedir =  os.path.dirname ( os.path.realpath(__file__) )
      print ( open(filedir + "/README.txt").read() )
      sys.exit(0)


def main ():

    getopts()
    globals.init_globals (BASE=BASE)
    globals.init()
    if globals.DEBUG:
      globals.logger.info("Started with DEBUG ")
    else:
      globals.logger.info("Started")

#    Service.load()
#    Container.load()

    #  ref: https://www.slideshare.net/dabeaz/an-introduction-to-python-concurrency
    #  Start RestServer listener thread 
    #  
    globals.restServer.start()
  
    monitor.start_events_listener()

    #   Wait for api listerner to end (with join)
    globals.logger.info("Terminating ...")
    globals.restServer.quit()
    globals.restServer.join()


if __name__ == '__main__':
  main()
