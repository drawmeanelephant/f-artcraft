#!/usr/bin/env python3
"""Horse — Celestial Seal V1R00. Fire element. A chestnut horse in three-
quarter bust, pale blaze, a mane like a dark flame, gold browband; the
seventh branch. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, lin, rad, gold_lin,
                          smooth, cloud, coin, blossom)
from orient.zodiac import ZodiacPlate, almond_eye, blush, bust

p = ZodiacPlate("horse-V1R00", "HORSE", "馬", "午", "fire", "2026 · 2038", "Horse")
d = p.d

COAT_HI = "#C87840"
COAT = "#9E4E24"
COAT_LO = "#662A10"
COAT_DEEP = "#3A1608"
MANE = "#2E1408"
CREAM = "#F4E0C0"

cloud(d, 250, 264, 0.9, "Cloud upper L", fill=GOLD, opacity=12)
cloud(d, 750, 264, 0.9, "Cloud upper R", fill=GOLD, opacity=12)
for i, (x, y, r) in enumerate([(300, 560, 3), (700, 560, 3), (660, 330, 3), (340, 330, 3)]):
    d.shape("ellipse", f"Spark {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=GOLD_HI, opacity=45, stroke=NONE)

paws = bust(d, lin(0, 520, 0, 772, (0, COAT), (0.55, COAT_LO), (1, COAT_DEEP)),
            half_top=60, half_bottom=190, paw_fill="#7E3A18", paw_line="#3A1608")
# chest blaze
d.path("M470,548 C458,620 458,704 470,762 L530,762 C542,704 542,620 530,548 "
       "C512,540 488,540 470,548 Z", "Chest blaze",
       fill=lin(0, 540, 0, 764, (0, "#E8C8A0"), (1, "#B08A62")), opacity=35, stroke=NONE)

# ears
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 64
    d.path(f"M{x:.1f},322 C{x - 20:.1f},286 {x - 10 + sign*8:.1f},258 {x + sign*6:.1f},248 "
           f"C{x + sign*26:.1f},270 {x + sign*26:.1f},300 {x + sign*18:.1f},330 Z",
           f"Ear {nm}", fill=lin(0, 250, 0, 334, (0, COAT_HI), (1, COAT_LO)),
           stroke=INK, strokeWidth=5)
    d.path(f"M{x + sign*2:.1f},314 C{x - 8:.1f},288 {x - 2:.1f},270 {x + sign*6:.1f},262 "
           f"C{x + sign*16:.1f},278 {x + sign*16:.1f},298 {x + sign*10:.1f},314 Z",
           f"Ear inner {nm}", fill="#D8A078", opacity=70, stroke=NONE)

# mane — dark flame locks down the right side of the neck
for i, (x, y, w, h, rot) in enumerate([(592, 350, 62, 110, 18), (616, 410, 70, 118, 8),
                                       (626, 478, 64, 110, -2), (612, 542, 54, 96, -10)]):
    d.path(f"M{x:.1f},{y:.1f} C{x + 46:.1f},{y + 18:.1f} {x + 56:.1f},{y + h*0.55:.1f} "
           f"{x + 20:.1f},{y + h:.1f} C{x + 4:.1f},{y + h*0.62:.1f} "
           f"{x - 8:.1f},{y + h*0.3:.1f} {x:.1f},{y:.1f} Z", f"Mane lock {i+1}",
           fill=lin(0, y, 0, y + h, (0, "#5A2A12"), (0.6, MANE), (1, "#180A04")),
           stroke=INK, strokeWidth=3)
    d.path(f"M{x + 14:.1f},{y + 16:.1f} C{x + 34:.1f},{y + h*0.3:.1f} "
           f"{x + 34:.1f},{y + h*0.6:.1f} {x + 20:.1f},{y + h*0.82:.1f}",
           f"Mane glint {i+1}", fill=NONE, stroke="#A86A3A", strokeWidth=3, opacity=45, cap="round")

# head — long face, three-quarter
HEAD = ("M500,300 C560,300 606,324 622,372 C636,414 632,462 614,500 "
        "C596,538 554,556 500,556 C446,556 404,538 386,500 "
        "C368,462 364,414 378,372 C394,324 440,300 500,300 Z")
d.path(HEAD, "Head", fill=lin(0, 300, 0, 556, (0, COAT_HI), (0.48, COAT), (1, COAT_LO)),
       stroke=INK, strokeWidth=7)
d.path("M456,306 C478,296 522,296 544,306 C536,326 464,326 456,306 Z",
       "Forelock", fill=MANE, stroke=INK, strokeWidth=3)
# blaze
d.path("M486,310 C512,310 520,318 520,336 L520,478 C520,502 512,516 500,516 "
       "C488,516 480,502 480,478 L480,336 C480,318 488,310 486,310 Z",
       "Blaze", fill=lin(0, 310, 0, 516, (0, "#FFF6E0"), (1, "#E0C8A0")),
       opacity=90, stroke=NONE)

# eyes
almond_eye(d, 432, 408, 68, 50, "Eye L", iris="#4A2A14", iris2="#1E0E06", look=(0.06, 0.04))
almond_eye(d, 568, 408, 68, 50, "Eye R", iris="#4A2A14", iris2="#1E0E06", look=(-0.06, 0.04))
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 66
    d.path(f"M{x - 30:.1f},380 Q{x:.1f},368 {x + 30:.1f},382", f"Brow {nm}",
           fill=NONE, stroke=MANE, strokeWidth=7, cap="round")

# gold browband
d.path("M388,362 C430,340 570,340 612,362", "Browband", fill=NONE,
       stroke=gold_lin(340, 366), strokeWidth=9, cap="round")
d.shape("ellipse", "Browband jewel", x=490, y=344, width=20, height=20,
        fill=rad((0, "#FFE8A8"), (1, "#C08A2E")), stroke=INK, strokeWidth=2)

# muzzle
d.path("M500,442 C542,442 566,462 570,490 C574,522 544,546 500,546 "
       "C456,546 426,522 430,490 C434,462 458,442 500,442 Z", "Muzzle",
       fill=lin(0, 442, 0, 546, (0, "#E8C8A4"), (1, "#B88A60")), stroke=NONE, opacity=95)
for sign, nm in ((-1, "L"), (1, "R")):
    d.shape("ellipse", f"Nostril {nm}", x=500 + sign*22 - 7, y=492, width=14, height=9,
            fill="#3A1E10", stroke=NONE)
d.path("M500,508 C510,516 514,526 508,534", "Lip", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
d.path("M500,534 C490,540 478,540 468,536 M500,534 C510,540 522,540 532,536",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
blush(d, 414, 466, 22, "Cheek L", color="#E08A5A", opacity=20)
blush(d, 586, 466, 22, "Cheek R", color="#E08A5A", opacity=20)

p.close()
