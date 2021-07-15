from launcher.rlauncher import RLauncher
from client.adclient import AdClient
import json

class AdTypesLauncher(RLauncher):
    def __init__(self):
        super(AdTypesLauncher, self).__init__()
    def initialize(self):
        return 0
    def run(self):
        if self.isGet():
            driver, server, dbname, uid, pwd, mem, memserver = self.getDBInfo()
            adclient = AdClient()
            adclient.connect(driver, server, dbname, uid, pwd)
            adtypes = adclient.getAdTypes()
            adclient.close()
            ret = {}
            ret["result"] = 0
            ret["ad_types"] = adtypes
            ret = json.dumps(ret)
            print(ret)
        return 0
    def finalize(self):
        return 0
