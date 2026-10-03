#!/usr/bin/env python3
"""Gate: pure-black map blotches (no-data holes, unmasked lakes, bathymetry smears) in the rendered video.
Samples 2 frames/s, ignores deliberately dark scenes, reports connected near-black areas larger than 0.35 % of the frame.
Usage: blotch.py <video.mp4> <timeline.json>  -> prints JSON list of {t, area_pct}"""
import json, os, subprocess, sys
import numpy as np
import cv2

mp4, tlp = sys.argv[1], sys.argv[2]
tl = json.load(open(tlp))
ff = os.environ.get('FFMPEG_PATH', 'ffmpeg')
W, H = 270, 480
raw = subprocess.run([ff, '-v', 'error', '-i', mp4, '-vf', f'fps=2,scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
n = len(raw) // (W * H * 3)
frames = np.frombuffer(raw[:n * W * H * 3], np.uint8).reshape(n, H, W, 3)
DARK = ('dark', 'neon', 'night', 'noir')
out = []
for i, fr in enumerate(frames):
    t = i / 2 + 0.25
    sc = next((s for s in tl['scenes'] if s['start'] <= t < s['end']), None)
    if sc and (any(k in (sc.get('style') or '') for k in DARK) or tl.get('preset', {}).get('projection') == 'globe' or sc.get('transition') in ('film',) and t - sc['start'] < 0.7):
        continue
    f = fr.astype(int)
    lum = f @ np.array([0.3, 0.59, 0.11])
    # near-black holes (no-data pixels, unmasked lakes); deep-sea navy is real bathymetry and is left alone
    mask = (lum < 14).astype(np.uint8)
    mask[int(H * 0.60):int(H * 0.80)] = 0  # caption band (outlined text)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    nlab, lab, st, _ = cv2.connectedComponentsWithStats(mask)
    for k in range(1, nlab):
        a = st[k, cv2.CC_STAT_AREA] / (W * H) * 100
        if a > 0.35:
            # a real hole is black inside a lit map; a vignette corner or a graded (danger) scene darkens gradually
            comp = (lab == k).astype(np.uint8)
            ring = cv2.dilate(comp, np.ones((13, 13), np.uint8)) - comp
            ring_lum = lum[ring > 0].mean() if (ring > 0).any() else 0
            if ring_lum < 58:
                continue
            out.append({'t': round(t, 1), 'area_pct': round(a, 2), 'x': int(st[k, 0]), 'y': int(st[k, 1])})
print(json.dumps(out))
