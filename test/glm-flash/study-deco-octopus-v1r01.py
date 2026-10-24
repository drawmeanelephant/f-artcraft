#!/usr/bin/env python3
"""study-deco-octopus V1R01 — fixes from the V1R00 proof:
round bell mantle (was reading as a baguette), larger kohl-lined eyes set
lower, form-following shade crescent, halo dropped (read as accidental),
arm fan pulled in so every arm emerges from under the dome.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work"))
from vc import Draw, REPO, OUT

INK = "#14181F"
GOLD = "#D9A441"
GOLD_DK = "#B0842F"
CREAM = "#EFE3C8"
CREAM_DK = "#D9C9A6"
HERE = os.path.join(REPO, "test", "glm-flash")


def arm(p0, ang, R, sweep, w0, w1, flip=1, n=42):
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
        w = w0 + (w1 - w0) * (t ** 1.15)
        px, py = cx + R * math.cos(phi), cy + R * math.sin(phi)
        outer.append((px + math.cos(phi) * w / 2, py + math.sin(phi) * w / 2))
        inner.append((px - math.cos(phi) * w / 2, py - math.sin(phi) * w / 2))
    pts = outer + inner[::-1]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def ray(cx, cy, a, r0, r1, w):
    a = math.radians(a)
    ca, sa = math.cos(a), math.sin(a)
    px, py = -sa, ca
    return (f"M{cx + ca * r0 + px * w:.1f},{cy + sa * r0 + py * w:.1f} "
            f"L{cx + ca * r0 - px * w:.1f},{cy + sa * r0 - py * w:.1f} "
            f"L{cx + ca * r1:.1f},{cy + sa * r1:.1f} Z")


d = Draw()
d.new_doc("study-deco-octopus-v1r01", 1000, 1000)

d.shape("rect", "Field", x=0, y=0, width=1000, height=1000, fill=INK)
for i in range(24):
    a = i * 15
    d.path(ray(500, 470, a, 185, i % 2 and 430 or 470, 13),
           f"Ray {i}", fill=i % 2 and GOLD_DK or GOLD, opacity=88)

d.shape("rect", "Frame outer", x=26, y=26, width=948, height=948, fill="none",
        stroke=GOLD, strokeWidth=3)
d.shape("rect", "Frame inner", x=40, y=40, width=920, height=920, fill="none",
        stroke=GOLD_DK, strokeWidth=1.5)
for i, (x, y) in enumerate([(40, 40), (940, 40), (40, 940), (940, 940)]):
    d.shape("rect", f"Corner {i}", x=x - 9, y=y - 9, width=18, height=18, fill=GOLD)

# octopus — arms all emerge from under the dome, curl out and up
P0 = (500, 480)
ARMS = [(58, 230, -170, 30), (82, 185, -185, 34), (106, 165, -200, 34), (128, 140, -215, 30)]
for ang, R, sweep, w in ARMS:
    d.path(arm(P0, ang, R, sweep, w, 4, flip=1), f"Arm R {ang}",
           fill=CREAM, stroke=GOLD_DK, strokeWidth=2)
    d.path(arm(P0, 180 - ang, R, sweep, w, 4, flip=-1), f"Arm L {ang}",
           fill=CREAM, stroke=GOLD_DK, strokeWidth=2)

# mantle: round bell
d.path("M370 480 C362 330 400 222 500 222 C600 222 638 330 630 480 "
       "C560 506 440 506 370 480 Z", "Mantle", fill=CREAM, stroke=GOLD_DK, strokeWidth=2.5)
# shade follows the right form
d.path("M562 240 C612 272 634 366 630 478 C604 496 576 502 558 494 "
       "C588 410 588 310 562 240 Z", "Mantle shade", fill=CREAM_DK, opacity=70)

# eyes: larger, lower, deco kohl lines
for i, x in enumerate((448, 552)):
    d.shape("ellipse", f"Eye {i}", x=x - 30, y=352, width=60, height=22, fill=INK)
    d.shape("ellipse", f"Glint {i}", x=x - 16, y=357, width=12, height=8, fill=CREAM)
    ln = -1 if i == 0 else 1
    d.path(f"M{x + ln * 30} 362 L{x + ln * 62} 358", f"Kohl {i}",
           fill="none", stroke=INK, strokeWidth=3, cap="round")

d.cmd("select.none")
d.call("save_file", {"path": f"{HERE}/study-deco-octopus-V1R01.vectorcraft"}, "save native")
for fmt, path, scale in [("svg", f"{HERE}/study-deco-octopus-V1R01.svg", None),
                         ("png", f"{HERE}/study-deco-octopus-V1R01@2x.png", 2),
                         ("pdf", f"{OUT}/study-deco-octopus-V1R01.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    d.call("export", args, f"export {fmt}")
print("DECO V1R01 DONE, calls:", d.count, "errors:", len(d.errors))
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])
