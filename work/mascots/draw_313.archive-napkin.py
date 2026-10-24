#!/usr/bin/env python3
"""Archive Napkin — mascot portrait V1R00.
The nearest medium for the duration of the outage, and the record ever
since: a wrinkled cocktail napkin, the ballpoint diagram smeared where the
grease took first, kept exactly as found. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Archive Napkin — Mascot Portrait", 1000, 1000)

INK = "#2A2016"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#181109"}, {"offset": 1, "color": "#0D0905"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7C6444"}, {"offset": 0.7, "color": "#4E3E2A"},
    {"offset": 1, "color": "#2A2014"}]}}
NAPKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2ECDA"}, {"offset": 0.7, "color": "#D9CFB2"},
    {"offset": 1, "color": "#B0A488"}]}}
UNDER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C4B898"}, {"offset": 1, "color": "#8E8268"}]}}
INK_BP = "#3A56A0"      # ballpoint blue
GREASE = "#8A6A3C"
GLASS = "#E8E2CE"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A704C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2D4B4", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(202,240,8),(794,238,7),(166,536,9),(832,552,8),
                               (254,762,7),(746,748,9),(144,400,6),(854,398,7),
                               (400,118,7),(606,116,8),(340,820,6),(662,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5C4A34", opacity=45, stroke=NONE)

# --- the napkin: stored as it was found -----------------------------------------
# cast shadow, heavier where the wrinkles lift the cloth
d.shape("ellipse", "Napkin shadow", x=270, y=640, width=470, height=90,
        fill="#140D08", opacity=50, stroke=NONE)
# body: a square gone soft — wavy edges, no corner true
d.path("M306,296 C390,286 470,302 556,296 C616,292 662,304 702,318 "
       "C710,382 700,446 706,522 C710,592 696,652 682,700 "
       "C604,708 542,694 472,702 C402,708 338,686 290,662 "
       "C282,582 296,502 288,432 C284,372 296,330 306,296 Z",
       "Napkin", fill=NAPKIN_GRAD, stroke=INK, strokeWidth=5,
       join="round")
# the curled corner: top-right lifts, showing the underside
d.path("M702,318 C676,322 652,332 638,350 C660,352 686,344 706,330 Z",
       "Corner curl", fill=UNDER_GRAD, stroke=INK, strokeWidth=4,
       join="round")
d.path("M638,350 C660,340 688,332 706,330", "Curl shadow", fill=NONE,
       stroke="#7A6E52", strokeWidth=3, opacity=60, cap="round")
# creases: the wrinkles are part of the provenance
for i, (p) in enumerate([
        "M340,330 C400,400 460,480 520,560",
        "M660,360 C580,420 500,470 400,540",
        "M330,560 C420,560 520,590 640,640",
        "M470,310 C480,380 470,470 490,540"]):
    d.path(p, f"Crease {i+1}", fill=NONE, stroke="#9C8F70",
           strokeWidth=3, opacity=55, cap="round")
# fold shading: the hollows read darker
d.path("M340,330 C400,400 460,480 520,560 L540,580 C470,500 400,410 330,340 Z",
       "Crease shade 1", fill="#8E8268", opacity=22, stroke=NONE)
d.path("M400,540 C500,470 580,420 660,360 L668,380 C590,440 510,490 414,552 Z",
       "Crease shade 2", fill="#8E8268", opacity=18, stroke=NONE)
# lift highlights along the ridge sides
d.path("M352,322 C410,392 468,470 528,548", "Crease light 1", fill=NONE,
       stroke="#FBF6E8", strokeWidth=4, opacity=50, cap="round")

# --- the grease: it was there before the diagram ----------------------------------
# the ring — provenance, not a stain
d.shape("ellipse", "Grease ring", x=352, y=330, width=150, height=140,
        fill=NONE, stroke=GREASE, strokeWidth=14, opacity=32)
d.shape("ellipse", "Grease ring core", x=370, y=348, width=114, height=104,
        fill=NONE, stroke=GREASE, strokeWidth=5, opacity=22)
# the damp corner: darker, ballpoint skipped here
d.path("M560,640 C600,660 640,676 682,700 C630,706 570,700 530,690 "
       "C540,672 550,656 560,640 Z", "Damp corner", fill="#7A6E52",
       opacity=30, stroke=NONE)
# small blots of the same weather
for i, (x, y, w) in enumerate([(560,300,26),(330,560,18),(620,540,20)]):
    d.shape("ellipse", f"Blot {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill=GREASE, opacity=16, stroke=NONE)

# --- the ballpoint diagram: a structure drawn while it collapsed -------------------
# box 1: the registry, upper right of the ring
d.path("M480,396 L560,392 L564,436 L484,440 Z", "Box registry",
       fill=NONE, stroke=INK_BP, strokeWidth=4, join="round")
# box 2: the mirror, lower left
d.path("M370,540 L448,546 L442,592 L364,586 Z", "Box mirror",
       fill=NONE, stroke=INK_BP, strokeWidth=4, join="round")
# box 3: the replica, lower right, begun before the ink gave
d.path("M530,560 L606,554 L612,596 L536,604 Z", "Box replica",
       fill=NONE, stroke=INK_BP, strokeWidth=4, join="round")
# arrows: registry feeding both — the collapse mapped in real time
d.path("M492,442 C470,470 446,500 424,540 M424,540 L434,520 M424,540 L404,532",
       "Arrow L", fill=NONE, stroke=INK_BP, strokeWidth=3.5,
       cap="round")
d.path("M548,442 C560,480 572,520 580,556 M580,556 L578,534 M580,556 L560,548",
       "Arrow R", fill=NONE, stroke=INK_BP, strokeWidth=3.5,
       cap="round")
d.path("M446,570 C470,576 500,574 528,570", "Arrow between", fill=NONE,
       stroke=INK_BP, strokeWidth=3, cap="round")
# hurried labels — ballpoint shorthand, all witness
d.text("DB", "Label registry", x=522, y=424, size=16, font="Source Sans 3",
       color=INK_BP, justify="center")
d.text("BAK", "Label mirror", x=404, y=572, size=15, font="Source Sans 3",
       color=INK_BP, justify="center")
d.text("NEW", "Label replica", x=572, y=586, size=15, font="Source Sans 3",
       color=INK_BP, justify="center")
# the smear: drawn fast, the heel of a hand across wet ink
for i, (x, y, w) in enumerate([(450,470,90),(420,520,70),(560,470,60),
                               (380,610,80),(540,620,60)]):
    d.shape("ellipse", f"Smear {i+1}", x=x, y=y, width=w, height=w*0.35,
            fill=INK_BP, opacity=20, stroke=NONE)
# drag streaks: ink pulled sideways before it dried
d.path("M470,436 C510,450 550,448 586,458", "Drag streak 1", fill=NONE,
       stroke=INK_BP, strokeWidth=7, opacity=20, cap="round")
d.path("M380,560 C420,574 470,572 516,580", "Drag streak 2", fill=NONE,
       stroke=INK_BP, strokeWidth=6, opacity=18, cap="round")
d.path("M540,548 C572,558 600,556 622,564", "Drag streak 3", fill=NONE,
       stroke=INK_BP, strokeWidth=5, opacity=18, cap="round")
# skip strokes where the grease won: the pen stuttered through the ring
d.path("M380,400 L404,430 M412,432 L418,438", "Skip stroke 1",
       fill=NONE, stroke=INK_BP, strokeWidth=2.5, cap="round",
       opacity=55)
# the last word of the outage, scrawled at the rim
d.text("IT WAS WHAT WAS NEAREST", "Margin note", x=500, y=668, size=11,
       font="Source Sans 3", color=INK_BP, justify="center")

# --- the glass that made the ring, kept in evidence --------------------------------
# a faint coupe at the right rim, more memory than object
d.shape("ellipse", "Glass shadow", x=712, y=706, width=90, height=16,
        fill="#140D08", opacity=45, stroke=NONE)
d.path("M726,640 C726,668 740,684 756,686 L754,704 L782,704 L780,686 "
       "C796,684 810,668 810,640 Z", "Coupe bowl", fill=NONE,
       stroke=GLASS, strokeWidth=4, opacity=55, join="round")
d.shape("ellipse", "Coupe rim", x=724, y=632, width=88, height=14,
        fill=NONE, stroke=GLASS, strokeWidth=3.5, opacity=55)
d.path("M730,652 C740,664 796,664 806,652", "Coupe meniscus",
       fill=NONE, stroke="#C9A45C", strokeWidth=3, opacity=45,
       cap="round")

# --- dim bar motes ------------------------------------------------------------------
for i, (x, y, w) in enumerate([(300,240,5),(380,220,4),(560,210,5),(660,250,4),
                               (240,460,4),(740,470,5),(200,560,5),(780,580,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E2D4B4", opacity=28, stroke=NONE)

# --- captions ---------------------------------------------------------------------
d.text("ARCHIVE NAPKIN", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EDE4CC", justify="center")
r = d.text("WITNESS BEFORE PERMISSION", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C4A87C", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("313.archive-napkin-V1R00")
