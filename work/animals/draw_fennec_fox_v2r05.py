#!/usr/bin/env python3
"""fennec-fox V2R05 — kill the earring ruffs, commit to the snout: cheeks
taper decisively into a narrow muzzle, bigger nose at the tip. Everything
else held from V2R04.
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
    """Tapered ribbon along a quadratic bezier S -> C -> T."""
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
d.new_doc("fennec-fox-v2r05", 1000, 1000)

d.shape("rect", "Paper", x=0, y=0, width=1000, height=1000, fill=PAPER)
d.shape("ellipse", "Spot", x=200, y=165, width=600, height=600, fill=SUN)

# ears: two huge leaves, inner ears shaded
for i, x0 in enumerate((368, 632)):
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

# head: cranium, then an honest snout — cheeks taper hard to a narrow tip
d.path("M356 372 C356 316 416 292 500 292 C584 292 644 316 644 372 "
       "C644 428 570 478 522 502 "          # right cheek -> snout, long taper
       "C508 508 492 508 478 502 "          # narrow tip
       "C430 478 356 428 356 372 Z", "Head", fill=SAND)

# nose: a proper wedge at the tip
d.path("M472 486 C486 500 514 500 528 486 C524 508 476 508 472 486 Z",
       "Nose", fill=INK)
d.path("M488 518 Q500 526 512 518", "Mouth",
       fill="none", stroke=INK, strokeWidth=3, cap="round")

# eyes: higher and wider
for i, x in enumerate((424, 576)):
    d.shape("ellipse", f"Eye {i}", x=x - 17, y=356, width=34, height=34, fill=PAPER)
    d.shape("ellipse", f"Pupil {i}", x=x - 8, y=365, width=16, height=16, fill=INK)

# whiskers from the muzzle sides, short
for i, (x0, y0, x1, y1) in enumerate([(470, 494, 404, 504), (472, 504, 412, 528),
                                      (530, 494, 596, 504), (528, 504, 588, 528)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Whisker {i}",
           fill="none", stroke=INK, strokeWidth=2.5, cap="round")

# tail: bushy swoosh laid on the ground to the right, ink-dipped far end
d.path(quad_ribbon((615, 655), (760, 700), (800, 590), 86, 30), "Tail", fill=SAND)
d.path(quad_ribbon((615, 655), (760, 700), (800, 590), 86, 30, t0=0.72),
       "Tail tip", fill=INK)

# dressing: two paper dashes on the sun
for i, (x0, y0, x1, y1) in enumerate([(300, 300, 356, 300), (262, 620, 306, 620)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Dash {i}",
           fill="none", stroke=PAPER, strokeWidth=5, cap="round")

# caption, mirroring the plate: FENNEC FOX, Virelai Sans 56pt, centred
d.text("FENNEC FOX", "Name", x=500, y=940, size=56, font="Virelai Sans",
       color=INK, justify="center")

d.cmd("select.none")
d.call("save_file", {"path": f"{HERE}/fennec-fox-V2R05.vectorcraft"}, "save native")
for fmt, path, scale in [("svg", f"{HERE}/fennec-fox-V2R05.svg", None),
                         ("png", f"{HERE}/fennec-fox-V2R05@2x.png", 2),
                         ("pdf", f"{OUT}/fennec-fox-V2R05.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    d.call("export", args, f"export {fmt}")
print("FENNEC V2R05 DONE, calls:", d.count, "errors:", len(d.errors))
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])
