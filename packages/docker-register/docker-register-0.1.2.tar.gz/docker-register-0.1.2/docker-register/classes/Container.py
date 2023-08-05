from sys import stdout, version_info
import json
import globals
import DkClient
import time
import threading
from Callbacks import Callbacks
import jsonpickle

container_lock = threading.RLock()
containers = dict ()
labels = dict()

dockerClient = DkClient.DkClient ()

class Container(object):

  id = ''
  name = ''
  ports = ''
  labels = dict()
  hostname = ''
  networks = dict()
  
  def __init__(self,id):
    self.id = id

  @staticmethod
  def process (data):
    data_t = data["Type"]
    try:
      if data_t == "container":
  #        json.dump(data,stdout)
        name = data["Actor"]["Attributes"]["name"]
        id = data["Actor"]["ID"]
        action = data["Action"]
        if action == 'create' or action == 'start':
          Container.register(id)
        if action == 'stop' or action == 'destroy':
          Container.unregister(id,name)
        if action == 'update':
          Container.update(id)
    except Exception as ex:
      globals.logger.warn ("caught error in Container process(): " + data_t )
      globals.logger.warn ("exception: " +  str(ex) )
      pass


  @staticmethod
  def add (container):
    global containers 
    globals.logger.debug('Adding container ' + container.name + ' (' + container.id + ')' )
    container_lock.acquire()
    containers [ container.id ] = container
    container_lock.release()
  
  @staticmethod
  def remove (id):
      container_lock.acquire()
      if id in containers:
        globals.logger.debug('Removing container ' + id )
        containers.pop ( id )
      container_lock.release()

  @staticmethod
  def load():
    try:
      global containers
      _containers = dockerClient.client.containers
      for c in _containers.list():
        labels = dict()
        container = Container ( c.id )
        container.name = c.name

        info = dockerClient.apiClient.inspect_container(c.id)
        published_ports = Container.get_ports(info)
        container.labels = c.labels
        container.hostname = Container.get_hostname(info)
        container.networks = Container.get_networks(info)
        container.published_ports = published_ports
        Container.add ( container )
        globals.logger.info ("loaded container " + container.name )
    except Exception as ex:
      globals.logger.warn ("caught error in Container load() " )
      globals.logger.warn ("exception: " +  str(ex) )
      pass

  @staticmethod
  def unload():
      global containers
      _containers = dockerClient.client.containers
      container_lock.acquire()
      containers = dict ()
      container_lock.release()

  @staticmethod
  def get_hostname (info): 
    _h = info['Config']['Hostname']
    return (_h)

  @staticmethod
  def get_networks (info): 
    _networks = info['NetworkSettings']['Networks']
    networks = []
    for key, value in _networks.items():
      networks.append ( { "name": key, "ip": value['IPAddress'] } )

    globals.logger.debug ( "returning networks: " + str(networks) )
    return (networks)

  @staticmethod
  def get_ports (info): 
    published_ports = []
    ports = dict()
    _ports = info['NetworkSettings']['Ports']
#    print ("\nINFO ports: " + str(ports) )
    for targetport, published_list in _ports.items():
      if published_list:
        ports[ targetport ] =  published_list 
        
    return ports

  @staticmethod
  def register(id):
    try:
      c = dockerClient.client.containers.get(id)
      container = Container ( c.id )
      container.name = c.name
      container.labels = c.labels

      info = dockerClient.apiClient.inspect_container(c.id)
      published_ports = Container.get_ports(info)
      container.hostname = Container.get_hostname(info)
      container.networks = Container.get_networks(info)
      container.published_ports = published_ports
      Container.add ( container )
      globals.logger.info("registering container {} ({})".format(container.name, container.id) )

      Callbacks.process ( "container", "register", container )
    except Exception as ex:
      globals.logger.warn ("caught error in Container register() " )
      globals.logger.warn ("exception: " +  str(ex) )
      pass

  @staticmethod
  def update(id):
    try:
      c = dockerClient.client.containers.get(id)
      container = Container ( c.id )
      container.name = c.name
      container.labels = c.labels

      info = dockerClient.apiClient.inspect_container(c.id)
      published_ports = Container.get_ports(info)
      container.hostname = Container.get_hostname(info)
      container.networks = Container.get_networks(info)
      container.published_ports = published_ports
      Container.add ( container )
      globals.logger.info("updating container {} ({})".format(container.name, container.id) )

      Callbacks.process ( "container", "update", container )
    except Exception as ex:
      globals.logger.warn ("caught error in Container update() " )
      globals.logger.warn ("exception: " +  str(ex) )
      pass

  @staticmethod
  def unregister(id,name):
    try:
      global containers

      globals.logger.info("Unregistering container {} ({})".format(name, id) )

      Container.remove ( id )
      Callbacks.process ("container", "unregister")
    except Exception as ex:
      globals.logger.warn ("caught error in Container unregister() " )
      globals.logger.warn ("exception: " +  str(ex) )
      pass


