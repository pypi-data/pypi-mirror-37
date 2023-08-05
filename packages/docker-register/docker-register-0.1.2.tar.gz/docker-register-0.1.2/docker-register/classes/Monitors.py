from sys import stdout, version_info
import json
import globals
from Service import Service
from Container import Container



class Monitors(object):

  def __init__(self):
    pass

  @staticmethod
  def process (data):
#  json.dump(data,stdout)
    data_t = data["Type"]
    if data_t == "container":
      Container.process(data)
    if data_t == "service":
      Service.process(data)

  @staticmethod
  def load ():
    Service.load()
    Container.load()


