#!/usr/bin/env python3
"""Dragon — Celestial Seal V1R00. Earth element. The only mythical beast in
the ring, so it gets the full ceremonial treatment: antlers, whiskers, a
flame mane, a pearl held between the forelegs. Front bust inside the
twelve-branch seal. 1000x1000. Gradients + translucent shading."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, GOLD_LO, lin, rad,
                          gold_lin, smooth, cloud, coin, blossom)
from orient.zodiac import (ZodiacPlate, almond_eye, brow, blush, fang,
                           whisker, scale_rows)

p = ZodiacPlate("dragon-V1R00", "DRAGON", "龍", "辰", "earth",
                "2024 · 2036", "Dragon")
d = p.d

JADE_HI = "#A8E0C0"
JADE = "#56A882"
JADE_LO = "#25624A"
JADE_DEEP = "#143C2C"
VERM = "#C03A28"
VERM_HI = "#EE8552"

# --- field ornament ------------------------------------------------------------
cloud(d, 238, 620, 1.0, "Cloud L", fill=GOLD, opacity=13)
cloud(d, 762, 600, 0.9, "Cloud R", fill=GOLD, opacity=11)
for i, (x, y, r) in enumerate([(300, 286, 3), (706, 268, 3), (742, 500, 3), (256, 502, 3)]):
    d.shape("ellipse", f"Spark {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=GOLD_HI, opacity=50, stroke=NONE)

# --- body / shoulders ----------------------------------------------------------
BODY = ("M300,772 C300,690 318,620 362,574 C398,538 442,520 500,520 "
        "C558,520 602,538 638,574 C682,620 700,690 700,772 Z")
d.path(BODY, "Body", fill=lin(0, 520, 0, 772, (0, JADE), (0.5, JADE_LO), (1, JADE_DEEP)),
       stroke=INK, strokeWidth=7)
d.path("M330,742 C334,660 354,606 398,572", "Shoulder light L",
       fill=NONE, stroke=JADE_HI, strokeWidth=11, opacity=24, cap="round")
d.path("M670,742 C666,660 646,606 602,572", "Shoulder light R",
       fill=NONE, stroke=JADE_HI, strokeWidth=11, opacity=18, cap="round")

# neck collar
d.path("M414,546 C446,528 554,528 586,546", "Collar", fill=NONE,
       stroke=gold_lin(528, 552), strokeWidth=13, cap="round")
d.path("M420,542 C450,526 550,526 580,542", "Collar light", fill=NONE,
       stroke="#FFF0C0", strokeWidth=3, opacity=55, cap="round")

scale_rows(d, 366, 596, 126, 7, "Shoulder scales L", color="#1E5240", hi="#9ADCB8")
scale_rows(d, 634, 596, 126, 7, "Shoulder scales R", color="#1E5240", hi="#9ADCB8")

# gold plastron
d.path("M442,542 C430,604 426,680 438,764 L562,764 C574,680 570,604 558,542 "
       "C538,532 462,532 442,542 Z", "Plastron",
       fill=lin(0, 535, 0, 766, (0, "#F8D792"), (0.45, "#DFA95A"), (1, "#8E5A1E")),
       stroke=INK, strokeWidth=4)
d.path("M450,552 C440,610 438,676 446,752", "Plastron light",
       fill=NONE, stroke="#FFF0C0", strokeWidth=7, opacity=32, cap="round")
for i in range(6):
    y = 566 + i * 32
    w = 126 - i * 6
    d.path(f"M{500 - w/2:.1f},{y:.1f} Q500,{y + 16:.1f} {500 + w/2:.1f},{y:.1f}",
           f"Plastron plate {i+1}", fill=NONE, stroke="#7A4A16", strokeWidth=2.3,
           opacity=48, cap="round")

# --- forelegs ---------------------------------------------------------------------
for sign, nm in ((-1, "L"), (1, "R")):
    x0 = 500 + sign * 142
    leg = (f"M{x0:.1f},586 C{x0 - sign*26:.1f},626 {x0 - sign*34:.1f},682 "
           f"{x0 - sign*26:.1f},724 L{x0 + sign*26:.1f},724 "
           f"C{x0 + sign*34:.1f},682 {x0 + sign*26:.1f},628 {x0 + sign*14:.1f},592 Z")
    d.path(leg, f"Foreleg {nm}", fill=lin(0, 590, 0, 726, (0, JADE), (1, JADE_DEEP)),
           stroke=INK, strokeWidth=6)
    for k, (dx, dy, r) in enumerate([(-10, 624, 9), (2, 650, 8), (8, 676, 7)]):
        d.path(f"M{x0 + sign*dx - r:.1f},{dy:.1f} A{r},{r*0.7:.1f} 0 0 1 {x0 + sign*dx + r:.1f},{dy:.1f}",
               f"Leg scale {nm}{k+1}", fill=NONE, stroke="#1E5240", strokeWidth=2, opacity=50, cap="round")
    d.path(f"M{x0 - sign*10:.1f},602 C{x0 - sign*22:.1f},640 {x0 - sign*20:.1f},690 {x0 - sign*16:.1f},714",
           f"Foreleg light {nm}", fill=NONE, stroke="#C8F0D8", strokeWidth=5, opacity=30, cap="round")

# --- ears (behind mane) ------------------------------------------------------------
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 136
    d.path(f"M{x:.1f},356 C{x + sign*38:.1f},322 {x + sign*54:.1f},352 "
           f"{x + sign*34:.1f},394 C{x + sign*20:.1f},414 {x + sign*4:.1f},396 {x + sign*2:.1f},374 Z",
           f"Ear {nm}", fill=lin(0, 330, 0, 410, (0, "#F2B25E"), (1, "#B55A24")),
           stroke=INK, strokeWidth=4)
    d.path(f"M{x + sign*10:.1f},360 C{x + sign*30:.1f},346 {x + sign*36:.1f},364 "
           f"{x + sign*26:.1f},384", f"Ear inner {nm}", fill=NONE,
           stroke="#F8DCA0", strokeWidth=4, opacity=55, cap="round")

# --- flame mane ---------------------------------------------------------------------
def lick(ang, length, width, curl, label, fill, base_r=114):
    a = math.radians(ang)
    rx, ry = math.cos(a), math.sin(a)
    tx, ty = -ry, rx
    bx, by = 500 + rx * base_r, 404 + ry * base_r
    tipx = bx + rx * length + tx * curl
    tipy = by + ry * length + ty * curl
    p0 = (bx + tx * width / 2, by + ty * width / 2)
    p1 = (bx - tx * width / 2, by - ty * width / 2)
    d.path(f"M{p0[0]:.1f},{p0[1]:.1f} "
           f"C{bx + rx*length*0.18 + tx*width*0.95:.1f},{by + ry*length*0.18 + ty*width*0.95:.1f} "
           f"{tipx + tx*width*0.1:.1f},{tipy + ty*width*0.1:.1f} {tipx:.1f},{tipy:.1f} "
           f"C{tipx - tx*width*0.45 + rx*8:.1f},{tipy - ty*width*0.45 + ry*8:.1f} "
           f"{p1[0] + rx*10:.1f},{p1[1] + ry*10:.1f} {p1[0]:.1f},{p1[1]:.1f} "
           f"Q{bx:.1f},{by:.1f} {p0[0]:.1f},{p0[1]:.1f} Z",
           label, fill=fill, stroke="#7A2418", strokeWidth=2.2)

for i, ang in enumerate(range(148, 397, 18)):
    ln = 110 + 26 * math.sin(i * 1.9)
    wd = 46 + 10 * math.cos(i * 1.3)
    curl = 22 if i % 2 == 0 else -20
    lick(ang, ln, wd, curl, f"Mane outer {i+1}", rad((0, VERM_HI), (1, VERM)))
for i, ang in enumerate(range(158, 388, 23)):
    lick(ang, 68 + 12 * math.cos(i * 1.2), 32, -14 if i % 2 else 14,
         f"Mane inner {i+1}", rad((0, "#F8CE84"), (1, "#C96A24")), base_r=108)

# --- antlers --------------------------------------------------------------------------
IVORY = "#F6E2B0"
def antler(sign, label):
    ax = 500 + sign * 64
    main = [(ax, 298), (ax + sign * 16, 248), (ax + sign * 28, 202), (ax + sign * 22, 158)]
    rear = [(ax - sign * 14, 302), (ax + sign * 2, 250), (ax + sign * 12, 208), (ax + sign * 8, 172)]
    for pts, nm, w_out, w_in in ((main, "main", 22, 14), (rear, "rear", 13, 7)):
        d.path(smooth(pts), f"{label} {nm}", fill=NONE, stroke=INK, strokeWidth=w_out, cap="round")
        d.path(smooth(pts), f"{label} {nm} ivory", fill=NONE, stroke=IVORY,
               strokeWidth=w_in, cap="round")
        d.path(smooth(pts), f"{label} {nm} shade", fill=NONE, stroke="#B58A4A",
               strokeWidth=max(2, w_in * 0.28), opacity=45, cap="round")
    for j, (bx, by, tx, ty) in enumerate([
            (ax + sign * 8, 254, ax + sign * 66, 236),
            (ax + sign * 20, 212, ax + sign * 82, 188),
            (ax + sign * 24, 174, ax + sign * 68, 138)]):
        d.path(f"M{bx:.1f},{by:.1f} Q{(bx+tx)/2 + sign*8:.1f},{ty - 12:.1f} {tx:.1f},{ty:.1f}",
               f"{label} tine {j+1}", fill=NONE, stroke=INK, strokeWidth=14, cap="round")
        d.path(f"M{bx:.1f},{by:.1f} Q{(bx+tx)/2 + sign*8:.1f},{ty - 12:.1f} {tx:.1f},{ty:.1f}",
               f"{label} tine ivory {j+1}", fill=NONE, stroke=IVORY, strokeWidth=8, cap="round")

antler(-1, "Antler L")
antler(1, "Antler R")

# --- head ------------------------------------------------------------------------------
HEAD = ("M500,278 C574,278 628,304 648,356 C664,400 658,450 632,490 "
        "C602,536 552,556 500,556 C448,556 398,536 368,490 "
        "C342,450 336,400 352,356 C372,304 426,278 500,278 Z")
d.path(HEAD, "Head", fill=lin(0, 278, 0, 556, (0, JADE_HI), (0.42, JADE), (1, JADE_LO)),
       stroke=INK, strokeWidth=7)
d.path("M414,296 C450,282 550,282 586,298 C566,314 434,314 414,296 Z",
       "Forehead light", fill="#FFFFFF", opacity=18, stroke=NONE)
for i, (x, y, r) in enumerate([(500, 326, 11), (482, 344, 9), (518, 344, 9), (500, 360, 9)]):
    d.path(f"M{x-r:.1f},{y:.1f} A{r},{r*0.8:.1f} 0 0 1 {x+r:.1f},{y:.1f}",
           f"Forehead scale {i+1}", fill=NONE, stroke="#2A6A50", strokeWidth=2.3,
           opacity=50, cap="round")
d.path("M500,336 L508,438 L500,448 L492,438 Z", "Nose ridge",
       fill=lin(0, 336, 0, 448, (0, "#F8D792"), (1, "#C08A3E")), opacity=35, stroke=NONE)

for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 68
    d.path(f"M{x:.1f},350 C{x + sign*34:.1f},330 {x + sign*60:.1f},344 "
           f"{x + sign*66:.1f},370 C{x + sign*38:.1f},356 {x + sign*18:.1f},356 {x:.1f},364 Z",
           f"Brow {nm}", fill=lin(0, 330, 0, 372, (0, VERM_HI), (1, VERM)),
           stroke="#7A2418", strokeWidth=3)

almond_eye(d, 434, 404, 80, 58, "Eye L", iris="#FFD36A", iris2="#C07A1E", look=(0.1, 0.04))
almond_eye(d, 566, 404, 80, 58, "Eye R", iris="#FFD36A", iris2="#C07A1E", look=(-0.1, 0.04))
blush(d, 420, 450, 26, "Cheek L", color="#F08A5A", opacity=22)
blush(d, 580, 450, 26, "Cheek R", color="#F08A5A", opacity=22)
for sign, nm in ((-1, "L"), (1, "R")):
    for k, (dx, dy, r) in enumerate([(52, 472, 6), (44, 492, 5), (36, 510, 5)]):
        d.path(f"M{500 + sign*dx - r:.1f},{dy:.1f} A{r},{r*0.8:.1f} 0 0 1 {500 + sign*dx + r:.1f},{dy:.1f}",
               f"Cheek scale {nm}{k+1}", fill=NONE, stroke="#2A6A50", strokeWidth=2,
               opacity=42, cap="round")

MUZ = ("M500,430 C536,430 562,442 570,464 C576,486 560,510 534,518 "
       "C520,523 508,525 500,525 C492,525 480,523 466,518 "
       "C440,510 424,486 430,464 C438,442 464,430 500,430 Z")
d.path(MUZ, "Muzzle", fill=lin(0, 430, 0, 525, (0, "#E8F6DC"), (1, "#A8D8BC")),
       stroke=INK, strokeWidth=4)
d.path("M464,464 C480,454 520,454 536,464 C532,482 518,492 500,492 "
       "C482,492 468,482 464,464 Z", "Nose",
       fill=lin(0, 454, 0, 492, (0, "#3E7A60"), (1, "#183C2C")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=480, y=460, width=20, height=8, fill="#FFFFFF", opacity=40, stroke=NONE)
for sign, nm in ((-1, "L"), (1, "R")):
    d.shape("ellipse", f"Nostril {nm}", x=500 + sign*16 - 5, y=472,
            width=10, height=7, fill="#0E241A", stroke=NONE)

d.path("M448,504 C470,516 486,514 500,506 C514,514 530,516 552,504",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=4.2, cap="round")
fang(d, 472, 508, 15, 25, "Fang L")
fang(d, 528, 508, 15, 25, "Fang R")
d.path("M500,525 C512,548 520,572 514,604 C506,590 502,588 496,606 "
       "C488,576 488,548 500,525 Z", "Beard",
       fill=lin(0, 525, 0, 606, (0, VERM_HI), (1, VERM)), stroke="#7A2418", strokeWidth=3)
d.path("M500,534 C505,556 507,576 505,592", "Beard light", fill=NONE,
       stroke="#FFC48A", strokeWidth=2.4, opacity=55, cap="round")

whisker(d, 444, 482, 336, 474, 232, 404, "Whisker L1", sw=3.6)
whisker(d, 442, 494, 326, 508, 218, 490, "Whisker L2", sw=3.0)
whisker(d, 556, 482, 664, 474, 768, 404, "Whisker R1", sw=3.6)
whisker(d, 558, 494, 674, 508, 782, 490, "Whisker R2", sw=3.0)
for x, y, s, nm in ((232, 404, -1, "L"), (768, 404, 1, "R")):
    d.path(f"M{x:.1f},{y:.1f} C{x + s*18:.1f},{y - 24:.1f} {x + s*42:.1f},{y - 12:.1f} "
           f"{x + s*30:.1f},{y + 8:.1f}", f"Whisker curl {nm}", fill=NONE,
           stroke=GOLD_HI, strokeWidth=3, opacity=80, cap="round")

# --- pearl ---------------------------------------------------------------------------
d.shape("ellipse", "Pearl halo", x=386, y=540, width=228, height=228,
        fill=rad((0, "#FFE9B0", 45), (0.5, "#FFC46B", 12), (1, "#FFC46B", 0)), stroke=NONE)
for i, ang in enumerate((18, 68, 120, 172, 224, 276, 328)):
    a = math.radians(ang)
    bx, by = 500 + 60 * math.cos(a), 652 + 60 * math.sin(a)
    tx, ty = -math.sin(a), math.cos(a)
    L = 30 if i % 2 else 40
    tipx, tipy = bx + math.cos(a) * L + tx * 10, by + math.sin(a) * L + ty * 10
    d.path(f"M{bx + tx*8:.1f},{by + ty*8:.1f} Q{tipx:.1f},{tipy:.1f} "
           f"{bx - tx*8:.1f},{by - ty*8:.1f} Q{bx:.1f},{by:.1f} "
           f"{bx + tx*8:.1f},{by + ty*8:.1f} Z", f"Pearl flame {i+1}",
           fill=lin(0, 600, 0, 720, (0, "#FFE6A8"), (1, "#E88232")), opacity=90, stroke=NONE)

d.shape("ellipse", "Pearl", x=456, y=608, width=88, height=88,
        fill=rad((0, "#FFFFFF"), (0.55, "#F6E2B0"), (1, "#C9A056")),
        stroke=INK, strokeWidth=3.4)
d.shape("ellipse", "Pearl glint", x=470, y=618, width=28, height=18,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M500,640 C508,654 516,662 508,674", "Pearl reflection", fill=NONE,
       stroke="#FFF8E0", strokeWidth=3, opacity=55, cap="round")

# --- claws ----------------------------------------------------------------------------
def claw(cx, cy, label):
    d.shape("ellipse", f"{label} palm", x=cx - 25, y=cy - 20, width=50, height=40,
            fill=lin(0, cy - 22, 0, cy + 20, (0, "#F6CE86"), (1, "#B57A2E")),
            stroke=INK, strokeWidth=3)
    for j, (dx, dy) in enumerate([(-16, 2), (-4, 8), (8, 8), (18, 2)]):
        d.path(f"M{cx + dx:.1f},{cy + dy:.1f} Q{cx + dx * 1.15:.1f},{cy + dy + 22:.1f} "
               f"{cx + dx * 1.25:.1f},{cy + dy + 34:.1f}", f"{label} claw {j+1}",
               fill=NONE, stroke="#F8E0A8", strokeWidth=5, cap="round")

claw(366, 736, "Claw L")
claw(634, 736, "Claw R")

p.close()
