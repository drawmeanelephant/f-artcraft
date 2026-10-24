#!/usr/bin/env python3
"""Mandala — Symbol Plate V1R00. A twelve-fold cosmic diagram in gold and
rose on deep aubergine: 24 outer petals, 16 middle, 8 inner, an eight-point
star core. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, GOLD_LO, LATIN, DEVA,
                          lin, rad, gold_lin)
from orient.plate import Plate

p = Plate("Mandala — Symbol Plate", 1000, 1000)
d = p.d

p.backdrop(top="#241026", bottom="#08030A", glow=("#6A2A4A", 14))
p.stars(n=40, color="#F6D8B8", seed=23, maxr=2.4)
p.disc("#33142A", "#0E050C", rim="#D8B060", rim2="#5A3418")
p.ring_ticks(n=48, color=GOLD, width=1.6, r_in=392, r_out=402)
p.chop("मं", font=DEVA, size=30, w=54, h=54, x=872, y=94)

CX, CY = 500, 460
GOLD_FILL = lin(0, 180, 0, 740, (0, "#F8E0A0"), (0.45, "#E8C074"), (1, "#A87828"))

def petal(ang, r0, r1, w, label, fill=NONE, opacity=100, sw=2.2, stroke=GOLD):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    tx, ty = CX + ca * r1, CY + sa * r1
    bx, by = CX + ca * r0, CY + sa * r0
    nx, ny = -sa, ca
    c1 = (CX + ca * (r0 + (r1-r0)*0.35) + nx*w, CY + sa * (r0 + (r1-r0)*0.35) + ny*w)
    c2 = (CX + ca * (r0 + (r1-r0)*0.7) + nx*w*0.55, CY + sa * (r0 + (r1-r0)*0.7) + ny*w*0.55)
    c3 = (CX + ca * (r0 + (r1-r0)*0.7) - nx*w*0.55, CY + sa * (r0 + (r1-r0)*0.7) - ny*w*0.55)
    c4 = (CX + ca * (r0 + (r1-r0)*0.35) - nx*w, CY + sa * (r0 + (r1-r0)*0.35) - ny*w)
    d.path(f"M{bx + nx*w*0.25:.1f},{by + ny*w*0.25:.1f} "
           f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {tx:.1f},{ty:.1f} "
           f"C{c3[0]:.1f},{c3[1]:.1f} {c4[0]:.1f},{c4[1]:.1f} "
           f"{bx - nx*w*0.25:.1f},{by - ny*w*0.25:.1f} Z",
           label, fill=fill, opacity=opacity, stroke=stroke, strokeWidth=sw)

# outer ring
d.shape("ellipse", "Outer ring", x=CX-352, y=CY-352, width=704, height=704,
        fill=NONE, stroke=GOLD, strokeWidth=3)
d.shape("ellipse", "Outer ring 2", x=CX-338, y=CY-338, width=676, height=676,
        fill=NONE, stroke=GOLD, strokeWidth=1.4, opacity=55)
for i in range(24):
    ang = i * 15
    petal(ang, 296, 352, 26, f"Outer petal {i+1}", fill=lin(0, 160, 0, 760, (0, "#7A2A48"), (1, "#3A1024")),
          opacity=70, sw=2)
    # dot between petals
    a = math.radians(ang + 7.5)
    d.shape("ellipse", f"Outer dot {i+1}", x=CX + 350*math.cos(a) - 3,
            y=CY + 350*math.sin(a) - 3, width=6, height=6, fill=GOLD_HI, opacity=75, stroke=NONE)

# middle ring
d.shape("ellipse", "Middle ring", x=CX-292, y=CY-292, width=584, height=584,
        fill=NONE, stroke=GOLD, strokeWidth=2, opacity=80)
for i in range(16):
    petal(i * 22.5 + 11.25, 214, 286, 30, f"Middle petal {i+1}",
          fill=rad((0, "#D87090", 40), (1, "#D87090", 12)), opacity=100, sw=2)

# inner eight-petal lotus
d.shape("ellipse", "Inner ring", x=CX-208, y=CY-208, width=416, height=416,
        fill=NONE, stroke=GOLD, strokeWidth=2.4)
for i in range(8):
    petal(i * 45, 92, 202, 40, f"Inner petal {i+1}",
          fill=lin(0, 260, 0, 660, (0, "#F8DCA0"), (0.5, "#E0A860"), (1, "#A86A28")),
          opacity=88, sw=2.4)

# core: circles + 8-point star + rosette
d.shape("ellipse", "Core disc", x=CX-96, y=CY-96, width=192, height=192,
        fill=rad((0, "#F8E0A0"), (0.6, "#D8A858"), (1, "#8A5A1E")),
        stroke=INK, strokeWidth=3)
star = []
for i in range(16):
    ang = math.radians(-90 + i * 22.5)
    r = 84 if i % 2 == 0 else 34
    star.append((CX + r*math.cos(ang), CY + r*math.sin(ang)))
d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in star) + " Z",
       "Eight point star", fill=lin(0, 380, 0, 540, (0, "#8A2A44"), (1, "#3A0E1E")),
       stroke=GOLD_HI, strokeWidth=1.8)
for i in range(8):
    a = math.radians(i * 45)
    d.shape("ellipse", f"Core dot {i+1}", x=CX + 40*math.cos(a) - 4,
            y=CY + 40*math.sin(a) - 4, width=8, height=8, fill=GOLD_HI, opacity=85, stroke=NONE)
d.shape("ellipse", "Core jewel", x=CX-14, y=CY-14, width=28, height=28,
        fill=rad((0, "#FFF6D8"), (1, "#E0A040")), stroke=INK, strokeWidth=2)

# corner diamonds outside the disc, in the dark field
for x, y in ((120, 120), (880, 120), (120, 820), (880, 820)):
    d.path(f"M{x},{y-14} L{x+14},{y} L{x},{y+14} L{x-14},{y} Z",
           f"Corner diamond {x}-{y}", fill=NONE, stroke=GOLD, strokeWidth=1.4, opacity=45)

p.caption("MANDALA", "मंडल · COSMIC DIAGRAM", name_color="#F6E6C0",
          sub_color="#D8B060", name_size=54, sub_size=20, tracking_name=140,
          tracking_sub=120)
p.finish("mandala-V1R00")
