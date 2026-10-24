#!/usr/bin/env python3
"""False Rest Lantern — mascot portrait V1R00.
A lantern standing upright over quiet smoldering ruins, casting an
even amber glow. It arrives already lit; what it burns is not
recorded. A room still smoldering and a room actually resting return
the same reading inside its radius. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("False Rest Lantern — Mascot Portrait", 1000, 1000)

INK = "#332224"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241A20"}, {"offset": 1, "color": "#0E0A0C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5C4A4A"}, {"offset": 0.7, "color": "#3E3236"},
    {"offset": 1, "color": "#1D161A"}]}}
GLOW = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2B45E"}, {"offset": 0.55, "color": "#A8683C"},
    {"offset": 1, "color": "#4E3A3E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#463A38"}, {"offset": 1, "color": "#1A1216"}]}}
GLASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F8D68A"}, {"offset": 0.55, "color": "#EEA94E"},
    {"offset": 1, "color": "#C87A32"}]}}
FRAME = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C4638"}, {"offset": 1, "color": "#362820"}]}}
RUIN = "#241C20"
AMBER = "#F0B45C"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A7468", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D6C4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(206,238,7),(804,240,8),(164,530,8),(836,552,7),
                               (258,764,8),(744,752,7),(144,398,6),(856,402,7),
                               (400,118,7),(608,116,8),(342,822,6),(666,818,7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A3A3C", opacity=45, stroke=NONE)

# --- the even glow: it falls the same on the resting and the smoldering -----------
d.shape("ellipse", "Lantern glow", x=270, y=140, width=460, height=460,
        fill=GLOW, opacity=75, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0808",
       strokeWidth=4, opacity=70)
# the light pool on the ground, spread evenly
d.shape("ellipse", "Glow pool", x=330, y=676, width=340, height=44,
        fill=AMBER, opacity=22, stroke=NONE)

# --- the ruins, quiet at the edges --------------------------------------------------
# left: broken wall stub, jagged top
d.path("M206,700 L206,540 L238,522 L252,548 L278,530 L296,560 L320,548 "
       "L320,700 Z", "Wall stub L", fill=RUIN, stroke=INK, strokeWidth=5,
       join="round")
# right: collapsed column drum + tilted beam
d.shape("ellipse", "Column drum", x=660, y=620, width=96, height=60,
        fill=RUIN, stroke=INK, strokeWidth=5)
d.path("M664,624 L756,676", "Drum split", fill=NONE, stroke=INK,
       strokeWidth=3.5, opacity=70)
d.path("M700,700 L806,540 L830,556 L740,700 Z", "Fallen beam",
       fill="#2E2428", stroke=INK, strokeWidth=5, join="round")
# rubble scatter along the floor
for i, (x, y, w, h) in enumerate([(330,676,44,26),(392,684,30,18),(580,680,38,22),
                                  (628,690,26,14),(252,686,34,16),(770,684,36,18)]):
    d.shape("ellipse", f"Rubble {i+1}", x=x, y=y, width=w, height=h,
            fill=RUIN, stroke=INK, strokeWidth=3.5)
# embers still alive in the rubble — the same reading as rest
for i, (x, y, r) in enumerate([(352,684,4),(606,686,5),(786,690,4),
                               (276,692,3),(706,694,3)]):
    d.shape("ellipse", f"Ember {i+1}", x=x-r, y=y-r, width=2*r, height=2*r,
            fill=AMBER, opacity=75, stroke=NONE)
# thin smoke off the rubble, unhurried
d.path("M356,676 C344,640 364,616 352,586 C344,566 354,546 348,528",
       "Smoke 1", fill=NONE, stroke="#9A8A92", strokeWidth=4,
       cap="round", opacity=45)
d.path("M608,678 C622,646 602,622 616,594 C624,576 614,556 622,540",
       "Smoke 2", fill=NONE, stroke="#9A8A92", strokeWidth=4,
       cap="round", opacity=40)
d.path("M784,682 C776,652 794,632 784,604 C778,588 786,572 780,556",
       "Smoke 3", fill=NONE, stroke="#9A8A92", strokeWidth=3.5,
       cap="round", opacity=35)

# --- the lantern, standing on its slab at floor level --------------------------------
d.shape("ellipse", "Lantern shadow", x=430, y=688, width=140, height=24,
        fill="#060410", opacity=55, stroke=NONE)
# handle ring + bail — it was built to be held at a respectful distance
d.shape("ellipse", "Handle ring", x=486, y=330, width=28, height=28,
        fill=NONE, stroke=INK, strokeWidth=5)
d.path("M462,394 C458,350 542,350 538,394", "Bail", fill=NONE,
       stroke=INK, strokeWidth=5)
# chimney + cap
d.path("M474,394 L526,394 L530,414 L470,414 Z", "Chimney",
       fill=FRAME, stroke=INK, strokeWidth=4, join="round")
d.path("M446,414 L554,414 L560,430 L440,430 Z", "Cap",
       fill=FRAME, stroke=INK, strokeWidth=4, join="round")
# frame rails
d.shape("rectangle", "Top rail", x=444, y=430, width=112, height=14,
        radius=4, fill=FRAME, stroke=INK, strokeWidth=4)
# glass: the amber is specified, the fuel is not
d.shape("rectangle", "Glass", x=458, y=446, width=84, height=160,
        fill=GLASS, stroke=INK, strokeWidth=4)
# mullions
d.path("M486,446 L486,606 M514,446 L514,606 M458,510 L542,510 M458,562 L542,562",
       "Mullions", fill=NONE, stroke=INK, strokeWidth=3.5, opacity=75)
# the flame, mid-burn, already lit on arrival
d.shape("ellipse", "Flame glow", x=476, y=522, width=48, height=54,
        fill="#FCE9BC", opacity=42, stroke=NONE)
d.path("M500,570 C488,556 488,536 500,520 C512,536 512,556 500,570 Z",
       "Flame", fill="#FDF3D2", stroke=INK, strokeWidth=3)
d.path("M500,564 C495,556 495,546 500,538 C505,546 505,556 500,564 Z",
       "Flame core", fill="#FFFDF4", stroke=NONE)
# base + foot, held level over the rubble
d.shape("rectangle", "Base rail", x=444, y=606, width=112, height=16,
        radius=4, fill=FRAME, stroke=INK, strokeWidth=4)
d.path("M440,622 L560,622 L574,656 L426,656 Z", "Foot",
       fill=FRAME, stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Stand", x=480, y=656, width=40, height=26,
        fill=FRAME, stroke=INK, strokeWidth=4)
# standing slab under the stand — it has never once been lowered
d.shape("rectangle", "Slab", x=446, y=682, width=108, height=18,
        radius=4, fill="#3A2E2C", stroke=INK, strokeWidth=4)
d.path("M452,690 L470,690 M524,688 L546,690", "Slab cracks", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=60)

# --- captions ----------------------------------------------------------------------
d.text("FALSE REST LANTERN", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#F2E4CE", justify="center")
r = d.text("QUIET, MISREAD AS REST", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#D0AA82", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("242.false-rest-lantern-V1R00")
