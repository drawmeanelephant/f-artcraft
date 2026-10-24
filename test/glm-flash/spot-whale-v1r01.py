#!/usr/bin/env python3
"""spot-whale V1R01 — anatomy fixes from the V1R00 proof:
blunt whale head (was a fish snout), deeper belly, small dorsal fin, and a
horizontal whale fluke (was a vertical fish tail). Style, palette, dressing
all held from V1R00.
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
d.new_doc("spot-whale-v1r01", 1000, 1000)

d.shape("rect", "Paper", x=0, y=0, width=1000, height=1000, fill=PAPER)
d.shape("ellipse", "Spot", x=215, y=175, width=570, height=570, fill=SPOT)
for i, (x, y, r) in enumerate([(150, 205, 30), (222, 138, 16)]):
    d.shape("ellipse", f"Bubble {i}", x=x - r, y=y - r, width=2 * r, height=2 * r,
            fill="none", stroke=BODY, strokeWidth=2.5)

# whale: blunt head, deep belly, dorsal bump, horizontal fluke
d.path("M842 462 "
       "C842 430 812 396 760 368 "          # blunt forehead
       "C700 334 640 322 560 318 "          # back, dorsal area flat-ish
       "C430 314 300 360 262 452 "          # toward the tail joint
       "C220 436 150 424 112 428 "          # fluke: upper edge sweeping left
       "C146 448 168 460 174 470 "          # to the notch
       "C150 478 128 494 118 512 "          # lower fluke wing
       "C160 512 228 500 266 486 "          # back to the joint, below
       "C310 552 430 584 540 578 "          # deep belly
       "C680 570 790 530 842 462 Z",
       "Whale", fill=BODY)

# small dorsal fin on the back ridge
d.path("M560 318 C574 296 596 288 620 292 C604 300 590 308 582 320 Z",
       "Dorsal", fill=BODY)

# under-jaw: short cream crescent, lower
d.path("M838 470 C790 508 700 534 596 546 C640 516 740 488 838 470 Z",
       "Jaw", fill=PAPER)

# eye: paper ring + vermilion dot
d.shape("ellipse", "Eye", x=716, y=404, width=50, height=50, fill=PAPER)
d.shape("ellipse", "Pupil", x=732, y=420, width=21, height=21, fill=SPOT)

# spout: three arcs from the blowhole
for i, dstr in enumerate([
        "M612 286 C612 252 616 230 624 206",
        "M588 292 C572 266 566 244 570 222",
        "M636 290 C652 266 658 244 654 222"]):
    d.path(dstr, f"Spout {i}", fill="none", stroke=BODY, strokeWidth=7, cap="round")
d.shape("ellipse", "Spout dot", x=615, y=184, width=18, height=18, fill=BODY)

# water dashes
for i, (x0, y0, x1, y1) in enumerate([(408, 614, 476, 614), (506, 630, 588, 630),
                                      (614, 612, 668, 612)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Wave in {i}",
           fill="none", stroke=PAPER, strokeWidth=6, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(96, 706, 196, 706), (120, 742, 178, 742),
                                      (760, 724, 856, 724)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Wave out {i}",
           fill="none", stroke=BODY, strokeWidth=5, cap="round")

d.cmd("select.none")
d.call("save_file", {"path": f"{HERE}/spot-whale-V1R01.vectorcraft"}, "save native")
for fmt, path, scale in [("svg", f"{HERE}/spot-whale-V1R01.svg", None),
                         ("png", f"{HERE}/spot-whale-V1R01@2x.png", 2),
                         ("pdf", f"{OUT}/spot-whale-V1R01.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    d.call("export", args, f"export {fmt}")
print("SPOT WHALE V1R01 DONE, calls:", d.count, "errors:", len(d.errors))
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])
