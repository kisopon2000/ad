import ext
from lib.web import RequestApi

print('Content-Type:application/json\n')

request = RequestApi()
launcher = ext.g_REQUEST[request.getRequestApi()]();
if launcher.atstart() == 0:
    if launcher.initialize() == 0:
        launcher.run()
        launcher.finalize()
        launcher.atend()
