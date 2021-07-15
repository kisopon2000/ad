#==========================================================================
# Add your file.
#==========================================================================
from func.heartbeat import HeartbeatLauncher
from func.ads import AdsLauncher
from func.ad_types import AdTypesLauncher
from func.ad_recommendations import AdRecommendationsLauncher
from func.ad_histories import AdHistoriesLauncher

#==========================================================================
# Register api and class. (YourClass is defined above file)
#   URL : /api/<YourApi>
#     -> g_REQUEST[<YourApi>] = YourClass
#==========================================================================
g_REQUEST = {}
g_REQUEST['heartbeat'] = HeartbeatLauncher
g_REQUEST['ads'] = AdsLauncher
g_REQUEST['ad-types'] = AdTypesLauncher
g_REQUEST['ad-recommendations'] = AdRecommendationsLauncher
g_REQUEST['ad-histories'] = AdHistoriesLauncher
