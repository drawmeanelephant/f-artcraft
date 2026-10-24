#!/usr/bin/env python3
"""Rooster — Celestial Seal V1R00. Metal element. A proud gold rooster with
a lacquer comb, folded wing, and a fan of teal sickle feathers sweeping up
behind; the tenth branch. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, lin, rad, gold_lin,
                          smooth, cloud, coin, blossom, ribbon, bez)
from orient.zodiac import ZodiacPlate

p = ZodiacPlate("rooster-V1R00", "ROOSTER", "雞", "酉", "metal", "2029 · 2041", "Rooster")
d = p.d

PLUME_HI = "#5AB0A0"
PLUME = "#2E7A70"
PLUME_LO = "#16423C"
BODY_HI = "#E8A24E"
BODY_MID = "#C06A28"
BODY_LO = "#7A3812"
COMB = "#C8302A"
COMB_HI = "#F06A4A"
GOLD_F = "#F2C46A"

cloud(d, 252, 262, 0.9, "Cloud upper L", fill=GOLD, opacity=11)
cloud(d, 748, 262, 0.9, "Cloud upper R", fill=GOLD, opacity=11)
for i, (x, y, r) in enumerate([(300, 600, 3), (700, 600, 3), (640, 330, 3), (360, 330, 3)]):
    d.shape("ellipse", f"Spark {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=GOLD_HI, opacity=45, stroke=NONE)

# --- tail fan, right side --------------------------------------------------------
feathers = [
    ((606, 668), (690, 620), (726, 500), (700, 392), 36),
    ((604, 676), (716, 640), (788, 540), (774, 434), 32),
    ((602, 684), (722, 688), (812, 610), (808, 512), 28),
    ((600, 692), (692, 724), (760, 690), (776, 606), 24),
]
for i, (p0, p1, p2, p3, wd) in enumerate(feathers):
    spine = [bez(p0, p1, p2, p3, t) for t in [k/16 for k in range(17)]]
    widths = [wd * (0.55 + 0.45 * (1 - k/16)) for k in range(17)]
    dd, L, R, norms = ribbon(spine, widths)
    d.path(dd, f"Tail feather {i+1}",
           fill=lin(0, 420, 0, 700, (0, PLUME_HI), (0.55, PLUME), (1, PLUME_LO)),
           stroke=INK, strokeWidth=3)
    d.path(dd, f"Tail feather rim {i+1}", fill=NONE, stroke="#F2C46A",
           strokeWidth=2, opacity=45)
    for k in (5, 8, 11):
        (x, y), (nx, ny, w) = spine[k], norms[k]
        d.path(f"M{x - nx*w*0.6:.1f},{y - ny*w*0.6:.1f} L{x + nx*w*0.4:.1f},{y + ny*w*0.4:.1f}",
               f"Tail barb {i+1}-{k}", fill=NONE, stroke="#A8E0D0", strokeWidth=2,
               opacity=45, cap="round")

# red saddle at the tail root
d.path("M576,632 C612,640 630,664 626,700 C608,712 588,708 574,696 "
       "C582,674 582,650 576,632 Z", "Saddle", fill=lin(0, 632, 0, 708, (0, "#D8403A"), (1, "#8E1F1E")),
       stroke=INK, strokeWidth=3, opacity=90)

# --- body --------------------------------------------------------------------------
BODY = ("M410,706 C398,648 416,586 456,558 C482,540 518,540 544,558 "
        "C584,586 602,648 590,706 C584,752 552,776 500,776 "
        "C448,776 416,752 410,706 Z")
d.path(BODY, "Body", fill=lin(0, 540, 0, 776, (0, BODY_HI), (0.5, BODY_MID), (1, BODY_LO)),
       stroke=INK, strokeWidth=7)
# breast feathers
for i in range(3):
    y = 600 + i * 36
    w = 92 - i * 14
    d.path(f"M{500-w/2:.1f},{y:.1f} Q500,{y+26:.1f} {500+w/2:.1f},{y:.1f}",
           f"Breast feather {i+1}", fill=NONE, stroke="#F8C88E", strokeWidth=3,
           opacity=38, cap="round")

# folded wing (left)
WING = ("M438,606 C414,630 410,682 436,720 C458,750 490,758 512,740 "
        "C488,714 474,674 478,626 C462,608 448,602 438,606 Z")
d.path(WING, "Wing", fill=lin(0, 606, 0, 758, (0, "#E89A58"), (1, "#A85A24")),
       stroke=INK, strokeWidth=5)
for k in range(3):
    d.path(f"M{430 + k*4:.1f},{630 + k*34:.1f} Q{474 - k*4:.1f},{664 + k*28:.1f} "
           f"{512 - k*16:.1f},{702 + k*22:.1f}", f"Wing feather {k+1}",
           fill=NONE, stroke="#F8C08A", strokeWidth=4, opacity=60, cap="round")
for k in range(3):
    d.path(f"M{452 + k*16:.1f},{742 - k*4:.1f} Q{468 + k*12:.1f},{760 - k*4:.1f} "
           f"{484 + k*8:.1f},{748 - k*2:.1f}", f"Wing tip {k+1}",
           fill=NONE, stroke="#5A2A10", strokeWidth=3, opacity=45, cap="round")

# --- neck ---------------------------------------------------------------------------
NECK = ("M446,584 C438,516 456,468 484,446 L516,446 "
        "C544,468 562,516 554,584 C528,568 472,568 446,584 Z")
d.path(NECK, "Neck", fill=lin(0, 446, 0, 584, (0, "#F8D890"), (0.55, "#D89A3E"), (1, "#A8661E")),
       stroke=INK, strokeWidth=6)
for i in range(7):
    a = math.radians(198 + i * 24)
    x = 500 + math.cos(a) * 40
    y = 492 + math.sin(a) * 52
    d.path(f"M{x:.1f},{y:.1f} C{x - 10:.1f},{y + 22:.1f} {x - 2:.1f},{y + 40:.1f} "
           f"{x + 8:.1f},{y + 52:.1f} C{x + 18:.1f},{y + 32:.1f} "
           f"{x + 14:.1f},{y + 12:.1f} {x:.1f},{y:.1f} Z", f"Hackle {i+1}",
           fill=lin(0, y, 0, y + 52, (0, "#FBE0A0"), (1, "#C8882E")),
           stroke="#8A5A14", strokeWidth=2)

# --- head --------------------------------------------------------------------------
HEAD = ("M500,340 C546,340 578,364 586,402 C594,440 574,472 538,484 "
        "C522,490 512,492 500,492 C488,492 478,490 462,484 "
        "C426,472 406,440 414,402 C422,364 454,340 500,340 Z")
d.path(HEAD, "Head", fill=lin(0, 340, 0, 492, (0, "#FAD890"), (0.5, "#E0A64A"), (1, "#B07024")),
       stroke=INK, strokeWidth=6)
# comb
for i, (x, y, r) in enumerate([(464, 334, 24), (500, 320, 31), (536, 334, 24)]):
    d.path(f"M{x - r:.1f},{y + 18:.1f} C{x - r*1.1:.1f},{y - r*0.6:.1f} "
           f"{x - r*0.2:.1f},{y - r*1.1:.1f} {x:.1f},{y - r*0.5:.1f} "
           f"C{x + r*0.2:.1f},{y - r*1.1:.1f} {x + r*1.1:.1f},{y - r*0.6:.1f} "
           f"{x + r:.1f},{y + 18:.1f} Z", f"Comb {i+1}",
           fill=lin(0, y - r, 0, y + 18, (0, COMB_HI), (1, COMB)), stroke=INK, strokeWidth=2.5)
# wattles
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 20
    d.path(f"M{x:.1f},472 C{x + sign*16:.1f},496 {x + sign*14:.1f},524 "
           f"{x + sign*2:.1f},536 C{x - sign*10:.1f},520 {x - sign*12:.1f},494 {x:.1f},472 Z",
           f"Wattle {nm}", fill=lin(0, 472, 0, 536, (0, COMB_HI), (1, COMB)),
           stroke=INK, strokeWidth=2.5)
# eyes
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 38
    d.shape("ellipse", f"Eye {nm}", x=x - 17, y=400, width=34, height=34,
            fill=rad((0, "#FFF6D0"), (1, "#E8C060")), stroke=INK, strokeWidth=3.2)
    d.shape("ellipse", f"Pupil {nm}", x=x - 6, y=407, width=13, height=15,
            fill="#1A1208", stroke=NONE)
    d.shape("ellipse", f"Glint {nm}", x=x, y=403, width=5, height=5,
            fill="#FFFFFF", opacity=90, stroke=NONE)
# beak
d.path("M470,434 L500,422 L530,434 L500,460 Z", "Beak",
       fill=lin(0, 422, 0, 460, (0, "#F8D890"), (1, "#C08A2E")), stroke=INK, strokeWidth=3)
d.path("M470,434 L530,434", "Beak line", fill=NONE, stroke="#8A5A14", strokeWidth=2, opacity=55)

# --- feet ---------------------------------------------------------------------------
for sign, nm in ((-1, "L"), (1, "R")):
    fx = 500 + sign * 48
    d.path(f"M{fx:.1f},742 L{fx:.1f},784", f"Leg {nm}", fill=NONE, stroke="#D88A2E",
           strokeWidth=8, cap="round")
    for k, dx in enumerate((-20, 0, 20)):
        d.path(f"M{fx:.1f},782 L{fx + dx:.1f},796", f"Toe {nm}{k+1}", fill=NONE,
               stroke="#E8A040", strokeWidth=7, cap="round")

p.close()
