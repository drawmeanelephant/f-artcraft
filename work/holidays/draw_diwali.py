#!/usr/bin/env python3
"""Diwali — Festival Seal V1R00.

The anchor of the Indian festival series. A tall-flamed clay diya on a
perspective rangoli, two lamps flanking it, marigold torana on the upper arc,
firework bursts in the corners. Deep plum, marigold, gold. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, GOLD_LO, PAPER, LATIN, DEVA,
                          PCX, PCY, PR, lin, rad, gold_lin, smooth, blend)
from festival_kit import (seal_disc, glow, dust, ring_dots, lamp, rangoli,
                          garland, firework, deva_seal, caption, leaf_at)

PLUM_HI = "#5A1838"
PLUM = "#3C0E26"
PLUM_LO = "#1B0511"
MARIGOLD = "#F2A33C"
MARIGOLD_LO = "#D9701C"
ROSE = "#D45C74"

p = __import__("orient.plate", fromlist=["Plate"]).Plate("Diwali — Festival Seal")
d = p.d

# --- field ------------------------------------------------------------------
p.backdrop(top="#1C0A18", bottom="#060307", glow=("#7A1E42", 16))
dust(d, n=46, r=402, colors=("#F6E3B8", "#F2A33C"), seed=23,
     smin=1.0, smax=2.6, opmin=8, opmax=26, label="Backdrop dust")
seal_disc(p, PLUM_HI, PLUM_LO, rim=GOLD, rim2="#5A2A12")
dust(d, n=64, r=392, colors=("#F6E3B8", "#F2A33C", "#E8C074"), seed=7,
     smin=1.0, smax=3.2, opmin=10, opmax=34, label="Disc dust")

# faint mandala field: 32 rays + concentric guides
for i in range(32):
    a = math.radians(i * 11.25)
    x0, y0 = PCX + 116 * math.cos(a), PCY + 116 * math.sin(a)
    x1, y1 = PCX + 378 * math.cos(a), PCY + 378 * math.sin(a)
    d.shape("line", f"Field ray {i+1}", x1=round(x0, 1), y1=round(y0, 1),
            x2=round(x1, 1), y2=round(y1, 1), stroke=GOLD, strokeWidth=1.6,
            opacity=9, cap="round")
for rr, op in ((150, 14), (232, 11), (312, 9)):
    d.shape("ellipse", f"Field ring {rr}", x=PCX - rr, y=PCY - rr,
            width=2 * rr, height=2 * rr, fill=NONE, stroke=GOLD,
            strokeWidth=1.4, opacity=op)
ring_dots(d, r=397, n=60, size=2.6, color=GOLD, opacity=34)

# --- rangoli floor ----------------------------------------------------------
glow(d, 500, 700, 330, "#C2455A", a=18, label="Rangoli glow", squash=0.36)
rangoli(d, 500, 702, 298, 100,
        col=(GOLD, MARIGOLD, "#C2455A", "#F6D9A0"), opacity=92, label="Rangoli")

# --- torana ----------------------------------------------------------------
garland(d, r=366, a0=-150, a1=-30, swags=4, sag=25, flower_r=15.5)

# --- fireworks -------------------------------------------------------------
firework(d, 268, 332, 64, col1=GOLD, col2=MARIGOLD, rays=18, seed=11,
         label="Firework L")
firework(d, 732, 332, 64, col1="#F0B26A", col2=ROSE, rays=18, seed=29,
         label="Firework R")

# --- lamps -----------------------------------------------------------------
lamp(d, 500, 628, 296, label="Central diya", flame_h=286, sparks=5, glow_a=30)
lamp(d, 272, 682, 142, label="Diya L", flame_h=132, glow_a=34)
lamp(d, 728, 682, 142, label="Diya R", flame_h=132, glow_a=34)

# --- stray petals and sparks ----------------------------------------------
for i, (x, y, s, ang, col) in enumerate([
        (338, 792, 9, -24, MARIGOLD), (402, 816, 7, 12, "#F6D9A0"),
        (612, 806, 8, -8, MARIGOLD), (676, 786, 10, 26, "#E8791F"),
        (366, 748, 6, 40, "#F6D9A0"), (642, 754, 6, -32, MARIGOLD)]):
    leaf_at(d, x, y, ang, s * 2.0, s * 0.52, fill=col, stroke="#8A4010",
            label=f"Fallen petal {i+1}", vein=False)
for i, (x, y, s) in enumerate([(410, 372, 3.0), (598, 348, 2.4),
                               (352, 516, 2.6), (666, 470, 3.2),
                               (500, 250, 2.4), (446, 300, 2.0)]):
    glow(d, x, y, 12, "#FFD98A", a=40, label=f"Spark glow {i+1}")
    d.shape("ellipse", f"Spark {i+1}", x=x - s, y=y - s, width=s * 2,
            height=s * 2, fill="#FFF2C4", opacity=85, stroke=NONE)

# --- seal and name ---------------------------------------------------------
deva_seal(d, "दीप", cx=744, cy=213, s=64, size=27)
caption(p, "DIWALI", "दीपावली · FESTIVAL OF LIGHTS",
        name_color="#F6E7C8", sub_color="#D8A85E",
        name_size=52, tracking_name=96, sub_size=20, tracking_sub=40)
p.finish("diwali-V1R00")
