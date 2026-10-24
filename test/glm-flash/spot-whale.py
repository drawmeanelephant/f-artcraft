#!/usr/bin/env python3
"""spot-whale V1R00 — the finished GLM-Flash style test piece.

Style: mid-century spot-flat (Charley Harper grammar) — the winning study
style. Flat shape abstraction, one spot circle, paper + charcoal + vermilion,
no outlines, no gradients (deliberately: that is the style's grammar, and
the point of the test — see test/glm-flash/README.md).

The whale is one closed silhouette: nose, dome back, notched fluke, belly.
Eye = paper ring + vermilion dot, rhyming with the octopus study.
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
d.new_doc("spot-whale", 1000, 1000)

# field + spot sun
d.shape("rect", "Paper", x=0, y=0, width=1000, height=1000, fill=PAPER)
d.shape("ellipse", "Spot", x=215, y=175, width=570, height=570, fill=SPOT)

# bubbles, top-left
for i, (x, y, r) in enumerate([(150, 205, 30), (222, 138, 16)]):
    d.shape("ellipse", f"Bubble {i}", x=x - r, y=y - r, width=2 * r, height=2 * r,
            fill="none", stroke=BODY, strokeWidth=2.5)

# whale: one closed silhouette — nose right, dome back, fluke left
d.path("M835 470 "
       "C835 408 758 322 520 318 "
       "C400 316 300 360 262 445 "
       "C230 420 160 390 128 380 "
       "C136 412 160 448 190 468 "
       "C160 488 142 516 135 545 "
       "C170 538 225 522 265 505 "
       "C300 560 420 566 520 560 "
       "C650 552 780 530 835 470 Z",
       "Whale", fill=BODY)

# under-jaw: cream crescent along the belly front
d.path("M828 486 C760 532 640 552 520 556 C560 522 700 500 828 486 Z",
       "Jaw", fill=PAPER)

# eye: paper ring + vermilion dot
d.shape("ellipse", "Eye", x=716, y=402, width=52, height=52, fill=PAPER)
d.shape("ellipse", "Pupil", x=733, y=419, width=22, height=22, fill=SPOT)

# spout: three arcs from the blowhole
for i, dstr in enumerate([
        "M612 306 C612 268 616 244 624 218",
        "M588 312 C572 284 566 260 570 236",
        "M636 310 C652 284 658 262 654 238"]):
    d.path(dstr, f"Spout {i}", fill="none", stroke=BODY, strokeWidth=7, cap="round")
d.shape("ellipse", "Spout dot", x=614, y=196, width=18, height=18, fill=BODY)

# water: paper dashes under the belly on the spot, ink dashes on the paper
for i, (x0, y0, x1, y1) in enumerate([(408, 604, 476, 604), (506, 620, 588, 620),
                                      (614, 602, 668, 602)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Wave in {i}",
           fill="none", stroke=PAPER, strokeWidth=6, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(96, 706, 196, 706), (120, 742, 178, 742),
                                      (760, 724, 856, 724)]):
    d.path(f"M{x0} {y0} L{x1} {y1}", f"Wave out {i}",
           fill="none", stroke=BODY, strokeWidth=5, cap="round")

d.cmd("select.none")
d.call("save_file", {"path": f"{HERE}/spot-whale-V1R00.vectorcraft"}, "save native")
for fmt, path, scale in [("svg", f"{HERE}/spot-whale-V1R00.svg", None),
                         ("png", f"{HERE}/spot-whale-V1R00@2x.png", 2),
                         ("pdf", f"{OUT}/spot-whale-V1R00.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    d.call("export", args, f"export {fmt}")
print("SPOT WHALE DONE, calls:", d.count, "errors:", len(d.errors))
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])
