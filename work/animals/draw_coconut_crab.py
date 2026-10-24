#!/usr/bin/env python3
"""Coconut crab — field-guide plate V1R00. The land crab that lifts
coconuts and steals cutlery: island plate, moon-crab mood. Frontal robber
crab, crusher claw resting over a husked coconut, a stolen fork glinting
on moonlit sand, palm crown under a full moon. Floor closes on the disc's
own arc. 1000x1000. House style: gradients + translucent shading, never
flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Coconut Crab — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#33182A"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0B1020"), (1, "#04050C"))
PLATE_GRAD = rad((0, "#CBD6D4"), (0.5, "#7E919E"), (1, "#2A3644"))
SAND_GRAD = lin(0, 720, 0, 890, (0, "#97A2AE"), (0.55, "#566270"), (1, "#252E3A"))
SHELL_GRAD = rad((0, "#9A6A72"), (0.55, "#6A4152"), (1, "#432840"))
LEG_GRAD = lin(400, 540, 300, 760, (0, "#C25E36"), (0.6, "#9A4228"), (1, "#6E2F22"))
CLAW_GRAD = rad((0, "#B07880"), (0.7, "#7A4456"), (1, "#4E2C44"))
NUT_GRAD = rad((0, "#8A6A48"), (0.75, "#5E4128"), (1, "#38250F"))
PALM = "#141E2A"

# --- backdrop + moonlit island plate ---------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#7E919E", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1C2632", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E2DC", strokeWidth=3, opacity=40)

# the moon + its halo, high left over the lagoon
d.shape("ellipse", "Moon halo", x=168, y=98, width=270, height=270,
        fill=rad((0, "#F0EAD2", 30), (0.55, "#F0EAD2", 12), (1, "#F0EAD2", 0)),
        stroke=NONE)
d.shape("ellipse", "Moon", x=226, y=156, width=124, height=124,
        fill=rad((0, "#F6F0DC"), (0.8, "#E8E0C4"), (1, "#C4B894")), stroke=NONE)
for i, (x, y, w) in enumerate([(255, 185, 16), (300, 225, 22), (268, 246, 12)]):
    d.shape("ellipse", f"Moon mare {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#C9BE9C", opacity=35, stroke=NONE)

# salt stars, kept inside the disc
stars = [(170, 250, 4), (215, 160, 5), (430, 105, 4), (560, 130, 5),
         (640, 190, 4), (740, 120, 5), (820, 215, 4), (355, 200, 3),
         (120, 380, 4), (860, 330, 4), (700, 90, 3), (500, 150, 3)]
for i, (x, y, w) in enumerate(stars):
    if on_disc(x, y, pad=18):
        d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
                fill="#EDF2EA", opacity=65, stroke=NONE)

# coconut palm on the right, crown leaning into the moonlight
d.path("M742,716 C758,600 778,470 806,330 C812,300 818,278 826,262 "
       "C830,256 838,258 836,266 C826,300 818,330 812,360 "
       "C788,480 770,600 758,716 Z", "Palm trunk", fill=PALM, opacity=90, stroke=NONE)
for i, (c1x, c1y, c2x, c2y, ex, ey) in enumerate([
        (790, 250, 700, 210, 628, 236),   # frond left-down
        (812, 236, 740, 180, 690, 172),   # frond left-up
        (836, 232, 796, 170, 762, 152),   # frond up
        (848, 244, 822, 196, 790, 182),   # frond right-up
        (854, 258, 838, 224, 806, 208),   # frond right
        (802, 268, 720, 280, 660, 320),   # frond left-low droop
        ]):
    d.path(f"M828,258 Q{c1x},{c1y} {c2x},{c2y} Q{c2x+8},{c2y+6} {ex},{ey} "
           f"Q{(c2x+ex)/2},{c2y+26} {826},{272} Z",
           f"Frond {i+1}", fill=PALM, opacity=88, stroke=NONE)
# hanging coconuts in the crown
for i, (x, y) in enumerate([(814, 286), (840, 292), (796, 296)]):
    d.shape("ellipse", f"Crown nut {i+1}", x=x, y=y, width=20, height=24,
            fill="#1C2836", opacity=90, stroke=NONE)

# --- moonlit sand floor closing on the disc's own arc ------------------------------
fy = 722
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C330,706 440,732 560,724 C660,718 740,712 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Sand floor", fill=SAND_GRAD, stroke=NONE)
d.path(f"M{fl+8:.0f},{fy} C330,706 440,732 560,724 C660,718 740,712 {fr-8:.0f},{fy}",
       "Sand crest", fill=NONE, stroke="#C4D0D6", strokeWidth=5, opacity=40, cap="round")
# the last reach of a wave, feathering out up the shore
d.path(f"M{fl+30:.0f},{fy-16} C340,690 460,714 580,706 C680,700 740,700 {fr-40:.0f},{fy-8}",
       "Surf line", fill=NONE, stroke="#E8F0EE", strokeWidth=7, opacity=22, cap="round")
d.path(f"M{fl+60:.0f},{fy-30} C380,644 520,668 640,660",
       "Surf ghost", fill=NONE, stroke="#E8F0EE", strokeWidth=4, opacity=14, cap="round")
# moon-sheen pooling on the wet sand
for i, (x, y, w) in enumerate([(300, 790, 170), (560, 812, 210), (720, 772, 130)]):
    d.shape("ellipse", f"Sheen {i+1}", x=x - w/2, y=y, width=w, height=13,
            fill="#D8E2DC", opacity=16, stroke=NONE)
# shell chips and a crab-track trail in the sand
for i, (x, y, w) in enumerate([(215, 758, 7), (262, 782, 5), (700, 800, 8),
                               (762, 748, 6), (642, 770, 5), (470, 806, 6)]):
    d.shape("ellipse", f"Shell chip {i+1}", x=x, y=y, width=w, height=w*0.6,
            fill="#C4D0D6", opacity=35, stroke=NONE)
for k in range(5):
    x = 356 + k * 26
    d.shape("ellipse", f"Track {k+1}", x=x, y=782 + (k % 2) * 7, width=5, height=9,
            fill="#1E2830", opacity=40, stroke=NONE)

# --- the crab ----------------------------------------------------------------------
# walking legs — two-jointed sweeps, ink edge + ember core, knees bowed high,
# toes planted on the sand well inside the disc; the coconut and carapace
# are drawn over them so bases tuck under the body
def leg(base, mid, tip, label, op=100):
    dd = f"M{base[0]},{base[1]} L{mid[0]},{mid[1]} L{tip[0]},{tip[1]}"
    d.path(dd, label + " edge", fill=NONE, stroke="#2A1220", strokeWidth=17,
           cap="round", opacity=op)
    d.path(dd, label, fill=NONE, stroke=LEG_GRAD, strokeWidth=9,
           cap="round", opacity=op)
    d.shape("ellipse", label + " knee", x=mid[0] - 8, y=mid[1] - 8,
            width=16, height=16, fill="#8A3E26", stroke=INK,
            strokeWidth=2.5, opacity=op)

# left legs fan out behind the coconut; right legs open the stance
leg((440, 600), (318, 545), (208, 686), "Leg L1")
leg((435, 615), (300, 610), (218, 736), "Leg L2")
leg((432, 628), (322, 668), (262, 752), "Leg L3", 80)
leg((545, 600), (672, 545), (786, 688), "Leg R1")
leg((550, 615), (694, 606), (804, 730), "Leg R2")
leg((552, 628), (676, 664), (752, 748), "Leg R3", 80)

# --- the husked coconut the crusher claw owns ---------------------------------------
d.shape("ellipse", "Coconut shadow", x=250, y=746, width=150, height=18,
        fill="#10161E", opacity=45, stroke=NONE)
d.shape("ellipse", "Coconut", x=252, y=640, width=128, height=118,
        fill=NUT_GRAD, stroke=INK, strokeWidth=5)
# husk fibre arcs
for i, (x, dy) in enumerate([(272, 6), (296, 14), (322, 10)]):
    d.path(f"M{x},{664+dy} C{x-8},{694+dy} {x-4},{724+dy} {x+4},{744+dy}",
           f"Fibre {i+1}", fill=NONE, stroke="#38250F",
           strokeWidth=3.5, opacity=55, cap="round")
# the three germ pores — the coconut's face, peeking under the claw
for i, (x, y) in enumerate([(266, 716), (282, 726), (272, 738)]):
    d.shape("ellipse", f"Nut pore {i+1}", x=x, y=y, width=9, height=8,
            fill="#241608", opacity=80, stroke=NONE)

# contact shadow under the crab
d.shape("ellipse", "Crab shadow", x=300, y=732, width=420, height=26,
        fill="#10161E", opacity=42, stroke=NONE)

# small right claw — the nimble one that pockets cutlery
d.path("M560,600 C600,606 634,626 652,656 C662,674 662,692 650,700 "
       "C636,708 616,700 606,682 C596,664 590,644 582,628 "
       "C576,616 568,606 560,600 Z",
       "Small claw", fill=CLAW_GRAD, stroke=INK, strokeWidth=5)
# the stolen fork, handle caught in the pincer, tines to the sand
d.path("M628,690 L672,752 L678,747 L634,685 Z M672,752 l6,-10 "
       "M676,755 l6,-10 M680,758 l6,-10", "Stolen fork",
       fill="#D8E2E4", opacity=85, stroke="#8A9AA4", strokeWidth=2.5)
d.shape("ellipse", "Fork glint", x=650, y=716, width=7, height=7,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M650,696 C662,706 664,720 656,728 C646,726 638,714 638,700 Z "
       "M632,698 C624,712 624,724 632,730 C642,728 646,714 644,702 Z",
       "Small pincer", fill="#8A5060", stroke=INK, strokeWidth=3.5)

# carapace — broad shield dome, wider than tall, front edge scalloped
d.path("M350,556 C360,508 408,476 472,472 C540,476 590,506 602,554 "
       "C608,580 596,600 564,610 C520,622 452,624 404,614 "
       "C366,606 344,584 350,556 Z",
       "Carapace", fill=SHELL_GRAD, stroke=INK, strokeWidth=6)
# carapace dome light + rim shadow
d.shape("ellipse", "Dome light", x=400, y=486, width=170, height=56,
        fill="#D8A8AC", opacity=18, stroke=NONE)
d.path("M368,586 C420,606 528,608 584,588 C540,614 430,616 380,600 "
       "C372,596 368,592 368,586 Z", "Carapace skirt", fill="#2E1C30",
       opacity=50, stroke=NONE)
# frontal scallops between the eye stalks
d.path("M430,608 C440,600 452,600 460,608 C470,600 482,600 490,608 "
       "C498,602 508,602 514,608", "Front scallop", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=70, cap="round")
# eye stalks — short pygmy bumps under the front edge
for sgn in (-1, 1):
    x = 472 + sgn * 26
    d.path(f"M{x-9},612 C{x-9},598 {x-6},590 {x},588 C{x+6},590 {x+9},598 {x+9},612 Z",
           f"Eye stalk {'L' if sgn < 0 else 'R'}", fill="#5E3A48",
           stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Eye {'L' if sgn < 0 else 'R'}", x=x-5, y=590,
            width=10, height=9, fill="#140A12", stroke=NONE)
    d.shape("ellipse", f"Eye glint {'L' if sgn < 0 else 'R'}", x=x-2, y=591,
            width=3, height=3, fill="#F0EAD2", opacity=80, stroke=NONE)
# antennae — short forward sweeps, kept thick enough to read at plate scale
for sgn in (-1, 1):
    d.path(f"M{472 + sgn * 14},616 C{472 + sgn * 30},{640} "
           f"{472 + sgn * 52},{654} {472 + sgn * 72},{658}",
           f"Antenna {'L' if sgn < 0 else 'R'}", fill=NONE, stroke="#7A4456",
           strokeWidth=4, opacity=80, cap="round")

# big left crusher claw — the coconut-lifter, resting over the nut
d.path("M402,584 C360,576 318,584 292,606 C268,626 258,654 266,678 "
       "C274,700 296,712 322,710 C350,708 372,690 380,664 "
       "C388,636 380,612 360,598 C344,588 422,592 402,584 Z",
       "Crusher palm", fill=CLAW_GRAD, stroke=INK, strokeWidth=6)
# palm knuckle light + the dark gape between the fingers
d.shape("ellipse", "Palm light", x=284, y=600, width=56, height=40,
        fill="#D8A8AC", opacity=20, stroke=NONE)
# crusher fingers gripping down over the coconut crown
d.path("M300,706 C306,722 320,734 338,738 C348,736 352,728 346,720 "
       "C334,712 322,704 314,694 C306,688 298,694 300,706 Z",
       "Crusher dactyl", fill="#8A5060", stroke=INK, strokeWidth=4)
d.path("M348,714 C358,726 372,732 388,730 C394,724 392,714 384,708 "
       "C370,702 358,700 348,700 C342,704 342,710 348,714 Z",
       "Crusher fixed finger", fill="#7A4456", stroke=INK, strokeWidth=4)
# molar teeth on the crusher — pale ridges along the finger edge
for k, (x, y) in enumerate([(336, 720), (346, 726), (356, 729)]):
    d.shape("ellipse", f"Molar {k+1}", x=x, y=y, width=8, height=6,
            fill="#D8C4B8", opacity=55, stroke=NONE)
# claw arm joining carapace to palm
d.path("M398,568 C372,566 350,572 336,586 C346,596 364,600 382,596 "
       "C396,590 402,580 398,568 Z", "Crusher arm", fill=SHELL_GRAD,
       stroke=INK, strokeWidth=4)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#101820", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
d.text("COCONUT CRAB", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#D8E2DC", justify="center")

d.finish("coconut-crab-V1R00")
