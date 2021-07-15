#====================
# web.py
#====================

import os
import sys
import json
import cgi
import re
import subprocess
import config.defines as const

class RequestApi():
    #--------------------
    # private
    #--------------------
    m_init = False
    m_request_method = None
    m_request_url = None
    def __init(self):
        self.m_request_method = os.environ['REQUEST_METHOD']
        self.m_request_url = os.environ['HTTP_X_ORIGINAL_URL']
        self.m_init = True
    #--------------------
    # public
    #--------------------
    def getRequestApi(self):
        if not self.m_init:
            self.__init()
        api = re.search(r'/api/[a-zA-Z0-9\/\-]+', self.m_request_url)
        api = api.group()
        api = api.replace('/api/', '')
        return api
    def getToken(self):
        if const.ENV_TOKEN_KEY in os.environ:
            return os.environ[const.ENV_TOKEN_KEY]
        if const.ENV_TOKEN_KEY_IIS in os.environ:
            return os.environ[const.ENV_TOKEN_KEY_IIS]
        return None
    def parseToken(self, in_token):
        cwd = os.getcwd()
        os.chdir("../../system/cmd")
        handle = subprocess.run(["./adcrypt.exe", "-decode", "-in", in_token], stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin=subprocess.DEVNULL)
        os.chdir(cwd)
        val = handle.stdout.decode("utf8")
        val = val.replace('\n','')
        if '[ERROR]' in val:
            return None
        else:
            val = json.loads(val)
            return val
    def isGet(self):
        if not self.m_init:
            self.__init()
        if self.m_request_method == "GET":
            return True
        else:
            return False
    def isDelete(self):
        if not self.m_init:
            self.__init()
        if self.m_request_method == "DELETE":
            return True
        else:
            return False
    def isPost(self):
        if not self.m_init:
            self.__init()
        if self.m_request_method == "POST":
            return True
        else:
            return False
    def isPut(self):
        if not self.m_init:
            self.__init()
        if self.m_request_method == "PUT":
            return True
        else:
            return False
    def parseGet(self):
        if not self.m_init:
            self.__init()
        if self.m_request_method == "GET":
            return cgi.FieldStorage()
        else:
            return None
    def parseDelete(self):
        if not self.m_init:
            self.__init()
        if self.m_request_method == "DELETE":
            return cgi.FieldStorage()
        else:
            return None
    def parsePost(self):
        if not self.m_init:
            self.__init()
        if self.m_request_method == "POST":
            content_length = int(os.environ["CONTENT_LENGTH"])
            request_body = sys.stdin.read(content_length)
            request_dict = json.loads(request_body)
            return request_dict
        else:
            return None
    def parsePut(self):
        if not self.m_init:
            self.__init()
        if self.m_request_method == "PUT":
            content_length = int(os.environ["CONTENT_LENGTH"])
            request_body = sys.stdin.read(content_length)
            request_dict = json.loads(request_body)
            return request_dict
        else:
            return None
