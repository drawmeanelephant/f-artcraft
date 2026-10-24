#!/usr/bin/env python3
"""Pig — Celestial Seal V1R00. Water element. A rose pig with a broad snout,
floppy ears, a curly tail and two little tusks: the last branch, the year
of the home. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, lin, rad, gold_lin,
                          smooth, cloud, coin, blossom)
from orient.zodiac import ZodiacPlate, blush, whisker, bust

p = ZodiacPlate("pig-V1R00", "PIG", "豬", "亥", "water", "2031 · 2043", "Pig")
d = p.d

PIG_HI = "#F6C0C0"
PIG = "#E098A0"
PIG_LO = "#B86A7A"
PIG_DEEP = "#7E3E50"
SNOUT = "#F2A8AE"

cloud(d, 252, 260, 0.9, "Cloud upper L", fill=GOLD, opacity=12)
cloud(d, 748, 260, 0.9, "Cloud upper R", fill=GOLD, opacity=12)
for i, (x, y, r) in enumerate([(300, 560, 3), (700, 560, 3), (660, 330, 3), (340, 330, 3)]):
    d.shape("ellipse", f"Spark {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=GOLD_HI, opacity=45, stroke=NONE)

# curly tail
sp = []
for i in range(36):
    t = i / 35
    a = t * 2.4 * math.pi
    r = 34 - t * 12
    sp.append((690 + r * math.cos(a), 700 + r * math.sin(a) + t * 8))
d.path(smooth(sp), "Tail", fill=NONE, stroke=INK, strokeWidth=18, cap="round")
d.path(smooth(sp), "Tail pink", fill=NONE, stroke=lin(0, 660, 0, 740, (0, PIG_HI), (1, PIG_LO)),
       strokeWidth=12, cap="round")
d.shape("ellipse", "Tail tuft", x=692, y=676, width=18, height=16, fill=PIG_LO, stroke=INK, strokeWidth=2)

paws = bust(d, lin(0, 520, 0, 772, (0, PIG), (0.55, PIG_LO), (1, PIG_DEEP)),
            half_top=60, half_bottom=188, paw_fill=PIG_HI, paw_line="#8A4A5A")
d.path("M452,550 C440,622 440,702 452,762 L548,762 C560,702 560,622 548,550 "
       "C526,540 474,540 452,550 Z", "Belly",
       fill=lin(0, 542, 0, 764, (0, "#F8D0D0"), (1, "#D898A2")), opacity=60, stroke=NONE)

# ears — floppy triangles
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 108
    d.path(f"M{x:.1f},338 C{x + sign*48:.1f},326 {x + sign*72:.1f},354 "
           f"{x + sign*64:.1f},410 C{x + sign*58:.1f},440 {x + sign*36:.1f},448 "
           f"{x + sign*20:.1f},430 C{x + sign*34:.1f},396 {x + sign*26:.1f},356 {x:.1f},338 Z",
           f"Ear {nm}", fill=lin(0, 330, 0, 448, (0, PIG), (1, PIG_LO)),
           stroke=INK, strokeWidth=5.5)
    d.path(f"M{x + sign*14:.1f},352 C{x + sign*38:.1f},346 {x + sign*50:.1f},368 "
           f"{x + sign*44:.1f},408", f"Ear inner {nm}", fill=NONE, stroke=PIG_HI,
           strokeWidth=7, opacity=55, cap="round")

# head
HEAD = ("M500,310 C570,310 620,338 634,392 C648,440 632,490 598,512 "
        "C568,532 534,538 500,538 C466,538 432,532 402,512 "
        "C368,490 352,440 366,392 C380,338 430,310 500,310 Z")
d.path(HEAD, "Head", fill=lin(0, 310, 0, 538, (0, PIG_HI), (0.5, PIG), (1, PIG_LO)),
       stroke=INK, strokeWidth=7)
d.path("M414,330 C450,314 550,314 586,330 C564,348 436,348 414,330 Z",
       "Forehead light", fill="#FFFFFF", opacity=20, stroke=NONE)

# eyes
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 62
    d.shape("ellipse", f"Eye {nm}", x=x - 17, y=396, width=34, height=32,
            fill="#2A1418", stroke=INK, strokeWidth=2)
    d.shape("ellipse", f"Eye glint {nm}", x=x - 5, y=402, width=10, height=10,
            fill="#FFFFFF", opacity=90, stroke=NONE)
    d.path(f"M{x - 24:.1f},382 Q{x:.1f},372 {x + 24:.1f},384", f"Lid {nm}",
           fill=NONE, stroke=PIG_LO, strokeWidth=4, opacity=55, cap="round")

# snout — the hero shape
d.path("M500,430 C548,430 578,450 582,482 C586,518 550,540 500,540 "
       "C450,540 414,518 418,482 C422,450 452,430 500,430 Z", "Snout",
       fill=lin(0, 430, 0, 540, (0, "#FFC8CE"), (0.6, SNOUT), (1, "#C87A86")),
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Snout sheen", x=446, y=448, width=108, height=34,
        fill="#FFFFFF", opacity=22, stroke=NONE)
for sign, nm in ((-1, "L"), (1, "R")):
    d.shape("ellipse", f"Nostril {nm}", x=500 + sign*24 - 9, y=482, width=18, height=26,
            fill="#6E2E40", stroke=INK, strokeWidth=1.8)
    d.shape("ellipse", f"Nostril glint {nm}", x=500 + sign*24 - 4, y=486, width=6, height=8,
            fill="#FFFFFF", opacity=25, stroke=NONE)
# mouth
d.path("M500,522 C510,530 520,530 528,524 M500,522 C490,530 480,530 472,524",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
# little tusks
for sign, nm in ((-1, "L"), (1, "R")):
    d.path(f"M{500 + sign*44:.1f},516 C{500 + sign*50:.1f},506 "
           f"{500 + sign*54:.1f},512 {500 + sign*52:.1f},524 "
           f"C{500 + sign*48:.1f},522 {500 + sign*46:.1f},520 {500 + sign*44:.1f},516 Z",
           f"Tusk {nm}", fill="#FFF6E0", stroke=INK, strokeWidth=1.8)
blush(d, 408, 458, 28, "Cheek L", color="#F0788A", opacity=32)
blush(d, 592, 458, 28, "Cheek R", color="#F0788A", opacity=32)

p.close()
