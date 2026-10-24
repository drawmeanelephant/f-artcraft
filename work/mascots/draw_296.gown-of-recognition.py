#!/usr/bin/env python3
"""Gown of Recognition — mascot portrait V1R00.
A stub pulled from the queue and stood on a pedestal: thick ceremonial
gown, sleeves pinned so the wearer cannot point, the bright sash withheld
and folded on the plinth until the workflow beneath is standardized.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Gown of Recognition — Mascot Portrait", 1000, 1000)

INK = "#2E2028"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161020"}, {"offset": 1, "color": "#080610"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#443A56"}, {"offset": 0.7, "color": "#262034"},
    {"offset": 1, "color": "#131018"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C2436"}, {"offset": 1, "color": "#12101A"}]}}
GOWN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#84384A"}, {"offset": 0.6, "color": "#5C2534"},
    {"offset": 1, "color": "#3C1622"}]}}
GOWN_DARK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#66293A"}, {"offset": 1, "color": "#3A1522"}]}}
GOLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8B45E"}, {"offset": 1, "color": "#9A7434"}]}}
STONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E6678"}, {"offset": 1, "color": "#3C3646"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0DEC8"}, {"offset": 0.7, "color": "#D4BC9C"},
    {"offset": 1, "color": "#AC8F6E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A7A9E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFC4E0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#423A52", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0A12",
       strokeWidth=4, opacity=70)

# --- queue stanchions: the line it was pulled out of ---------------------------------------------
for i, cx in enumerate([250, 750]):
    d.shape("ellipse", f"Post base {i+1}", x=cx-22, y=686, width=44,
            height=12, fill="#6E5A30", stroke=INK, strokeWidth=3)
    d.path(f"M{cx},{686} L{cx},{590}", f"Post {i+1}", fill=NONE,
           stroke="#B08A44", strokeWidth=7, cap="round")
    d.shape("ellipse", f"Post knob {i+1}", x=cx-9, y=574, width=18,
            height=18, fill="#D8B45E", stroke=INK, strokeWidth=3)
# the velvet rope, sagging to where the pedestal interrupts it
d.path("M250,592 C310,632 340,636 366,616", "Rope L", fill=NONE,
       stroke="#84384A", strokeWidth=8, cap="round", opacity=90)
d.path("M750,592 C690,632 660,636 634,616", "Rope R", fill=NONE,
       stroke="#84384A", strokeWidth=8, cap="round", opacity=90)

# --- the pedestal ------------------------------------------------------------------
d.shape("ellipse", "Pedestal shadow", x=330, y=676, width=340, height=26,
        fill="#060408", opacity=55, stroke=NONE)
d.shape("rectangle", "Pedestal base", x=356, y=668, width=288, height=34,
        fill=STONE, stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Pedestal shaft", x=398, y=606, width=204, height=66,
        fill=STONE, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Pedestal top slab", x=366, y=586, width=268, height=24,
        fill=STONE, stroke=INK, strokeWidth=5, radius=6)
# engraved plaque, kept carefully blank of actionable detail
d.shape("rectangle", "Plaque", x=452, y=624, width=96, height=34,
        fill=GOLD, stroke=INK, strokeWidth=3, radius=5)
d.path("M466,638 L534,638 M472,648 L528,648", "Plaque engraving",
       fill=NONE, stroke="#7A5A24", strokeWidth=2.5, opacity=80)

# --- the trailing hem, pooling over the slab -------------------------------------------
d.path("M382,556 C344,566 322,580 330,594 L396,594 C388,578 388,566 382,556 Z",
       "Train pool L", fill=GOWN_DARK, stroke=INK, strokeWidth=4)
d.path("M618,560 C650,570 668,582 662,594 L606,594 C614,578 612,568 618,560 Z",
       "Train pool R", fill=GOWN_DARK, stroke=INK, strokeWidth=4)

# --- the gown --------------------------------------------------------------------------
d.path("M430,346 C420,420 400,500 380,596 L620,596 C600,500 580,420 570,346 "
       "C540,332 460,332 430,346 Z", "Gown", fill=GOWN, stroke=INK,
       strokeWidth=6, join="round")
# weight of the fabric: vertical fold shading
for i, (x, o) in enumerate([(452,30),(500,26),(548,30)]):
    d.path(f"M{x},360 C{x-12},450 {x-16},520 {x-22},590",
           f"Fold shade {i+1}", fill=NONE, stroke="#2A0E18",
           strokeWidth=10, cap="round", opacity=o)
d.path("M470,350 C462,450 458,520 452,590", "Fold light L", fill=NONE,
       stroke="#A8566A", strokeWidth=8, cap="round", opacity=30)
d.path("M532,350 C540,450 544,520 550,590", "Fold light R", fill=NONE,
       stroke="#A8566A", strokeWidth=8, cap="round", opacity=30)
# gold hem band with bead trim
d.path("M380,596 L620,596 L616,570 L384,570 Z", "Hem band",
       fill=GOLD, stroke=INK, strokeWidth=4)
for i, x in enumerate(range(398, 620, 32)):
    d.shape("ellipse", f"Hem bead {i+1}", x=x, y=578, width=9, height=9,
            fill="#6E4E1E", opacity=80, stroke=NONE)

# --- sleeves, pinned closed against the body ----------------------------------------------
# left sleeve stub folded inward
d.path("M436,368 C408,392 402,430 414,470 C424,492 448,496 462,482 "
       "C452,444 452,404 436,368 Z", "Sleeve L", fill=GOWN_DARK,
       stroke=INK, strokeWidth=5)
# right sleeve stub folded inward
d.path("M564,368 C592,392 598,430 586,470 C576,492 552,496 538,482 "
       "C548,444 548,404 564,368 Z", "Sleeve R", fill=GOWN_DARK,
       stroke=INK, strokeWidth=5)
# the pins that keep them from pointing
for i, (cx, cy) in enumerate([(446,462),(554,462)]):
    d.shape("ellipse", f"Pin head {i+1}", x=cx-8, y=cy-24, width=16,
            height=16, fill="#D8B45E", stroke=INK, strokeWidth=3)
    d.path(f"M{cx},{cy-8} L{cx},{cy+26}", f"Pin shaft {i+1}", fill=NONE,
           stroke="#D8B45E", strokeWidth=3.5, cap="round")
    d.path(f"M{cx-6},{cy+26} L{cx+6},{cy+26}", f"Pin tip {i+1}", fill=NONE,
           stroke="#D8B45E", strokeWidth=3.5, cap="round")

# --- the withheld sash: only its anchor loops remain ---------------------------------------
d.path("M556,376 L430,548", "Sash ghost", fill=NONE, stroke="#D8B45E",
       strokeWidth=10, dash=[4,14], cap="round", opacity=35)
for i, (x, y) in enumerate([(534,402),(498,448),(462,494)]):
    d.shape("ellipse", f"Sash loop {i+1}", x=x-6, y=y-6, width=12, height=12,
            fill=NONE, stroke="#D8B45E", strokeWidth=3, opacity=75)
# the sash itself, folded and out of reach on the plinth
d.shape("rectangle", "Sash folded", x=374, y=562, width=58, height=22,
        fill=GOLD, stroke=INK, strokeWidth=3.5, radius=8)
d.path("M378,573 L428,573", "Sash crease", fill=NONE, stroke="#8A6428",
       strokeWidth=2.5, opacity=80)
d.path("M386,584 L380,596 M398,584 L394,596 M410,584 L410,596",
       "Sash fringe", fill=NONE, stroke="#D8B45E", strokeWidth=3,
       cap="round", opacity=85)

# --- the high ceremonial collar -------------------------------------------------------------
d.path("M444,344 C430,300 452,272 500,266 C548,272 570,300 556,344 "
       "C530,330 470,330 444,344 Z", "Collar", fill=GOWN_DARK,
       stroke=INK, strokeWidth=5)
d.path("M444,344 C430,300 452,272 500,266 C548,272 570,300 556,344",
       "Collar trim", fill=NONE, stroke="#D8B45E", strokeWidth=4,
       opacity=90)

# --- the head: seen at last, wishing it weren't ----------------------------------------------
d.shape("ellipse", "Head", x=452, y=238, width=96, height=92,
        fill=SKIN, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Head sheen", x=470, y=248, width=42, height=20,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# half-lidded eyes: visibility without enthusiasm
d.shape("ellipse", "Eye L", x=472, y=286, width=15, height=15,
        fill="#2A1C18", stroke=NONE)
d.shape("ellipse", "Eye R", x=513, y=286, width=15, height=15,
        fill="#2A1C18", stroke=NONE)
d.path("M467,284 L492,284 M508,284 L533,284", "Lids", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M480,314 C492,318 508,318 520,314", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# the little ceremonial cap, pinned like everything else
d.path("M474,244 C478,222 522,222 526,244 C510,236 490,236 474,244 Z",
       "Cap", fill=GOLD, stroke=INK, strokeWidth=4, join="round")

# --- ceremonial dust motes ----------------------------------------------------------------------
for i, (x, y, w) in enumerate([(252,428,5),(306,300,6),(706,246,5),(782,470,6),
                               (232,634,5),(788,612,5),(380,240,5),(648,196,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#B8A6CE", opacity=35, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("GOWN OF RECOGNITION", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#E8DCEE", justify="center")
r = d.text("PERCEIVED, NOT RENDERED", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#BCA6CC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("296.gown-of-recognition-V1R00")
