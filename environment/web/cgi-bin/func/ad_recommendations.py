import os
import json

from distutils.util import strtobool
from launcher.rlauncher import RLauncher
from client.adclient import AdClient
from client.analysisclient import AnalysisClient

class AdRecommendationsLauncher(RLauncher):
    def __init__(self):
        super(AdRecommendationsLauncher, self).__init__()
    def initialize(self):
        return 0
    def run(self):
        if self.isGet():
            token = self.getToken()
            user_id = token["user_id"]
            get = self.parseGet()
            ad_user_id = get['ad_user_id'].value
            ad_type_id = get['ad_type_id'].value
            is_multi = strtobool(get['is_multi'].value)
            driver, server, dbname, uid, pwd, mem, memserver = self.getDBInfo()
            adclient = AdClient()
            adclient.connect(driver, server, dbname, uid, pwd, mem, memserver)
            ads = adclient.getRecommendedAd(user_id, ad_type_id, mem, is_multi)
            adclient.close()
            ret = {}
            ret["result"] = 0
            ret["ads"] = ads
            ret = json.dumps(ret)
            print(ret)
        # driver, server, dbname, uid, pwd = self.getDBInfo()
        # analysisclient = AnalysisClient()
        # analysisclient.connect(driver, server, dbname, uid, pwd)
        # analysisclient.createModel()
        # analysisclient.close()
        return 0
    def finalize(self):
        return 0
