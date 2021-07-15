#====================
# utility.py
#====================

import os
import datetime
import xml.etree.ElementTree as xmlparser
import config.defines as const
from distutils.util import strtobool

class SystemConfigApi():
    #--------------------
    # private
    #--------------------
    m_init = False
    m_configpath = os.path.dirname(__file__) + '\..\config\config.xml'
    m_xmlroot = None
    def __init(self):
        self.xmlroot = xmlparser.parse(self.m_configpath)
        self.m_xmlroot = self.xmlroot.getroot()
        self.m_init = True
    #--------------------
    # public
    #--------------------
    def getLogMaxFileCycle(self):
        if not self.m_init:
            self.__init()
        return self.m_xmlroot.find('log/maxfilecycle').text
    def getLogMaxFileSize(self):
        if not self.m_init:
            self.__init()
        return self.m_xmlroot.find('log/maxfilesize').text
    def getLogLevel(self):
        if not self.m_init:
            self.__init()
        return self.m_xmlroot.find('log/level').text
    def getDBDriver(self):
        if not self.m_init:
            self.__init()
        return self.m_xmlroot.find('db/driver').text
    def getDBServer(self):
        if not self.m_init:
            self.__init()
        return self.m_xmlroot.find('db/server').text
    def getDBName(self):
        if not self.m_init:
            self.__init()
        return self.m_xmlroot.find('db/dbname').text
    def getDBUid(self):
        if not self.m_init:
            self.__init()
        return self.m_xmlroot.find('db/uid').text
    def getDBMemcacheEnable(self):
        if not self.m_init:
            self.__init()
        return strtobool(self.m_xmlroot.find('db/memcache/enable').text)
    def getDBMemcacheServer(self):
        if not self.m_init:
            self.__init()
        return self.m_xmlroot.find('db/memcache/server').text
    def getDBPwd(self):
        if not self.m_init:
            self.__init()
        return self.m_xmlroot.find('db/pwd').text
    def getAnalysisType(self):
        if not self.m_init:
            self.__init()
        return self.m_xmlroot.find('analysis/type').text
    def getAnalysisModel(self):
        if not self.m_init:
            self.__init()
        return self.m_xmlroot.find('analysis/model').text
    def save(self):
        self.xmlroot.write(self.m_configpath)
        self.m_init = False

class LogApi():
    #--------------------
    # private
    #--------------------
    m_init = False
    m_outputpath = ''
    m_maxfilecycle = 0
    m_maxfilesize = 0
    m_level = 0
    def __init(self):
        outputdir = os.path.dirname(__file__) + '\..\log'
        outputpath = os.path.dirname(__file__) + '\..\log\log.000'
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)
        self.m_outputpath = outputpath
        config = SystemConfigApi()
        self.m_maxfilecycle = int(config.getLogMaxFileCycle())
        self.m_maxfilesize = int(config.getLogMaxFileSize())
        level = config.getLogLevel()
        if level == 'ERR':
            self.m_level = const.LOG_LEVEL_ERR
        elif level == 'WAR':
            self.m_level = const.LOG_LEVEL_WAR
        elif level == 'INF':
            self.m_level = const.LOG_LEVEL_INF
        elif level == 'DBG':
            self.m_level = const.LOG_LEVEL_DBG
        else:
            self.m_level = const.LOG_LEVEL_OTH
        self.m_init = True
    def __renameRecurse(self, in_cycle):
        if in_cycle == 0:
            return 0
        else:
            cycle = in_cycle - 1
            if in_cycle == self.m_maxfilecycle:
                outputpath = os.path.dirname(__file__) + '\..\log\log.' + format(cycle, '03d')
                if os.path.exists(outputpath):
                    # 最大世代は単純削除
                    os.remove(outputpath)
            else:
                oldpath = os.path.dirname(__file__) + '\..\log\log.' + format(cycle, '03d')
                newpath = os.path.dirname(__file__) + '\..\log\log.' + format(in_cycle, '03d')
                if os.path.exists(oldpath):
                    # 中間世代はリネーム
                    os.rename(oldpath, newpath)
            self.__renameRecurse(cycle)
    def __log(self, in_type, in_level, in_message):
        if in_level < self.m_level:
            return
        if os.path.exists(self.m_outputpath):
            if os.path.getsize(self.m_outputpath) > self.m_maxfilesize:
                self.__renameRecurse(self.m_maxfilecycle)
        date = '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] '
        message = date + '<' + in_type + '> ' + in_message
        file = open(self.m_outputpath, 'a')
        file.write(message + '\n')
        file.close()
    #--------------------
    # public
    #--------------------
    def log(self, in_message):
        if not self.m_init:
            self.__init()
        self.__log('INF', const.LOG_LEVEL_INF, in_message)
    def warning(self, in_message):
        if not self.m_init:
            self.__init()
        self.__log('WAR', const.LOG_LEVEL_WAR, in_message)
    def debug(self, in_message):
        if not self.m_init:
            self.__init()
        self.__log('DBG', const.LOG_LEVEL_DBG, in_message)
    def error(self, in_message):
        if not self.m_init:
            self.__init()
        self.__log('ERR', const.LOG_LEVEL_ERR, in_message)
