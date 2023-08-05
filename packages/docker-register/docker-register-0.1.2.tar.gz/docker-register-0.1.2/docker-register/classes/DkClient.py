from sys import stdout, version_info
import json
import docker
import globals

class DkClient ():

  client = docker.DockerClient(base_url='unix://var/run/docker.sock')
#  client = docker.Client(base_url='unix://var/run/docker.sock')
  apiClient = docker.APIClient (base_url='unix://var/run/docker.sock')

  def __init__(self):
    pass

  def show_services (self):
    
    _services = self.client.services.list()
    print( "services: {} \n".format (_services) )

      



