#!/usr/bin/env python3
"""Rim check: nothing may be drawn outside the plate disc.

Samples a column far from the disc (x=12) to learn the backdrop colour at each
row, then flags any pixel outside r=430 that differs from that row's backdrop.
Usage: python3 check_rim.py out/<slug>@2x.png ...
"""
import sys
import numpy as np
from PIL import Image

R_OUT = 430          # pixels are checked beyond this radius (canvas units)
TOL = 10             # per-channel tolerance


def check(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    scale = w / 1000.0
    a = np.asarray(im).astype(int)
    # backdrop reference per row, from a column that is never part of the art
    ref = a[:, 4, :]
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = 500 * scale, 460 * scale
    # the name block sits below the disc on purpose, so stop the check above it
    outside = (np.hypot(xx - cx, yy - cy) > R_OUT * scale) & (yy < 890 * scale)
    diff = np.abs(a - ref[:, None, :]).max(axis=2)
    bad = outside & (diff > TOL)
    n = int(bad.sum())
    if n:
        ys, xs = np.nonzero(bad)
        print(f"{path}: {n} px outside the disc, e.g. "
              f"({xs[0] / scale:.0f},{ys[0] / scale:.0f})")
    else:
        print(f"{path}: clean")
    return n


if __name__ == "__main__":
    total = sum(check(p) for p in sys.argv[1:])
    sys.exit(1 if total else 0)
