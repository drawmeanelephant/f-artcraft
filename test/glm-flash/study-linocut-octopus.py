#!/usr/bin/env python3
"""Style study 3/3 — LINOCUT octopus (carved-block grammar).

Solid ink mass + one spot-colour block, angular faceted curves, paper-colour
carve marks. Part of the GLM-Flash style exploration (test/glm-flash/README.md).
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work"))
from vc import Draw, REPO, OUT

PAPER = "#F4EFE4"     # warm block-print paper
INK = "#1A1714"       # carved ink
SPOT = "#C6402E"      # spot block
HERE = os.path.join(REPO, "test", "glm-flash")


def arm(p0, ang, R, sweep, w0, w1, flip=1, n=14):
    """Faceted taper arm — few samples on purpose: linocut curves are angular."""
    a0 = math.radians(ang)
    ux, uy = math.cos(a0), math.sin(a0)
    cx = p0[0] + (-uy * flip) * R
    cy = p0[1] + (ux * flip) * R
    phi0 = math.atan2(p0[1] - cy, p0[0] - cx)
    sw = math.radians(sweep)
    outer, inner = [], []
    for k in range(n + 1):
        phi = phi0 + sw * k / n
        t = k / n
        w = w0 + (w1 - w0) * (t ** 1.1)
        px, py = cx + R * math.cos(phi), cy + R * math.sin(phi)
        outer.append((px + math.cos(phi) * w / 2, py + math.sin(phi) * w / 2))
        inner.append((px - math.cos(phi) * w / 2, py - math.sin(phi) * w / 2))
    pts = outer + inner[::-1]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


d = Draw()
d.new_doc("study-linocut-octopus", 1000, 1000)

d.shape("rect", "Paper", x=0, y=0, width=1000, height=1000, fill=PAPER)
d.shape("ellipse", "Spot sun", x=200, y=100, width=600, height=600, fill=SPOT)

# frame, carved thick
d.shape("rect", "Frame", x=34, y=34, width=932, height=932, fill="none",
        stroke=INK, strokeWidth=10)

# octopus: solid black mass
P0 = (500, 470)
ARMS = [(42, 195, -170, 32), (70, 160, -185, 36), (100, 148, -200, 36), (128, 128, -210, 32)]
for ang, R, sweep, w in ARMS:
    d.path(arm(P0, ang, R, sweep, w, 5, flip=1), f"Arm R {ang}", fill=INK)
    d.path(arm(P0, 180 - ang, R, sweep, w, 5, flip=-1), f"Arm L {ang}", fill=INK)

# mantle: angular dome
d.path("M368 480 L376 340 C392 268 440 244 500 244 C560 244 608 268 624 340 L632 480 "
       "C556 514 444 514 368 480 Z", "Mantle", fill=INK)

# carve marks: paper-coloured dashes across the arms
dashes = [
    ("M420 560 L452 588", "M300 545 L330 570"), ("M580 560 L548 588", "M700 545 L670 570"),
    ("M415 640 L450 668", "M295 635 L328 660"), ("M585 640 L550 668", "M705 635 L672 660"),
    ("M440 300 L470 322", "M530 300 L560 322"),
]
for i, (lft, rgt) in enumerate(dashes):
    d.path(lft, f"Carve L {i}", fill="none", stroke=PAPER, strokeWidth=6, cap="round")
    d.path(rgt, f"Carve R {i}", fill="none", stroke=PAPER, strokeWidth=6, cap="round")

# eyes carved as paper circles with ink dots
for i, x in enumerate((446, 554)):
    d.shape("ellipse", f"Eye {i}", x=x - 30, y=318, width=60, height=60, fill=PAPER)
    d.shape("ellipse", f"Pupil {i}", x=x - 12, y=336, width=24, height=24, fill=INK)

d.cmd("select.none")
d.call("save_file", {"path": f"{HERE}/study-linocut-octopus-V1R00.vectorcraft"}, "save native")
for fmt, path, scale in [("svg", f"{HERE}/study-linocut-octopus-V1R00.svg", None),
                         ("png", f"{HERE}/study-linocut-octopus-V1R00@2x.png", 2),
                         ("pdf", f"{OUT}/study-linocut-octopus-V1R00.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    d.call("export", args, f"export {fmt}")
print("LINOCUT STUDY DONE, calls:", d.count, "errors:", len(d.errors))
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])
