#!/usr/bin/env python3
"""Shared cursor shapes for #1249 — the VirelaiOS cursor set.

Register: chrome level. Every cursor is a closed, chunky silhouette that
must survive reduction to a 2-color mask at 16x24 — white fill, warm-INK
outline (~3 px at the 32x48 master = 1.5 px at ship size, closing every
shape), rounded joins. Interior detail is allowed only where it survives
as dark fill. No pure black, no gradients (the mask path drops them).

Layout: one shape function per cursor, `SHAPES` maps slug-suffix -> fn(d).
Each driver does:

    d = Draw()
    new_doc(d, "cursor-arrow-V1R00")
    SHAPES["arrow"](d)
    d.finish("cursor-arrow-V1R00")

HOTSPOTS are recorded in art/virelai/HOTSPOTS.md (master px + 16x24 px).
"""
import math

from vc import NONE
from virelai.vkit import INK

W, H = 32, 48            # master = 2x the shipping 16x24
WHITE = "#FFFFFF"
SAND = "#F59E0B"         # shipped Warning token — busy glass
SW = 3                   # outline weight at master

HOTSPOTS = {             # (master_x, master_y) — halve for the 16x24 table
    "arrow":       (2, 2),    # tip
    "ibeam":       (16, 24),  # bar midpoint
    "hand":        (12, 4),   # index fingertip
    "grab":        (16, 28),  # palm center
    "grabbing":    (16, 28),  # fist center
    "resize-x":    (16, 24),  # midpoint
    "resize-y":    (16, 24),  # midpoint
    "crosshair":   (16, 24),  # center gap
    "busy":        (16, 24),  # glass waist
    "not-allowed": (16, 24),  # ring center
}


def new_doc(d, slug):
    return d.call("run_command", {"command": "file.new", "params": {
        "name": slug, "width": W, "height": H, "units": "Pixels",
        "backgroundContents": "transparent", "colorMode": "rgb"}},
        "file.new")


def _rrect(x, y, w, h, r):
    """Rounded-rect path (draw_shape has no corner radius)."""
    r = min(r, w / 2, h / 2)
    return (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} "
            f"L{x+w},{y+h-r} Q{x+w},{y+h} {x+w-r},{y+h} "
            f"L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
            f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")


def _capsule(x0, y0, x1, y1, w):
    """Thick line as a closed rounded capsule path."""
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln * w / 2, dx / ln * w / 2
    return (f"M{x0+nx:.1f},{y0+ny:.1f} L{x1+nx:.1f},{y1+ny:.1f} "
            f"A{w/2},{w/2} 0 0 1 {x1-nx:.1f},{y1-ny:.1f} "
            f"L{x0-nx:.1f},{y0-ny:.1f} "
            f"A{w/2},{w/2} 0 0 1 {x0+nx:.1f},{y0+ny:.1f} Z")


def _part(d, path_d, label, fill=WHITE):
    d.path(path_d, label, fill=fill, stroke=INK, strokeWidth=SW, join="round")


# --- the set -------------------------------------------------------------------

def arrow(d):
    """Classic slanted pointer — refresh of the shipping 16x24 bitmap.
    Tip, long left edge, notch, tail leg, right-pointing base."""
    _part(d, "M2,2 L2,35 L11,27 L17,40.5 L22,38.5 L17,25 L27,25 Z", "arrow")


def ibeam(d):
    """Text caret — rounded slab-serif I, one closed path."""
    _part(d, "M8,6.5 L24,6.5 Q26.5,6.5 26.5,9 L26.5,10.5 "
             "Q26.5,13 24,13 L19.5,13 L19.5,35 L24,35 "
             "Q26.5,35 26.5,37.5 L26.5,39 Q26.5,41.5 24,41.5 "
             "L8,41.5 Q5.5,41.5 5.5,39 L5.5,37.5 "
             "Q5.5,35 8,35 L12.5,35 L12.5,13 L8,13 "
             "Q5.5,13 5.5,10.5 L5.5,9 Q5.5,6.5 8,6.5 Z", "ibeam")


def hand(d):
    """Link hand — white-glove pointer, index extended. Built from
    overlapping primitives; seams survive the mask as finger creases."""
    _part(d, _rrect(8, 16, 18, 22, 7), "fist")            # palm/knuckle block
    _part(d, _capsule(12, 4, 12, 24, 6.5), "index")       # extended index
    _part(d, _capsule(19.5, 10, 19.5, 24, 5), "middle")   # curled finger bumps
    _part(d, _capsule(24.5, 13, 24.5, 25, 4.5), "ring")
    _part(d, _capsule(6, 30, 11, 22, 5), "thumb")         # thumb, angled out


