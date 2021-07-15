from launcher.rllog import RLLog
from lib.web import RequestApi

class RLWeb(RLLog):
    m_cRequestApi = None
    m_cToken = None
    def __init__(self):
        super(RLWeb, self).__init__()
        self.m_cRequestApi = RequestApi()
    def parseToken(self):
        token = self.m_cRequestApi.getToken()
        if token == None:
            self.error("<!> Cannot get token")
            return None
        token = self.m_cRequestApi.parseToken(token)
        if token == None:
            self.error("<!> Token parse error")
            return None
        else:
            self.m_cToken = token
            return token
    def getToken(self):
        return self.m_cToken
    def isGet(self):
        return self.m_cRequestApi.isGet()
    def isDelete(self):
        return self.m_cRequestApi.isDelete()
    def isPost(self):
        return self.m_cRequestApi.isPost()
    def isPut(self):
        return self.m_cRequestApi.isPut()
    def parseGet(self):
        return self.m_cRequestApi.parseGet()
    def parseDelete(self):
        return self.m_cRequestApi.parseDelete()
    def parsePost(self):
        return self.m_cRequestApi.parsePost()
    def parsePut(self):
        return self.m_cRequestApi.parsePut()
