#!/usr/bin/env python3
"""Rabbit — Celestial Seal V1R00. Wood element. A moon-pale rabbit with long
ears, a plum blossom in paw, and a soft green seal; the fourth branch. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, lin, rad, gold_lin,
                          smooth, cloud, coin, blossom)
from orient.zodiac import ZodiacPlate, almond_eye, blush, fang, whisker, bust

p = ZodiacPlate("rabbit-V1R00", "RABBIT", "兔", "卯", "wood", "2023 · 2035", "Rabbit")
d = p.d

FUR_HI = "#FFFDF6"
FUR = "#EFE6D4"
FUR_LO = "#C8BBA2"
PINK = "#F0A8B8"

cloud(d, 252, 256, 0.9, "Cloud upper L", fill=GOLD, opacity=12)
cloud(d, 748, 256, 0.9, "Cloud upper R", fill=GOLD, opacity=12)
d.shape("ellipse", "Moon glow", x=300, y=180, width=400, height=400,
        fill=rad((0, "#FFF6D8", 22), (1, "#FFF6D8", 0)), stroke=NONE)

paws = bust(d, lin(0, 520, 0, 772, (0, FUR), (0.55, FUR_LO), (1, "#9E9078")),
            half_top=50, half_bottom=176, paw_fill=FUR_HI, paw_line="#A89878")
# belly
d.path("M454,552 C444,624 444,702 454,762 L546,762 C556,702 556,624 546,552 "
       "C526,542 474,542 454,552 Z", "Belly",
       fill=lin(0, 544, 0, 764, (0, "#FFFFFF"), (1, "#E8DCC4")), opacity=95, stroke=NONE)

# ears — long, one slightly cocked
for sign, nm, tilt in ((-1, "L", -8), (1, "R", 9)):
    x = 500 + sign * 58
    d.path(f"M{x:.1f},330 C{x - 34:.1f},280 {x - 32 + sign*10:.1f},196 "
           f"{x + sign*6:.1f},166 C{x + sign*36:.1f},196 {x + sign*38:.1f},278 {x + sign*18:.1f},330 Z",
           f"Ear {nm}", fill=lin(0, 170, 0, 340, (0, FUR_HI), (0.6, FUR), (1, FUR_LO)),
           stroke=INK, strokeWidth=6)
    d.path(f"M{x:.1f},318 C{x - 14:.1f},270 {x - 12:.1f},214 {x + sign*4:.1f},186 "
           f"C{x + 16:.1f},214 {x + 16:.1f},270 {x + 4:.1f},318 Z",
           f"Ear inner {nm}", fill=rad((0, "#FFE0E6"), (0.6, PINK), (1, "#D08098")),
           opacity=75, stroke=NONE)

# head
HEAD = ("M500,304 C566,304 618,332 632,386 C644,436 626,484 590,508 "
        "C560,526 530,532 500,532 C470,532 440,526 410,508 "
        "C374,484 356,436 368,386 C382,332 434,304 500,304 Z")
d.path(HEAD, "Head", fill=lin(0, 304, 0, 532, (0, "#FFFFFF"), (0.55, FUR), (1, FUR_LO)),
       stroke=INK, strokeWidth=7)
d.path("M412,322 C448,306 552,306 588,322 C566,340 434,340 412,322 Z",
       "Forehead light", fill="#FFFFFF", opacity=55, stroke=NONE)

# eyes
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 58
    d.shape("ellipse", f"Eye {nm}", x=x - 15, y=396, width=30, height=38,
            fill="#3A1E22", stroke=INK, strokeWidth=2)
    d.shape("ellipse", f"Eye glint {nm}", x=x - 4, y=403, width=10, height=10,
            fill="#FFFFFF", opacity=92, stroke=NONE)
    d.path(f"M{x - 24:.1f},386 Q{x:.1f},372 {x + 24:.1f},388",
           f"Eye shine {nm}", fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=45, cap="round")

# muzzle
d.path("M500,440 C534,440 558,456 560,478 C562,506 536,524 500,524 "
       "C464,524 438,506 440,478 C442,456 466,440 500,440 Z", "Muzzle",
       fill="#FFFFFF", opacity=75, stroke=NONE)
d.shape("ellipse", "Nose", x=478, y=466, width=44, height=28,
        fill=lin(0, 466, 0, 494, (0, "#FFB8C6"), (1, "#D07890")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=488, y=470, width=10, height=5, fill="#FFFFFF", opacity=60, stroke=NONE)
d.path("M500,494 L500,506", "Philtrum", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
d.path("M500,506 C490,512 478,512 468,508 M500,506 C510,512 522,512 532,508",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
d.shape("rectangle", "Tooth", x=493, y=508, width=14, height=18, radius=2,
        fill="#FFFDF8", stroke=INK, strokeWidth=1.6)
d.path("M500,516 L500,524", "Tooth split", fill=NONE, stroke="#C8BBA2", strokeWidth=1.6)
blush(d, 414, 468, 30, "Cheek L", color="#F08A9A", opacity=35)
blush(d, 586, 468, 30, "Cheek R", color="#F08A9A", opacity=35)
for j, (y0, y1) in enumerate(((478, 458), (486, 488), (494, 516))):
    whisker(d, 444, y0, 360, y1 - 2, 274, y1, f"Whisker L{j+1}", color="#D8CBB4", sw=2.2, op=80)
    whisker(d, 556, y0, 640, y1 - 2, 726, y1, f"Whisker R{j+1}", color="#D8CBB4", sw=2.2, op=80)

# plum blossom held at the chest
d.path("M420,700 C400,678 390,658 398,642 C406,628 420,632 420,650 "
       "C420,632 434,628 442,642 C450,658 440,678 420,700 Z",
       "Branch leaf L", fill=lin(0, 618, 0, 690, (0, "#8AC0A0"), (1, "#3E7A5E")),
       stroke="#1E4A38", strokeWidth=2.5)
blossom(d, 420, 710, 44, petals=5, label="Plum blossom", fill="#FFD8E2",
        core="#C2455A", rot=-90)
d.path("M420,732 C400,746 384,752 372,748", "Blossom stem", fill=NONE,
       stroke="#5A3A1A", strokeWidth=4, cap="round")

p.close()
