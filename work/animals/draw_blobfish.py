#!/usr/bin/env python3
"""Blobfish — field-guide plate V1R00. The famous droop, played as a straight
specimen portrait: the decompressed, gelatinous face slumped on a wet slab,
hanging nose, heavy frown, tiny eyes. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Blobfish — Field Plate", 1000, 1000)

INK = "#4A2C33"   # deep mauve, not black
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#14202E"}, {"offset": 1, "color": "#060A12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCE6EE"}, {"offset": 0.7, "color": "#A7BACB"},
    {"offset": 1, "color": "#71879E"}]}}
SLAB_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#7D93A8"}, {"offset": 1, "color": "#46596D"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FBD9D3"}, {"offset": 0.62, "color": "#EDAAA6"},
    {"offset": 1, "color": "#C9787E"}]}}
NOSE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFE2DC"}, {"offset": 0.6, "color": "#F0B1AC"},
    {"offset": 1, "color": "#D08389"}]}}
FIN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E9A4A3"}, {"offset": 1, "color": "#C27077"}]}}
LIP_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#C9737C"}, {"offset": 1, "color": "#9C4F5B"}]}}
EYE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A3A44"}, {"offset": 1, "color": "#160E12"}]}}

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4C6178", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EAF1F6", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=170, y=170, width=230, height=130, fill="#8EA3B8", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=200, width=200, height=110, fill="#8EA3B8", opacity=18, stroke=NONE)
# marine snow drifting down the upper plate
for i, (x, y, w, o) in enumerate([(210,330,7,45),(250,240,5,35),(330,150,6,40),(420,110,5,30),
                                  (600,120,6,40),(690,170,5,35),(770,260,7,45),(800,360,5,30),
                                  (170,450,6,35),(840,470,6,35),(300,200,4,30),(720,330,4,30),
                                  (150,560,5,30),(855,580,5,30)]):
    d.shape("ellipse", f"Marine snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=o, stroke=NONE)

# --- wet slab: closes on the disc's own arc so it never leaks past the rim ---------
d.path("M206,760 C330,738 670,738 794,760 A420,420 0 0 1 206,760 Z",
       "Slab", fill=SLAB_GRAD, stroke=NONE)
d.path("M226,762 C340,744 660,744 774,762", "Slab sheen",
       fill=NONE, stroke="#E6EEF4", strokeWidth=4, opacity=45, cap="round")
d.path("M268,810 C380,800 620,800 732,810 A420,420 0 0 1 268,810 Z",
       "Slab depth", fill="#3F5266", opacity=25, stroke=NONE)

# shadow + puddle under the slumped body
d.shape("ellipse", "Body shadow", x=236, y=738, width=528, height=56, fill="#2E3E50", opacity=35, stroke=NONE)
d.shape("ellipse", "Puddle", x=252, y=770, width=496, height=34, fill="#DDEAF2", opacity=22, stroke=NONE)
d.shape("ellipse", "Puddle glint", x=610, y=782, width=100, height=9, fill="#FFFFFF", opacity=40, stroke=NONE)

# --- pectoral fins, sagging at the sides --------------------------------------------
d.path("M252,648 C216,662 194,694 194,730 C222,732 244,712 262,686 Z",
       "Fin L", fill=FIN_GRAD, stroke=INK, strokeWidth=5, opacity=90)
d.path("M748,648 C784,662 806,694 806,730 C778,732 756,712 738,686 Z",
       "Fin R", fill=FIN_GRAD, stroke=INK, strokeWidth=5, opacity=90)
for i, dd in enumerate(["M244,664 C224,680 210,700 204,720", "M252,676 C238,692 226,708 220,724",
                        "M756,664 C776,680 790,700 796,720", "M748,676 C762,692 774,708 780,724"]):
    d.path(dd, f"Fin ray {i+1}", fill=NONE, stroke="#A35A64", strokeWidth=3, opacity=45, cap="round")

# --- body: one gelatinous slump, widest at the bottom where gravity won --------------
d.path("M500,292 C608,292 682,360 702,452 C718,524 742,590 764,646 "
       "C784,698 766,746 712,762 C630,778 370,778 288,762 "
       "C234,746 216,698 236,646 C258,590 282,524 298,452 "
       "C318,360 392,292 500,292 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
# gelatin sheen: crown highlight + side glazes
d.shape("ellipse", "Crown sheen", x=408, y=308, width=184, height=58, fill="#FFFFFF", opacity=26, stroke=NONE)
d.shape("ellipse", "Crown sheen hot", x=452, y=318, width=70, height=20, fill="#FFFFFF", opacity=40, stroke=NONE)
d.path("M318,430 C304,500 282,580 260,636", "Glaze L", fill=NONE,
       stroke="#FFFFFF", strokeWidth=8, opacity=22, cap="round")
d.path("M684,440 C698,500 718,570 740,624", "Glaze R", fill=NONE,
       stroke="#FFFFFF", strokeWidth=6, opacity=16, cap="round")
# jowls: translucent sag shading low on each side
d.shape("ellipse", "Jowl L", x=266, y=640, width=160, height=110, fill="#B8646E", opacity=26, stroke=NONE)
d.shape("ellipse", "Jowl R", x=574, y=640, width=160, height=110, fill="#B8646E", opacity=26, stroke=NONE)
d.path("M300,676 C330,712 380,736 430,742", "Jowl fold L", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=35, cap="round")
d.path("M700,676 C670,712 620,736 570,742", "Jowl fold R", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=35, cap="round")
# skin pores / soft prickles
for i, (x, y, w) in enumerate([(380,360,6),(440,340,5),(560,342,6),(620,366,5),(340,420,5),
                               (660,420,6),(320,520,5),(680,520,5),(310,600,6),(690,600,6),
                               (360,740,5),(640,740,5),(500,330,4)]):
    d.shape("ellipse", f"Pore {i+1}", x=x, y=y, width=w, height=w, fill="#B26A72", opacity=45, stroke=NONE)

# --- eyes: small, wet, set under heavy sagging lids ---------------------------------
d.shape("ellipse", "Lid shade L", x=380, y=410, width=90, height=40, fill="#B8646E", opacity=30, stroke=NONE)
d.shape("ellipse", "Lid shade R", x=530, y=410, width=90, height=40, fill="#B8646E", opacity=30, stroke=NONE)
d.shape("ellipse", "Eye L", x=404, y=432, width=34, height=30, fill=EYE_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye R", x=562, y=432, width=34, height=30, fill=EYE_GRAD, stroke=INK, strokeWidth=3)
d.path("M394,440 C408,426 432,424 448,438", "Lid L", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M552,438 C568,424 592,426 606,440", "Lid R", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.shape("ellipse", "Glint L", x=412, y=440, width=8, height=7, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=570, y=440, width=8, height=7, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M398,474 C412,484 434,484 446,474", "Bag L", fill=NONE, stroke=INK, strokeWidth=3, opacity=35, cap="round")
d.path("M554,474 C566,484 588,484 602,474", "Bag R", fill=NONE, stroke=INK, strokeWidth=3, opacity=35, cap="round")

# --- the frown: thick downturned lips ------------------------------------------------
d.path("M360,722 C398,684 602,684 640,722 C610,708 566,700 500,700 "
       "C434,700 390,708 360,722 Z", "Lips", fill=LIP_GRAD, stroke=INK, strokeWidth=5)
d.path("M372,716 C414,694 586,694 628,716", "Mouth line", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M420,700 C440,694 460,692 470,692", "Lip sheen", fill=NONE,
       stroke="#F2BDB8", strokeWidth=3, opacity=55, cap="round")
d.path("M360,722 C350,734 346,744 348,756", "Mouth corner L", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=50, cap="round")
d.path("M640,722 C650,734 654,744 652,756", "Mouth corner R", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=50, cap="round")

# --- the nose: a soft lobe hanging from the brow over the mouth -----------------------
d.path("M478,438 C462,500 426,576 430,630 C434,684 566,684 570,630 "
       "C574,576 538,500 522,438 C512,424 488,424 478,438 Z",
       "Nose", fill=NOSE_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Nose sheen", x=458, y=592, width=60, height=38, fill="#FFFFFF", opacity=32, stroke=NONE)
d.shape("ellipse", "Nose sheen hot", x=470, y=600, width=20, height=11, fill="#FFFFFF", opacity=55, stroke=NONE)
d.path("M492,450 C484,494 468,540 456,584", "Nose ridge", fill=NONE,
       stroke="#FFFFFF", strokeWidth=4, opacity=25, cap="round")
d.path("M446,660 C478,676 522,676 554,660", "Nose underside", fill=NONE,
       stroke="#A2565F", strokeWidth=5, opacity=40, cap="round")

# --- water beading off onto the slab --------------------------------------------------
for i, (x, y, w, h) in enumerate([(232,770,10,7),(266,786,7,5),(744,768,12,8),(712,790,8,5),
                                  (520,796,9,6)]):
    d.shape("ellipse", f"Droplet {i+1}", x=x, y=y, width=w, height=h,
            fill="#F4FAFD", opacity=55, stroke=NONE)

# --- name -------------------------------------------------------------------------------
d.text("BLOBFISH", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#D5E1EA", justify="center")

d.finish("blobfish-V1R00")
