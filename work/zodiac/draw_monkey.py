#!/usr/bin/env python3
"""Monkey — Celestial Seal V1R00. Metal element. A golden monkey with a
heart-shaped face, a peach of longevity, and a tail curled behind; the
ninth branch. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, lin, rad, gold_lin,
                          smooth, cloud, coin, blossom)
from orient.zodiac import ZodiacPlate, almond_eye, blush, whisker, bust

p = ZodiacPlate("monkey-V1R00", "MONKEY", "猴", "申", "metal", "2028 · 2040", "Monkey")
d = p.d

FUR_HI = "#C89A62"
FUR = "#A06E3E"
FUR_LO = "#6E4420"
FACE_HI = "#F2D8B0"
FACE = "#E0BE8C"
PEACH = "#F2A88E"

cloud(d, 252, 260, 0.9, "Cloud upper L", fill=GOLD, opacity=12)
cloud(d, 748, 260, 0.9, "Cloud upper R", fill=GOLD, opacity=12)
for i, (x, y, r) in enumerate([(300, 560, 3), (700, 560, 3), (660, 330, 3), (340, 330, 3)]):
    d.shape("ellipse", f"Spark {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=GOLD_HI, opacity=45, stroke=NONE)

# tail curling out to the right
tail = [(632,690),(710,700),(762,730),(770,772),(738,800),(700,790),(686,764)]
d.path(smooth(tail), "Tail", fill=NONE, stroke=INK, strokeWidth=24, cap="round")
d.path(smooth(tail), "Tail fur", fill=NONE, stroke=lin(0, 680, 0, 800, (0, FUR), (1, FUR_LO)),
       strokeWidth=17, cap="round")
d.shape("ellipse", "Tail tip", x=674, y=750, width=22, height=20, fill=FACE, opacity=70, stroke=NONE)

paws = bust(d, lin(0, 520, 0, 772, (0, FUR), (0.55, FUR_LO), (1, "#3E2610")),
            half_top=56, half_bottom=184, paw_fill=FACE_HI, paw_line="#7A5A32")
d.path("M452,550 C440,622 440,702 452,762 L548,762 C560,702 560,622 548,550 "
       "C526,540 474,540 452,550 Z", "Belly",
       fill=lin(0, 542, 0, 764, (0, "#E8C8A0"), (1, "#B8895E")), opacity=75, stroke=NONE)

# ears
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 128
    d.shape("ellipse", f"Ear {nm}", x=x - 50, y=364, width=100, height=112,
            fill=lin(0, 360, 0, 480, (0, FUR), (1, FUR_LO)), stroke=INK, strokeWidth=6)
    d.shape("ellipse", f"Ear inner {nm}", x=x - 32, y=386, width=64, height=72,
            fill=FACE, opacity=75, stroke=NONE)

# head
HEAD = ("M500,296 C572,296 624,324 638,380 C650,430 630,484 590,508 "
        "C560,526 530,532 500,532 C470,532 440,526 410,508 "
        "C370,484 350,430 362,380 C376,324 428,296 500,296 Z")
d.path(HEAD, "Head", fill=lin(0, 296, 0, 532, (0, FUR_HI), (0.5, FUR), (1, FUR_LO)),
       stroke=INK, strokeWidth=7)
# heart-shaped face plate
FACE_PATH = ("M500,340 C540,340 570,358 578,394 C586,432 566,468 538,484 "
             "C522,492 512,494 500,494 C488,494 478,492 462,484 "
             "C434,468 414,432 422,394 C430,358 460,340 500,340 Z")
d.path(FACE_PATH, "Face plate", fill=rad((0, "#FBE6C4"), (0.7, FACE), (1, "#C89A62")),
       stroke="#B8895E", strokeWidth=3)
# forehead tuft
for i, (x, y, rot) in enumerate([(482, 304, -16), (500, 298, 0), (518, 304, 16)]):
    d.path(f"M{x:.1f},{y:.1f} C{x - 8:.1f},{y + 22:.1f} {x - 2 + rot*0.3:.1f},{y + 40:.1f} "
           f"{x + rot*0.7:.1f},{y + 48:.1f} C{x + 10:.1f},{y + 30:.1f} "
           f"{x + 8:.1f},{y + 14:.1f} {x:.1f},{y:.1f} Z", f"Tuft {i+1}",
           fill=FUR_LO, stroke=INK, strokeWidth=2)

# eyes
almond_eye(d, 438, 406, 66, 50, "Eye L", iris="#B8742E", iris2="#5A2E10", look=(0.08, 0.04))
almond_eye(d, 562, 406, 66, 50, "Eye R", iris="#B8742E", iris2="#5A2E10", look=(-0.08, 0.04))
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 62
    d.path(f"M{x - 28:.1f},378 Q{x:.1f},366 {x + 28:.1f},380", f"Brow {nm}",
           fill=NONE, stroke=FUR_LO, strokeWidth=6, cap="round")

# muzzle
d.path("M500,438 C538,438 562,456 564,480 C566,508 538,526 500,526 "
       "C462,526 434,508 436,480 C438,456 462,438 500,438 Z", "Muzzle",
       fill=lin(0, 438, 0, 526, (0, "#FFF0D4"), (1, "#E0C49A")), stroke=NONE, opacity=90)
d.shape("ellipse", "Nose", x=484, y=462, width=32, height=20,
        fill=lin(0, 462, 0, 482, (0, "#C88A76"), (1, "#8A5040")), stroke=INK, strokeWidth=2.6)
d.path("M500,482 L500,492", "Philtrum", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
d.path("M500,492 C490,500 474,500 464,494 M500,492 C510,500 526,500 536,494",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3.2, cap="round")
d.path("M476,514 C488,520 512,520 524,514", "Chin", fill=NONE, stroke="#C89A62",
       strokeWidth=4, opacity=50, cap="round")
blush(d, 414, 458, 30, "Cheek L", color="#E8826A", opacity=32)
blush(d, 586, 458, 30, "Cheek R", color="#E8826A", opacity=32)

# peach at the chest
d.shape("ellipse", "Peach", x=462, y=636, width=76, height=72,
        fill=rad((0, "#FFD0B0"), (0.55, PEACH), (1, "#D8705E")), stroke=INK, strokeWidth=3)
d.path("M500,646 C506,636 514,632 522,634", "Peach cleft", fill=NONE,
       stroke="#C86050", strokeWidth=2.4, opacity=60, cap="round")
d.path("M500,638 C500,618 512,604 530,600", "Peach leaf stem", fill=NONE,
       stroke="#5A3A1A", strokeWidth=3, cap="round")
d.path("M530,600 C548,592 566,600 568,616 C550,624 534,618 530,600 Z",
       "Peach leaf", fill=lin(0, 596, 0, 624, (0, "#8AC09A"), (1, "#3E7A56")),
       stroke="#1E4A34", strokeWidth=2)

p.close()
