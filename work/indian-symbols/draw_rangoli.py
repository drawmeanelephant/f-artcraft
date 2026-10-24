#!/usr/bin/env python3
"""Rangoli — Symbol Plate V1R00. A floor mandala of coloured powders:
magenta, marigold, emerald and gold petals on warm terracotta, with the
white dot grid that holds the geometry. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, GOLD_LO, LATIN, DEVA,
                          lin, rad, gold_lin)
from orient.plate import Plate

p = Plate("Rangoli — Symbol Plate", 1000, 1000)
d = p.d

p.backdrop(top="#1A0E0A", bottom="#070302", glow=("#8A3A1E", 12))
p.stars(n=30, color="#F6D8B8", seed=61, maxr=2.0)
p.disc("#3A1A12", "#120604", rim="#D8B060", rim2="#4E2A14")
p.ring_ticks(n=12, color=GOLD, width=2.2)
p.chop("रंगोली", font=DEVA, size=16, w=64, h=64, x=868, y=94, horizontal=True)

CX, CY = 500, 460

def petal(ang, r0, r1, w, label, fill, edge, op=100, sw=2.4):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    tx, ty = CX + ca * r1, CY + sa * r1
    bx, by = CX + ca * r0, CY + sa * r0
    nx, ny = -sa, ca
    c1 = (CX + ca * (r0 + (r1-r0)*0.22) + nx*w*1.2, CY + sa * (r0 + (r1-r0)*0.22) + ny*w*1.2)
    c2 = (CX + ca * (r0 + (r1-r0)*0.74) + nx*w*0.8, CY + sa * (r0 + (r1-r0)*0.74) + ny*w*0.8)
    c3 = (CX + ca * (r0 + (r1-r0)*0.74) - nx*w*0.8, CY + sa * (r0 + (r1-r0)*0.74) - ny*w*0.8)
    c4 = (CX + ca * (r0 + (r1-r0)*0.22) - nx*w*1.2, CY + sa * (r0 + (r1-r0)*0.22) - ny*w*1.2)
    d.path(f"M{bx + nx*4:.1f},{by + ny*4:.1f} "
           f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {tx:.1f},{ty:.1f} "
           f"C{c3[0]:.1f},{c3[1]:.1f} {c4[0]:.1f},{c4[1]:.1f} "
           f"{bx - nx*4:.1f},{by - ny*4:.1f} Z",
           label, fill=fill, opacity=op, stroke=edge, strokeWidth=sw)

# floor wash
d.shape("ellipse", "Floor wash", x=CX-360, y=CY-360, width=720, height=720,
        fill=rad((0, "#6A2E1E", 55), (0.7, "#4A1E14", 30), (1, "#4A1E14", 0)), stroke=NONE)
d.shape("ellipse", "Outer chalk", x=CX-342, y=CY-342, width=684, height=684,
        fill=NONE, stroke="#F0E0C0", strokeWidth=2, opacity=40)
d.shape("ellipse", "Outer chalk 2", x=CX-328, y=CY-328, width=656, height=656,
        fill=NONE, stroke="#F0E0C0", strokeWidth=1.2, opacity=25)

# ring 1 — magenta, 24 petals
for i in range(24):
    petal(i * 15, 268, 340, 30, f"Magenta petal {i+1}",
          lin(0, 140, 0, 800, (0, "#F06A9A"), (1, "#A81E56")), "#6E1038", op=92)
    a = math.radians(i * 15 + 7.5)
    d.shape("ellipse", f"White dot outer {i+1}", x=CX + 352*math.cos(a) - 3,
            y=CY + 352*math.sin(a) - 3, width=6, height=6, fill="#FFF6E0", opacity=80, stroke=NONE)

# ring 2 — marigold, 18 petals
for i in range(18):
    petal(i * 20 + 10, 196, 258, 34, f"Marigold petal {i+1}",
          lin(0, 200, 0, 720, (0, "#FFC24E"), (1, "#D8701E")), "#8A3E0E", op=95)
    a = math.radians(i * 20)
    d.shape("ellipse", f"Green dot {i+1}", x=CX + 274*math.cos(a) - 4,
            y=CY + 274*math.sin(a) - 4, width=8, height=8, fill="#2E7A4A", opacity=85, stroke=NONE)

# ring 3 — emerald, 12 petals
for i in range(12):
    petal(i * 30, 128, 186, 38, f"Emerald petal {i+1}",
          lin(0, 280, 0, 640, (0, "#6AC88A"), (1, "#1E6A3E")), "#0E3A20", op=95)

# ring 4 — gold, 8 petals
for i in range(8):
    petal(i * 45, 58, 118, 40, f"Gold petal {i+1}",
          lin(0, 340, 0, 580, (0, "#FFE8A8"), (1, "#C88A2E")), "#7A4A16", op=98)

# core
d.shape("ellipse", "Core outer", x=CX-56, y=CY-56, width=112, height=112,
        fill=rad((0, "#F06A9A"), (0.6, "#C82E62"), (1, "#7A1038")), stroke="#FFF0C0", strokeWidth=3)
d.shape("ellipse", "Core inner", x=CX-32, y=CY-32, width=64, height=64,
        fill=rad((0, "#FFF6D8"), (0.6, "#F8C860"), (1, "#D88A2E")), stroke="#8A3E0E", strokeWidth=2)
d.shape("ellipse", "Core jewel", x=CX-12, y=CY-12, width=24, height=24,
        fill=rad((0, "#FFFDF0"), (1, "#F0C060")), stroke="#8A3E0E", strokeWidth=1.5)
for i in range(8):
    a = math.radians(i * 45 + 22.5)
    d.shape("ellipse", f"Core dot {i+1}", x=CX + 44*math.cos(a) - 3,
            y=CY + 44*math.sin(a) - 3, width=6, height=6, fill="#FFF6E0", opacity=90, stroke=NONE)

# corner flower marks outside the disc
for x, y in ((130, 130), (870, 130), (130, 790), (870, 790)):
    for k in range(4):
        a = math.radians(k * 90 + 45)
        d.shape("ellipse", f"Corner petal {x}-{y}-{k}", x=x + 16*math.cos(a) - 6,
                y=y + 16*math.sin(a) - 6, width=12, height=7, fill="#C82E62",
                opacity=55, stroke=NONE, rotation=math.degrees(a) + 90)
    d.shape("ellipse", f"Corner core {x}-{y}", x=x-3, y=y-3, width=6, height=6,
            fill=GOLD, opacity=70, stroke=NONE)

p.caption("RANGOLI", "रंगोली · WELCOME FLOOR ART", name_color="#F6E6C0",
          sub_color="#D8B060", name_size=54, sub_size=20, tracking_name=140,
          tracking_sub=110)
p.finish("rangoli-V1R00")
