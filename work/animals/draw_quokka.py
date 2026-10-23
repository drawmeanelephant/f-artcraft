#!/usr/bin/env python3
"""Quokka — field-guide plate V1R00. Head/bust portrait, "world's happiest animal":
round teddy-bear face, small rounded ears, permanent smile, warm brown-grey fur.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Quokka — Field Plate", 1000, 1000)

INK = "#4A3324"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3B2C1F"}, {"offset": 1, "color": "#181009"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F6E8C9"}, {"offset": 0.7, "color": "#DEC295"},
    {"offset": 1, "color": "#AC8557"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DDBD92"}, {"offset": 0.72, "color": "#B28A5E"},
    {"offset": 1, "color": "#8A6640"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C29A6E"}, {"offset": 1, "color": "#8F6A45"}]}}
BUST_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#AE875A"}, {"offset": 1, "color": "#7A5836"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7C5F3A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F7EDD8", strokeWidth=3, opacity=55)
# plate patina: soft blotches + speckles
d.shape("ellipse", "Patina 1", x=170, y=200, width=240, height=150, fill="#B9905F", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=590, y=620, width=270, height=160, fill="#B9905F", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(210,300,8),(760,250,7),(180,560,9),(810,560,8),(260,760,7),(730,750,9),
                               (140,420,6),(860,410,7),(410,130,7),(590,120,8),(340,820,6),(660,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#8F6E42", opacity=40, stroke=NONE)

# --- bust / shoulders (behind head) -------------------------------------------
d.path("M330,818 C312,735 392,672 500,672 C608,672 688,735 670,818 "
       "C642,856 575,870 500,870 C425,870 358,856 330,818 Z",
       "Shoulders", fill=BUST_GRAD, stroke=INK, strokeWidth=7)
# chest light patch + neck shadow under the head
d.shape("ellipse", "Chest light", x=420, y=770, width=160, height=90, fill="#E8D2AC", opacity=45, stroke=NONE)
d.shape("ellipse", "Under-head shadow", x=370, y=700, width=260, height=60, fill="#6E4E2E", opacity=30, stroke=NONE)
# a few fur strokes on the chest
for lbl, dd in [("Chest fur 1", "M430,800 C450,812 470,818 492,820"),
                ("Chest fur 2", "M508,822 C534,820 556,812 574,800"),
                ("Chest fur 3", "M470,845 C495,850 525,849 548,842")]:
    d.path(dd, lbl, fill=NONE, stroke="#6E4E2E", strokeWidth=6, opacity=45, cap="round")

# --- ears: small, rounded, set high on the head --------------------------------
d.path("M358,248 C412,248 448,292 441,345 C435,392 392,418 355,402 "
       "C318,386 306,335 322,292 C330,270 340,248 358,248 Z",
       "Ear L", fill=EAR_GRAD, stroke=INK, strokeWidth=7)
d.path("M642,248 C588,248 552,292 559,345 C565,392 608,418 645,402 "
       "C682,386 694,335 678,292 C670,270 660,248 642,248 Z",
       "Ear R", fill=EAR_GRAD, stroke=INK, strokeWidth=7)
d.path("M366,296 C394,296 412,320 408,350 C404,376 380,388 362,377 "
       "C344,366 338,336 348,314 C353,302 356,296 366,296 Z",
       "Inner ear L", fill="#6E4A30", opacity=85, stroke=NONE)
d.path("M634,296 C606,296 588,320 592,350 C596,376 620,388 638,377 "
       "C656,366 662,336 652,314 C647,302 644,296 634,296 Z",
       "Inner ear R", fill="#6E4A30", opacity=85, stroke=NONE)
d.path("M330,300 C340,275 358,258 380,254", "Ear rim L", fill=NONE,
       stroke="#E8D2AC", strokeWidth=6, opacity=50, cap="round")
d.path("M670,300 C660,275 642,258 620,254", "Ear rim R", fill=NONE,
       stroke="#E8D2AC", strokeWidth=6, opacity=50, cap="round")

# --- head ----------------------------------------------------------------------
d.path("M500,330 C655,330 745,438 742,562 C739,688 632,780 500,780 "
       "C368,780 261,688 258,562 C255,438 345,330 500,330 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=8)
# cheek fur flicks on the silhouette
d.path("M264,542 L244,550 L266,564 L248,576 L270,588", "Fur flick L",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M736,542 L756,550 L734,564 L752,576 L730,588", "Fur flick R",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# head top highlight + cheek shading + chin shadow
d.shape("ellipse", "Head highlight", x=380, y=348, width=240, height=84, fill="#FFFFFF", opacity=12, stroke=NONE)
d.shape("ellipse", "Cheek shade L", x=296, y=615, width=74, height=44, fill="#8A6640", opacity=30, stroke=NONE)
d.shape("ellipse", "Cheek shade R", x=630, y=615, width=74, height=44, fill="#8A6640", opacity=30, stroke=NONE)
d.path("M372,728 C430,762 570,762 628,728 C570,744 430,744 372,728 Z",
       "Chin shadow", fill="#8A6640", opacity=35, stroke=NONE)
# forehead fur strokes
for lbl, dd in [("Forehead fur 1", "M462,368 C468,352 478,342 492,336"),
                ("Forehead fur 2", "M510,336 C522,342 532,352 538,368"),
                ("Forehead fur 3", "M486,350 C494,340 506,340 514,350")]:
    d.path(dd, lbl, fill=NONE, stroke="#8A6640", strokeWidth=5, opacity=50, cap="round")

# --- muzzle + face ---------------------------------------------------------------
d.shape("ellipse", "Muzzle patch", x=360, y=540, width=280, height=185,
        fill="#EFDDB9", opacity=70, stroke=NONE)
# warm blush on the cheeks
d.shape("ellipse", "Blush L", x=318, y=585, width=82, height=48, fill="#C08A5E", opacity=25, stroke=NONE)
d.shape("ellipse", "Blush R", x=600, y=585, width=82, height=48, fill="#C08A5E", opacity=25, stroke=NONE)
# eyes: dark, bright, friendly
d.shape("ellipse", "Eye L", x=388, y=478, width=48, height=54, fill="#2E1F14", stroke=NONE)
d.shape("ellipse", "Eye R", x=564, y=478, width=48, height=54, fill="#2E1F14", stroke=NONE)
d.shape("ellipse", "Glint L", x=400, y=488, width=11, height=11, fill="#FFFFFF", opacity=92, stroke=NONE)
d.shape("ellipse", "Glint R", x=576, y=488, width=11, height=11, fill="#FFFFFF", opacity=92, stroke=NONE)
d.shape("ellipse", "Glint L2", x=416, y=508, width=5, height=5, fill="#FFFFFF", opacity=60, stroke=NONE)
d.shape("ellipse", "Glint R2", x=592, y=508, width=5, height=5, fill="#FFFFFF", opacity=60, stroke=NONE)
# soft happy arcs above the eyes
d.path("M384,462 C402,450 428,448 448,458", "Brow light L", fill=NONE,
       stroke="#EAD3AC", strokeWidth=6, opacity=65, cap="round")
d.path("M552,458 C572,448 598,450 616,462", "Brow light R", fill=NONE,
       stroke="#EAD3AC", strokeWidth=6, opacity=65, cap="round")
# nose
d.path("M472,570 C472,556 486,548 500,548 C514,548 528,556 528,570 "
       "C528,582 516,592 500,592 C484,592 472,582 472,570 Z",
       "Nose", fill="#38271B", stroke=NONE)
d.path("M480,560 C488,554 498,553 506,556", "Nose glint", fill=NONE,
       stroke="#FFFFFF", strokeWidth=4, opacity=40, cap="round")
d.path("M500,592 L500,610", "Philtrum", fill=NONE, stroke=INK, strokeWidth=5, opacity=70, cap="round")
# THE smile: corners pulled high
d.path("M408,588 C430,634 465,652 500,654 C535,652 570,634 592,588",
       "Smile", fill=NONE, stroke=INK, strokeWidth=9, cap="round")
d.path("M410,588 C400,580 394,571 392,562", "Smile corner L", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.path("M590,588 C600,580 606,571 608,562", "Smile corner R", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.path("M450,670 C480,680 520,680 550,670", "Lower lip light", fill=NONE,
       stroke="#8A6640", strokeWidth=6, opacity=40, cap="round")
# short whiskers
for lbl, dd in [("Whisker L1", "M366,606 L328,598"), ("Whisker L2", "M368,632 L332,636"),
                ("Whisker R1", "M634,606 L672,598"), ("Whisker R2", "M632,632 L668,636")]:
    d.path(dd, lbl, fill=NONE, stroke=INK, strokeWidth=4, opacity=45, cap="round")

# --- name ----------------------------------------------------------------------
d.text("QUOKKA", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#F4E6C6", justify="center")

d.finish("quokka-V1R00")
