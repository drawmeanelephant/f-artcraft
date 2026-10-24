#!/usr/bin/env python3
"""spot-whale V1R03 — the joint is the read: body now tapers into a 24pt
tail stem, fluke is a paddle on that stem, belly deepened, forehead blunted.
Dressing (spot, spout, eye, dashes) held.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work"))
from vc import Draw, REPO, OUT

PAPER = "#F2EBDD"
BODY = "#2E2E38"
SPOT = "#E0673F"
HERE = os.path.join(REPO, "test", "glm-flash")

d = Draw()
d.new_doc("spot-whale-v1r03", 1000, 1000)

d.shape("rect", "Paper", x=0, y=0, width=1000, height=1000, fill=PAPER)
d.shape("ellipse", "Spot", x=215, y=175, width=570, height=570, fill=SPOT)
for i, (x, y, r) in enumerate([(150, 205, 30), (222, 138, 16)]):
    d.shape("ellipse", f"Bubble {i}", x=x - r, y=y - r, width=2 * r, height=2 * r,
            fill="none", stroke=BODY, strokeWidth=2.5)

# body: blunt head, low back, 24pt tail stem, deep belly
d.path("M850 470 "
       "C850 400 720 328 540 326 "          # blunt forehead -> low long back
       "C420 326 320 388 295 462 "          # taper into the stem (top)
       "C291 470 291 478 295 486 "          # stem back edge — narrow
       "C345 562 455 592 560 586 "          # deep belly
       "C690 578 810 538 850 470 Z",
       "Whale", fill=BODY)

# fluke: paddle on the narrow stem
d.path("M298 462 C250 446 180 440 118 444 C152 460 176 470 186 476 "
       "C170 486 148 500 126 518 C190 516 258 504 300 486 Z", "Fluke", fill=BODY)

# dorsal fin
d.path("M470 326 C486 298 514 286 544 292 C522 302 504 314 496 328 Z",
       "Dorsal", fill=BODY)

# jaw sliver at the mouth corner
d.path("M846 462 C812 494 768 516 716 528 C756 498 800 476 846 462 Z",
       "Jaw", fill=PAPER)

# eye + spout above
d.shape("ellipse", "Eye", x=722, y=402, width=50, height=50, fill=PAPER)
d.shape("ellipse", "Pupil", x=738, y=418, width=21, height=21, fill=SPOT)
for i, dstr in enumerate([
        "M742 352 C742 320 746 300 754 278",
        "M718 358 C702 334 696 314 700 294",
        "M766 356 C782 332 788 312 784 292"]):
    d.path(dstr, f"Spout {i}", fill="none", stroke=BODY, strokeWidth=7, cap="round")
d.shape("ellipse", "Spout dot", x=745, y=256, width=18, height=18, fill=BODY)

# water dashes
for i, (x0, y0, x1, y1) in enumerate([(408, 622, 476, 622), (506, 638, 588, 638),
                                      (614, 620, 668, 620)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Wave in {i}",
           fill="none", stroke=PAPER, strokeWidth=6, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(96, 706, 196, 706), (120, 742, 178, 742),
                                      (760, 724, 856, 724)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Wave out {i}",
           fill="none", stroke=BODY, strokeWidth=5, cap="round")

d.cmd("select.none")
d.call("save_file", {"path": f"{HERE}/spot-whale-V1R03.vectorcraft"}, "save native")
for fmt, path, scale in [("svg", f"{HERE}/spot-whale-V1R03.svg", None),
                         ("png", f"{HERE}/spot-whale-V1R03@2x.png", 2),
                         ("pdf", f"{OUT}/spot-whale-V1R03.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    d.call("export", args, f"export {fmt}")
print("SPOT WHALE V1R03 DONE, calls:", d.count, "errors:", len(d.errors))
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])
