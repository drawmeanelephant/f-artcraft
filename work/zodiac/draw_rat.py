#!/usr/bin/env python3
"""Rat — Celestial Seal V1R00. Water element. A round-eared silver rat with
a long curling tail and a cash coin: the first branch, associated with
cleverness and stored wealth. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, lin, rad, gold_lin,
                          smooth, cloud, coin, blossom)
from orient.zodiac import ZodiacPlate, almond_eye, blush, fang, whisker, bust, scale_rows

p = ZodiacPlate("rat-V1R00", "RAT", "鼠", "子", "water", "2020 · 2032", "Rat")
d = p.d

FUR_HI = "#D8D2E4"
FUR = "#A79EB8"
FUR_LO = "#6C627E"
FUR_DEEP = "#453C56"
PINK = "#E8A8B8"
PINK_HI = "#F8D2DC"

cloud(d, 258, 250, 0.9, "Cloud upper L", fill=GOLD, opacity=12)
cloud(d, 742, 250, 0.9, "Cloud upper R", fill=GOLD, opacity=12)
for i, (x, y, r) in enumerate([(300, 560, 3), (700, 560, 3), (676, 320, 3), (324, 320, 3)]):
    d.shape("ellipse", f"Spark {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=GOLD_HI, opacity=45, stroke=NONE)

# tail, swept out to the right and curled
spine = [smooth([(640, 690), (742, 700), (790, 748), (762, 796), (710, 792)], closed=False)]
from orient.plate import smooth as sm
tail = [(640, 688), (700, 690), (752, 706), (778, 740), (772, 774), (744, 792), (716, 780)]
d.path(sm(tail), "Tail", fill=NONE, stroke=INK, strokeWidth=26, cap="round")
d.path(sm(tail), "Tail fur", fill=NONE, stroke=lin(0, 680, 0, 800, (0, FUR), (1, FUR_LO)),
       strokeWidth=19, cap="round")
d.path(sm(tail[:-2]), "Tail light", fill=NONE, stroke="#E8E2F0", strokeWidth=4,
       opacity=35, cap="round")
d.shape("ellipse", "Tail tip", x=706, y=768, width=24, height=20, fill=PINK, opacity=70, stroke=NONE)

paws = bust(d, lin(0, 520, 0, 772, (0, FUR), (0.55, FUR_LO), (1, FUR_DEEP)),
            half_top=52, half_bottom=182, paw_fill=FUR_HI, paw_line="#6A5A78")
# belly
d.path("M452,548 C440,620 440,700 452,762 L548,762 C560,700 560,620 548,548 "
       "C526,538 474,538 452,548 Z", "Belly",
       fill=lin(0, 540, 0, 764, (0, "#F2ECF6"), (1, "#C8BED6")), stroke=NONE, opacity=90)

# ears
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 118
    d.shape("ellipse", f"Ear {nm}", x=x - 64, y=286, width=128, height=136,
            fill=rad((0, FUR_HI), (0.65, FUR), (1, FUR_LO)), stroke=INK, strokeWidth=6,
            rotation=sign * 14)
    d.shape("ellipse", f"Ear inner {nm}", x=x - 42, y=306, width=84, height=98,
            fill=rad((0, PINK_HI), (0.7, PINK), (1, "#C87890")), opacity=80,
            stroke=NONE, rotation=sign * 14)

# head
HEAD = ("M500,302 C566,302 616,330 628,384 C640,436 620,482 584,504 "
        "C556,522 528,528 500,528 C472,528 444,522 416,504 "
        "C380,482 360,436 372,384 C384,330 434,302 500,302 Z")
d.path(HEAD, "Head", fill=lin(0, 302, 0, 528, (0, FUR_HI), (0.5, FUR), (1, FUR_LO)),
       stroke=INK, strokeWidth=7)
d.shape("ellipse", "Head light", x=414, y=320, width=172, height=54,
        fill="#FFFFFF", opacity=16, stroke=NONE)

# snout
d.path("M500,430 C540,430 566,448 566,472 C566,500 540,520 500,520 "
       "C460,520 434,500 434,472 C434,448 460,430 500,430 Z", "Snout",
       fill=rad((0, "#F4EEF8"), (1, "#CFC4DC")), stroke=NONE, opacity=95)
d.path("M500,452 C512,452 520,460 520,470 C520,482 512,490 500,490 "
       "C488,490 480,482 480,470 C480,460 488,452 500,452 Z", "Nose",
       fill=lin(0, 452, 0, 490, (0, "#F0A8B4"), (1, "#C87088")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=488, y=458, width=8, height=5, fill="#FFFFFF", opacity=60, stroke=NONE)
d.path("M500,490 L500,502", "Philtrum", fill=NONE, stroke=INK, strokeWidth=3.2, cap="round")
d.path("M500,502 C490,508 478,508 468,504 M500,502 C510,508 522,508 532,504",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3.2, cap="round")
# buck teeth
d.shape("rectangle", "Tooth L", x=490, y=504, width=9, height=14, radius=2,
        fill="#FFFDF2", stroke=INK, strokeWidth=1.6)
d.shape("rectangle", "Tooth R", x=501, y=504, width=9, height=14, radius=2,
        fill="#FFFDF2", stroke=INK, strokeWidth=1.6)

# eyes
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 58
    d.shape("ellipse", f"Eye {nm}", x=x - 17, y=388, width=34, height=40,
            fill="#1A1218", stroke=INK, strokeWidth=2)
    d.shape("ellipse", f"Eye glint {nm}", x=x - 6, y=396, width=11, height=11,
            fill="#FFFFFF", opacity=90, stroke=NONE)
    d.path(f"M{x - 26:.1f},378 Q{x:.1f},360 {x + 26:.1f},380",
           f"Eye shine {nm}", fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=35, cap="round")

# whiskers
for j, (y0, y1) in enumerate(((470, 446), (478, 478), (486, 512))):
    whisker(d, 440, y0, 348, y1 - 4, 250, y1, f"Whisker L{j+1}", color="#F4EEF8", sw=2.4, op=80)
    whisker(d, 560, y0, 652, y1 - 4, 750, y1, f"Whisker R{j+1}", color="#F4EEF8", sw=2.4, op=80)

# coin at the chest
coin(d, 500, 650, 54, "Cash coin")
d.text("財", "Coin glyph", x=500, y=665, size=40, font="Noto Sans CJK SC",
       color="#6E4A16", justify="center")

# paws over the coin rim
for cx, cy in paws:
    d.shape("ellipse", f"Paw front {cx}", x=cx - 26, y=cy - 12, width=52, height=36,
            fill=FUR_HI, stroke=INK, strokeWidth=3)
    for j, dx in enumerate((-12, 0, 12)):
        d.path(f"M{cx + dx:.1f},{cy + 4:.1f} L{cx + dx:.1f},{cy + 14:.1f}",
               f"Paw toe {cx}-{j}", fill=NONE, stroke="#6A5A78", strokeWidth=2, opacity=55, cap="round")

p.close()
