#!/usr/bin/env python3
"""spot-whale V1R02 — the silhouette-code pass:
narrow tail stem ending in a horizontal fluke paddle (kills the fish read),
blunter forehead, small raked dorsal fin, spout moved to the blowhole above
the eye, shorter jaw crescent. Same style/palette/dressing as V1R01.
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
d.new_doc("spot-whale-v1r02", 1000, 1000)

d.shape("rect", "Paper", x=0, y=0, width=1000, height=1000, fill=PAPER)
d.shape("ellipse", "Spot", x=215, y=175, width=570, height=570, fill=SPOT)
for i, (x, y, r) in enumerate([(150, 205, 30), (222, 138, 16)]):
    d.shape("ellipse", f"Bubble {i}", x=x - r, y=y - r, width=2 * r, height=2 * r,
            fill="none", stroke=BODY, strokeWidth=2.5)

# whale: blunt head -> low back -> narrow tail stem -> horizontal fluke paddle
d.path("M846 448 "
       "C846 424 826 402 788 380 "          # blunt forehead drop
       "C720 342 640 326 540 326 "          # low, long back
       "C420 328 320 380 292 452 "          # into the tail stem (top)
       "C288 466 288 478 292 490 "          # stem back edge (narrow!)
       "C240 452 170 438 118 442 "          # fluke: upper lobe to the left
       "C150 462 172 472 180 478 "          # notch
       "C150 486 128 500 116 518 "          # lower lobe
       "C180 522 258 508 296 494 "          # fluke underside back to the stem
       "C330 552 430 582 540 576 "          # deep belly
       "C680 568 800 522 846 448 Z",
       "Whale", fill=BODY)

# raked dorsal fin on the ridge
d.path("M470 326 C486 298 514 286 544 292 C522 302 504 314 496 328 Z",
       "Dorsal", fill=BODY)

# short jaw crescent at the mouth corner only
d.path("M842 452 C810 486 762 510 706 524 C748 494 796 470 842 452 Z",
       "Jaw", fill=PAPER)

# eye + spout above it (blowhole at the head)
d.shape("ellipse", "Eye", x=730, y=396, width=50, height=50, fill=PAPER)
d.shape("ellipse", "Pupil", x=746, y=412, width=21, height=21, fill=SPOT)
for i, dstr in enumerate([
        "M742 348 C742 316 746 296 754 274",
        "M718 354 C702 330 696 310 700 290",
        "M766 352 C782 328 788 308 784 288"]):
    d.path(dstr, f"Spout {i}", fill="none", stroke=BODY, strokeWidth=7, cap="round")
d.shape("ellipse", "Spout dot", x=745, y=252, width=18, height=18, fill=BODY)

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
d.call("save_file", {"path": f"{HERE}/spot-whale-V1R02.vectorcraft"}, "save native")
for fmt, path, scale in [("svg", f"{HERE}/spot-whale-V1R02.svg", None),
                         ("png", f"{HERE}/spot-whale-V1R02@2x.png", 2),
                         ("pdf", f"{OUT}/spot-whale-V1R02.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale:
        args["scale"] = scale
    d.call("export", args, f"export {fmt}")
print("SPOT WHALE V1R02 DONE, calls:", d.count, "errors:", len(d.errors))
for lbl, e in d.errors:
    print(" -", lbl, ":", e[:200])
