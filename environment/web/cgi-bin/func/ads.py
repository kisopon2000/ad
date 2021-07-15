from launcher.rlauncher import RLauncher
from client.adclient import AdClient
import json

class AdsLauncher(RLauncher):
    def __init__(self):
        super(AdsLauncher, self).__init__()
    def initialize(self):
        return 0
    def run(self):
        if self.isGet():
            driver, server, dbname, uid, pwd, mem, memserver = self.getDBInfo()
            adclient = AdClient()
            adclient.connect(driver, server, dbname, uid, pwd)
            get = self.parseGet()
            ret = {}
            if not get.getvalue('ad_id'):
                ret["result"] = 1
            else:
                ad = adclient.getAds(str(get.getvalue('ad_id')))
                ad_target_campany_sectors = adclient.getTargetCompanySectors(str(get.getvalue('ad_id')))
                ad_target_campany_scales = adclient.getTargetCompanyScales(str(get.getvalue('ad_id')))
                ad_target_user_departments = adclient.getTargetUserDepartments(str(get.getvalue('ad_id')))
                ad_target_user_positions = adclient.getTargetUserPositions(str(get.getvalue('ad_id')))
                adclient.close()
                ret["result"] = 0
                ret["ads"] = ad
                ret["ads"].extend(ad_target_campany_sectors)
                ret["ads"].extend(ad_target_campany_scales)
                ret["ads"].extend(ad_target_user_departments)
                ret["ads"].extend(ad_target_user_positions)
                ret = json.dumps(ret)
            print(ret)
        if self.isPost():
            driver, server, dbname, uid, pwd, mem, memserver = self.getDBInfo()
            adclient = AdClient()
            adclient.connect(driver, server, dbname, uid, pwd)
            post = self.parsePost()
            ret = {}
            ret["result"] = adclient.postAds(str(post['company_id']),str(post['ad_landing_page_url']),str(post['ad_type_id']),str(post['ad_image_url']))
            adclient.close()
            ret = json.dumps(ret)
            print(ret)
        if self.isPut():
            driver, server, dbname, uid, pwd, mem, memserver = self.getDBInfo()
            adclient = AdClient()
            adclient.connect(driver, server, dbname, uid, pwd)
            put = self.parsePut()
            ret = {}
            ret["result"] = adclient.putAds(str(put['ad_id']),str(put['company_id']),str(put['ad_landing_page_url']),str(put['ad_type_id']),str(put['ad_image_url']))
            adclient.close()
            ret = json.dumps(ret)
            print(ret)
        if self.isDelete():
            driver, server, dbname, uid, pwd, mem, memserver = self.getDBInfo()
            adclient = AdClient()
            adclient.connect(driver, server, dbname, uid, pwd)
            delete = self.parseDelete()
            ret = {}
            ret["result"] = adclient.deleteAds(str(delete.getvalue('ad_id')))
            adclient.close()
            ret = json.dumps(ret)
            print(ret)
        return 0
    def finalize(self):
        return 0
