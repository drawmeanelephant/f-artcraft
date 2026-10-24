#!/usr/bin/env python3
"""fennec-fox V2R02 — the tail, final form: a thick bushy ribbon wrapping
around the front paws (quadratic-bezier centreline, stays on the sun for
contrast), ink-dipped tip. Nose/mouth lowered slightly. Everything else
held from V2R01.
"""
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


def quad_ribbon(s, c, t_end, w0, w1, n=60, t0=0.0):
    """Tapered ribbon along a quadratic bezier S -> (ctrl) C -> T."""
    rib = []
    for k in range(n + 1):
        t = t0 + (1 - t0) * k / n
        x = (1 - t) ** 2 * s[0] + 2 * (1 - t) * t * c[0] + t ** 2 * t_end[0]
        y = (1 - t) ** 2 * s[1] + 2 * (1 - t) * t * c[1] + t ** 2 * t_end[1]
        dx = 2 * (1 - t) * (c[0] - s[0]) + 2 * t * (t_end[0] - c[0])
        dy = 2 * (1 - t) * (c[1] - s[1]) + 2 * t * (t_end[1] - c[1])
        L = (dx * dx + dy * dy) ** 0.5 or 1
        nx, ny = -dy / L, dx / L
        w = w0 + (w1 - w0) * (t ** 1.1)
        rib.append((x + nx * w / 2, y + ny * w / 2))
        rib.insert(0, (x - nx * w / 2, y - ny * w / 2))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in rib) + " Z"


d = Draw()
d.new_doc("fennec-fox-v2r02", 1000, 1000)

d.shape("rect", "Paper", x=0, y=0, width=1000, height=1000, fill=PAPER)
d.shape("ellipse", "Spot", x=200, y=165, width=600, height=600, fill=SUN)

# ears: two huge leaves, inner ears shaded
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

# body: low crouch mound
d.path("M370 560 C400 470 440 440 500 440 C560 440 600 470 630 560 "
       "C650 620 640 682 600 700 C540 716 460 716 400 700 C360 682 350 620 370 560 Z",
       "Body", fill=SAND)

# head: wide, flat-topped, short
d.path("M352 404 C352 336 412 310 500 310 C588 310 648 336 648 404 "
       "C648 468 570 522 500 522 C430 522 352 468 352 404 Z", "Head", fill=SAND)

# tail: bushy wrap around the front paws, ink-dipped tip at the left end
d.path(quad_ribbon((618, 652), (500, 782), (382, 655), 88, 40), "Tail", fill=SAND)
d.path(quad_ribbon((618, 652), (500, 782), (382, 655), 88, 40, t0=0.74),
       "Tail tip", fill=INK)

# face: nose + smile
d.path("M486 478 C494 490 506 490 514 478 C510 492 490 492 486 478 Z",
       "Nose", fill=INK)
d.path("M478 504 Q500 520 522 504", "Mouth",
       fill="none", stroke=INK, strokeWidth=3, cap="round")
for i, x in enumerate((443, 557)):
    d.shape("ellipse", f"Eye {i}", x=x - 17, y=384, width=34, height=34, fill=PAPER)
    d.shape("ellipse", f"Pupil {i}", x=x - 8, y=393, width=16, height=16, fill=INK)

# whiskers from the muzzle, fanning out-down
for i, (x0, y0, x1, y1) in enumerate([(478, 512, 408, 530), (480, 522, 416, 554),
                                      (522, 512, 592, 530), (520, 522, 584, 554)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Whisker {i}",
           fill="none", stroke=INK, strokeWidth=2.5, cap="round")

# dressing: ground ticks under the tail wrap, paper dashes on the sun
for i, (x0, x1) in enumerate([(400, 470), (530, 600)]):
    d.path(f"M{x0} 736 L{x1} 736", f"Ground {i}",
           fill="none", stroke=SAND_DK, strokeWidth=5, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(300, 300, 356, 300), (660, 620, 706, 620)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Dash {i}",
           fill="none", stroke=PAPER, strokeWidth=5, cap="round")

# caption, mirroring the plate: FENNEC FOX, Virelai Sans 56pt, centred
d.text("FENNEC FOX", "Name", x=500, y=940, size=56, font="Virelai Sans",
       color=INK, justify="center")

d.cmd("select.none")
d.call("save_file", {"path": f"{HERE}/fennec-fox-V2R02.vectorcraft"}, "save native")
for fmt, path, scale in [("svg", f"{HERE}/fennec-fox-V2R02.svg", None),
                         ("png", f"{HERE}/fennec-fox-V2R02@2x.png", 2),
                         ("pdf", f"{OUT}/fennec-fox-V2R02.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    d.call("export", args, f"export {fmt}")
print("FENNEC V2R02 DONE, calls:", d.count, "errors:", len(d.errors))
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])
