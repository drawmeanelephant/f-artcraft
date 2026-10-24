#!/usr/bin/env python3
"""Goat — Celestial Seal V1R00. Earth element. An ivory mountain goat with
swept-back horns, a beard, and the horizontal pupil that gives goats their
unsettling calm; the eighth branch. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, lin, rad, gold_lin,
                          smooth, cloud, coin, blossom)
from orient.zodiac import ZodiacPlate, almond_eye, blush, bust, curved_horn

p = ZodiacPlate("goat-V1R00", "GOAT", "羊", "未", "earth", "2027 · 2039", "Goat")
d = p.d

FUR_HI = "#FFFDF4"
FUR = "#EFE4CA"
FUR_LO = "#C8B896"
FUR_DEEP = "#96866A"
HORN = "#D8C49A"

cloud(d, 250, 262, 0.9, "Cloud upper L", fill=GOLD, opacity=12)
cloud(d, 750, 262, 0.9, "Cloud upper R", fill=GOLD, opacity=12)
for i, (x, y, r) in enumerate([(300, 560, 3), (700, 560, 3), (662, 330, 3), (338, 330, 3)]):
    d.shape("ellipse", f"Spark {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=GOLD_HI, opacity=45, stroke=NONE)

paws = bust(d, lin(0, 520, 0, 772, (0, FUR), (0.55, FUR_LO), (1, FUR_DEEP)),
            half_top=54, half_bottom=180, paw_fill=FUR_HI, paw_line="#8A7A5E",
            collar=gold_lin(530, 550))
# shaggy chest
for i, (x, y, w, h) in enumerate([(440, 570, 60, 120), (500, 580, 66, 140), (560, 570, 60, 120)]):
    d.path(f"M{x:.1f},{y:.1f} C{x - w*0.7:.1f},{y + h*0.3:.1f} {x - w*0.3:.1f},{y + h*0.8:.1f} "
           f"{x:.1f},{y + h:.1f} C{x + w*0.3:.1f},{y + h*0.8:.1f} {x + w*0.7:.1f},{y + h*0.3:.1f} "
           f"{x:.1f},{y:.1f} Z", f"Chest shag {i+1}",
           fill=lin(0, y, 0, y + h, (0, "#FFFDF4"), (1, "#D8C8A8")), opacity=65, stroke=NONE)

# ears — horizontal
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 142
    d.shape("ellipse", f"Ear {nm}", x=x - 58, y=372, width=116, height=46,
            fill=lin(0, 370, 0, 418, (0, FUR), (1, FUR_LO)), stroke=INK,
            strokeWidth=5, rotation=sign * 12)
    d.shape("ellipse", f"Ear inner {nm}", x=x - 40, y=380, width=80, height=26,
            fill="#E8C8B8", opacity=60, stroke=NONE, rotation=sign * 12)

# horns — swept back and out
curved_horn(d, 432, 338, -1, 128, "Horn L", fill=lin(0, 210, 0, 342, (0, "#F4E8C8"), (1, "#A88E60")),
            width=30, curve=0.78)
curved_horn(d, 568, 338, 1, 128, "Horn R", fill=lin(0, 210, 0, 342, (0, "#F4E8C8"), (1, "#A88E60")),
            width=30, curve=0.78)

# head
HEAD = ("M500,306 C568,306 616,334 630,388 C642,438 624,486 590,510 "
        "C560,530 530,536 500,536 C470,536 440,530 410,510 "
        "C376,486 358,438 370,388 C384,334 432,306 500,306 Z")
d.path(HEAD, "Head", fill=lin(0, 306, 0, 536, (0, FUR_HI), (0.55, FUR), (1, FUR_LO)),
       stroke=INK, strokeWidth=7)
d.path("M414,324 C450,308 550,308 586,324 C564,342 436,342 414,324 Z",
       "Forehead light", fill="#FFFFFF", opacity=45, stroke=NONE)
# forelock
for i, (x, y, rot) in enumerate([(478, 314, -14), (500, 310, 0), (522, 314, 14)]):
    d.path(f"M{x:.1f},{y:.1f} C{x - 10:.1f},{y + 24:.1f} {x - 4 + rot*0.4:.1f},{y + 44:.1f} "
           f"{x + rot*0.8:.1f},{y + 54:.1f} C{x + 12:.1f},{y + 34:.1f} "
           f"{x + 10:.1f},{y + 16:.1f} {x:.1f},{y:.1f} Z", f"Forelock {i+1}",
           fill="#E8DCC0", stroke="#A89878", strokeWidth=2, opacity=80)

# eyes with horizontal pupils
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 62
    d.shape("ellipse", f"Eye {nm}", x=x - 24, y=394, width=48, height=40,
            fill=rad((0, "#E8D8A8"), (1, "#C8B080")), stroke=INK, strokeWidth=3.5)
    d.shape("ellipse", f"Iris {nm}", x=x - 16, y=398, width=32, height=28,
            fill="#C89A4E", stroke=NONE)
    d.shape("rectangle", f"Pupil {nm}", x=x - 17, y=397, width=34, height=11, radius=5,
            fill="#1A1208", stroke=NONE)
    d.shape("ellipse", f"Glint {nm}", x=x - 6, y=402, width=6, height=6,
            fill="#FFFFFF", opacity=85, stroke=NONE)
    d.path(f"M{x - 28:.1f},384 Q{x:.1f},374 {x + 28:.1f},386", f"Brow {nm}",
           fill=NONE, stroke="#8A7A5E", strokeWidth=5, opacity=55, cap="round")

# muzzle
d.path("M500,438 C538,438 562,456 564,482 C566,512 538,532 500,532 "
       "C462,532 434,512 436,482 C438,456 462,438 500,438 Z", "Muzzle",
       fill="#FFFDF4", opacity=85, stroke=NONE)
d.path("M500,466 C514,466 524,474 524,484 C524,496 514,504 500,504 "
       "C486,504 476,496 476,484 C476,474 486,466 500,466 Z", "Nose",
       fill=lin(0, 466, 0, 504, (0, "#D8B0A0"), (1, "#9A6A5A")), stroke=INK, strokeWidth=3)
d.path("M500,504 L500,514", "Philtrum", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
d.path("M500,514 C490,520 478,520 468,516 M500,514 C510,520 522,520 532,516",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
# beard
d.path("M500,532 C514,558 522,592 512,640 C506,620 502,618 498,642 "
       "C488,604 486,560 500,532 Z", "Beard",
       fill=lin(0, 532, 0, 622, (0, "#F4E8CE"), (1, "#C0B08E")), stroke="#8A7A5E", strokeWidth=2.5)
for k, dx in enumerate((-8, 0, 8)):
    d.path(f"M{500 + dx:.1f},{540:.1f} C{500 + dx*1.4:.1f},{560:.1f} "
           f"{500 + dx*1.3:.1f},{584:.1f} {500 + dx*1.1:.1f},{600:.1f}",
           f"Beard strand {k+1}", fill=NONE, stroke="#FFFDF4", strokeWidth=2, opacity=60, cap="round")
blush(d, 414, 462, 26, "Cheek L", color="#E8A08A", opacity=28)
blush(d, 586, 462, 26, "Cheek R", color="#E8A08A", opacity=28)

p.close()
