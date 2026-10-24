#!/usr/bin/env python3
"""Peacock — Symbol Plate V1R00. A fan of eleven feather eyes in teal, gold
and indigo, with the bird's crest at the base. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, GOLD_LO, LATIN, DEVA,
                          lin, rad, gold_lin)
from orient.plate import Plate

p = Plate("Peacock — Symbol Plate", 1000, 1000)
d = p.d

p.backdrop(top="#0A2226", bottom="#03080A", glow=("#1E6A6A", 14))
p.stars(n=44, color="#F6E3B8", seed=41, maxr=2.4)
p.disc("#0E3438", "#04100F", rim="#D8B060", rim2="#3E3A18")
p.ring_ticks(n=12, color=GOLD, width=2.2)
p.chop("मोर", font=DEVA, size=22, w=60, h=60, x=872, y=94, horizontal=True)

CX, CY = 500, 812

# deep moon behind the fan, to carry the upper field
d.shape("ellipse", "Moon glow", x=200, y=120, width=600, height=600,
        fill=rad((0, "#2E8A7A", 18), (0.6, "#2E8A7A", 6), (1, "#2E8A7A", 0)), stroke=NONE)
d.shape("ellipse", "Peacock moon", x=232, y=152, width=536, height=536,
        fill=rad((0, "#1E5A56"), (0.65, "#123E3C"), (1, "#081E1E")),
        stroke=GOLD, strokeWidth=2.5, )
d.shape("ellipse", "Peacock moon inner", x=248, y=168, width=504, height=504,
        fill=NONE, stroke=GOLD, strokeWidth=1.2, opacity=45)

def feather(ang, length, width, label):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    nx, ny = -sa, ca
    tipx, tipy = CX + ca * length, CY + sa * length
    ex, ey = CX + ca * length * 0.80, CY + sa * length * 0.80
    # stem
    d.path(f"M{CX:.1f},{CY:.1f} Q{CX + ca*length*0.45:.1f},{CY + sa*length*0.45:.1f} {tipx:.1f},{tipy:.1f}",
           f"{label} stem", fill=NONE, stroke="#C8A050", strokeWidth=3, opacity=75, cap="round")
    # barbs along the stem
    for k in range(4, 8):
        t = k / 9
        px, py = CX + ca * length * t, CY + sa * length * t
        for sgn in (-1, 1):
            d.path(f"M{px:.1f},{py:.1f} Q{px + sgn*nx*16 + ca*8:.1f},{py + sgn*ny*16 + sa*8:.1f} "
                   f"{px + sgn*nx*26 + ca*14:.1f},{py + sgn*ny*26 + sa*14:.1f}",
                   f"{label} barb {k}-{sgn}", fill=NONE, stroke="#2E8A7A",
                   strokeWidth=2.2, opacity=35, cap="round")
    # eye
    d.shape("ellipse", f"{label} eye outer", x=ex - width*0.62, y=ey - width*0.78,
            width=width*1.24, height=width*1.56,
            fill=rad((0, "#3AB0A0"), (0.6, "#1E7A72"), (1, "#0E4A48")),
            stroke="#0A2E2C", strokeWidth=2.5, rotation=math.degrees(a) + 90)
    d.shape("ellipse", f"{label} eye gold", x=ex - width*0.38, y=ey - width*0.5,
            width=width*0.76, height=width*1.0,
            fill=gold_lin(ey - width, ey + width), stroke="#8A5A1E", strokeWidth=1.8,
            rotation=math.degrees(a) + 90)
    d.shape("ellipse", f"{label} eye dark", x=ex - width*0.25, y=ey - width*0.34,
            width=width*0.5, height=width*0.68,
            fill=rad((0, "#2A4AB0"), (0.7, "#16205E"), (1, "#080A2A")),
            stroke="#080A1A", strokeWidth=1.5, rotation=math.degrees(a) + 90)
    d.shape("ellipse", f"{label} eye glint", x=ex - width*0.08, y=ey - width*0.18,
            width=width*0.16, height=width*0.2, fill="#FFFFFF", opacity=55, stroke=NONE,
            rotation=math.degrees(a) + 90)
    # tip flame beyond the eye
    d.path(f"M{ex + ca*width*0.8:.1f},{ey + sa*width*0.8:.1f} "
           f"Q{tipx + nx*width*0.18:.1f},{tipy + ny*width*0.18:.1f} {tipx:.1f},{tipy:.1f} "
           f"Q{tipx - nx*width*0.18:.1f},{tipy - ny*width*0.18:.1f} "
           f"{ex - ca*width*0.8:.1f},{ey - sa*width*0.8:.1f} Z",
           f"{label} tip", fill=lin(0, tipy, 0, ey, (0, "#7AD8C0"), (1, "#1E6A60")),
           stroke="#0A2E2C", strokeWidth=1.8)

for i in range(13):
    ang = 194 + i * 12.67
    L = 570 - abs(i - 6) * 38
    feather(ang, L, 40 - abs(i - 6) * 1.2, f"Feather {i+1}")

# body / crest at the base
d.shape("ellipse", "Body", x=CX-46, y=CY-16, width=92, height=64,
        fill=lin(0, CY-18, 0, CY+60, (0, "#2E8A7A"), (1, "#0E3A36")),
        stroke=INK, strokeWidth=3)
d.path(f"M{CX:.1f},{CY-8} C{CX-4:.1f},{CY-54} {CX+6:.1f},{CY-78} {CX+2:.1f},{CY-96}",
       "Neck", fill=NONE, stroke=INK, strokeWidth=16, cap="round")
d.path(f"M{CX:.1f},{CY-8} C{CX-4:.1f},{CY-54} {CX+6:.1f},{CY-78} {CX+2:.1f},{CY-96}",
       "Neck colour", fill=NONE, stroke=lin(0, CY-130, 0, CY, (0, "#4AB0A0"), (1, "#1E6A60")),
       strokeWidth=11, cap="round")
d.shape("ellipse", "Head", x=CX-18, y=CY-114, width=36, height=30,
        fill=lin(0, CY-146, 0, CY-112, (0, "#4AB0A0"), (1, "#1E6A60")),
        stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Eye", x=CX-7, y=CY-106, width=8, height=8, fill="#0A0A14", stroke=NONE)
# crest: three gold dots on stalks
for k, dx in enumerate((-14, 0, 14)):
    d.path(f"M{CX+2:.1f},{CY-114} Q{CX+dx:.1f},{CY-138} {CX+dx*1.4:.1f},{CY-152}",
           f"Crest stalk {k+1}", fill=NONE, stroke="#C8A050", strokeWidth=2, cap="round")
    d.shape("ellipse", f"Crest dot {k+1}", x=CX+dx*1.4-5, y=CY-158, width=10, height=10,
            fill=rad((0, "#F8E0A0"), (1, "#C08A2E")), stroke=INK, strokeWidth=1.5)
d.path(f"M{CX+16:.1f},{CY-98} L{CX+30:.1f},{CY-93} L{CX+16:.1f},{CY-88} Z",
       "Beak", fill=gold_lin(CY-126, CY-110), stroke=INK, strokeWidth=1.8)

p.caption("PEACOCK", "मोर · NATIONAL BIRD OF INDIA", name_color="#F6E6C0",
          sub_color="#D8B060", name_size=54, sub_size=20, tracking_name=140,
          tracking_sub=100)
p.finish("peacock-V1R00")
