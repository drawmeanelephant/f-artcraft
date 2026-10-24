#!/usr/bin/env python3
"""Style study 1/3 — ART DECO octopus, flat poster grammar.

Sunburst rays, double-rule frame, two-tone flat shading, luxe palette on
deep charcoal. Every element is programmatic: fan geometry, arc-swept
tapered arms, stepped ornaments. Part of the GLM-Flash style exploration
(test/glm-flash/README.md).
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work"))
from vc import Draw, REPO, OUT

INK = "#14181F"       # deep charcoal-navy field
GOLD = "#D9A441"      # ray gold
GOLD_DK = "#B0842F"   # deep gold
CREAM = "#EFE3C8"     # octopus body
CREAM_DK = "#D9C9A6"  # shade tone
VERM = "#C64B33"      # vermilion accent
HERE = os.path.join(REPO, "test", "glm-flash")


def arm(p0, ang, R, sweep, w0, w1, flip=1, n=42):
    """Tapered curl arm: arc centerline from p0, initial direction ang
    (deg, y down), radius R, sweep deg (sign = curl direction), width
    w0 -> w1 along the radial normal. Closed polygon path."""
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
    """Deco sunburst ray: tapered triangle from r0 to r1."""
    a = math.radians(a)
    ca, sa = math.cos(a), math.sin(a)
    px, py = -sa, ca
    return (f"M{cx + ca * r0 + px * w:.1f},{cy + sa * r0 + py * w:.1f} "
            f"L{cx + ca * r0 - px * w:.1f},{cy + sa * r0 - py * w:.1f} "
            f"L{cx + ca * r1:.1f},{cy + sa * r1:.1f} Z")


d = Draw()
d.new_doc("study-deco-octopus", 1000, 1000)

# field + flat sunburst
d.shape("rect", "Field", x=0, y=0, width=1000, height=1000, fill=INK)
for i in range(24):
    a = i * 15
    d.path(ray(500, 470, a, 185, i % 2 and 430 or 470, 13),
           f"Ray {i}", fill=i % 2 and GOLD_DK or GOLD, opacity=88)

# deco frame: double rule + stepped corner squares
d.shape("rect", "Frame outer", x=26, y=26, width=948, height=948, fill="none",
        stroke=GOLD, strokeWidth=3)
d.shape("rect", "Frame inner", x=40, y=40, width=920, height=920, fill="none",
        stroke=GOLD_DK, strokeWidth=1.5)
for i, (x, y) in enumerate([(40, 40), (940, 40), (40, 940), (940, 940)]):
    d.shape("rect", f"Corner {i}", x=x - 9, y=y - 9, width=18, height=18, fill=GOLD)

# vermilion ring accent behind the subject
d.shape("ellipse", "Halo", x=310, y=250, width=380, height=380, fill="none",
        stroke=VERM, strokeWidth=2.5)

# octopus — cream with poster two-tone shade, gold outlines
P0 = (500, 480)
ARMS = [(38, 210, -175, 30), (66, 165, -190, 34), (96, 150, -205, 34), (124, 130, -215, 30)]
for ang, R, sweep, w in ARMS:
    d.path(arm(P0, ang, R, sweep, w, 4, flip=1), f"Arm R {ang}",
           fill=CREAM, stroke=GOLD_DK, strokeWidth=2)
    d.path(arm(P0, 180 - ang, R, sweep, w, 4, flip=-1), f"Arm L {ang}",
           fill=CREAM, stroke=GOLD_DK, strokeWidth=2)

# head dome + shade crescent
d.path("M380 470 L380 360 C380 271 411 210 500 210 C589 210 620 271 620 360 L620 470 "
       "C583 500 417 500 380 470 Z", "Mantle", fill=CREAM, stroke=GOLD_DK, strokeWidth=2.5)
d.path("M560 232 C604 252 620 302 620 360 L620 452 C604 470 578 478 560 472 "
       "C592 400 592 300 560 232 Z", "Mantle shade", fill=CREAM_DK, opacity=70)

# deco eyes: horizontal almonds
for i, x in enumerate((448, 552)):
    d.shape("ellipse", f"Eye {i}", x=x - 26, y=330, width=52, height=18, fill=INK)
    d.shape("ellipse", f"Glint {i}", x=x - 14, y=334, width=10, height=7, fill=CREAM)

d.cmd("select.none")
r = d.call("save_file", {"path": f"{HERE}/study-deco-octopus-V1R00.vectorcraft"}, "save native")
print("save:", json.dumps(r)[:100] if r else "")
for fmt, path, scale in [("svg", f"{HERE}/study-deco-octopus-V1R00.svg", None),
                         ("png", f"{HERE}/study-deco-octopus-V1R00@2x.png", 2),
                         ("pdf", f"{OUT}/study-deco-octopus-V1R00.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    r = d.call("export", args, f"export {fmt}")
    print(fmt, "ok" if r else "FAIL")
print("DECO STUDY DONE, calls:", d.count, "errors:", len(d.errors))
