#!/usr/bin/env python3
"""Cartopy orthographic globe with a growing route (Shapely interpolate = Turf `along`) and camera following the tip -> transparent PNG
sequence -> assets/vfx clip.

  python3 tools/py/route_anim.py fx_py_route "41.0,28.9" "38.9,-77.0" "40.7,-74.0" [--frames 48]
"""
import sys, os, subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import cartopy.crs as ccrs
from shapely.geometry import LineString
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import OUT, ROOT

clip = sys.argv[1]
args = sys.argv[2:]
if '--frames' in args:
    i = args.index('--frames'); del args[i:i + 2]
pts = [tuple(float(v) for v in a.split(',')) for a in args]
n = int(sys.argv[sys.argv.index('--frames') + 1]) if '--frames' in sys.argv else 48
line = LineString([(lo, la) for la, lo in pts])                 # lon/lat; Shapely walks it in degrees (fine for a route sketch)
d = os.path.join(OUT, clip); os.makedirs(d, exist_ok=True)
for i in range(n):
    u = min(1.0, (i + 1) / (n - 4)); u = 3 * u * u - 2 * u ** 3
    tip = line.interpolate(u, normalized=True)
    sub = LineString([line.interpolate(t * u, normalized=True) for t in np.linspace(0, 1, 40)])
    fig = plt.figure(figsize=(5.4, 9.6), dpi=100); fig.patch.set_alpha(0)
    ax = fig.add_axes([0.02, 0.2, 0.96, 0.6], projection=ccrs.Orthographic(tip.x, tip.y)); ax.patch.set_alpha(0)
    ax.set_global(); ax.coastlines(linewidth=0.5, color='white', alpha=0.6)
    ax.plot(*sub.xy, transform=ccrs.Geodetic(), color='#ff3b3b', linewidth=5, solid_capstyle='round', path_effects=[pe.withStroke(linewidth=14, foreground='#ff3b3b', alpha=0.3)])
    ax.plot([tip.x], [tip.y], 'o', color='white', markersize=9, transform=ccrs.Geodetic())
    fig.savefig(os.path.join(d, f'f{i:04d}.png'), transparent=True); plt.close(fig)
subprocess.run([sys.executable, os.path.join(ROOT, 'tools/vfx_ingest.py'), d, clip, '--key', 'alpha', '--width', '540', '--fps', '24', '--dur', '10', '--source', 'tools/py/route_anim.py'], check=True)
