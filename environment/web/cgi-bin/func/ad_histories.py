import os
import json

from launcher.rlauncher import RLauncher
from client.adclient import AdClient
from client.analysisclient import AnalysisClient

class AdHistoriesLauncher(RLauncher):
    def __init__(self):
        super(AdHistoriesLauncher, self).__init__()
    def initialize(self):
        return 0
    def run(self):
        if self.isPut():
            token = self.getToken()
            company_id = token["company_id"]
            user_id = token["user_id"]
            put = self.parsePut()
            ad_id = put['ad_id']
            is_displayed = put['is_displayed']
            is_clicked = put['is_clicked']
            driver, server, dbname, uid, pwd, mem, memserver = self.getDBInfo()
            adclient = AdClient()
            adclient.connect(driver, server, dbname, uid, pwd)
            ads = adclient.updateAdHistories(company_id, user_id, ad_id, is_displayed, is_clicked)
            adclient.close()
            ret = {}
            ret["result"] = 0
            ret = json.dumps(ret)
            print(ret)
        return 0
    def finalize(self):
        return 0
