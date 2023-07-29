import warnings as warn
warn.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd

try:
    from tweetkeywordmapper.core.map_services import TweetKeywordGeoPandas
    from tweetkeywordmapper.core import constants as cons
except:
    from core.map_services import TweetKeywordGeoPandas
    from core import constants as cons

ws = cons.workspace
    
TweetKeywordGeoPandas(ws, {}, '', function='map_field')