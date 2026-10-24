#!/usr/bin/env python3
"""Om — Symbol Plate V1R00. The primordial sound as a gold glyph inside a
radiant yantra ring, resting on a lotus. Deep indigo, gold leaf, no noise.
1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, GOLD_LO, PAPER, LATIN, DEVA,
                          lin, rad, gold_lin, blossom, lotus)
from orient.plate import Plate

p = Plate("Om — Symbol Plate", 1000, 1000)
d = p.d

p.backdrop(top="#101A30", bottom="#04060C", glow=("#2A4A7A", 14))
p.stars(n=46, color="#F6E3B8", seed=19, maxr=2.6)
p.disc("#16233E", "#070C18", rim="#D8B060", rim2="#5A4418")
p.ring_ticks(n=12, color=GOLD, width=2.5)
p.chop("ॐ", font=DEVA, size=34, w=54, h=54, x=872, y=94)

# radiant yantra rings
for r, sw, op in ((330, 2.5, 70), (300, 1.6, 45), (250, 2.2, 60), (196, 1.4, 40)):
    d.shape("ellipse", f"Ring {r}", x=500 - r, y=460 - r, width=2*r, height=2*r,
            fill=NONE, stroke=GOLD, strokeWidth=sw, opacity=op)
# 36 rays between the rings
for i in range(36):
    a = math.radians(i * 10)
    r0, r1 = 302, 330
    d.path(f"M{500 + r0*math.cos(a):.1f},{460 + r0*math.sin(a):.1f} "
           f"L{500 + r1*math.cos(a):.1f},{460 + r1*math.sin(a):.1f}",
           f"Ray {i+1}", fill=NONE, stroke=GOLD, strokeWidth=2.2 if i % 3 == 0 else 1.2,
           opacity=55 if i % 3 == 0 else 32, cap="round")
# 24 petal collar
for i in range(24):
    a = math.radians(i * 15)
    px, py = 500 + 330 * math.cos(a), 460 + 330 * math.sin(a)
    d.shape("ellipse", f"Petal {i+1}", x=px - 18, y=py - 10, width=36, height=20,
            fill=NONE, stroke=GOLD, strokeWidth=1.6, opacity=48,
            rotation=math.degrees(a) + 90)
# inner halo
d.shape("ellipse", "Halo", x=286, y=246, width=428, height=428,
        fill=rad((0, "#F0C878", 12), (0.6, "#F0C878", 4), (1, "#F0C878", 0)), stroke=NONE)

# the glyph
d.text("ॐ", "Om shadow", x=504, y=566, size=340, font=DEVA, color="#2A1A08",
       justify="center")
d.text("ॐ", "Om", x=500, y=562, size=340, font=DEVA, color="#F6D488",
       justify="center")
# subtle shadow pass behind is not possible after the fact; a thin outline ring keeps it grounded
d.path("M356,586 C420,612 580,612 644,586", "Glyph ground", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=30, cap="round")

# lotus base
lotus(d, 500, 706, 112, label="Lotus base", petal="#E8B85E", petal2="#C88A2E",
      edge="#8A5A14", core="#F8E0A0")
d.shape("ellipse", "Lotus shadow", x=370, y=738, width=260, height=26,
        fill="#000000", opacity=22, stroke=NONE)

# small gold dust in the field
for i, (x, y, r) in enumerate([(250, 300, 3), (750, 300, 3), (300, 620, 2.5), (700, 620, 2.5),
                                (220, 460, 2), (780, 460, 2)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=GOLD_HI, opacity=55, stroke=NONE)

p.caption("OM", "ॐ · THE PRIMORDIAL SOUND", name_color="#F6E6C0",
          sub_color="#D8B060", name_size=54, sub_size=20, tracking_name=160,
          tracking_sub=120)
p.finish("om-V1R00")
