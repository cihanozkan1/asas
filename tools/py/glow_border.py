#!/usr/bin/env python3
"""GeoPandas + Matplotlib glowing country border -> transparent PNG sequence -> assets/vfx clip.

  python3 tools/py/glow_border.py "Turkey" fx_py_glow_turkey [--color "#ffd60a"] [--frames 36]

Glow = stacked patheffects.withStroke layers (wide + faint -> thin + strong), pulsing over time; an extra Gaussian bloom
(blurred copy added with 'screen') makes it read like a real halo. Same idea as the MapLibre layer stack in remotion/.
"""
import sys, os, subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from PIL import Image, ImageFilter, ImageChops
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import countries, OUT, ROOT

name, clip = sys.argv[1], sys.argv[2]
color = sys.argv[sys.argv.index('--color') + 1] if '--color' in sys.argv else '#ffd60a'
n = int(sys.argv[sys.argv.index('--frames') + 1]) if '--frames' in sys.argv else 36
g = countries()
row = g[g['NAME'].str.lower() == name.lower()]
if row.empty:
    raise SystemExit('country not found: ' + name)
d = os.path.join(OUT, clip)
os.makedirs(d, exist_ok=True)
for i in range(n):
    pulse = 1 + 0.25 * np.sin(2 * np.pi * i / n)
    fig = plt.figure(figsize=(5.4, 9.6), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis('off'); fig.patch.set_alpha(0); ax.patch.set_alpha(0)
    effects = [pe.withStroke(linewidth=lw * pulse, foreground=color, alpha=a) for lw, a in ((34, 0.10), (22, 0.16), (12, 0.30), (6, 0.55))]
    row.plot(ax=ax, facecolor=color, alpha=1.0, edgecolor='white', linewidth=1.6, path_effects=effects)
    for coll in ax.collections:
        coll.set_facecolor(matplotlib.colors.to_rgba(color, 0.22))
    ax.set_aspect('equal')
    b = row.total_bounds; pad = max(b[2] - b[0], b[3] - b[1]) * 0.35
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2; half = max(b[2] - b[0], (b[3] - b[1]) * 9 / 16) / 2 + pad
    ax.set_xlim(cx - half, cx + half); ax.set_ylim(cy - half * 16 / 9, cy + half * 16 / 9)
    f = os.path.join(d, f'f{i:04d}.png')
    fig.savefig(f, transparent=True); plt.close(fig)
    im = Image.open(f).convert('RGBA')
    bloom = im.filter(ImageFilter.GaussianBlur(14))
    rgb = ImageChops.screen(im.convert('RGB'), bloom.convert('RGB'))
    a = ImageChops.lighter(im.getchannel('A'), bloom.getchannel('A'))
    rgb.putalpha(a); rgb.save(f)
subprocess.run([sys.executable, os.path.join(ROOT, 'tools/vfx_ingest.py'), d, clip, '--key', 'alpha', '--width', '540', '--fps', '24', '--dur', '10', '--source', 'tools/py/glow_border.py'], check=True)
