#!/usr/bin/env python3
"""Jarlabel Stranger — mascot portrait V1R00.
A hooded stranger carrying a jar of mismatched labels and a PDF labeled
text/plain. 1000x1000. Gradients + translucency, never flat."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jarlabel Stranger — Mascot Portrait", 1000, 1000)

INK = "#2E2634"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161020"}, {"offset": 1, "color": "#080510"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9A90B4"}, {"offset": 0.7, "color": "#6A608A"},
    {"offset": 1, "color": "#3B3552"}]}}
COAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C5278"}, {"offset": 1, "color": "#342E48"}]}}
FACE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EFD2B0"}, {"offset": 1, "color": "#C09A72"}]}}
GLASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8EFEF"}, {"offset": 1, "color": "#9AC4C6"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4F0E4"}, {"offset": 1, "color": "#D8D2BC"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#766C98", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2DCEE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(205,230,8),(792,236,7),(170,536,9),(822,556,8),
                               (255,750,7),(745,744,9),(145,396,6),(852,408,7),
                               (398,116,7),(602,114,8),(340,812,6),(660,810,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#554C74", opacity=45, stroke=NONE)

# ground shadow
d.shape("ellipse", "Ground shadow", x=310, y=742, width=380, height=42,
        fill="#241F36", opacity=60, stroke=NONE)

# --- the stranger: hooded coat --------------------------------------------------
d.path("M500,368 C575,368 630,430 640,520 C648,610 636,700 622,752 "
       "L378,752 C364,700 352,610 360,520 C370,430 425,368 500,368 Z",
       "Coat", fill=COAT, stroke=INK, strokeWidth=7)
# coat lapels / front opening
d.path("M470,470 L500,752 M530,470 L505,752", "Coat front", fill=NONE,
       stroke="#241F36", strokeWidth=5, opacity=70)
# hood: big cowl over the head
d.path("M500,296 C580,296 636,352 640,420 C642,468 610,500 560,512 "
       "C575,470 575,440 560,420 C540,395 460,395 440,420 C425,440 425,470 440,512 "
       "C390,500 358,468 360,420 C364,352 420,296 500,296 Z",
       "Hood", fill=COAT, stroke=INK, strokeWidth=7, join="round")
d.path("M440,420 C460,395 540,395 560,420 C575,440 575,470 560,512 "
       "C540,520 460,520 440,512 C425,470 425,440 440,420 Z",
       "Face", fill=FACE, stroke=INK, strokeWidth=5)
# hood shadow band over the eyes
d.path("M440,420 C460,395 540,395 560,420 C566,428 570,440 572,452 "
       "C540,440 460,440 428,452 C430,440 434,428 440,420 Z",
       "Hood shadow", fill="#3A3252", opacity=60, stroke=NONE)
# eyes — watchful
d.shape("ellipse", "Eye L", x=462, y=452, width=22, height=26, fill="#FBF6E8",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=516, y=452, width=22, height=26, fill="#FBF6E8",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=468, y=460, width=10, height=12, fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=522, y=460, width=10, height=12, fill=INK, stroke=NONE)
d.path("M478,496 C488,502 512,502 522,496", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")

# --- the jar of mismatched labels, cradled left ---------------------------------
# labels inside the jar (drawn first; the glass goes over them)
labels = [(392,566,58,26,-8,"URGENT"),(448,584,52,24,10,"misc"),
          (386,616,54,24,6,"IO-422"),(446,636,56,24,-7,"??"),
          (398,664,58,22,4,"FRAGILE")]
for i, (x, y, w, h, t, txt) in enumerate(labels):
    import math
    th = math.radians(t); c, s = math.cos(th), math.sin(th)
    cx, cy = x + w/2, y + h/2
    pts = []
    for dx, dy in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]:
        pts.append((cx+dx*c-dy*s, cy+dx*s+dy*c))
    dd = "M" + " L".join(f"{p[0]:.0f},{p[1]:.0f}" for p in pts) + " Z"
    d.path(dd, f"Label {i+1}", fill=PAPER, stroke=INK, strokeWidth=2.5)
    d.text(txt, f"Label txt {i+1}", x=cx, y=cy+4, size=9, font="Virelai Sans",
           color="#6E5844", justify="center")
d.path("M380,540 C360,560 356,600 364,640 C372,686 400,712 445,712 "
       "C490,712 516,686 524,640 C532,600 528,560 508,540 Z",
       "Jar glass", fill=GLASS, stroke=INK, strokeWidth=6, opacity=45)
# glass shine + lid
d.shape("ellipse", "Jar shine", x=374, y=560, width=30, height=110,
        fill="#FFFFFF", opacity=30, stroke=NONE)
d.path("M372,540 L522,540 L516,512 L378,512 Z", "Jar lid", fill="#8A6A44",
       stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Lid knob", x=432, y=498, width=26, height=18, fill="#8A6A44",
        stroke=INK, strokeWidth=4)
# left arm cradling the jar
d.path("M380,560 C350,585 340,620 348,655 C354,680 366,695 382,700",
       "Arm L", fill=NONE, stroke=COAT, strokeWidth=26, cap="round")
d.shape("ellipse", "Hand L", x=372, y=688, width=28, height=24, fill=FACE,
        stroke=INK, strokeWidth=5)

# --- the PDF labeled text/plain, held up right ----------------------------------
d.path("M616,520 L748,548 L728,676 L596,648 Z", "PDF sheet", fill=PAPER,
       stroke=INK, strokeWidth=5, join="round")
# dog-eared corner
d.path("M748,548 L726,540 L744,570 Z", "PDF fold", fill="#CFC8B0",
       stroke=INK, strokeWidth=3, join="round")
# header band "PDF"
d.path("M624,536 L716,556 L710,584 L618,564 Z", "PDF band", fill="#9A4A42",
       stroke=NONE, opacity=90)
r2 = d.text("PDF", "PDF head", x=668, y=566, size=20, font="Virelai Sans",
            color="#F4F0E4", justify="center")
if r2 and r2.get("id"):
    d.cmd("text.setStyle", "pdf track", ids=[r2["id"]], tracking=80)
# body text lines on the sheet
for i in range(4):
    d.path(f"M612,{592+i*16} L{700-i*6},{612+i*16}", f"PDF line {i+1}",
           fill=NONE, stroke="#A89E84", strokeWidth=5, cap="round", opacity=80)
# the mislabel stamp: text/plain
d.shape("rectangle", "Mime stamp", x=620, y=624, width=92, height=28,
        fill=NONE, stroke="#B43A32", strokeWidth=3, opacity=90, radius=3)
d.text("text/plain", "Mime word", x=666, y=645, size=14, font="Virelai Sans",
       color="#B43A32", justify="center")
# right hand on the sheet
d.path("M610,560 C595,585 592,610 600,634", "Arm R", fill=NONE, stroke=COAT,
       strokeWidth=26, cap="round")
d.shape("ellipse", "Hand R", x=590, y=622, width=28, height=24, fill=FACE,
        stroke=INK, strokeWidth=5)

# --- captions ------------------------------------------------------------------
d.text("JARLABEL STRANGER", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E2DCEE", justify="center")
r = d.text("COURIER OF MISFILED MIME", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A89CC8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("415.jarlabel-stranger-V1R00")
