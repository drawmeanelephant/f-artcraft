#!/usr/bin/env python3
"""Ox — Celestial Seal V1R00. Earth element. A broad-browed water buffalo
with ivory horns, a gold nose ring and a bell: patience, ploughing, the
second branch. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, lin, rad, gold_lin,
                          smooth, cloud, coin, blossom)
from orient.zodiac import ZodiacPlate, almond_eye, blush, whisker, bust, curved_horn

p = ZodiacPlate("ox-V1R00", "OX", "牛", "丑", "earth", "2021 · 2033", "Ox")
d = p.d

HIDE_HI = "#B07A4E"
HIDE = "#845436"
HIDE_LO = "#4E2C18"
HIDE_DEEP = "#2E180C"
CREAM = "#F2DFC0"
IVORY = "#F0E2C0"

cloud(d, 250, 260, 0.95, "Cloud upper L", fill=GOLD, opacity=12)
cloud(d, 750, 260, 0.95, "Cloud upper R", fill=GOLD, opacity=12)
for i, (x, y, r) in enumerate([(300, 560, 3), (700, 560, 3), (668, 330, 3), (332, 330, 3)]):
    d.shape("ellipse", f"Spark {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=GOLD_HI, opacity=45, stroke=NONE)

paws = bust(d, lin(0, 520, 0, 772, (0, HIDE), (0.55, HIDE_LO), (1, HIDE_DEEP)),
            half_top=64, half_bottom=196, paw_fill="#6E4428", paw_line="#3A2212",
            collar=gold_lin(530, 550))
# bell
d.shape("ellipse", "Bell", x=478, y=596, width=44, height=46,
        fill=rad((0, "#F8D792"), (0.6, "#D9A24E"), (1, "#8A5A1E")),
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Bell mouth", x=482, y=628, width=36, height=12,
        fill="#8A5A1E", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Bell clapper", x=494, y=638, width=12, height=12,
        fill=GOLD, stroke=INK, strokeWidth=1.5)
d.path("M500,556 C490,570 490,584 500,596", "Bell cord", fill=NONE, stroke="#5A3A1A", strokeWidth=3, cap="round")

# belly
d.path("M448,552 C436,624 436,704 448,764 L552,764 C564,704 564,624 552,552 "
       "C528,540 472,540 448,552 Z", "Belly",
       fill=lin(0, 544, 0, 766, (0, "#E8CFA8"), (1, "#B08A5E")), opacity=85, stroke=NONE)

# ears
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 140
    d.shape("ellipse", f"Ear {nm}", x=x - 54, y=366, width=108, height=52,
            fill=lin(0, 360, 0, 420, (0, HIDE), (1, HIDE_LO)), stroke=INK,
            strokeWidth=5, rotation=sign * 16)
    d.shape("ellipse", f"Ear inner {nm}", x=x - 36, y=376, width=72, height=30,
            fill="#C88A64", opacity=60, stroke=NONE, rotation=sign * 16)

# horns
curved_horn(d, 420, 338, -1, 102, "Horn L", fill=lin(0, 210, 0, 340, (0, "#FFF6DC"), (1, "#C8AE7C")), width=52, curve=0.72)
curved_horn(d, 580, 338, 1, 102, "Horn R", fill=lin(0, 210, 0, 340, (0, "#FFF6DC"), (1, "#C8AE7C")), width=52, curve=0.72)

# head
HEAD = ("M500,300 C572,300 622,326 638,378 C652,424 642,472 610,498 "
        "C580,522 542,532 500,532 C458,532 420,522 390,498 "
        "C358,472 348,424 362,378 C378,326 428,300 500,300 Z")
d.path(HEAD, "Head", fill=lin(0, 300, 0, 532, (0, HIDE_HI), (0.5, HIDE), (1, HIDE_LO)),
       stroke=INK, strokeWidth=7)
d.path("M408,320 C442,302 558,302 592,320 C570,340 430,340 408,320 Z",
       "Forehead light", fill="#FFFFFF", opacity=14, stroke=NONE)
# forelock
for i, (x, y, rot) in enumerate([(470, 310, -16), (500, 304, 0), (530, 310, 16)]):
    d.path(f"M{x:.1f},{y:.1f} C{x - 12:.1f},{y + 26:.1f} {x - 6 + rot*0.4:.1f},{y + 48:.1f} "
           f"{x + rot*0.9:.1f},{y + 58:.1f} C{x + 14:.1f},{y + 38:.1f} "
           f"{x + 12:.1f},{y + 18:.1f} {x:.1f},{y:.1f} Z", f"Forelock {i+1}",
           fill=HIDE_LO, stroke=INK, strokeWidth=2.5)

# brows + eyes
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 66
    d.path(f"M{x - 30:.1f},382 Q{x:.1f},370 {x + 30:.1f},384", f"Brow {nm}",
           fill=NONE, stroke="#3A2212", strokeWidth=7, cap="round")
almond_eye(d, 434, 410, 66, 48, "Eye L", iris="#8A5A2E", iris2="#3E2412", look=(0.05, 0.06))
almond_eye(d, 566, 410, 66, 48, "Eye R", iris="#8A5A2E", iris2="#3E2412", look=(-0.05, 0.06))
blush(d, 414, 454, 24, "Cheek L", color="#D07A4E", opacity=22)
blush(d, 586, 454, 24, "Cheek R", color="#D07A4E", opacity=22)

# muzzle
d.path("M500,426 C548,426 578,446 582,476 C586,510 552,536 500,536 "
       "C448,536 414,510 418,476 C422,446 452,426 500,426 Z", "Muzzle",
       fill=lin(0, 426, 0, 536, (0, "#FBF0D8"), (1, "#DCC4A0")), stroke=INK, strokeWidth=4)
d.path("M462,464 C480,454 520,454 538,464 C534,484 520,494 500,494 "
       "C480,494 466,484 462,464 Z", "Nose",
       fill=lin(0, 454, 0, 494, (0, "#C88A78"), (1, "#8A4E42")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=478, y=460, width=18, height=7, fill="#FFFFFF", opacity=40, stroke=NONE)
for sign, nm in ((-1, "L"), (1, "R")):
    d.shape("ellipse", f"Nostril {nm}", x=500 + sign*17 - 4, y=470, width=9, height=7,
            fill="#4A2418", stroke=NONE)
d.path("M452,508 C474,520 486,518 500,510 C514,518 526,520 548,508",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3.6, cap="round")

# nose ring
d.shape("ellipse", "Nose ring", x=478, y=494, width=44, height=52,
        fill=NONE, stroke=gold_lin(490, 556), strokeWidth=7)
d.shape("ellipse", "Nose ring glint", x=482, y=498, width=22, height=24,
        fill=NONE, stroke="#FFF0C0", strokeWidth=2, opacity=55)

p.close()
