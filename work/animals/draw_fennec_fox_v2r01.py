#!/usr/bin/env python3
"""fennec-fox V2R01 — anatomy fixes from the V2R00 proof:
bushy tail (thick along its whole visible length, dipped ink tip drawn ON
the ribbon), no open-grin muzzle wedge (nose + smile line instead),
whiskers anchored at the muzzle, wide flat-topped head over a low crouch.
Spot-flat grammar, palette and caption held.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, REPO, OUT

PAPER = "#F2EBDD"
SAND = "#E5C99A"
SAND_DK = "#C89B62"
SUN = "#E09B3D"
INK = "#2E2E38"
HERE = os.path.join(REPO, "art", "animals", "fennec-fox")


def curl(p0, ang, R, sweep, w0, w1, flip=1, n=48, t0=0.0):
    """Tapered curl ribbon; t0 skips ahead along the centreline (for tips)."""
    a0 = math.radians(ang)
    ux, uy = math.cos(a0), math.sin(a0)
    cx = p0[0] + (-uy * flip) * R
    cy = p0[1] + (ux * flip) * R
    phi0 = math.atan2(p0[1] - cy, p0[0] - cx)
    sw = math.radians(sweep)
    outer, inner = [], []
    for k in range(n + 1):
        t = t0 + (1 - t0) * k / n
        phi = phi0 + sw * t
        w = w0 + (w1 - w0) * (t ** 1.2)
        px, py = cx + R * math.cos(phi), cy + R * math.sin(phi)
        outer.append((px + math.cos(phi) * w / 2, py + math.sin(phi) * w / 2))
        inner.append((px - math.cos(phi) * w / 2, py - math.sin(phi) * w / 2))
    pts = outer + inner[::-1]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


d = Draw()
d.new_doc("fennec-fox-v2r01", 1000, 1000)

d.shape("rect", "Paper", x=0, y=0, width=1000, height=1000, fill=PAPER)
d.shape("ellipse", "Spot", x=200, y=165, width=600, height=600, fill=SUN)

# ears first: two huge leaves, inner ears shaded
for i, x0 in enumerate((372, 628)):
    s = -1 if i == 0 else 1
    d.path(f"M{x0} 372 C{x0 + s * 62} 322 {x0 + s * 76} 200 {x0 + s * 47} 118 "
           f"C{x0 + s * 31} 70 {x0 - s * 31} 70 {x0 - s * 47} 118 "
           f"C{x0 - s * 76} 200 {x0 - s * 62} 322 {x0} 372 Z",
           f"Ear {'L' if i == 0 else 'R'}", fill=SAND)
    d.path(f"M{x0} 354 C{x0 + s * 41} 310 {x0 + s * 50} 210 {x0 + s * 29} 142 "
           f"C{x0 + s * 19} 107 {x0 - s * 19} 107 {x0 - s * 29} 142 "
           f"C{x0 - s * 50} 210 {x0 - s * 41} 310 {x0} 354 Z",
           f"Ear inner {'L' if i == 0 else 'R'}", fill=SAND_DK, opacity=55)

# body: low crouch mound (head goes over it)
d.path("M370 560 C400 470 440 440 500 440 C560 440 600 470 630 560 "
       "C650 620 640 682 600 700 C540 716 460 716 400 700 C360 682 350 620 370 560 Z",
       "Body", fill=SAND)

# head: wide, flat-topped, short — cheeks widest at y~420, small chin
d.path("M352 404 C352 336 412 310 500 310 C588 310 648 336 648 404 "
       "C648 468 570 522 500 522 C430 522 352 468 352 404 Z", "Head", fill=SAND)

# tail: bushy curl, thick where visible, ink-dipped tip ON the ribbon
P0 = (612, 618)
tail_d, tip = None, None
a0 = math.radians(28)
ux, uy = math.cos(a0), math.sin(a0)
CX, CY = P0[0] + (-uy) * 128, P0[1] + (ux) * 128
phi0 = math.atan2(P0[1] - CY, P0[0] - CX)
sw = math.radians(-210)
pts = []
for k in range(49):
    t = k / 48
    phi = phi0 + sw * t
    w = 96 + (24 - 96) * (t ** 1.25)
    pts.append((CX + 128 * math.cos(phi), CY + 128 * math.sin(phi), w, phi))
outer = [(x + w / 2 * math.cos(p), y + w / 2 * math.sin(p)) for x, y, w, p in pts]
inner = [(x - w / 2 * math.cos(p), y - w / 2 * math.sin(p)) for x, y, w, p in pts]
seq = outer + inner[::-1]
d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in seq) + " Z", "Tail", fill=SAND)
# dipped tip: last 20% of the same ribbon, in ink
sub = []
for k in range(21):
    t = 0.80 + 0.20 * k / 20
    phi = phi0 + sw * t
    w = 96 + (24 - 96) * (t ** 1.25)
    x, y = CX + 128 * math.cos(phi), CY + 128 * math.sin(phi)
    sub.append((x + w / 2 * math.cos(phi), y + w / 2 * math.sin(phi)))
    sub.insert(0, (x - w / 2 * math.cos(phi), y - w / 2 * math.sin(phi)))
d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in sub) + " Z", "Tail tip", fill=INK)

# face: nose + smile, no grin wedge
d.path("M486 470 C494 482 506 482 514 470 C510 484 490 484 486 470 Z",
       "Nose", fill=INK)
d.path("M478 496 Q500 512 522 496", "Mouth",
       fill="none", stroke=INK, strokeWidth=3, cap="round")
for i, x in enumerate((443, 557)):
    d.shape("ellipse", f"Eye {i}", x=x - 17, y=384, width=34, height=34, fill=PAPER)
    d.shape("ellipse", f"Pupil {i}", x=x - 8, y=393, width=16, height=16, fill=INK)

# whiskers from the muzzle, fanning out-down
for i, (x0, y0, x1, y1) in enumerate([(478, 506, 408, 524), (480, 516, 416, 548),
                                      (522, 506, 592, 524), (520, 516, 584, 548)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Whisker {i}",
           fill="none", stroke=INK, strokeWidth=2.5, cap="round")

# dressing: ground ticks, paper dashes on the sun
for i, (x0, x1) in enumerate([(400, 470), (530, 600)]):
    d.path(f"M{x0} 730 L{x1} 730", f"Ground {i}",
           fill="none", stroke=SAND_DK, strokeWidth=5, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(300, 300, 356, 300), (660, 620, 706, 620)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Dash {i}",
           fill="none", stroke=PAPER, strokeWidth=5, cap="round")

# caption, mirroring the plate: FENNEC FOX, Virelai Sans 56pt, centred
d.text("FENNEC FOX", "Name", x=500, y=940, size=56, font="Virelai Sans",
       color=INK, justify="center")

d.cmd("select.none")
d.call("save_file", {"path": f"{HERE}/fennec-fox-V2R01.vectorcraft"}, "save native")
for fmt, path, scale in [("svg", f"{HERE}/fennec-fox-V2R01.svg", None),
                         ("png", f"{HERE}/fennec-fox-V2R01@2x.png", 2),
                         ("pdf", f"{OUT}/fennec-fox-V2R01.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    d.call("export", args, f"export {fmt}")
print("FENNEC V2R01 DONE, calls:", d.count, "errors:", len(d.errors))
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])
