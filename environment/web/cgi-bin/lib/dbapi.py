#--------------------
# dbapi.py
#--------------------

import pyodbc
import memcache
from lib.utility import LogApi

class DBApi():
    m_cLogApi = None
    m_connection = None
    m_cursor = None
    m_memcache = None
    def connect(self, in_driver, in_server, in_dbname, in_uid, in_pwd, in_memcache=False, in_memcacheServer=False):
        if self.m_cLogApi == None:
            self.m_cLogApi = LogApi()
        dburl = 'DRIVER=' + in_driver + ';SERVER=' + in_server + ';DATABASE=' + in_dbname + ';UID=' + in_uid + ';PWD=' + in_pwd
        self.m_connection = pyodbc.connect(dburl)
        self.m_cursor = self.m_connection.cursor()
        if in_memcache:
            self.m_memcache = memcache.Client([in_memcacheServer], cache_cas=True)
    def close(self):
        self.m_cursor.close()
        self.m_connection.close()
    def getMemcachedData(self, in_key):
        return self.m_memcache.get(in_key)
    def log(self, in_message):
        self.m_cLogApi.log(in_message)
    def warning(self, in_message):
        self.m_cLogApi.warning(in_message)
    def debug(self, in_message):
        self.m_cLogApi.debug(in_message)
    def error(self, in_message):
        self.m_cLogApi.error(in_message)
