#!/usr/bin/env python3
"""Add a public-domain / CC0 Wikimedia Commons clip to the VFX library (assets/vfx/<name>/).

  python3 tools/vfx_fetch.py "File:Poas Volcano Eruption 2025 04 21.webm" poas_eruption [--start 0] [--dur 6] [--fps 24] [--width 540]

What it does: re-reads the licence from Commons (refuses anything that is not PD / CC0), downloads, trims,
extracts a JPEG frame sequence (assets/vfx/<name>/f0001.jpg ...) for the renderer's `clip` element, and records
source URL, author, licence and date in assets/vfx/MANIFEST.json and docs/LISANSLAR.md (zero-risk log).
Find candidates with tools/commons_search.py.
"""
import sys, os, json, re, subprocess, urllib.request, datetime, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commons_search import api, OK

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = os.environ.get('FFMPEG_PATH', 'ffmpeg')


def arg(name, default):
    return type(default)(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


title, name = sys.argv[1], sys.argv[2]
start, dur, fps, width = arg('--start', 0.0), arg('--dur', 6.0), arg('--fps', 24), arg('--width', 540)
info = api(action='query', titles=title, prop='imageinfo', iiprop='url|extmetadata|size')
pg = next(iter(info['query']['pages'].values()))
ii = pg['imageinfo'][0]
md = ii['extmetadata']
lic = (md.get('LicenseShortName') or {}).get('value', '')
if not OK.search(lic):
    raise SystemExit(f'licence "{lic}" is not PD/CC0: refused')
author = re.sub('<[^>]+>', '', (md.get('Artist') or {}).get('value', '')).strip()
out = os.path.join(ROOT, 'assets/vfx', name)
os.makedirs(out, exist_ok=True)
src = os.path.join(out, 'source' + os.path.splitext(urllib.parse.urlparse(ii['url']).path)[1])
req = urllib.request.Request(ii['url'], headers={'User-Agent': 'geo-shorts/1.0 (https://github.com/cihanozkan1/asas)'})
import time
for k in range(8):                                  # Wikimedia throttles shared IPs: wait and retry
    try:
        open(src, 'wb').write(urllib.request.urlopen(req, timeout=300).read()); break
    except urllib.error.HTTPError as e:
        if e.code != 429 or k == 7: raise
        time.sleep(15 * (k + 1))
for f in os.listdir(out):
    if f.startswith('f') and f.endswith('.jpg'):
        os.remove(os.path.join(out, f))
from vfx_ingest import ingest, log_license
m = ingest(src, name, 'none', start, dur, fps, width, lic, 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(title.replace(' ', '_')), f'author: {author}')
os.remove(src)                                   # keep only the frames (the source can be hundreds of MB)
log_license(name, f'Wikimedia Commons: {title} ({author or "?"})', lic, m['source'])
print(f"{name}: {m['frames']} frames, licence {lic}")
raise SystemExit(0)
