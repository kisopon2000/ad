from launcher.rlconfig import RLConfig
from lib.utility import LogApi

class RLLog(RLConfig):
    m_cLog = None
    def __init__(self):
        super(RLLog, self).__init__()
        self.m_cLog = LogApi()
    def log(self, in_message):
        self.m_cLog.log(in_message)
    def warning(self, in_message):
        self.m_cLog.warning(in_message)
    def debug(self, in_message):
        self.m_cLog.debug(in_message)
    def error(self, in_message):
        self.m_cLog.error(in_message)
