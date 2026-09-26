"""Warn about close-up cameras (zoom >= 12) whose viewport isn't covered by a Sentinel-2 detail bbox.

Blue Marble (8k) gets visibly blurry past ~zoom 10, and a detail bbox smaller than the viewport
shows as a sharp rectangle. Usage: python3 tools/authoring/check_zoom.py [video ids...]
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R = 0.42  # config.layout.globeRadius
ASPECT = 1920 / 1080


def viewport(lat, lon, zoom, margin=1.15):
    half_lon = math.degrees(1 / (zoom * R)) / 2 * margin
    half_lat = half_lon * ASPECT * math.cos(math.radians(lat))
    return lon - half_lon, lat - half_lat, lon + half_lon, lat + half_lat


def covered(vp, boxes):
    return any(b[0] <= vp[0] and b[1] <= vp[1] and b[2] >= vp[2] and b[3] >= vp[3] for b in boxes)


def main(ids):
    vids = ids or sorted(os.listdir(os.path.join(ROOT, 'videos')))
    bad = 0
    for v in vids:
        p = os.path.join(ROOT, 'videos', v, 'script.json')
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        boxes = [i['bbox'] for i in d.get('imagery', [])]
        for i, s in enumerate(d['scenes']):
            c = s.get('camera') or {}
            if 'zoom' not in c or 'lat' not in c or c.get('follow'):
                continue
            if c['zoom'] < 12:
                continue
            vp = viewport(c['lat'], c['lon'], c['zoom'])
            if not covered(vp, boxes):
                bad += 1
                print(f'{v} sahne {i + 1}: zoom {c["zoom"]} görüş alanı {[round(x, 2) for x in vp]} kapsanmıyor')
    print('OK' if not bad else f'{bad} sorun')


if __name__ == '__main__':
    main(sys.argv[1:])
