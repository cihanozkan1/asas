#!/usr/bin/env python3
"""Datashader density map (millions of points: migration, cities, events) -> PNG with alpha, and a Plotly choropleth frame.

  python3 tools/py/density.py out.png [--n 2000000]      (demo: synthetic points around given hubs)
For real data pass your own lon/lat arrays to `density()`; colour ramp is fire-like on transparent background.
"""
import sys, numpy as np, pandas as pd
import datashader as ds, datashader.transfer_functions as tf
from colorcet import fire

def density(lon, lat, w=1080, h=1920, extent=((-30, 60), (20, 70))):
    df = pd.DataFrame({'x': lon, 'y': lat})
    cvs = ds.Canvas(plot_width=w, plot_height=h, x_range=extent[0], y_range=extent[1])
    img = tf.shade(cvs.points(df, 'x', 'y'), cmap=fire, how='eq_hist')
    return tf.set_background(img, None) if False else img

if __name__ == '__main__':
    out = sys.argv[1]; n = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 500000
    rng = np.random.default_rng(1)
    hubs = np.array([[29, 41], [12.5, 41.9], [2.3, 48.8], [-0.1, 51.5], [13.4, 52.5]])
    k = rng.integers(0, len(hubs), n)
    pts = hubs[k] + rng.normal(0, 1.6, (n, 2))
    density(pts[:, 0], pts[:, 1]).to_pil().save(out)
    print('wrote', out)
