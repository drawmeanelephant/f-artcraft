#!/usr/bin/env python3
"""Dog — Celestial Seal V1R00. Earth element. A golden dog with drooping
ears, a red collar and a lolling tongue: loyalty, the eleventh branch.
1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, lin, rad, gold_lin,
                          smooth, cloud, coin, blossom)
from orient.zodiac import ZodiacPlate, almond_eye, blush, whisker, bust

p = ZodiacPlate("dog-V1R00", "DOG", "狗", "戌", "earth", "2030 · 2042", "Dog")
d = p.d

FUR_HI = "#E8B45E"
FUR = "#C08A36"
FUR_LO = "#8A5A1E"
EAR = "#6E4218"
CREAM = "#F8E8C8"

cloud(d, 252, 260, 0.9, "Cloud upper L", fill=GOLD, opacity=12)
cloud(d, 748, 260, 0.9, "Cloud upper R", fill=GOLD, opacity=12)
for i, (x, y, r) in enumerate([(300, 560, 3), (700, 560, 3), (660, 330, 3), (340, 330, 3)]):
    d.shape("ellipse", f"Spark {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=GOLD_HI, opacity=45, stroke=NONE)

# tail wagging at the right
d.path("M636,700 C690,686 726,654 736,614", "Tail", fill=NONE, stroke=INK,
       strokeWidth=30, cap="round")
d.path("M636,700 C690,686 726,654 736,614", "Tail fur", fill=NONE,
       stroke=lin(0, 610, 0, 710, (0, FUR_HI), (1, FUR_LO)), strokeWidth=23, cap="round")
d.path("M646,696 C690,684 720,656 728,624", "Tail light", fill=NONE,
       stroke="#F8DCA8", strokeWidth=4, opacity=40, cap="round")

paws = bust(d, lin(0, 520, 0, 772, (0, FUR), (0.55, FUR_LO), (1, "#4E2E0E")),
            half_top=58, half_bottom=186, paw_fill=FUR_HI, paw_line="#7A4A14")
d.path("M452,552 C440,624 440,702 452,762 L548,762 C560,702 560,624 548,552 "
       "C526,542 474,542 452,552 Z", "Chest",
       fill=lin(0, 544, 0, 764, (0, "#F8E0B8"), (1, "#C89A62")), opacity=80, stroke=NONE)

# collar
d.path("M438,548 C466,566 534,566 562,548", "Collar", fill=NONE,
       stroke=lin(0, 544, 0, 570, (0, "#D8403A"), (1, "#8E1F1E")),
       strokeWidth=18, cap="round")
d.shape("ellipse", "Collar tag", x=486, y=566, width=28, height=32,
        fill=rad((0, "#FFE8A0"), (1, "#C08A2E")), stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Collar tag hole", x=494, y=572, width=12, height=6,
        fill="#6E4A16", stroke=NONE, opacity=60)

# ears — drooping
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 126
    d.path(f"M{x:.1f},344 C{x + sign*44:.1f},340 {x + sign*66:.1f},380 "
           f"{x + sign*60:.1f},438 C{x + sign*56:.1f},486 {x + sign*34:.1f},510 "
           f"{x + sign*14:.1f},500 C{x + sign*30:.1f},456 {x + sign*26:.1f},392 {x:.1f},344 Z",
           f"Ear {nm}", fill=lin(0, 344, 0, 510, (0, "#8A561E"), (1, EAR)),
           stroke=INK, strokeWidth=5.5)

# head
HEAD = ("M500,310 C570,310 620,338 636,392 C650,440 634,490 600,512 "
        "C570,532 534,538 500,538 C466,538 430,532 400,512 "
        "C366,490 350,440 364,392 C380,338 430,310 500,310 Z")
d.path(HEAD, "Head", fill=lin(0, 310, 0, 538, (0, FUR_HI), (0.5, FUR), (1, FUR_LO)),
       stroke=INK, strokeWidth=7)
d.path("M414,330 C450,314 550,314 586,330 C564,348 436,348 414,330 Z",
       "Forehead light", fill="#FFFFFF", opacity=18, stroke=NONE)
# brow spots
for sign, nm in ((-1, "L"), (1, "R")):
    d.shape("ellipse", f"Brow spot {nm}", x=500 + sign*54 - 9, y=356, width=18, height=12,
            fill=CREAM, opacity=55, stroke=NONE)

# eyes
almond_eye(d, 436, 406, 70, 54, "Eye L", iris="#5A3410", iris2="#2A1404", look=(0.08, 0.03))
almond_eye(d, 564, 406, 70, 54, "Eye R", iris="#5A3410", iris2="#2A1404", look=(-0.08, 0.03))
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 64
    d.path(f"M{x - 28:.1f},376 Q{x:.1f},366 {x + 28:.1f},378", f"Brow {nm}",
           fill=NONE, stroke="#5A3410", strokeWidth=6, cap="round")

# muzzle
d.path("M500,436 C542,436 570,456 574,482 C578,514 546,538 500,538 "
       "C454,538 422,514 426,482 C430,456 458,436 500,436 Z", "Muzzle",
       fill=lin(0, 436, 0, 538, (0, "#FFF6E4"), (1, "#E4CCA4")), stroke=NONE, opacity=95)
d.path("M500,458 C520,458 534,470 534,484 C534,502 518,512 500,512 "
       "C482,512 466,502 466,484 C466,470 480,458 500,458 Z", "Nose",
       fill=lin(0, 458, 0, 512, (0, "#3A2A22"), (1, "#140C08")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=484, y=464, width=16, height=8, fill="#FFFFFF", opacity=35, stroke=NONE)
d.path("M500,512 L500,520", "Philtrum", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
d.path("M500,520 C488,528 472,528 460,522 M500,520 C512,528 528,528 540,522",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3.2, cap="round")
# tongue
d.path("M486,526 C486,548 494,562 504,562 C516,562 520,548 516,528 "
       "C506,534 496,534 486,526 Z", "Tongue",
       fill=lin(0, 526, 0, 562, (0, "#F08A96"), (1, "#C85068")), stroke=INK, strokeWidth=2.5)
d.path("M500,534 L500,554", "Tongue fold", fill=NONE, stroke="#B84058", strokeWidth=2, opacity=50, cap="round")
blush(d, 412, 456, 26, "Cheek L", color="#E8825E", opacity=22)
blush(d, 588, 456, 26, "Cheek R", color="#E8825E", opacity=22)
for j, (y0, y1) in enumerate(((478, 458), (486, 488), (494, 516))):
    whisker(d, 440, y0, 352, y1 - 2, 264, y1, f"Whisker L{j+1}", color="#FFF6E4", sw=2.2, op=70)
    whisker(d, 560, y0, 648, y1 - 2, 736, y1, f"Whisker R{j+1}", color="#FFF6E4", sw=2.2, op=70)

p.close()
