#!/usr/bin/env python3
"""Gate G3: a free polygon ({'poly': [[lat, lon], ...]}) must sit on land in the satellite mosaic the video uses.
Measures the share of the polygon's pixels that look like land (same water test as the page). Hand-typed shapes that
spill into the sea fail. Usage: poly_land.py <id>...   exit 1 on error."""
import json, os, sys
import numpy as np
import cv2

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def polys_in(obj, found):
    if isinstance(obj, dict):
        if 'poly' in obj and isinstance(obj['poly'], list):
            found.append(obj['poly'])
        for v in obj.values():
            polys_in(v, found)
    elif isinstance(obj, list):
        for v in obj:
            polys_in(v, found)


def land_fraction(poly, details):
    lats = [p[0] for p in poly]; lons = [p[1] for p in poly]
    w, e, s, n = min(lons), max(lons), min(lats), max(lats)
    best = None
    for d in details:
        bw, bs, be, bn = d['bbox']
        if bw <= w and be >= e and bs <= s and bn >= n:
            area = (be - bw) * (bn - bs)
            if best is None or area < best[0]:
                best = (area, d)
    if not best:
        return None
    d = best[1]
    im = cv2.imread(os.path.join(ROOT, d['url'].lstrip('/')))
    if im is None:
        return None
    H, W = im.shape[:2]
    bw, bs, be, bn = d['bbox']
    px = lambda la, lo: (int((lo - bw) / (be - bw) * W), int((bn - la) / (bn - bs) * H))
    mask = np.zeros((H, W), np.uint8)
    cv2.fillPoly(mask, [np.array([px(la, lo) for la, lo in poly], np.int32)], 1)
    f = im.astype(int); b, g, r = f[..., 0], f[..., 1], f[..., 2]
    lum = r * 0.3 + g * 0.59 + b * 0.11
    water = (b > g * 0.92) & (b > r) & (lum < 120)
    black = lum < 8  # holes in the mosaic
    inside = mask.astype(bool)
    if inside.sum() == 0:
        return None
    return float((~water & ~black)[inside].mean()), int(inside.sum())


def check(vid):
    out = []
    sp = os.path.join(ROOT, 'videos', vid, 'script.json')
    if not os.path.exists(sp):
        sp = os.path.join(ROOT, 'tools/gates/golden', vid[2:] if vid.startswith('g_') else vid, 'script.json')
    script = json.load(open(sp))
    tlp = os.path.join(ROOT, 'output', vid)
    tls = sorted([f for f in os.listdir(tlp) if f.startswith('timeline.') and f.endswith('.json')], key=lambda f: -os.path.getmtime(os.path.join(tlp, f)))
    details = json.load(open(os.path.join(tlp, tls[0])))['assets'].get('detail', []) if tls else []
    found = []
    polys_in(script, found)
    seen = set()
    for p in found:
        k = json.dumps(p)
        if k in seen:
            continue
        seen.add(k)
        r = land_fraction(p, details)
        if r is None:
            out.append(('warn', f'polygon near ({p[0][0]:.3f},{p[0][1]:.3f}) is not covered by a satellite box: cannot verify it sits on land'))
        elif r[0] < 0.85:
            out.append(('error', f'polygon near ({p[0][0]:.3f},{p[0][1]:.3f}) is only {r[0] * 100:.0f}% land (need >=85%): it spills into the sea'))
    return out


if __name__ == '__main__':
    bad = 0
    for vid in sys.argv[1:]:
        res = check(vid)
        errs = [m for s, m in res if s == 'error']
        bad += len(errs)
        print(f'\n== {vid}: {len(errs)} error(s), {len(res) - len(errs)} warning(s)')
        for s, m in res:
            print(f"  {'ERROR' if s == 'error' else 'warn '} [poly-land] {m}")
    sys.exit(1 if bad else 0)
