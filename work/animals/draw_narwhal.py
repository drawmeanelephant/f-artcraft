#!/usr/bin/env python3
"""Narwhal — field-guide plate V1R00. Full-body profile, spiral tusk.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; every accent was checked to land inside."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Narwhal — Field Plate", 1000, 1000)

INK = "#3B3448"          # warm dark slate, not black
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E2438"}, {"offset": 1, "color": "#050E1A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8FC3D4"}, {"offset": 0.7, "color": "#5E93AC"},
    {"offset": 1, "color": "#35617E"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E99B2"}, {"offset": 0.55, "color": "#A9BECC"},
    {"offset": 1, "color": "#D9E4EA"}]}}
FLUKE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E88A2"}, {"offset": 1, "color": "#A9BECC"}]}}
FIN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8AA2B8"}, {"offset": 1, "color": "#5E7890"}]}}
TUSK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6EFDD"}, {"offset": 0.6, "color": "#E3D5B0"},
    {"offset": 1, "color": "#BFAE85"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E5A74", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFE8EE", strokeWidth=3, opacity=55)
# plate patina: deep-water blotches + speckles (all inside the rim)
d.shape("ellipse", "Patina 1", x=170, y=200, width=240, height=150, fill="#4E86A2", opacity=25, stroke=NONE)
d.shape("ellipse", "Patina 2", x=560, y=600, width=260, height=140, fill="#3A6E8C", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 3", x=640, y=180, width=180, height=120, fill="#4E86A2", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(200,300,8),(760,240,7),(170,560,9),(800,560,8),(260,755,7),(730,740,9),
                               (140,420,6),(860,430,7),(400,120,7),(560,110,8),(340,815,6),(655,810,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#2E5A74", opacity=45, stroke=NONE)
# rising bubbles, upper right, left of the tusk
for i, (x, y, w) in enumerate([(745,235,14),(715,175,10),(730,150,16),(690,125,9),(630,110,12)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w, fill="#FFFFFF", opacity=18, stroke=NONE)
# ice glints: tiny diamonds
for i, (cx, cy, s) in enumerate([(300,160,10),(180,480,8),(830,660,9),(430,840,8),(160,620,7)]):
    d.path(f"M{cx},{cy-s} L{cx+s},{cy} L{cx},{cy+s} L{cx-s},{cy} Z",
           f"Ice glint {i+1}", fill="#DDF2F6", opacity=30, stroke=NONE)
# faint wave lines low on the plate
d.path("M250,750 C350,738 450,765 540,755 C620,746 680,760 730,752",
       "Wave line 1", fill=NONE, stroke="#DDF2F6", strokeWidth=6, opacity=18, cap="round")
d.path("M310,790 C390,778 460,802 550,792 C620,784 660,796 700,790",
       "Wave line 2", fill=NONE, stroke="#DDF2F6", strokeWidth=5, opacity=14, cap="round")

# --- tail flukes (behind body) --------------------------------------------------
d.path("M268,455 C228,425 180,412 148,425 C172,455 200,472 232,483 "
       "C200,494 174,512 150,545 C182,550 228,528 262,502 Z",
       "Tail flukes", fill=FLUKE_GRAD, stroke=INK, strokeWidth=6)
d.path("M165,432 C185,452 205,468 226,480", "Fluke crease upper",
       fill=NONE, stroke="#4A6478", strokeWidth=5, opacity=45, cap="round")
d.path("M163,538 C188,530 212,516 230,500", "Fluke crease lower",
       fill=NONE, stroke="#4A6478", strokeWidth=5, opacity=45, cap="round")

# --- far flipper (tip peeks below the belly) ------------------------------------
d.path("M605,530 C602,568 588,600 558,620 C590,622 626,592 634,545 Z",
       "Far flipper", fill="#546C82", stroke=NONE, opacity=80)

# --- tusk (drawn before the body so the head hides its root) ---------------------
BASE = (678.0, 438.0)
TIP = (880.0, 315.0)           # stays ~13px inside the plate rim
vx, vy = TIP[0]-BASE[0], TIP[1]-BASE[1]
L = math.hypot(vx, vy)
ux, uy = vx/L, vy/L            # along the tusk
px, py = -uy, ux               # perpendicular
HW = 13.0                      # half width at base
bx1, by1 = BASE[0]-px*HW, BASE[1]-py*HW
bx2, by2 = BASE[0]+px*HW, BASE[1]+py*HW
d.path(f"M{bx1:.0f},{by1:.0f} L{TIP[0]:.0f},{TIP[1]:.0f} L{bx2:.0f},{by2:.0f} Z",
       "Tusk", fill=TUSK_GRAD, stroke=INK, strokeWidth=5)
# spiral grooves: diagonal curved strokes wrapping the cone
for j, t in enumerate([0.08, 0.17, 0.26, 0.35, 0.44, 0.53, 0.62, 0.71, 0.80, 0.88]):
    cx = BASE[0]+vx*t; cy = BASE[1]+vy*t
    w = HW*(1-t)*0.92
    g = w*1.15                 # forward shift -> helix diagonal
    x1 = cx-px*w-ux*g; y1 = cy-py*w-uy*g
    x2 = cx+px*w+ux*g; y2 = cy+py*w+uy*g
    mx = cx+px*w*0.18; my = cy+py*w*0.18
    d.path(f"M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}",
           f"Groove {j+1}", fill=NONE, stroke="#8A7A54", strokeWidth=4,
           opacity=75, cap="round")
# sheen along the tusk's lit edge
d.path(f"M{bx1+4:.0f},{by1+2:.0f} L{TIP[0]-6:.0f},{TIP[1]+8:.0f}",
       "Tusk sheen", fill=NONE, stroke="#FFF8E8", strokeWidth=3, opacity=55, cap="round")

# --- body ------------------------------------------------------------------------
d.path("M710,442 C695,408 655,388 605,380 C520,368 400,378 330,408 "
       "C295,425 272,438 262,452 C256,470 255,488 260,505 "
       "C310,540 400,565 490,568 C580,570 650,545 685,505 "
       "C700,485 707,462 710,442 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
# dorsal ridge: narwhals have a low ridge, not a fin
d.path("M452,373 C405,378 355,392 312,414", "Dorsal ridge",
       fill=NONE, stroke="#5E7890", strokeWidth=9, opacity=50, cap="round")
# belly sheen + back shadow (kept inside the silhouette)
d.shape("ellipse", "Belly sheen", x=360, y=505, width=260, height=55,
        fill="#FFFFFF", opacity=22, stroke=NONE)
d.shape("ellipse", "Back shadow", x=400, y=370, width=200, height=34,
        fill="#3A5870", opacity=25, stroke=NONE)
# mottled skin: translucent blotches, denser on the back
for i, (x, y, w, h, c, o) in enumerate([
        (600,385,55,30,"#5C748C",30),(520,375,40,24,"#5C748C",28),(440,382,48,26,"#5C748C",30),
        (360,398,44,26,"#5C748C",28),(300,425,36,22,"#5C748C",26),(640,420,30,20,"#5C748C",24),
        (470,410,34,20,"#5C748C",22),(380,438,30,18,"#5C748C",20),
        (560,400,42,22,"#E9F2F5",35),(420,418,36,20,"#E9F2F5",32),(330,445,30,18,"#E9F2F5",30),
        (610,450,26,16,"#E9F2F5",30),(490,445,30,18,"#E9F2F5",28),(540,470,26,16,"#E9F2F5",25)]):
    d.shape("ellipse", f"Mottle {i+1}", x=x, y=y, width=w, height=h, fill=c, opacity=o, stroke=NONE)

# --- near flipper ------------------------------------------------------------------
d.path("M540,552 C528,590 505,620 475,638 C505,648 555,612 572,556 Z",
       "Near flipper", fill=FIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M548,565 C540,595 522,618 498,632", "Flipper crease",
       fill=NONE, stroke="#4A6478", strokeWidth=4, opacity=50, cap="round")

# --- face ----------------------------------------------------------------------------
d.shape("ellipse", "Eye", x=648, y=452, width=17, height=14, fill="#1C1826", stroke=NONE)
d.shape("ellipse", "Eye glint", x=653, y=455, width=5, height=5, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M692,470 C674,486 654,492 634,489", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M578,390 C590,386 606,386 618,390", "Blowhole",
       fill=NONE, stroke=INK, strokeWidth=5, opacity=60, cap="round")

# --- name ----------------------------------------------------------------------------
d.text("NARWHAL", "Name", x=500, y=960, size=60, font="Virelai Sans",
       color="#CFE3EA", justify="center")

d.finish("narwhal-V1R00")
