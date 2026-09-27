#!/usr/bin/env python3
"""Cut the display base/pedestal off a character cut-out: a wide flat blob under the feet.

  python3 tools/strip_pedestal.py assets/characters/<id>.png [...] [--dry]
"""
import sys
import numpy as np
from PIL import Image


def pedestal_row(img):
    a = np.array(img.split()[-1]) > 40
    h = a.shape[0]
    spans = []
    for y in range(h):
        xs = np.flatnonzero(a[y])
        spans.append((xs[-1] - xs[0] + 1) if xs.size else 0)
    spans = np.array(spans)
    legs = np.median(spans[int(h * 0.62):int(h * 0.78)])
    if legs <= 0:
        return None
    # from the bottom up: rows much wider than the legs belong to the base
    y = h - 1
    while y > h * 0.8 and (spans[y] == 0 or spans[y] > legs * 1.3):
        y -= 1
    base = h - 1 - y
    if h * 0.025 <= base <= h * 0.2:
        return y + 1
    # fallback: a flat disc as wide as the figure; walk up until the rows get clearly narrower
    yb = h - 1
    while yb > 0 and spans[yb] == 0:
        yb -= 1
    lo = int(h * 0.82)
    y = lo + int(np.argmax(spans[lo:]))
    bottom = spans[y]
    while y > h * 0.75 and spans[y] >= bottom * 0.72:
        y -= 1
    base = yb - y
    if h * 0.03 <= base <= h * 0.2 and spans[max(0, y - 12)] < bottom * 0.62:
        return y + 1
    return None


def main(paths, dry):
    for p in paths:
        img = Image.open(p).convert('RGBA')
        cut = pedestal_row(img)
        print(p, 'base at', cut, 'of', img.height)
        if cut and not dry:
            img.crop((0, 0, img.width, cut)).crop(img.crop((0, 0, img.width, cut)).getbbox()).save(p, optimize=True)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--dry']
    main(args, '--dry' in sys.argv)
