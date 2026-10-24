#!/usr/bin/env python3
"""fennec-fox V2R00 — spot-flat rendition (GLM-Flash idiom).

Second reading of the fennec-fox plate: same subject, same caption, new
style. Spot-flat grammar: flat silhouettes, spot-circle hub, minimal face,
thin-line dressing — no gradients (deliberate idiom break, per the
spot-flat charter in PROMPTS.md). Palette keys to the subject: desert sand
on an ochre sun, charcoal accents. Reference: fennec-fox-V1R00.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, REPO, OUT

PAPER = "#F2EBDD"     # page
SAND = "#E5C99A"      # body
SAND_DK = "#C89B62"   # shade accent / tail tip ring
SUN = "#E09B3D"       # spot circle
INK = "#2E2E38"       # charcoal accents
HERE = os.path.join(REPO, "art", "animals", "fennec-fox")


def curl(p0, ang, R, sweep, w0, w1, flip=1, n=48):
    """Tapered curl centreline ribbon (the shared spot-flat helper)."""
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
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z", \
        outer[-1]  # tip centre, for the tail-tip mark


d = Draw()
d.new_doc("fennec-fox-v2r00", 1000, 1000)

d.shape("rect", "Paper", x=0, y=0, width=1000, height=1000, fill=PAPER)
d.shape("ellipse", "Spot", x=200, y=165, width=600, height=600, fill=SUN)

# ears first (behind the head): two huge leaf shapes + inner ears
for i, x0 in enumerate((382, 618)):
    s = -1 if i == 0 else 1
    d.path(f"M{x0} 360 C{x0 + s * 62} 316 {x0 + s * 74} 196 {x0 + s * 46} 118 "
           f"C{x0 + s * 30} 72 {x0 - s * 30} 72 {x0 - s * 46} 118 "
           f"C{x0 - s * 74} 196 {x0 - s * 62} 316 {x0} 360 Z",
           f"Ear {'L' if i == 0 else 'R'}", fill=SAND)
    d.path(f"M{x0} 344 C{x0 + s * 40} 306 {x0 + s * 48} 206 {x0 + s * 28} 140 "
           f"C{x0 + s * 18} 106 {x0 - s * 18} 106 {x0 - s * 28} 140 "
           f"C{x0 - s * 48} 206 {x0 - s * 40} 306 {x0} 344 Z",
           f"Ear inner {'L' if i == 0 else 'R'}", fill=SAND_DK, opacity=55)

# tail: bushy curl around the right side, dark tip
tail_d, tail_tip = curl((575, 640), 25, 120, -215, 74, 14, flip=1)
d.path(tail_d, "Tail", fill=SAND)
d.shape("ellipse", "Tail tip", x=tail_tip[0] - 17, y=tail_tip[1] - 17,
        width=34, height=34, fill=INK)

# body + head: one soft silhouette, crouched
d.path("M360 470 C360 380 420 330 500 330 C580 330 640 380 640 470 "
       "C640 545 610 600 560 632 C560 680 540 712 500 712 C460 712 440 680 440 632 "
       "C390 600 360 545 360 470 Z", "Body", fill=SAND)

# muzzle wedge slightly lighter
d.path("M452 470 C476 520 524 520 548 470 C540 540 520 566 500 566 C480 566 460 540 452 470 Z",
       "Muzzle", fill=PAPER, opacity=45)

# minimal face: paper rings + ink dots, tiny nose, whisker ticks
for i, x in enumerate((443, 557)):
    d.shape("ellipse", f"Eye {i}", x=x - 17, y=398, width=34, height=34, fill=PAPER)
    d.shape("ellipse", f"Pupil {i}", x=x - 8, y=407, width=16, height=16, fill=INK)
d.path("M487 486 C494 496 506 496 513 486 C508 500 492 500 487 486 Z",
       "Nose", fill=INK)
for i, (x0, y0, x1, y1) in enumerate([(430, 520, 368, 540), (432, 536, 380, 566),
                                      (570, 520, 632, 540), (568, 536, 620, 566)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Whisker {i}",
           fill="none", stroke=INK, strokeWidth=2.5, cap="round")

# dressing: ground ticks under the paws, two paper dashes on the sun
for i, (x0, x1) in enumerate([(400, 470), (530, 600)]):
    d.path(f"M{x0} 726 L{x1} 726", f"Ground {i}",
           fill="none", stroke=SAND_DK, strokeWidth=5, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(300, 300, 356, 300), (660, 620, 706, 620)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Dash {i}",
           fill="none", stroke=PAPER, strokeWidth=5, cap="round")

# caption, mirroring the plate: FENNEC FOX, Virelai Sans 56pt, centred
d.text("FENNEC FOX", "Name", x=500, y=940, size=56, font="Virelai Sans",
       color=INK, justify="center")

d.cmd("select.none")
d.call("save_file", {"path": f"{HERE}/fennec-fox-V2R00.vectorcraft"}, "save native")
for fmt, path, scale in [("svg", f"{HERE}/fennec-fox-V2R00.svg", None),
                         ("png", f"{HERE}/fennec-fox-V2R00@2x.png", 2),
                         ("pdf", f"{OUT}/fennec-fox-V2R00.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    d.call("export", args, f"export {fmt}")
print("FENNEC V2R00 DONE, calls:", d.count, "errors:", len(d.errors))
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])
