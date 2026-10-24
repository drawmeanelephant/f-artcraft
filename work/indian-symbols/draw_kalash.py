#!/usr/bin/env python3
"""Kalash — Symbol Plate V1R00. The sacred pot: mango leaves, coconut, red
cloth and gold coin, the vessel of plenty. Deep maroon and gold. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, GOLD_LO, LATIN, DEVA,
                          lin, rad, gold_lin, coin, mango_leaf)
from orient.plate import Plate

p = Plate("Kalash — Symbol Plate", 1000, 1000)
d = p.d

p.backdrop(top="#2A0E14", bottom="#080306", glow=("#7A2A2A", 14))
p.stars(n=40, color="#F6D8B8", seed=53, maxr=2.2)
p.disc("#3E121A", "#12040A", rim="#D8B060", rim2="#5A2A18")
p.ring_ticks(n=12, color=GOLD, width=2.2)
p.chop("कलश", font=DEVA, size=20, w=58, h=60, x=872, y=94, horizontal=True)

CX = 500

# prabhavali halo behind the pot
d.shape("ellipse", "Halo glow", x=180, y=140, width=640, height=640,
        fill=rad((0, "#E8A050", 12), (0.65, "#E8A050", 4), (1, "#E8A050", 0)), stroke=NONE)
d.shape("ellipse", "Halo ring", x=192, y=152, width=616, height=616,
        fill=NONE, stroke=GOLD, strokeWidth=2.4, opacity=55)
d.shape("ellipse", "Halo ring 2", x=210, y=170, width=580, height=580,
        fill=NONE, stroke=GOLD, strokeWidth=1.2, opacity=35)
for i in range(24):
    a = math.radians(i * 15)
    d.shape("ellipse", f"Halo dot {i+1}", x=CX + 308*math.cos(a) - 3,
            y=460 + 308*math.sin(a) - 3, width=6, height=6, fill=GOLD_HI, opacity=60, stroke=NONE)

# --- mango leaves ---------------------------------------------------------------
def leaf(cx, cy, ang, L, W, label):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    nx, ny = -sa, ca
    tx, ty = cx + ca * L, cy + sa * L
    d.path(f"M{cx + nx*W*0.45:.1f},{cy + ny*W*0.45:.1f} "
           f"C{cx + ca*L*0.3 + nx*W:.1f},{cy + sa*L*0.3 + ny*W:.1f} "
           f"{tx + nx*W*0.55:.1f},{ty + ny*W*0.55:.1f} {tx:.1f},{ty:.1f} "
           f"C{tx - nx*W*0.55:.1f},{ty - ny*W*0.55:.1f} "
           f"{cx + ca*L*0.3 - nx*W:.1f},{cy + sa*L*0.3 - ny*W:.1f} "
           f"{cx - nx*W*0.45:.1f},{cy - ny*W*0.45:.1f} Z",
           label, fill=lin(0, cy, 0, ty, (0, "#5AA86A"), (1, "#1E5A34")),
           stroke="#123A20", strokeWidth=2.2)
    d.path(f"M{cx:.1f},{cy:.1f} Q{cx + ca*L*0.55 + nx*W*0.25:.1f},{cy + sa*L*0.55 + ny*W*0.25:.1f} "
           f"{tx:.1f},{ty:.1f}", f"{label} vein", fill=NONE, stroke="#A8D8A0",
           strokeWidth=2, opacity=45, cap="round")

for i, (ang, L, W) in enumerate([(235, 150, 26), (252, 172, 28), (270, 186, 30),
                                  (288, 172, 28), (305, 150, 26)]):
    leaf(CX, 500, ang, L, W, f"Mango leaf {i+1}")

# coconut
d.shape("ellipse", "Coconut shadow", x=CX-42, y=398, width=84, height=90,
        fill="#000000", opacity=30, stroke=NONE)
d.shape("ellipse", "Coconut", x=CX-38, y=378, width=76, height=86,
        fill=rad((0, "#A87A4A"), (0.55, "#7A4E28"), (1, "#3E2410")),
        stroke=INK, strokeWidth=3)
for i, (dx, dy) in enumerate([(-12, 410), (2, 402), (16, 414)]):
    d.shape("ellipse", f"Coconut eye {i+1}", x=CX+dx-5, y=dy, width=10, height=10,
            fill="#2A1608", stroke=NONE)
for k in range(5):
    d.path(f"M{CX-30 + k*15:.1f},386 C{CX-34 + k*15:.1f},406 {CX-30 + k*15:.1f},426 "
           f"{CX-24 + k*15:.1f},440", f"Coconut fibre {k+1}", fill=NONE,
           stroke="#C89A6A", strokeWidth=1.6, opacity=25, cap="round")

# --- pot --------------------------------------------------------------------------
POT = ("M500,530 C588,530 636,592 636,674 C636,748 578,788 500,788 "
       "C422,788 364,748 364,674 C364,592 412,530 500,530 Z")
d.path(POT, "Pot", fill=lin(0, 530, 0, 788, (0, "#E8B060"), (0.35, "#C8862E"), (0.75, "#8A5A18"), (1, "#5A3A0E")),
       stroke=INK, strokeWidth=5)
# neck + rim
d.shape("rectangle", "Neck", x=CX-38, y=486, width=76, height=58, radius=6,
        fill=lin(0, 486, 0, 544, (0, "#D8A04E"), (1, "#8A5A1E")), stroke=INK, strokeWidth=4)
d.shape("ellipse", "Rim", x=CX-62, y=470, width=124, height=34,
        fill=lin(0, 470, 0, 504, (0, "#F8D890"), (1, "#A86A24")), stroke=INK, strokeWidth=4)
d.shape("ellipse", "Rim inner", x=CX-48, y=478, width=96, height=18,
        fill="#3A1E08", stroke=NONE, opacity=80)
# base
d.shape("rectangle", "Foot", x=CX-60, y=774, width=120, height=26, radius=6,
        fill=lin(0, 774, 0, 800, (0, "#D8A04E"), (1, "#7A4A16")), stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot shadow", x=CX-96, y=792, width=192, height=24,
        fill="#000000", opacity=30, stroke=NONE)

# gold bands
for y, hw in ((566, 86), (614, 122), (742, 112)):
    d.path(f"M{CX-hw:.1f},{y:.1f} Q500,{y+14:.1f} {CX+hw:.1f},{y:.1f}",
           f"Band {y}", fill=NONE, stroke=gold_lin(y, y + 16), strokeWidth=7, opacity=85)
# central medallion
d.shape("ellipse", "Medallion", x=CX-60, y=642, width=120, height=120,
        fill=rad((0, "#F8D890"), (0.6, "#D8A04E"), (1, "#8A5A1E")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Medallion inner", x=CX-42, y=660, width=84, height=84,
        fill="#7A2A1E", stroke=GOLD_HI, strokeWidth=2)
d.text("श्री", "Medallion glyph", x=CX, y=722, size=44, font=DEVA, color=GOLD_HI, justify="center")
# petal collar on the belly
for i in range(9):
    a = math.radians(210 + i * 15)
    x, y = CX + 92 * math.cos(a), 674 + 74 * math.sin(a)
    d.shape("ellipse", f"Belly petal {i+1}", x=x-10, y=y-6, width=20, height=12,
            fill=NONE, stroke=GOLD, strokeWidth=1.6, opacity=55,
            rotation=math.degrees(a) + 90)

# red cloth around the neck
d.path(f"M{CX-44:.1f},520 C{CX-20:.1f},540 {CX+20:.1f},540 {CX+44:.1f},520 "
       f"L{CX+52:.1f},552 C{CX+18:.1f},572 {CX-18:.1f},572 {CX-52:.1f},552 Z",
       "Cloth", fill=lin(0, 520, 0, 572, (0, "#D8403A"), (1, "#8E1F1E")),
       stroke=INK, strokeWidth=3)
for k, dx in enumerate((-28, -8, 14, 34)):
    d.path(f"M{CX+dx:.1f},552 C{CX+dx+4:.1f},578 {CX+dx+10:.1f},596 {CX+dx+6:.1f},612",
           f"Cloth tail {k+1}", fill=NONE, stroke="#C0332E", strokeWidth=5, cap="round")

# coins at the base
# a pair of coins leaning at the foot, not under it
for i, (dx, dy, r) in enumerate([(-150, 742, 24), (150, 742, 24)]):
    d.shape("ellipse", f"Coin {i+1}", x=CX + dx - r, y=dy - r, width=r*2, height=r*2,
            fill=rad((0, "#F8E0A0"), (0.6, "#D8A04E"), (1, "#8A5A1E")),
            stroke="#5A3A0E", strokeWidth=2.4)
    d.shape("ellipse", f"Coin ring {i+1}", x=CX + dx - r*0.62, y=dy - r*0.62,
            width=r*1.24, height=r*1.24, fill=NONE, stroke="#7A4A16", strokeWidth=1.4, opacity=55)
    d.path(f"M{CX+dx-8:.1f},{dy+8:.1f} L{CX+dx:.1f},{dy-8:.1f} L{CX+dx+8:.1f},{dy+8:.1f}",
           f"Coin mark {i+1}", fill=NONE, stroke="#7A4A16", strokeWidth=2, opacity=55, cap="round")

p.caption("KALASH", "कलश · VESSEL OF PLENTY", name_color="#F6E6C0",
          sub_color="#D8B060", name_size=54, sub_size=20, tracking_name=140,
          tracking_sub=110)
p.finish("kalash-V1R00")
