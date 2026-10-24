#!/usr/bin/env python3
"""study-linocut-octopus V1R01 — carve marks now follow the arm geometry
(taken from the arm centerlines, not fixed coordinates), plus mantle texture.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work"))
from vc import Draw, REPO, OUT

PAPER = "#F4EFE4"
INK = "#1A1714"
SPOT = "#C6402E"
HERE = os.path.join(REPO, "test", "glm-flash")


def arm_points(p0, ang, R, sweep, flip=1, n=14):
    a0 = math.radians(ang)
    ux, uy = math.cos(a0), math.sin(a0)
    cx = p0[0] + (-uy * flip) * R
    cy = p0[1] + (ux * flip) * R
    phi0 = math.atan2(p0[1] - cy, p0[0] - cx)
    sw = math.radians(sweep)
    pts = []
    for k in range(n + 1):
        phi = phi0 + sw * k / n
        pts.append((cx + R * math.cos(phi), cy + R * math.sin(phi)))
    return pts


def arm_path(p0, ang, R, sweep, w0, w1, flip=1, n=14):
    pts = arm_points(p0, ang, R, sweep, flip, n)
    a0 = math.radians(ang)
    ux, uy = math.cos(a0), math.sin(a0)
    cx = p0[0] + (-uy * flip) * R
    cy = p0[1] + (ux * flip) * R
    outer, inner = [], []
    for k, (px, py) in enumerate(pts):
        t = k / n
        w = w0 + (w1 - w0) * (t ** 1.1)
        nx, ny = (px - cx) / R, (py - cy) / R
        outer.append((px + nx * w / 2, py + ny * w / 2))
        inner.append((px - nx * w / 2, py - ny * w / 2))
    seq = outer + inner[::-1]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in seq) + " Z"


d = Draw()
d.new_doc("study-linocut-octopus-v1r01", 1000, 1000)

d.shape("rect", "Paper", x=0, y=0, width=1000, height=1000, fill=PAPER)
d.shape("ellipse", "Spot sun", x=200, y=100, width=600, height=600, fill=SPOT)
d.shape("rect", "Frame", x=34, y=34, width=932, height=932, fill="none",
        stroke=INK, strokeWidth=10)

P0 = (500, 470)
ARMS = [(42, 195, -170, 32), (70, 160, -185, 36), (100, 148, -200, 36), (128, 128, -210, 32)]
arm_geom = []
for side, flip in (("R", 1), ("L", -1)):
    for ang, R, sweep, w in ARMS:
        a = ang if side == "R" else 180 - ang
        pts = arm_points(P0, a, R, sweep, flip)
        d.path(arm_path(P0, a, R, sweep, w, 5, flip=flip), f"Arm {side} {ang}", fill=INK)
        arm_geom.append((side, ang, pts))

# angular dome
d.path("M368 480 L376 340 C392 268 440 244 500 244 C560 244 608 268 624 340 L632 480 "
       "C556 514 444 514 368 480 Z", "Mantle", fill=INK)

# carve marks: short dashes ACROSS each arm, tracking its centreline
for side, ang, pts in arm_geom:
    for t in (0.35, 0.6, 0.82):
        i = min(int(t * (len(pts) - 1)), len(pts) - 2)
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        d.path(f"M{mx - nx * 9:.1f} {my - ny * 9:.1f} L{mx + nx * 9:.1f} {my + ny * 9:.1f}",
               f"Carve {side} {ang} {t}", fill="none", stroke=PAPER, strokeWidth=6, cap="round")

# mantle carve texture: three short dashes on the dome
for i, (x, y) in enumerate([(560, 290), (585, 330), (600, 375)]):
    d.path(f"M{x} {y} L{x + 26} {y + 12}", f"Mantle carve {i}",
           fill="none", stroke=PAPER, strokeWidth=5, cap="round")

# eyes + angled carve brows
for i, x in enumerate((446, 554)):
    d.shape("ellipse", f"Eye {i}", x=x - 30, y=318, width=60, height=60, fill=PAPER)
    d.shape("ellipse", f"Pupil {i}", x=x - 12, y=336, width=24, height=24, fill=INK)
    bd = -1 if i == 0 else 1
    d.path(f"M{x + bd * 12} 306 L{x + bd * 44} 296", f"Brow {i}",
           fill="none", stroke=PAPER, strokeWidth=6, cap="round")

d.cmd("select.none")
d.call("save_file", {"path": f"{HERE}/study-linocut-octopus-V1R01.vectorcraft"}, "save native")
for fmt, path, scale in [("svg", f"{HERE}/study-linocut-octopus-V1R01.svg", None),
                         ("png", f"{HERE}/study-linocut-octopus-V1R01@2x.png", 2),
                         ("pdf", f"{OUT}/study-linocut-octopus-V1R01.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    d.call("export", args, f"export {fmt}")
print("LINOCUT V1R01 DONE, calls:", d.count, "errors:", len(d.errors))
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])
