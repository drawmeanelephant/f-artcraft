#!/usr/bin/env python3
"""Lotus — Symbol Plate V1R00. A full moon behind a five-row padma in rose
and gold, rising from still water. Purity, awakening. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, GOLD_LO, LATIN, DEVA,
                          lin, rad, gold_lin)
from orient.plate import Plate

p = Plate("Lotus — Symbol Plate", 1000, 1000)
d = p.d

p.backdrop(top="#0E1A26", bottom="#04070A", glow=("#2A5A6A", 14))
p.stars(n=44, color="#F6E3B8", seed=31, maxr=2.4)
p.disc("#122A34", "#050E12", rim="#D8B060", rim2="#4E3A18")
p.ring_ticks(n=12, color=GOLD, width=2.2)
p.chop("कमल", font=DEVA, size=21, w=58, h=140, x=872, y=94)

CX, CY = 500, 690
# moon
d.shape("ellipse", "Moon halo", x=250, y=150, width=500, height=500,
        fill=rad((0, "#FFF0C8", 30), (0.55, "#FFF0C8", 10), (1, "#FFF0C8", 0)), stroke=NONE)
d.shape("ellipse", "Moon", x=300, y=200, width=400, height=400,
        fill=rad((0, "#FFFDF0"), (0.7, "#F4E6C0"), (1, "#D8C08A")), stroke=NONE)
for i, (x, y, r, op) in enumerate([(390, 300, 26, 8), (560, 260, 34, 7), (620, 390, 22, 6),
                                    (420, 450, 30, 6), (520, 470, 18, 5)]):
    d.shape("ellipse", f"Moon mare {i+1}", x=x-r, y=y-r, width=r*2, height=r*2,
            fill="#B8A070", opacity=op, stroke=NONE)

def petal(ang, r0, r1, w, label, fill, edge, op=100, sw=2):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    tx, ty = CX + ca * r1, CY + sa * r1
    bx, by = CX + ca * r0, CY + sa * r0
    nx, ny = -sa, ca
    c1 = (CX + ca * (r0 + (r1-r0)*0.22) + nx*w*1.25, CY + sa * (r0 + (r1-r0)*0.22) + ny*w*1.25)
    c2 = (CX + ca * (r0 + (r1-r0)*0.74) + nx*w*0.85, CY + sa * (r0 + (r1-r0)*0.74) + ny*w*0.85)
    c3 = (CX + ca * (r0 + (r1-r0)*0.74) - nx*w*0.85, CY + sa * (r0 + (r1-r0)*0.74) - ny*w*0.85)
    c4 = (CX + ca * (r0 + (r1-r0)*0.22) - nx*w*1.25, CY + sa * (r0 + (r1-r0)*0.22) - ny*w*1.25)
    d.path(f"M{bx + nx*4:.1f},{by + ny*4:.1f} "
           f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {tx:.1f},{ty:.1f} "
           f"C{c3[0]:.1f},{c3[1]:.1f} {c4[0]:.1f},{c4[1]:.1f} "
           f"{bx - nx*4:.1f},{by - ny*4:.1f} Z",
           label, fill=fill, opacity=op, stroke=edge, strokeWidth=sw)
    # crease
    d.path(f"M{bx:.1f},{by:.1f} Q{CX + ca*(r0+(r1-r0)*0.5):.1f},{CY + sa*(r0+(r1-r0)*0.5):.1f} {tx:.1f},{ty:.1f}",
           f"{label} crease", fill=NONE, stroke="#FFFFFF", strokeWidth=2, opacity=28, cap="round")

# back row
for i in range(11):
    ang = 200 + i * 14
    petal(ang, 40, 310, 42, f"Back petal {i+1}",
          lin(0, 380, 0, 700, (0, "#E890A8"), (1, "#9A3E62")), "#6E2440", op=92)
# mid row
for i in range(9):
    ang = 204 + i * 16.5
    petal(ang, 36, 262, 48, f"Mid petal {i+1}",
          lin(0, 430, 0, 700, (0, "#F8B8C8"), (1, "#D06A8A")), "#8A3454", op=96)
# seed pod
d.shape("ellipse", "Seed pod", x=CX-60, y=CY-92, width=120, height=62,
        fill=rad((0, "#F8E0A0"), (0.6, "#D8A84E"), (1, "#8A5A1E")), stroke=INK, strokeWidth=3)
for i in range(7):
    a = math.radians(200 + i * 23)
    d.shape("ellipse", f"Seed {i+1}", x=CX + math.cos(a)*34 - 4,
            y=CY - 70 + math.sin(a)*16 - 4, width=8, height=8, fill="#6E4218", opacity=75, stroke=NONE)


# front row
for i in range(7):
    ang = 208 + i * 20.7
    petal(ang, 30, 208, 54, f"Front petal {i+1}",
          lin(0, 500, 0, 700, (0, "#FFD8E2"), (1, "#E898AE")), "#9A445E", op=98)
# innermost row
for i in range(5):
    ang = 216 + i * 27
    petal(ang, 22, 150, 44, f"Inner petal {i+1}",
          lin(0, 550, 0, 700, (0, "#FFF0F4"), (1, "#F6C0CE")), "#B05A72", op=100)

# water
for i, (y, w, op) in enumerate([(790, 300, 60), (820, 240, 45), (848, 170, 30)]):
    d.path(f"M{500-w:.1f},{y:.1f} Q500,{y-20:.1f} {500+w:.1f},{y:.1f}",
           f"Ripple {i+1}", fill=NONE, stroke="#8FD0D8", strokeWidth=4, opacity=op, cap="round")
d.path("M300,770 Q500,750 700,770", "Water line", fill=NONE, stroke="#2A6A72",
       strokeWidth=10, opacity=35, cap="round")

p.caption("LOTUS", "कमल · PURITY AND AWAKENING", name_color="#F6E6C0",
          sub_color="#D8B060", name_size=54, sub_size=20, tracking_name=160,
          tracking_sub=110)
p.finish("lotus-V1R00")
