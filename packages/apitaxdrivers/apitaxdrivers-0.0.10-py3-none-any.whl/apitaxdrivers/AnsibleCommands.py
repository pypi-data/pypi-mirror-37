# Application imports
from apitax.drivers.DriverCommands import DriverCommands
from apitax.ah.State import State

# from apitax.drivers.plugins.commandtax.apitaxtests import *

# Openstack Command Driver for handling custom commands when the openstack driver is used
class AnsibleCommands(DriverCommands):

    def getDriverName(self):
        return 'ansible'


    def handle(self, command):
        import subprocess
        #call(["ansible-playbook"] + command)

        proc = subprocess.Popen(["ansible-playbook"] + command[:-2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        out = str(out.decode("utf-8"))
        err = str(err.decode("utf-8"))
        #print ('stdout:'+ str(out))
        #print ('stderr:'+str(err))
        return Response(status=200, body = "out: " + out + " ### err: " + err)
        #return self




class Response:

    def __init__(self, status=None, body=None):
        self.status = status
        self.body = body
	
    def getResponseBody(self):
        return self.body
        
    def getResponseStatusCode(self):
        return self.status