def grab(d):
    """Open hand — drag-ready. Four finger capsules + thumb + palm."""
    for i, (x, top, w) in enumerate([(8, 8, 4.5), (13, 5, 4.7),
                                     (18, 6, 4.7), (23, 9, 4.3)]):
        _part(d, _capsule(x, top, x, 24, w), f"finger {i+1}")
    _part(d, _capsule(5.5, 32, 10.5, 24, 4.5), "thumb")
    d.shape("ellipse", "palm", x=6, y=18, width=21, height=22,
            fill=WHITE, stroke=INK, strokeWidth=SW)


def grabbing(d):
    """Closed fist — drag active. Rounded fist + knuckle bumps + thumb
    bar across the front."""
    for i, x in enumerate([9, 13.5, 18, 22.5]):
        d.shape("ellipse", f"knuckle {i+1}", x=x - 3.2, y=11,
                width=6.4, height=7.5, fill=WHITE,
                stroke=INK, strokeWidth=SW)
    _part(d, _rrect(7, 14, 19, 27, 7), "fist")
    _part(d, _capsule(8.5, 30.5, 19, 27.5, 5.5), "thumb")


def resize_x(d):
    """Horizontal double arrow — window edge drag."""
    _part(d, "M4,24 L12,14 L12,19 L20,19 L20,14 L28,24 "
             "L20,34 L20,29 L12,29 L12,34 Z", "resize-x")


def resize_y(d):
    """Vertical double arrow — window edge drag."""
    _part(d, "M16,6 L26,14 L21,14 L21,34 L26,34 L16,42 "
             "L6,34 L11,34 L11,14 L6,14 Z", "resize-y")


def crosshair(d):
    """Precision cross — four arms leaving an open center pixel."""
    _part(d, _rrect(14.2, 4, 3.6, 17, 1.8), "arm top")
    _part(d, _rrect(14.2, 27, 3.6, 17, 1.8), "arm bottom")
    _part(d, _rrect(4, 22.2, 17, 3.6, 1.8), "arm left")
    _part(d, _rrect(19, 22.2, 9, 3.6, 1.8), "arm right")


def busy(d):
    """Hourglass — static wait state. Caps + pinched glass; amber sand
    survives the mask as interior dark."""
    _part(d, _rrect(7, 4.5, 18, 4.5, 2.2), "cap top")
    _part(d, _rrect(7, 39, 18, 4.5, 2.2), "cap bottom")
    _part(d, "M10,9 L22,9 L22,13 Q22,18 18.5,21 L17.4,22.2 "
             "Q16.7,23 16.7,24 Q16.7,25 17.4,25.8 L18.5,27 "
             "Q22,30 22,35 L22,39 L10,39 L10,35 Q10,30 13.5,27 "
             "L14.6,25.8 Q15.3,25 15.3,24 Q15.3,23 14.6,22.2 "
             "L13.5,21 Q10,18 10,13 Z", "glass")
    d.path("M12.5,36.5 L19.5,36.5 L17,30.5 L15,30.5 Z", "sand",
           fill=SAND, stroke=NONE)
    d.shape("ellipse", "grain", x=15.2, y=25.5, width=1.6, height=2.6,
            fill=SAND, stroke=NONE)


def not_allowed(d):
    """Refused drop — ink donut + descending ink bar. The bar is solid
    ink (no white fill): white-stroked bands read as hatching at 16 px.
    Bar ends tuck into the ring so the silhouette merges."""
    d.shape("ellipse", "ring halo", x=5, y=13, width=22, height=22,
            fill=WHITE, stroke=NONE)
    d.shape("ellipse", "ring ink", x=5.8, y=13.8, width=20.4, height=20.4,
            fill=INK, stroke=NONE)
    d.shape("ellipse", "ring inner", x=9.3, y=17.3, width=13.4, height=13.4,
            fill=WHITE, stroke=NONE)
    t = math.radians(45)
    c, s = math.cos(t), math.sin(t)
    w, h = 21, 4.8
    pts = [(16 + dx * c - dy * s, 24 + dx * s + dy * c)
           for dx, dy in [(-w / 2, -h / 2), (w / 2, -h / 2),
                          (w / 2, h / 2), (-w / 2, h / 2)]]
    d.path("M{0[0]:.1f},{0[1]:.1f} L{1[0]:.1f},{1[1]:.1f} "
           "L{2[0]:.1f},{2[1]:.1f} L{3[0]:.1f},{3[1]:.1f} Z".format(*pts),
           "bar", fill=INK, stroke=NONE)


SHAPES = {
    "arrow": arrow, "ibeam": ibeam, "hand": hand, "grab": grab,
    "grabbing": grabbing, "resize-x": resize_x, "resize-y": resize_y,
    "crosshair": crosshair, "busy": busy, "not-allowed": not_allowed,
}
