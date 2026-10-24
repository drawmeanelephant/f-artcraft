#!/usr/bin/env python3
"""Giant panda — field-guide plate V1R00. Frontal portrait in a bamboo stand
on a mist mountain: black ear-tufts, teardrop eye patches and shoulder cape
against a misty jade disc; bamboo canes flank the portrait, mist bands drift
through, moss-dark floor closes on the disc arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Giant Panda — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#101408"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0C1410"), (1, "#020403"))
PLATE_GRAD = rad((0, "#E4ECD8"), (0.55, "#AFC4A0"), (1, "#5E7A58"))
FLOOR_GRAD = lin(0, 768, 0, 880, (0, "#3A4A32"), (1, "#141C10"))
FACE = rad((0, "#F8F4E8"), (0.62, "#EAE2CC"), (1, "#C4B794"))
BLACK_FUR = lin(0, 240, 0, 800, (0, "#26261E"), (0.5, "#1A1A14"), (1, "#0E0E0A"))
BAMBOO = lin(0, 0, 0, 1000, (0, "#7A9458"), (1, "#44582E"))
BAMBOO_DK = "#3E5228"

# --- backdrop + misty jade plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#AFC4A0", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E5638", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8EEDC", strokeWidth=3, opacity=40)

# distant ridge lines — mountain silhouettes fading up the disc
d.path("M140,420 C220,370 300,352 380,368 C460,384 540,352 620,344 "
       "C700,336 780,356 850,392 L860,500 L140,500 Z",
       "Ridge far", fill="#7E9470", opacity=28, stroke=NONE)
d.path("M120,470 C200,430 280,420 360,436 C440,452 520,428 600,420 "
       "C680,412 760,436 830,470 L860,540 L120,540 Z",
       "Ridge near", fill="#5E7850", opacity=32, stroke=NONE)

# mist bands drifting across — soft stroked ribbons
for i, (y, w, o) in enumerate([(300, 90, 16), (390, 70, 20), (500, 110, 14), (610, 80, 18)]):
    d.path(f"M150,{y} C300,{y-24} 420,{y+18} 560,{y-8} C680,{y-28} 760,{y+10} 850,{y-6}",
           f"Mist {i+1}", fill=NONE, stroke="#F2F4E8", strokeWidth=w,
           opacity=o, cap="round")

# --- bamboo canes: segmented stalks flanking the portrait ----------------------
def cane(x, y0, y1, w, label):
    d.path(f"M{x},{y0} L{x},{y1}", f"{label} stalk",
           fill=NONE, stroke=BAMBOO, strokeWidth=w, cap="round")
    # joint rings every ~120pt
    j = y0 + 60
    k = 1
    while j < y1 - 40:
        d.path(f"M{x - w*0.62},{j} C{x - w*0.2},{j + 6} {x + w*0.2},{j + 6} {x + w*0.62},{j}",
               f"{label} joint {k}", fill=NONE, stroke=BAMBOO_DK,
               strokeWidth=4, opacity=80, cap="round")
        j += 118
        k += 1
    # highlight strip down the cane
    d.path(f"M{x - w*0.18},{y0 + 30} L{x - w*0.18},{y1 - 30}", f"{label} light",
           fill=NONE, stroke="#A8BE80", strokeWidth=3, opacity=45, cap="round")

def leaf(x, y, L, ang_deg, label, flip=1):
    """Pointed bamboo leaf from (x,y), length L, leaning ang_deg off vertical."""
    t = math.radians(ang_deg)
    ux, uy = math.sin(t) * flip, -math.cos(t)          # leaf axis, tip up-ish
    tx, ty = x + ux * L, y + uy * L
    wx, wy = -uy, ux                                    # width normal
    w = L * 0.16
    p = (f"M{x},{y} C{x + ux*L*0.3 + wx*w},{y + uy*L*0.3 + wy*w} "
         f"{x + ux*L*0.7 + wx*w*0.7},{y + uy*L*0.7 + wy*w*0.7} {tx},{ty} "
         f"C{x + ux*L*0.7 - wx*w*0.7},{y + uy*L*0.7 - wy*w*0.7} "
         f"{x + ux*L*0.3 - wx*w},{y + uy*L*0.3 - wy*w} {x},{y} Z")
    d.path(p, label, fill="#4A6032", stroke=NONE)
    d.path(f"M{x},{y} L{tx*0.92 + x*0.08:.0f},{ty*0.92 + y*0.08:.0f}",
           f"{label} vein", fill=NONE, stroke="#6E8A48", strokeWidth=2.5,
           opacity=60, cap="round")

cane(196, 210, 740, 26, "Cane L")
cane(238, 340, 752, 18, "Cane L2")
cane(806, 260, 738, 24, "Cane R")
leaf(196, 330, 86, 52, "Leaf L1")
leaf(196, 332, 70, 20, "Leaf L2")
leaf(238, 420, 76, -46, "Leaf L3", flip=-1)
leaf(806, 380, 80, -50, "Leaf R1", flip=-1)
leaf(806, 382, 64, -18, "Leaf R2", flip=-1)
leaf(806, 500, 72, 48, "Leaf R3")

# --- moss-dark forest floor: crest ~y768, bottom closes on the disc arc ---------
fy = 768
fdx = math.sqrt(R * R - (fy - CY) ** 2)
d.path(f"M{CX-fdx:.1f},{fy} C300,754 430,764 560,758 C650,754 730,760 {CX+fdx:.1f},{fy} "
       f"A{R},{R} 0 0 1 {CX-fdx:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{CX-fdx+8:.1f},{fy-2} C300,752 430,760 560,754 C650,750 730,756 {CX+fdx-8:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#D8E0BC", strokeWidth=4, opacity=30, cap="round")

# --- ears: flat-topped black tufts behind the crown -----------------------------
for side, cx in ((-1, 352), (1, 648)):
    d.shape("ellipse", f"Ear {'L' if side < 0 else 'R'}",
            x=cx - 82, y=196, width=164, height=150,
            fill=BLACK_FUR, stroke=INK, strokeWidth=6)
    d.shape("ellipse", f"Ear shade {'L' if side < 0 else 'R'}",
            x=cx - 46, y=230, width=92, height=84,
            fill="#060604", opacity=55, stroke=NONE)

# --- shoulder cape: the black bust closing on the disc arc ----------------------
by = 796
bdx = math.sqrt(R * R - (by - CY) ** 2)
bxl, bxr = CX - bdx, CX + bdx
d.path(f"M392,640 C340,664 300,706 280,748 C270,770 262,784 {bxl:.1f},{by} "
       f"A{R},{R} 0 0 1 {bxr:.1f},{by} "
       f"C738,784 730,770 720,748 C700,706 660,664 608,640 "
       f"C560,660 440,660 392,640 Z",
       "Shoulder cape", fill=BLACK_FUR, stroke=INK, strokeWidth=6)

# --- head: the big round moon of a face ------------------------------------------
SILH = ("M350,340 C384,302 440,282 500,282 C560,282 616,302 650,340 "
        "C686,380 700,432 696,488 C692,548 668,606 620,646 "
        "C584,676 540,690 500,690 C460,690 416,676 380,646 "
        "C332,606 308,548 304,488 C300,432 314,380 350,340 Z")
d.path(SILH, "Head", fill=FACE, stroke=INK, strokeWidth=6)
# crown shadow + cheek shading
d.path("M360,352 C392,318 444,300 500,300 C556,300 608,318 640,352 "
       "C600,332 552,322 500,322 C448,322 400,332 360,352 Z",
       "Crown shade", fill="#B8AC8C", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek shade L", x=318, y=540, width=90, height=70,
        fill="#B8AC8C", opacity=35, stroke=NONE)
d.shape("ellipse", "Cheek shade R", x=592, y=540, width=90, height=70,
        fill="#B8AC8C", opacity=35, stroke=NONE)

# --- eye patches: the signature teardrops, narrow end down-inward ---------------
def eyepatch(cx, cy, label, s):
    """Black teardrop: wide top leaning outward, tip pointing down-inward."""
    p = (f"M{cx},{cy - 66} C{cx + s*44},{cy - 60} {cx + s*62},{cy - 26} {cx + s*56},{cy + 8} "
         f"C{cx + s*50},{cy + 38} {cx + s*26},{cy + 66} {cx - s*4},{cy + 78} "
         f"C{cx - s*20},{cy + 66} {cx - s*30},{cy + 40} {cx - s*32},{cy + 12} "
         f"C{cx - s*34},{cy - 22} {cx - s*24},{cy - 56} {cx},{cy - 66} Z")
    d.path(p, label, fill="#141410", stroke=NONE)

eyepatch(415, 500, "Patch L", -1)
eyepatch(585, 500, "Patch R", 1)

# eyes: dark brown beads set high in each patch
d.shape("ellipse", "Eye L", x=398, y=484, width=34, height=36,
        fill=rad((0, "#4A3018"), (1, "#160E06")), stroke=NONE)
d.shape("ellipse", "Eye R", x=568, y=484, width=34, height=36,
        fill=rad((0, "#4A3018"), (1, "#160E06")), stroke=NONE)
d.shape("ellipse", "Glint L", x=406, y=491, width=7, height=7,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=576, y=491, width=7, height=7,
        fill="#FFFFFF", opacity=85, stroke=NONE)

# nose: broad black pad, slightly heart-shaped
d.path("M466,590 C474,574 490,568 500,572 C510,568 526,574 534,590 "
       "C540,606 532,624 512,630 C506,632 494,632 488,630 "
       "C468,624 460,606 466,590 Z",
       "Nose", fill="#0C0C08", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose shine", x=482, y=584, width=14, height=8,
        fill="#FFFFFF", opacity=25, stroke=NONE)
# philtrum + gentle W mouth
d.path("M500,630 C500,638 500,644 500,648", "Philtrum",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M500,648 C484,656 466,656 452,646 M500,648 C516,656 534,656 548,646",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# chin dimple shadow
d.shape("ellipse", "Chin shade", x=478, y=662, width=44, height=16,
        fill="#B8AC8C", opacity=40, stroke=NONE)

# a bamboo shoot held... no — keep the portrait clean; a fallen leaf on the floor
leaf(300, 812, 60, 70, "Fallen leaf")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A1208", strokeWidth=6)

# --- name ----------------------------------------------------------------------
d.text("GIANT PANDA", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#DCE4C6", justify="center")

d.finish("giant-panda-V1R00")
