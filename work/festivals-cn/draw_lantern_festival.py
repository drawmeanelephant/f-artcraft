#!/usr/bin/env python3
"""Lantern Festival — Festival Seal V1R00. The first full moon of the year:
a hero palace lantern under a silk cord, two companion lanterns, riddle
slips, and river lanterns drifting below. Jade, vermilion and gold. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, NONE, INK, GOLD, GOLD_HI, lin, rad, gold_lin,
                          cloud, blossom, CJK, LATIN)
from cn_kit import hanging_lantern, cord, firework

p = Plate("Lantern Festival — Festival Seal", 1000, 1000)
d = p.d

p.backdrop(top="#0E2222", bottom="#04090A", glow=("#2E7A6A", 12))
p.stars(n=38, color="#F6E3B8", seed=17, maxr=2.2)
p.disc("#123A34", "#05100E", rim="#D8B060", rim2="#3E3A18")
p.ring_ticks(n=12, color=GOLD, width=2.2)
p.chop("元宵", font=CJK, size=24, w=54, h=96, x=874, y=94)

# moon
d.shape("ellipse", "Moon halo", x=310, y=110, width=380, height=380,
        fill=rad((0, "#FFF0C8", 26), (0.55, "#FFF0C8", 8), (1, "#FFF0C8", 0)), stroke=NONE)
d.shape("ellipse", "Moon", x=350, y=150, width=300, height=300,
        fill=rad((0, "#FFFDF0"), (0.7, "#F4E6C0"), (1, "#D8C08A")), stroke=NONE)
for i, (x, y, r) in enumerate([(420, 230, 20), (540, 210, 26), (560, 320, 16)]):
    d.shape("ellipse", f"Moon mare {i+1}", x=x-r, y=y-r, width=r*2, height=r*2,
            fill="#B8A070", opacity=8, stroke=NONE)

# silk cord across the top
cord(d, 220, 120, 780, 120, 26, "Silk cord", sw=4)
for x in (300, 700):
    d.path(f"M{x},140 L{x},196", f"Cord drop {x}", fill=NONE, stroke="#B8342C",
           strokeWidth=3, cap="round")

# hero lantern
hanging_lantern(d, 500, 402, 200, 226, "元", "Hero lantern")
# companions
for x, ch, nm in ((286, "宵", "L"), (714, "節", "R")):
    d.path(f"M{x},132 L{x},{214}", f"Companion cord {nm}", fill=NONE, stroke="#B8342C",
           strokeWidth=2.6, cap="round")
    hanging_lantern(d, x, 286, 108, 124, ch, f"Companion {nm}")

# riddle slips
for i, (x, y, w, h) in enumerate([(190, 210, 54, 120), (756, 208, 54, 132), (810, 300, 46, 96)]):
    d.path(f"M{x + w/2:.1f},{y - 30:.1f} L{x + w/2:.1f},{y:.1f}", f"Riddle cord {i+1}",
           fill=NONE, stroke="#8A2A22", strokeWidth=2, cap="round")
    d.shape("rectangle", f"Riddle slip {i+1}", x=x, y=y, width=w, height=h, radius=3,
            fill=lin(0, y, 0, y + h, (0, "#F2D8A8"), (1, "#D8B070")),
            stroke="#7A4A16", strokeWidth=2)
    for k in range(4):
        d.path(f"M{x + 10:.1f},{y + 18 + k*22:.1f} L{x + w - 10:.1f},{y + 18 + k*22:.1f}",
               f"Riddle line {i+1}-{k}", fill=NONE, stroke="#8A5A1E", strokeWidth=2, opacity=55)

# fireworks in the corners
firework(d, 214, 372, 46, "Firework L", seed=7, n=10, op=45)
firework(d, 792, 386, 42, "Firework R", seed=19, n=10, op=40)

# still water below
d.path("M180,780 Q500,748 820,780", "Water line", fill=NONE, stroke="#2E6A62",
       strokeWidth=8, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(330, 810, 160), (500, 828, 220), (670, 810, 160)]):
    d.path(f"M{x-w:.1f},{y:.1f} Q{x:.1f},{y-18:.1f} {x+w:.1f},{y:.1f}",
           f"Ripple {i+1}", fill=NONE, stroke="#5AA89A", strokeWidth=2.6,
           opacity=30, cap="round")

p.caption("LANTERN FESTIVAL", "元宵節 · FIRST FULL MOON · DAY 15",
          name_color="#F6E6C0", sub_color="#D8B060", name_size=48, sub_size=20,
          tracking_name=60, tracking_sub=110)
p.finish("lantern-festival-V1R00")
