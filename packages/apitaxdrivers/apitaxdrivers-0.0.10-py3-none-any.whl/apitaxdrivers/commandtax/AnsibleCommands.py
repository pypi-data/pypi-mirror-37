# Application imports
from apitax.drivers.DriverCommands import DriverCommands
from apitax.ah.State import State

# from apitax.drivers.plugins.commandtax.apitaxtests import *

# Openstack Command Driver for handling custom commands when the openstack driver is used
class AnsibleCommands(DriverCommands):

    def getDriverName(self):
        return 'ansible'
        
    def getResponseBody(self):
        State.log.log("yes")
        return 'winner takes all'

    def handle(self, command):
        State.log.log(command)
        return self
