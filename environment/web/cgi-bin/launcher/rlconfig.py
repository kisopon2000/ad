from launcher.rlobject import RLObject
from lib.utility import SystemConfigApi

class RLConfig(RLObject):
    m_cConfig = None
    def __init__(self):
        self.m_cConfig = SystemConfigApi()
    def getDBInfo(self):
        return self.m_cConfig.getDBDriver(), self.m_cConfig.getDBServer(), self.m_cConfig.getDBName(), self.m_cConfig.getDBUid(), self.m_cConfig.getDBPwd(), self.m_cConfig.getDBMemcacheEnable(), self.m_cConfig.getDBMemcacheServer()
