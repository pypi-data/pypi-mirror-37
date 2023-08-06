from scriptax.catalogs.ScriptCatalog import ScriptCatalog

from apitaxdrivers.integrations.Github import Github
from scriptax.drivers.builtin.Scriptax import Scriptax


class GithubDriver(Scriptax):

    def __init__(self):
        super().__init__()
        self.git = Github(self.driverConfig.get('personal-access-token'), self.driverConfig.get('repo'))

    def isDriverConfigurable(self) -> bool:
        return True

    def getDriverName(self) -> str:
        return "github"

    def getDriverDescription(self) -> str:
        return "Provides access to a github repository for utilizing scripts"

    def getDriverHelpEndpoint(self) -> str:
        return "coming soon"

    def getDriverTips(self) -> str:
        return "coming soon"

    def getDriverScriptCatalog(self) -> ScriptCatalog:
        catalog = ScriptCatalog()
        for file in self.git.getFiles():
            path = file.path
            if path[-3:] == '.ah':
                catalog.add(label=path.split('/')[-1].split('.')[0].title(), path=self.git.getPath(path))
        return catalog

    def getDriverScript(self, path) -> str:
        return self.git.getFileContent(path)

    def renameDriverScript(self, original, now) -> bool:
        return self.git.renameFile(original, now)

    def saveDriverScript(self, path, content) -> bool:
        return self.git.createOrUpdate(path, content)

    def deleteDriverScript(self, path) -> bool:
        return self.git.deleteFile(path=path)
