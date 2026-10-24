#!/usr/bin/env python3
"""study-harper-octopus V1R01 — the top-left arm no longer arcs over the
dome (start angle tucked toward the base); everything else held.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work"))
from vc import Draw, REPO, OUT

PAPER = "#F2EBDD"
BODY = "#2E2E38"
SPOT = "#E0673F"
HERE = os.path.join(REPO, "test", "glm-flash")


def arm(p0, ang, R, sweep, w0, w1, flip=1, n=48):
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
        w = w0 + (w1 - w0) * (t ** 1.2)
        px, py = cx + R * math.cos(phi), cy + R * math.sin(phi)
        outer.append((px + math.cos(phi) * w / 2, py + math.sin(phi) * w / 2))
        inner.append((px - math.cos(phi) * w / 2, py - math.sin(phi) * w / 2))
    pts = outer + inner[::-1]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


d = Draw()
d.new_doc("study-harper-octopus-v1r01", 1000, 1000)

d.shape("rect", "Paper", x=0, y=0, width=1000, height=1000, fill=PAPER)
d.shape("ellipse", "Spot", x=265, y=205, width=470, height=470, fill=SPOT)
for i, (x, y, r) in enumerate([(755, 205, 34), (812, 285, 20), (742, 315, 12)]):
    d.shape("ellipse", f"Bubble {i}", x=x - r, y=y - r, width=2 * r, height=2 * r,
            fill="none", stroke=BODY, strokeWidth=2)

# fan tucked in: no arm starts above the dome's shoulder
P0 = (500, 470)
ARMS = [(56, 180, -175, 30), (78, 158, -190, 34), (102, 148, -200, 34), (126, 128, -210, 30)]
for ang, R, sweep, w in ARMS:
    d.path(arm(P0, ang, R, sweep, w, 5, flip=1), f"Arm R {ang}", fill=BODY)
    d.path(arm(P0, 180 - ang, R, sweep, w, 5, flip=-1), f"Arm L {ang}", fill=BODY)

d.path("M372 480 C372 350 400 250 500 250 C600 250 628 350 628 480 C560 512 440 512 372 480 Z",
       "Mantle", fill=BODY)
d.shape("ellipse", "Eye", x=462, y=330, width=76, height=76, fill=PAPER)
d.shape("ellipse", "Pupil", x=486, y=354, width=28, height=28, fill=SPOT)

d.cmd("select.none")
d.call("save_file", {"path": f"{HERE}/study-harper-octopus-V1R01.vectorcraft"}, "save native")
for fmt, path, scale in [("svg", f"{HERE}/study-harper-octopus-V1R01.svg", None),
                         ("png", f"{HERE}/study-harper-octopus-V1R01@2x.png", 2),
                         ("pdf", f"{OUT}/study-harper-octopus-V1R01.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    d.call("export", args, f"export {fmt}")
print("HARPER V1R01 DONE, calls:", d.count, "errors:", len(d.errors))
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])
