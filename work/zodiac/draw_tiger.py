#!/usr/bin/env python3
"""Tiger — Celestial Seal V1R00. Wood element. A round-eared tiger with
the 王 mark, cheek ruffs, and heavy stripes; the third branch. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, lin, rad, gold_lin,
                          smooth, cloud, coin, blossom)
from orient.zodiac import ZodiacPlate, almond_eye, blush, fang, whisker, bust

p = ZodiacPlate("tiger-V1R00", "TIGER", "虎", "寅", "wood", "2022 · 2034", "Tiger")
d = p.d

FUR_HI = "#F0A24E"
FUR = "#D06E24"
FUR_LO = "#94401A"
STRIPE = "#2A1610"
CREAM = "#F8E8C8"

cloud(d, 252, 258, 0.95, "Cloud upper L", fill=GOLD, opacity=12)
cloud(d, 748, 258, 0.95, "Cloud upper R", fill=GOLD, opacity=12)
for i, (x, y, r) in enumerate([(300, 560, 3), (700, 560, 3), (664, 330, 3), (336, 330, 3)]):
    d.shape("ellipse", f"Spark {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=GOLD_HI, opacity=45, stroke=NONE)

paws = bust(d, lin(0, 520, 0, 772, (0, FUR), (0.55, FUR_LO), (1, "#5A2410")),
            half_top=62, half_bottom=194, paw_fill=FUR_HI, paw_line="#7A3A14")
# body stripes
for sign, nm in ((-1, "L"), (1, "R")):
    for k, (dx, dy, w, h, rot) in enumerate([(118, 590, 18, 76, 12), (150, 650, 16, 66, 6),
                                              (108, 700, 14, 58, 2), (170, 720, 12, 48, -4)]):
        x = 500 + sign * dx
        d.path(f"M{x - w/2:.1f},{dy:.1f} C{x - w:.1f},{dy + h*0.3:.1f} "
               f"{x - w*0.8:.1f},{dy + h*0.7:.1f} {x - w*0.2:.1f},{dy + h:.1f} "
               f"C{x + w*0.4:.1f},{dy + h*0.6:.1f} {x + w*0.8:.1f},{dy + h*0.25:.1f} "
               f"{x + w/2:.1f},{dy:.1f} Z", f"Body stripe {nm}{k+1}",
               fill=STRIPE, opacity=88, stroke=NONE)
# belly
d.path("M450,548 C438,620 438,702 450,762 L550,762 C562,702 562,620 550,548 "
       "C528,538 472,538 450,548 Z", "Belly",
       fill=lin(0, 540, 0, 764, (0, "#FBF2DC"), (1, "#DCC49A")), opacity=92, stroke=NONE)

# ears
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 118
    d.shape("ellipse", f"Ear {nm}", x=x - 52, y=286, width=104, height=104,
            fill=lin(0, 286, 0, 390, (0, FUR_LO), (1, FUR)), stroke=INK, strokeWidth=6)
    d.shape("ellipse", f"Ear inner {nm}", x=x - 32, y=306, width=64, height=64,
            fill=rad((0, "#F8D8B0"), (1, "#C87A54")), opacity=75, stroke=NONE)

# cheek ruffs
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 118
    d.path(f"M{x:.1f},432 C{x + sign*44:.1f},420 {x + sign*66:.1f},444 "
           f"{x + sign*62:.1f},474 C{x + sign*56:.1f},504 {x + sign*30:.1f},516 "
           f"{x + sign*8:.1f},510 C{x + sign*26:.1f},492 {x + sign*28:.1f},462 {x:.1f},432 Z",
           f"Cheek ruff {nm}", fill=lin(0, 420, 0, 516, (0, "#FBF0D8"), (1, "#D8BE92")),
           stroke=INK, strokeWidth=4)
    for k in range(3):
        yy = 444 + k * 20
        d.path(f"M{x + sign*20:.1f},{yy:.1f} C{x + sign*38:.1f},{yy + 4:.1f} "
               f"{x + sign*48:.1f},{yy + 8:.1f} {x + sign*54:.1f},{yy + 14:.1f}",
               f"Ruff tuft {nm}{k+1}", fill=NONE, stroke="#B89464", strokeWidth=2.2,
               opacity=55, cap="round")

# head
HEAD = ("M500,296 C574,296 626,324 644,378 C660,426 650,478 618,506 "
        "C586,532 544,540 500,540 C456,540 414,532 382,506 "
        "C350,478 340,426 356,378 C374,324 426,296 500,296 Z")
d.path(HEAD, "Head", fill=lin(0, 296, 0, 540, (0, FUR_HI), (0.48, FUR), (1, FUR_LO)),
       stroke=INK, strokeWidth=7)
d.path("M414,318 C450,300 550,300 586,318 C564,336 436,336 414,318 Z",
       "Forehead light", fill="#FFFFFF", opacity=16, stroke=NONE)

# 王 forehead mark
for k, (y, w) in enumerate([(344, 58), (362, 46), (380, 58)]):
    d.path(f"M{500-w/2:.1f},{y:.1f} L{500+w/2:.1f},{y:.1f}", f"Wang bar {k+1}",
           fill=NONE, stroke=STRIPE, strokeWidth=8, cap="round")
d.path("M500,338 L500,382", "Wang stem", fill=NONE, stroke=STRIPE, strokeWidth=8, cap="round")

# forehead side stripes
for sign, nm in ((-1, "L"), (1, "R")):
    for k, (dx, dy, w) in enumerate([(100, 348, 38), (112, 382, 34), (108, 418, 30)]):
        x = 500 + sign * dx
        d.path(f"M{x:.1f},{dy:.1f} C{x + sign*w*0.5:.1f},{dy + 8:.1f} "
               f"{x + sign*w*0.6:.1f},{dy + 16:.1f} {x + sign*w*0.2:.1f},{dy + 24:.1f}",
               f"Head stripe {nm}{k+1}", fill=NONE, stroke=STRIPE, strokeWidth=9,
               opacity=90, cap="round")

# eyes
almond_eye(d, 434, 414, 72, 54, "Eye L", iris="#C8E07A", iris2="#6A8A2E", look=(0.08, 0.04))
almond_eye(d, 566, 414, 72, 54, "Eye R", iris="#C8E07A", iris2="#6A8A2E", look=(-0.08, 0.04))
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 62
    d.path(f"M{x - 34:.1f},378 Q{x:.1f},364 {x + 34:.1f},380", f"Brow {nm}",
           fill=NONE, stroke=STRIPE, strokeWidth=8, cap="round")

# muzzle
d.path("M500,438 C544,438 572,456 576,482 C580,514 548,538 500,538 "
       "C452,538 420,514 424,482 C428,456 456,438 500,438 Z", "Muzzle",
       fill=lin(0, 438, 0, 538, (0, "#FFF8E8"), (1, "#E4D0AC")), stroke=NONE, opacity=95)
d.path("M500,462 C520,462 532,474 532,486 C532,500 518,510 500,510 "
       "C482,510 468,500 468,486 C468,474 480,462 500,462 Z", "Nose",
       fill=lin(0, 462, 0, 510, (0, "#D89078"), (1, "#9A5040")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=485, y=468, width=16, height=6, fill="#FFFFFF", opacity=45, stroke=NONE)
d.path("M500,510 L500,520", "Philtrum", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
d.path("M500,520 C488,528 472,528 460,522 M500,520 C512,528 528,528 540,522",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3.4, cap="round")
fang(d, 470, 522, 13, 20, "Fang L")
fang(d, 530, 522, 13, 20, "Fang R")
for j, (y0, y1) in enumerate(((476, 452), (484, 484), (492, 516))):
    whisker(d, 440, y0, 350, y1 - 2, 256, y1, f"Whisker L{j+1}", color="#FFF8E8", sw=2.4)
    whisker(d, 560, y0, 650, y1 - 2, 744, y1, f"Whisker R{j+1}", color="#FFF8E8", sw=2.4)
blush(d, 412, 460, 24, "Cheek L", color="#E8705E", opacity=24)
blush(d, 588, 460, 24, "Cheek R", color="#E8705E", opacity=24)

p.close()
