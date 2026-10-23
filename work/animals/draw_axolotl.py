#!/usr/bin/env python3
"""Axolotl — field-guide plate V1R00. Head portrait, feathery external gills.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Axolotl — Field Plate", 1000, 1000)

INK = "#503139"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#123A40"}, {"offset": 1, "color": "#071A1E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C8EAE0"}, {"offset": 0.7, "color": "#9CCFC2"},
    {"offset": 1, "color": "#6FA79B"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FAD9DC"}, {"offset": 0.72, "color": "#EFB3BC"},
    {"offset": 1, "color": "#D98C99"}]}}
GILL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4687A"}, {"offset": 1, "color": "#B54356"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4F8A80", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2F4EC", strokeWidth=3, opacity=60)
# plate patina: soft blotches + speckles
d.shape("ellipse", "Patina 1", x=180, y=180, width=220, height=140, fill="#8FBFB2", opacity=25, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=640, width=260, height=150, fill="#8FBFB2", opacity=22, stroke=NONE)
for i, (x, y, w) in enumerate([(200,300,8),(760,240,7),(170,560,9),(800,560,8),(250,760,7),(730,740,9),
                               (130,420,6),(860,400,7),(400,120,7),(590,110,8),(330,830,6),(660,830,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#5F9386", opacity=40, stroke=NONE)
# rising bubbles, right side
for i, (x, y, w) in enumerate([(790,640,18),(815,560,12),(795,470,22),(830,390,14),(810,300,10)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w, fill="#FFFFFF", opacity=16, stroke=NONE)

# --- gills: stalk + computed filaments ----------------------------------------
def quad(p0, p1, p2, t):
    x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0]
    y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]
    tx = 2*(1-t)*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
    ty = 2*(1-t)*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
    return (x, y), (tx, ty)

def gill(stalk, label, sign):
    p0, p1, p2 = stalk
    d.path(f"M{p0[0]},{p0[1]} Q{p1[0]},{p1[1]} {p2[0]},{p2[1]}",
           f"{label} stalk", fill=NONE, stroke=GILL_GRAD, strokeWidth=15, cap="round")
    for j, t in enumerate([0.32, 0.5, 0.68, 0.85]):
        (x, y), (tx, ty) = quad(p0, p1, p2, t)
        import math
        ln = math.hypot(tx, ty) or 1
        nx, ny = -ty/ln*sign, tx/ln*sign
        L = 30 - j*4
        d.path(f"M{x:.0f},{y:.0f} L{x+nx*L:.0f},{y+ny*L:.0f}",
               f"{label} filament {j+1}", fill=NONE, stroke="#C8485C", strokeWidth=5, cap="round")

# left gills (sign=-1 fans filaments away from head)
gill([(332,480),(285,430),(252,372)], "Gill L1", -1)
gill([(318,540),(255,530),(196,498)],  "Gill L2", -1)
gill([(330,596),(270,624),(215,654)], "Gill L3", -1)
# right gills (mirror)
gill([(668,480),(715,430),(748,372)], "Gill R1", 1)
gill([(682,540),(745,530),(804,498)], "Gill R2", 1)
gill([(670,596),(730,624),(785,654)], "Gill R3", 1)
# gill base covers where stalks meet the head
d.shape("ellipse", "Gill base L", x=298, y=470, width=52, height=140, fill="#D98C99", stroke=NONE)
d.shape("ellipse", "Gill base R", x=650, y=470, width=52, height=140, fill="#D98C99", stroke=NONE)

# --- head ----------------------------------------------------------------------
d.path("M500,378 C622,378 700,448 702,545 C704,622 636,664 500,664 "
       "C364,664 296,622 298,545 C300,448 378,378 500,378 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
# head top highlight + chin shadow
d.shape("ellipse", "Head highlight", x=380, y=392, width=240, height=70, fill="#FFFFFF", opacity=14, stroke=NONE)
d.path("M380,632 C440,654 560,654 620,632 C560,644 440,644 380,632 Z",
       "Chin shadow", fill="#C97E8C", opacity=40, stroke=NONE)
# speckles
for i, (x, y, w) in enumerate([(385,445,7),(455,415,6),(560,418,7),(620,455,6),(365,560,6),(640,555,7),(500,430,5)]):
    d.shape("ellipse", f"Speckle {i+1}", x=x, y=y, width=w, height=w, fill="#B97F8C", opacity=55, stroke=NONE)

# --- face -----------------------------------------------------------------------
d.shape("ellipse", "Eye L", x=390, y=505, width=26, height=32, fill="#33222A", stroke=NONE)
d.shape("ellipse", "Eye R", x=584, y=505, width=26, height=32, fill="#33222A", stroke=NONE)
d.shape("ellipse", "Glint L", x=396, y=511, width=7, height=7, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=590, y=511, width=7, height=7, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Nostril L", x=458, y=582, width=9, height=7, fill="#8A5560", opacity=70, stroke=NONE)
d.shape("ellipse", "Nostril R", x=533, y=582, width=9, height=7, fill="#8A5560", opacity=70, stroke=NONE)
# the smile
d.path("M402,598 C448,622 552,622 598,598", "Smile", fill=NONE, stroke=INK, strokeWidth=8, cap="round")

# --- name ----------------------------------------------------------------------
d.text("AXOLOTL", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#CDE7DF", justify="center")

d.finish("axolotl-V1R00")
