import os, json, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(ROOT, 'data/cache')
OUT = os.path.join(ROOT, 'tools/py/out')
NE_COUNTRIES = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson'


def countries():
    """Natural Earth 1:50m countries (public domain) as a GeoDataFrame; downloaded once to data/cache."""
    import geopandas as gpd
    p = os.path.join(CACHE, 'ne_50m_admin_0_countries.geojson')
    if not os.path.exists(p):
        os.makedirs(CACHE, exist_ok=True)
        urllib.request.urlretrieve(NE_COUNTRIES, p)
    return gpd.read_file(p)
