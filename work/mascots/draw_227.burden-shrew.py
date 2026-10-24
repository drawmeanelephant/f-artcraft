#!/usr/bin/env python3
"""Burden Shrew — mascot portrait V1R00. mascots/M-0227.
Shrew mascot carrying heavy boxes down into a floor stairwell. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Burden Shrew — Mascot Portrait", 1000, 1000)

INK = "#2E2126"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1524"}, {"offset": 1, "color": "#0A0812"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C7B79E"}, {"offset": 0.7, "color": "#8B7C82"},
    {"offset": 1, "color": "#4C4656"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A8907E"}, {"offset": 0.7, "color": "#7A6257"},
    {"offset": 1, "color": "#55423D"}]}}
BOX_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D0AC7C"}, {"offset": 1, "color": "#9A784E"}]}}
VOID_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#332B44"}, {"offset": 1, "color": "#0C0A14"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5A5266", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4DACA", strokeWidth=3, opacity=55)
# dust motes hanging in the cellar air
for i, (x, y, r) in enumerate([(270,300,5),(700,260,4),(360,200,4),(640,180,5),
                               (500,150,3),(220,470,4),(790,460,4),(300,560,3)]):
    d.shape("ellipse", f"Mote {i+1}", x=x-r, y=y-r, width=2*r, height=2*r,
            fill="#EFE6D4", opacity=35, stroke=NONE)

# --- floor: the reporting floor's underside, ends on the disc's own arc --------
d.path("M196,748 C320,738 680,738 804,748 A420,420 0 0 1 196,748 Z",
       "Floor", fill="#6E5F56", opacity=60, stroke=NONE)
d.path("M196,748 C320,738 680,738 804,748", "Floor edge",
       fill=NONE, stroke="#3E3440", strokeWidth=4, opacity=70, cap="round")

# --- the stairwell: a dark mouth in the floor, steps dropping away --------------
# warm spill pooled at the lip of the opening
d.shape("ellipse", "Lip glow", x=380, y=742, width=300, height=56,
        fill="#E8B878", opacity=30, stroke=NONE)
# opening, perspective trapezoid — wide enough that she is visibly squeezing in
d.path("M410,756 L650,756 L610,845 L460,845 Z", "Stairwell mouth",
       fill=VOID_GRAD, stroke=INK, strokeWidth=5, join="round")
# descending step edges inside the shaft, fainter with depth
d.path("M430,772 L628,772", "Step edge 1", fill=NONE, stroke="#9A8468",
       strokeWidth=4, opacity=75, cap="round")
d.path("M445,792 L615,792", "Step edge 2", fill=NONE, stroke="#8A7458",
       strokeWidth=4, opacity=55, cap="round")
d.path("M460,812 L598,812", "Step edge 3", fill=NONE, stroke="#7A6448",
       strokeWidth=4, opacity=38, cap="round")
d.path("M475,830 L580,830", "Step edge 4", fill=NONE, stroke="#6A5438",
       strokeWidth=4, opacity=22, cap="round")

# --- the shrew, hunched at the lip under her stack -------------------------------
d.shape("ellipse", "Shrew shadow", x=368, y=742, width=180, height=22,
        fill="#3A3040", opacity=45, stroke=NONE)
# tail dragging behind onto the floor
d.path("M384,700 C344,712 320,730 306,752 C300,762 292,768 282,770",
       "Tail", fill=NONE, stroke="#6B5049", strokeWidth=10, cap="round")
# body: low slung, nose down toward the dark
d.path("M388,706 C376,636 402,576 452,556 C492,540 540,548 566,584 "
       "C584,608 588,646 578,684 C572,708 560,724 544,734 "
       "L430,734 C410,726 394,716 388,706 Z",
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=6, join="round")
# belly shade
d.path("M430,700 C460,714 520,714 552,694 C546,716 532,728 514,732 L446,732 "
       "C438,724 432,714 430,700 Z", "Belly shade", fill="#4E3E3A",
       opacity=45, stroke=NONE)
# haunch fold
d.path("M420,620 C412,656 414,692 428,720", "Haunch fold",
       fill=NONE, stroke="#4A3A36", strokeWidth=6, opacity=40, cap="round")
# head: pointed snout dipped toward the opening
d.path("M540,560 C576,548 616,556 640,584 C652,598 662,616 668,636 "
       "C678,646 686,656 688,666 C680,674 668,680 654,682 "
       "C640,690 622,694 604,692 C572,688 550,668 542,640 "
       "C536,616 534,584 540,560 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=6, join="round")
# snout taper
d.path("M612,640 C644,646 672,656 688,666 C680,674 668,680 654,682 "
       "C640,690 622,694 604,692 Z",
       "Snout shade", fill="#4E3E3A", opacity=40, stroke=NONE)
# nose tip
d.shape("ellipse", "Nose", x=676, y=658, width=18, height=14,
        fill="#3A2A2E", stroke=INK, strokeWidth=3)
# whiskers, dropping with her gaze
d.path("M670,646 C692,642 710,644 724,650 M668,660 C688,662 704,668 716,676",
       "Whiskers", fill=NONE, stroke="#3E3030", strokeWidth=3,
       opacity=70, cap="round")
# ear: small rounded, tucked under the load
d.path("M548,556 C544,532 556,514 578,512 C596,510 608,522 608,540 "
       "C594,548 570,554 548,556 Z", "Ear", fill="#8A6E60",
       stroke=INK, strokeWidth=5, join="round")
d.path("M560,548 C558,534 566,524 580,522", "Ear inner",
       fill=NONE, stroke="#4A3A36", strokeWidth=4, opacity=60, cap="round")
# eye: small, tired, watching the dark
d.shape("ellipse", "Eye", x=606, y=606, width=14, height=14,
        fill="#241A1E", stroke=NONE)
d.shape("ellipse", "Eye glint", x=609, y=608, width=4, height=4,
        fill="#E8DCC8", opacity=85, stroke=NONE)
# foreleg reaching down into the dark, paw finding the first step
d.path("M560,700 C556,724 548,750 536,772", "Foreleg",
       fill=NONE, stroke="#6B5049", strokeWidth=18, cap="round")
d.shape("ellipse", "Forepaw", x=520, y=766, width=26, height=16,
        fill="#8A6E60", stroke=INK, strokeWidth=4)
# hind foot planted on the floor behind
d.shape("ellipse", "Hind foot", x=394, y=722, width=44, height=18,
        fill="#8A6E60", stroke=INK, strokeWidth=4)

# --- the stack of boxes on her back, teetering slightly --------------------------
# bottom box, widest, settled into the fur
d.path("M368,528 L596,516 L604,600 L376,614 Z", "Box 1",
       fill=BOX_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M480,522 L488,606", "Box1 tape", fill=NONE, stroke="#7A5C3A",
       strokeWidth=8, opacity=60)
d.path("M386,560 L460,556", "Box1 rule", fill=NONE, stroke="#7A5C3A",
       strokeWidth=4, opacity=50, cap="round")
# middle box, tilted the other way
d.path("M398,438 L578,450 L570,522 L390,510 Z", "Box 2",
       fill=BOX_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M482,442 L476,516", "Box2 tape", fill=NONE, stroke="#7A5C3A",
       strokeWidth=8, opacity=60)
# manifest label on box 2
d.path("M508,466 L556,470 L552,500 L504,496 Z", "Box2 label",
       fill="#F0E6D0", stroke=INK, strokeWidth=3)
d.path("M512,476 L546,478 M511,486 L540,488", "Label rules",
       fill=NONE, stroke="#8A7E66", strokeWidth=3, opacity=80)
# top box, smallest, tipping furthest — the last straw made literal
d.path("M430,358 L560,344 L572,426 L440,440 Z", "Box 3",
       fill=BOX_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M492,352 L502,432", "Box3 tape", fill=NONE, stroke="#7A5C3A",
       strokeWidth=8, opacity=60)
d.path("M448,388 L478,384", "Box3 rule", fill=NONE, stroke="#7A5C3A",
       strokeWidth=4, opacity=50, cap="round")
# fur squashed flat where the stack sits
d.path("M392,540 C440,524 540,518 588,528", "Load line",
       fill=NONE, stroke="#4A3A36", strokeWidth=5, opacity=55, cap="round")
# strain ticks either side of the stack — nothing carried back up
d.path("M354,486 L338,478 M350,520 L332,518 M620,470 L638,460 M626,504 L644,500",
       "Strain ticks", fill=NONE, stroke=INK, strokeWidth=4,
       opacity=55, cap="round")

# --- name + role ------------------------------------------------------------------
d.text("BURDEN SHREW", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E2D8C8", justify="center")
d.text(" ".join("CARRIES ONLY DOWNWARD"), "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#A89C92", justify="center")

d.finish("227.burden-shrew-V1R00")
