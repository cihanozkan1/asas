#!/usr/bin/env python3
"""Cloud-free true-colour mosaic for a bounding box from Copernicus Sentinel-2 L2A (open data on AWS).

Licence: Copernicus Sentinel data are free, full and open, commercial use included; the only condition is the
credit "Contains modified Copernicus Sentinel data <year>" (added to every video description by src/meta.mjs).

  python3 tools/s2_fetch.py W S E N WIDTH out.jpg [--max-scenes 6]

Method: STAC search (Element84 earth-search, no key) -> lowest-cloud scenes of the last three years, per tile ->
read the 10 m "visual" (TCI) COG windows straight into the target grid (GDAL picks overviews when the box is
large, so a 7 degree box costs almost as little as a 1 degree box) -> mask cloud / shadow / snow-free-cloud with
the SCL band -> per-pixel median. Prints the years used as JSON on the last line.
"""
import sys, json, datetime as dt
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_bounds
from pystac_client import Client
from PIL import Image

W_, S_, E_, N_ = map(float, sys.argv[1:5])
width = int(sys.argv[5])
out = sys.argv[6]
max_scenes = int(sys.argv[sys.argv.index('--max-scenes') + 1]) if '--max-scenes' in sys.argv else 6

height = max(64, min(4096, round(width * (N_ - S_) / (E_ - W_))))
dst_tf = from_bounds(W_, S_, E_, N_, width, height)

cat = Client.open('https://earth-search.aws.element84.com/v1')
today = dt.date.today()
search = cat.search(collections=['sentinel-2-l2a'], bbox=[W_, S_, E_, N_],
                    datetime=f'{today.year - 3}-01-01/{today.isoformat()}',
                    query={'eo:cloud_cover': {'lt': 25}}, max_items=400)
items = list(search.items())
if not items:
    sys.exit('no Sentinel-2 scenes found for this box')

# Pick scenes by real footprint coverage of the box (a scene's geometry is its DATA footprint, so partial swaths
# are seen for what they are): greedily, lowest cloud first, until every part of the box is covered 3 times.
from rasterio.features import rasterize
G = 96
gtf = from_bounds(W_, S_, E_, N_, G, G)
def footprint(it):
    try:
        return rasterize([(it.geometry, 1)], out_shape=(G, G), transform=gtf, all_touched=True).astype(bool)
    except Exception:
        return np.zeros((G, G), bool)
cands = sorted(items, key=lambda i: i.properties.get('eo:cloud_cover', 100) + 0.3 * i.properties.get('s2:nodata_pixel_percentage', 0))
cover = np.zeros((G, G), int)
chosen = []
for it in cands:
    fp = footprint(it)
    if not fp.any():
        continue
    need = (cover < 3) & fp
    if need.sum() < 0.03 * G * G and chosen:
        continue
    chosen.append(it)
    cover += fp
    if len(chosen) >= max_scenes * 3 or (cover >= 3).all():
        break

env = dict(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR', AWS_NO_SIGN_REQUEST='YES', GDAL_HTTP_MULTIRANGE='YES',
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS='.tif', GDAL_HTTP_MAX_RETRY='4', GDAL_HTTP_RETRY_DELAY='2')
stack, valid, years = [], [], set()
with rasterio.Env(**env):
    for it in chosen:
        try:
            rgb = np.zeros((3, height, width), np.uint8)
            with rasterio.open(it.assets['visual'].href) as src:
                for b in range(3):
                    reproject(rasterio.band(src, b + 1), rgb[b], dst_transform=dst_tf, dst_crs='EPSG:4326',
                              resampling=Resampling.average)
            scl = np.zeros((height, width), np.uint8)
            with rasterio.open(it.assets['scl'].href) as src:
                reproject(rasterio.band(src, 1), scl, dst_transform=dst_tf, dst_crs='EPSG:4326', resampling=Resampling.nearest)
        except Exception as e:  # a broken scene must not sink the whole mosaic
            print('skip', it.id, e, file=sys.stderr)
            continue
        ok = (rgb.sum(axis=0) > 0) & ~np.isin(scl, [0, 1, 3, 8, 9, 10])   # no data, defective, shadow, cloud
        if ok.mean() < 0.02:
            continue
        stack.append(rgb)
        valid.append(ok)
        years.add(int(it.datetime.year))
if not stack:
    sys.exit('no usable pixels')

A = np.stack(stack).astype(np.float32)              # n,3,H,W
M = np.stack(valid)                                 # n,H,W
A[~np.broadcast_to(M[:, None], A.shape)] = np.nan
with np.errstate(all='ignore'):
    med = np.nanmedian(A, axis=0)                   # 3,H,W
hole = np.isnan(med[0])
if hole.any():                                      # only clouds there: use any scene that has data at all
    for rgb in stack:
        fill = hole & (rgb.sum(axis=0) > 0)
        med[:, fill] = rgb[:, fill]
        hole &= ~fill
img = np.clip(med, 0, 255)
# TCI is a little flat for a screen: gentle contrast lift, colour kept
img = np.clip((img / 255.0) ** 0.92 * 255.0 * 1.04, 0, 255).astype(np.uint8)
Image.fromarray(np.moveaxis(img, 0, -1)).save(out, quality=90)
print(json.dumps({'scenes': len(stack), 'years': sorted(years), 'size': [width, height]}))
