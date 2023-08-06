from apitax.drivers.Driver import Driver
from apitax.utilities.Files import getAllFiles
from apitax.ah.Options import Options
from pathlib import Path
from apitax.ah.Credentials import Credentials
from apitax.utilities.Json import read
from apitax.ah.State import State
from apitax.utilities.Files import getPath


class VsrxDriver(Driver):

    def __init__(self):
        super().__init__()
        self.users = read(getPath(State.paths['root'] + "/app/users.json"))

    def isCredentialsPosted(self):
        return False

    def isConfigurable(self):
        return True

    def isTokenable(self):
        return False
        
    def isApiAuthenticated(self):
        return False
        
    def piggyBackOffApiAuth(self):
        return True

    def getContentTypeJSON(self):
        # if(not self.isAuthenticated()):
        #   return {}
        return {'Content-Type': 'application/xml'}

    def getCatalog(self, auth):
        catalog = {'endpoints': {'demo': {'label': 'demo', 'value': 'http://172.25.190.59:3000'}}}
        catalog['selected'] = 'http://172.25.190.59:3000'
        return catalog

    def apitaxAuth(self, authObj):
        authObj = authObj['credentials']
        authRequest = ['apiAuthRequest']
        #print(authRequest)
        try:
            return self.users[authObj.username]['role']
        except:
            return None
        return None