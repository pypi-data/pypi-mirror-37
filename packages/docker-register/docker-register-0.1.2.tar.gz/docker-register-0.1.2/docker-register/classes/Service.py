from sys import stdout, version_info
import json
import globals
import DkClient
import time
import threading
from Callbacks import Callbacks
import jsonpickle

service_lock = threading.RLock()
services = dict ()
labels = dict()

dockerClient = DkClient.DkClient ()

class Service(object):

  id = ''
  name = ''
  ports = ''
  labels = dict()
  
  def __init__(self,id):
    self.id = id

  @staticmethod
  def process (data):
    data_t = data["Type"]
    try:
      if data_t == "service":
  #        json.dump(data,stdout)
        name = data["Actor"]["Attributes"]["name"]
        id = data["Actor"]["ID"]
        action = data["Action"]
        if action == 'create':
          Service.register_service(id)
        if action == 'remove':
          Service.unregister_service(id,name)
        if action == 'update':
          Service.update_service(id)
    except Exception as ex:
      globals.logger.warn ("caught error in Service process(): " + data_t )
      globals.logger.warn ("exception: " +  str(ex) )
      pass


  @staticmethod
  def add (service):
    global services 
    globals.logger.debug('Adding service ' + service.name + ' (' + service.id + ')' )
    service_lock.acquire()
    services [ service.id ] = service
    service_lock.release()
  
  @staticmethod
  def remove (id):
      service_lock.acquire()
      if id in services:
        globals.logger.debug('Removing service ' + id )
        services.pop ( id )
      service_lock.release()

  @staticmethod
  def load():
    try:
      global services
      _services = dockerClient.client.services
      for s in _services.list():
        labels = dict()
        if globals.DEBUG:
          globals.logger.debug ( "\n" )
          globals.logger.debug ( json.dump (s.attrs,stdout) )
        service = Service ( s.id )
        service.name = s.name
        if "Labels" in s.attrs['Spec']:
          for k,  v  in  s.attrs['Spec']['Labels'].items():
            labels[k] = v

        published_ports = Service.get_ports(s.attrs)
            
        service.labels = labels
        service.published_ports = published_ports
        Service.add ( service )
        globals.logger.info ("loaded service " + service.name )
    except Exception as ex:
      globals.logger.warn ("caught error in Service load() " )
      globals.logger.warn ("exception: " +  str(ex) )
      pass

  @staticmethod
  def unload():
      global services
      _services = dockerClient.client.services
      service_lock.acquire()
      services = dict ()
      service_lock.release()

  @staticmethod
  def get_ports (attrs): 
    published_ports = []
    if 'Ports' in attrs['Spec']['EndpointSpec']:
      ports = attrs['Spec']['EndpointSpec']['Ports']
      for p in ports:
        if 'PublishedPort' in p:
  #        print("   {}".format(p['PublishedPort'])) 
  #          published_ports = published_ports + str( p['PublishedPort']) + ' '
          published_ports.append ( { 'TargetPort' : p['TargetPort'] , 'PublishedPort' : p['PublishedPort'] } )

    if not published_ports:
      if 'Ports' in attrs['Endpoint']:
        ports = attrs['Endpoint']['Ports']
        for p in ports:
          if 'PublishedPort' in p:
#              published_ports = published_ports + str( p['PublishedPort']) + ' '
            published_ports.append ( { 'TargetPort' : p['TargetPort'] , 'PublishedPort' : p['PublishedPort'] } )

      if not published_ports:
        published_ports = 'None'

    return (published_ports)

  @staticmethod
  def register_service(id):
      global services

      service = dockerClient.client.services.get(id)
      if globals.DEBUG:
#        json.dump(service.attrs,stdout)
        globals.logger.debug ( json.dump(service.attrs,stdout) )
        globals.logger.info("")
        
      ports = service.attrs['Spec']['EndpointSpec']['Ports']
      published_ports = []
#      print("Registering service {} ({}) with ports:".format(service.name,id))
      for p in ports:
        if 'PublishedPort' in p:
#        print("   {}".format(p['PublishedPort'])) 
#          published_ports = published_ports + str( p['PublishedPort']) + ' '
          published_ports.append ( { 'TargetPort' : p['TargetPort'] , 'PublishedPort' : p['PublishedPort'] } )

      if not published_ports:
        if 'Ports' in service.attrs['Endpoint']:
          ports = service.attrs['Endpoint']['Ports']
          for p in ports:
            if 'PublishedPort' in p:
#              published_ports = published_ports + str( p['PublishedPort']) + ' '
              published_ports.append ( { 'TargetPort' : p['TargetPort'] , 'PublishedPort' : p['PublishedPort'] } )

      if not published_ports:
        published_ports = 'euphemeral'

      labels = dict ()
      if "Labels" in service.attrs['Spec']:
        for k,  v  in  service.attrs['Spec']['Labels'].items():
          labels[k] = v


      globals.logger.info("Registering service {} ({}) ports: {}".format(service.name,id,published_ports) )
      s = Service ( id )
      s.name = service.name
      s.ports = published_ports
      s.labels = labels

      Service.add ( s )

      Callbacks.process ( "service", "register", s )

  @staticmethod
  def update_service(id):
      global services

      service = dockerClient.client.services.get(id)
      if globals.DEBUG:
#        json.dump(service.attrs,stdout)
        globals.logger.debug ( json.dump(service.attrs,stdout) )
        globals.logger.info("")

      ports = service.attrs['Spec']['EndpointSpec']['Ports']
      published_ports = []
#      print("Registering service {} ({}) with ports:".format(service.name,id))
      for p in ports:
        if 'PublishedPort' in p:
#        print("   {}".format(p['PublishedPort'])) 
#          published_ports = published_ports + str( p['PublishedPort']) + ' '
          published_ports.append ( { 'TargetPort' : p['TargetPort'] , 'PublishedPort' : p['PublishedPort'] } )

      if not published_ports:
        if 'Ports' in service.attrs['Endpoint']:
          ports = service.attrs['Endpoint']['Ports']
          for p in ports:
            if 'PublishedPort' in p:
#              published_ports = published_ports + str( p['PublishedPort']) + ' '
              published_ports.append ( { 'TargetPort' : p['TargetPort'] , 'PublishedPort' : p['PublishedPort'] } )

      if not published_ports:
        published_ports = 'euphemeral'

      labels = dict ()
      if "Labels" in service.attrs['Spec']:
        for k,  v  in  service.attrs['Spec']['Labels'].items():
          labels[k] = v


      globals.logger.info("Updating service {} ({}) ports: {}".format(service.name,id,published_ports) )
      s = Service ( id )
      s.name = service.name
      s.ports = published_ports
      s.labels = labels

      Service.add ( s )

      Callbacks.process ("service", "update", s)

  @staticmethod
  def unregister_service(id,name):
      global services

      globals.logger.info("Unregistering service {} ({})".format(name, id) )
#      print("Unregistering service {} ({})\n".format(name, id))
      s = services[id]
      Service.remove ( id )
      Callbacks.process ("service", "unregister", s )


