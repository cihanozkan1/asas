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
    if base < h * 0.025 or base > h * 0.2:
        return None
    return y + 1


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
