#!/usr/bin/env python3
"""Fennec fox — field-guide plate V1R00. Head portrait, giant ears, desert-night.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Fennec Fox — Field Plate", 1000, 1000)

INK = "#4A3423"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#232A45"}, {"offset": 1, "color": "#12152A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2E0BC"}, {"offset": 0.7, "color": "#E2C794"},
    {"offset": 1, "color": "#C9A266"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F8ECD2"}, {"offset": 0.72, "color": "#E8CCA0"},
    {"offset": 1, "color": "#CBA873"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4E4C4"}, {"offset": 1, "color": "#D3B184"}]}}

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(140,120,7),(860,150,6),(920,340,8),(80,300,5),(180,880,6),(830,880,7)]):
    d.path(f"M{x},{y-w} L{x+w},{y} L{x},{y+w} L{x-w},{y} Z", f"Star {i+1}",
           fill="#FFFFFF", opacity=30, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A9834E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F6ECD6", strokeWidth=3, opacity=60)
# dunes at plate bottom — bottom edge follows the plate's lower arc so nothing
# leaks past the rim (plate disc: center 500,460 r=420)
d.path("M131,660 C280,620 420,652 520,634 C640,612 760,640 869,660 "
       "A420,420 0 0 1 131,660 Z",
       "Dune far", fill="#D9B87E", opacity=45, stroke=NONE)
d.path("M170,720 C300,690 430,722 560,702 C690,682 780,706 830,720 "
       "A420,420 0 0 1 170,720 Z",
       "Dune near", fill="#C9A266", opacity=50, stroke=NONE)
for i, (x, y, w) in enumerate([(210,300,8),(770,260,7),(170,540,9),(830,540,8),(260,200,7),(720,190,8)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#A9834E", opacity=35, stroke=NONE)

# --- ears ----------------------------------------------------------------------
d.path("M380,486 C314,420 276,306 292,168 C330,164 424,290 472,400 C480,438 452,476 424,486 Z",
       "Ear L", fill=EAR_GRAD, stroke=INK, strokeWidth=7)
d.path("M620,486 C686,420 724,306 708,168 C670,164 576,290 528,400 C520,438 548,476 576,486 Z",
       "Ear R", fill=EAR_GRAD, stroke=INK, strokeWidth=7)
# inner ears
d.path("M384,452 C340,404 310,308 318,212 C350,220 410,320 442,398 C444,424 422,446 406,452 Z",
       "Inner ear L", fill="#E9BCA4", stroke=NONE)
d.path("M616,452 C660,404 690,308 682,212 C650,220 590,320 558,398 C556,424 578,446 594,452 Z",
       "Inner ear R", fill="#E9BCA4", stroke=NONE)
# ear hair tufts
d.path("M330,300 C350,340 372,380 390,410", "Ear tuft L", fill=NONE, stroke="#C89B70", strokeWidth=5, opacity=60, cap="round")
d.path("M670,300 C650,340 628,380 610,410", "Ear tuft R", fill=NONE, stroke="#C89B70", strokeWidth=5, opacity=60, cap="round")
# ear rim light
d.path("M286,180 C300,260 340,370 396,440", "Ear rim L", fill=NONE, stroke="#FFF6E4", strokeWidth=5, opacity=45, cap="round")
d.path("M714,180 C700,260 660,370 604,440", "Ear rim R", fill=NONE, stroke="#FFF6E4", strokeWidth=5, opacity=45, cap="round")

# --- head ----------------------------------------------------------------------
d.path("M500,430 C600,430 668,492 670,585 C671,635 650,680 600,715 "
       "C560,742 520,755 500,755 C480,755 440,742 400,715 "
       "C350,680 329,635 330,585 C332,492 400,430 500,430 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
# white muzzle + cheek patches
d.shape("ellipse", "Cheek L", x=356, y=612, width=110, height=80, fill="#FFFFFF", opacity=35, stroke=NONE)
d.shape("ellipse", "Cheek R", x=534, y=612, width=110, height=80, fill="#FFFFFF", opacity=35, stroke=NONE)
d.shape("ellipse", "Muzzle", x=448, y=650, width=104, height=66, fill="#FFF8EC", opacity=55, stroke=NONE)
# forehead shading + highlight
d.shape("ellipse", "Head highlight", x=390, y=445, width=220, height=70, fill="#FFFFFF", opacity=15, stroke=NONE)
d.path("M370,700 C430,735 570,735 630,700 C570,720 430,720 370,700 Z",
       "Chin shadow", fill="#B8935E", opacity=35, stroke=NONE)
# fur part strokes on forehead
d.path("M470,470 L486,442 M500,466 L500,436 M530,470 L514,442", "Forehead fur",
       fill=NONE, stroke="#C8A070", strokeWidth=5, opacity=60, cap="round")

# --- face ----------------------------------------------------------------------
d.shape("ellipse", "Eye L", x=408, y=568, width=38, height=46, fill="#2E2018", stroke=NONE)
d.shape("ellipse", "Eye R", x=554, y=568, width=38, height=46, fill="#2E2018", stroke=NONE)
d.shape("ellipse", "Glint L", x=418, y=578, width=9, height=9, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=564, y=578, width=9, height=9, fill="#FFFFFF", opacity=90, stroke=NONE)
# eye liner flicks
d.path("M404,570 C414,556 434,552 448,560", "Liner L", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M552,560 C566,552 586,556 596,570", "Liner R", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# nose + mouth
d.path("M482,668 L518,668 C520,682 510,692 500,692 C490,692 480,682 482,668 Z",
       "Nose", fill="#33231A", stroke=NONE)
d.path("M470,712 C484,722 516,722 530,712", "Mouth", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M500,692 L500,706", "Philtrum", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# whiskers
for lbl, dd in [("W L1", "M340,640 C380,648 400,654 420,660"), ("W L2", "M336,672 L418,680"),
                ("W L3", "M344,704 C384,694 404,688 422,684"), ("W R1", "M660,640 C620,648 600,654 580,660"),
                ("W R2", "M664,672 L582,680"), ("W R3", "M656,704 C616,694 596,688 578,684")]:
    d.path(dd, lbl, fill=NONE, stroke=INK, strokeWidth=4, opacity=70, cap="round")

# --- name ----------------------------------------------------------------------
d.text("FENNEC FOX", "Name", x=500, y=960, size=56, font="Virelai Sans",
       color="#EAD9B8", justify="center")

d.finish("fennec-fox-V1R00")
