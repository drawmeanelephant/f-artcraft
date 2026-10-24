#!/usr/bin/env python3
"""Nowruz — Festival Seal V1R00.

The haft-sin table as an emblem: a round goldfish bowl at centre (its glass
sphere echoing the plate), a fan of sabzeh spring greens to the left tied in
the traditional red ribbon, and a hyacinth spike in a clay pot to the right.
Deep spring-green field, dawn-warm glow, drifting blossom petals. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, PAPER,
                          LATIN, CJK, lin, rad, gold_lin, smooth, blend)
from festival_kit import (seal_disc, glow, dust, ring_dots, caption, leaf_at)

SLUG = "nowruz-V1R00"
SS3 = "Source Sans 3"

LEAF_HI = "#8FD476"
LEAF = "#5CA44A"
LEAF_LO = "#2F6B34"
FIELD_HI = "#3E6B54"
FIELD_LO = "#0C1D15"
RIBBON = "#C0392E"
FISH_HI = "#F6B26A"
FISH = "#F2803C"
FISH_LO = "#C8521C"
WATER_HI = "#BFE4E2"
WATER = "#6FA8AC"
WATER_LO = "#3E6E74"
HYA_HI = "#B8A8F0"
HYA = "#8470CC"
HYA_LO = "#54408E"
POT_HI = "#D88A58"
POT_LO = "#6E3418"
PETAL = "#F6CBD2"

p = Plate("Nowruz — Festival Seal", 1000, 1000)
d = p.d


def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


# --- field ------------------------------------------------------------------
p.backdrop(top="#14201A", bottom="#060B08", glow=("#3E6B54", 12))
dust(d, n=40, r=404, colors=("#F6E3B8", "#BFE4E2"), seed=31,
     smin=0.8, smax=2.2, opmin=8, opmax=22, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim="#D8C078", rim2="#3E4A22")
dust(d, n=56, r=392, colors=("#F6E3B8", "#8FD476", "#F6CBD2"), seed=17,
     smin=1.0, smax=2.8, opmin=9, opmax=28, label="Disc dust")

# dawn glow behind the bowl + soft field guides
glow(d, 500, 540, 330, "#FFDFA8", a=20, label="Dawn glow", squash=0.9)
glow(d, 500, 300, 240, "#BFE4C8", a=12, label="Spring haze")
for rr, op in ((168, 12), (252, 9), (330, 8)):
    d.shape("ellipse", f"Field ring {rr}", x=PCX - rr, y=PCY - rr,
            width=2 * rr, height=2 * rr, fill=NONE, stroke=GOLD,
            strokeWidth=1.4, opacity=op)
ring_dots(d, r=398, n=56, size=2.6, color=GOLD, opacity=32)

# ground shadow shared by the three vessels
d.shape("ellipse", "Ground shadow", x=200, y=716, width=600, height=52,
        fill=rad((0, INK, 46), (0.6, INK, 22), (1, INK, 0)), stroke=NONE)

# --- sabzeh: sprouted greens in a shallow dish, red ribbon -------------------
SX, SY = 312, 668

def blade(x0, y0, x1, y1, bow, w, col, label):
    """One grass blade: tapered ribbon along a curved spine."""
    mx, my = (x0 + x1) / 2 + bow, (y0 + y1) / 2 - 6
    # spine
    d.path(f"M{x0:.1f},{y0:.1f} Q{mx:.1f},{my:.1f} {x1:.1f},{y1:.1f}",
           f"{label} spine", fill=NONE, stroke=col, strokeWidth=w,
           cap="round", opacity=92)
    # highlight edge
    d.path(f"M{x0:.1f},{y0 - 1:.1f} Q{mx - 2:.1f},{my:.1f} {x1:.1f},{y1:.1f}",
           f"{label} hi", fill=NONE, stroke=LEAF_HI, strokeWidth=w * 0.34,
           cap="round", opacity=50)

# dish: shallow brass-edged bowl
d.shape("ellipse", "Sabzeh dish shadow", x=SX - 104, y=SY + 14, width=208,
        height=26, fill=rad((0, INK, 40), (1, INK, 0)), stroke=NONE)
d.path(f"M{SX - 92:.1f},{SY:.1f} C{SX - 88:.1f},{SY + 26:.1f} "
       f"{SX - 40:.1f},{SY + 40:.1f} {SX:.1f},{SY + 40:.1f} "
       f"C{SX + 40:.1f},{SY + 40:.1f} {SX + 88:.1f},{SY + 26:.1f} "
       f"{SX + 92:.1f},{SY:.1f} Z", "Sabzeh dish",
       fill=lin((SX - 80, SY), (SX + 84, SY + 40),
                (0, "#E8D9B0"), (0.5, "#B89A62"), (1, "#6E4E22")),
       stroke=INK, strokeWidth=2.6)
d.shape("ellipse", "Sabzeh dish rim", x=SX - 92, y=SY - 11, width=184,
        height=24, fill=lin((0, SY - 11), (0, SY + 13),
                            (0, "#F6E8C0"), (1, "#C8A468")),
        stroke=INK, strokeWidth=2.4)
d.shape("ellipse", "Sabzeh soil", x=SX - 78, y=SY - 7, width=156, height=16,
        fill=rad((0, "#4A3A20"), (1, "#2A1E10")), stroke=NONE)

# grass blades fanning up from the soil line
import random
rnd = random.Random(42)
blades = []
for i in range(38):
    t = i / 37
    x0 = SX - 66 + 132 * t + rnd.uniform(-3, 3)
    spread = (t - 0.5) * 150
    top_x = SX + spread * 1.15 + rnd.uniform(-6, 6)
    top_y = SY - rnd.uniform(125, 200) + abs(t - 0.5) * 72
    bow = (t - 0.5) * 30 + rnd.uniform(-6, 6)
    col = [LEAF, LEAF_HI, LEAF_LO, "#79BE5C"][i % 4]
    blades.append((x0, SY - 6, top_x, top_y, bow,
                   rnd.uniform(4.2, 6.2), col))
# draw back-to-front by height so tall centre blades sit on top
for i, b in enumerate(sorted(blades, key=lambda v: v[3], reverse=True)):
    blade(*b, label=f"Sabzeh blade {i+1}")
# seed pearls on a few tips
for i, b in enumerate(sorted(blades, key=lambda v: v[3])[:8]):
    d.shape("ellipse", f"Sabzeh pearl {i+1}", x=b[2] - 2.4, y=b[3] - 4.4,
            width=4.8, height=5.4, fill="#EAF4C8", opacity=88, stroke=NONE)

# red ribbon tie around the clump
d.path(f"M{SX - 40:.1f},{SY - 40:.1f} C{SX - 18:.1f},{SY - 30:.1f} "
       f"{SX + 18:.1f},{SY - 30:.1f} {SX + 40:.1f},{SY - 40:.1f} "
       f"C{SX + 24:.1f},{SY - 20:.1f} {SX - 24:.1f},{SY - 20:.1f} "
       f"{SX - 40:.1f},{SY - 40:.1f} Z", "Sabzeh ribbon",
       fill=lin((SX, SY - 42), (SX, SY - 18), (0, "#E05A44"), (1, "#8E2418")),
       stroke="#5E1412", strokeWidth=1.8)
d.path(f"M{SX - 4:.1f},{SY - 36:.1f} C{SX - 16:.1f},{SY - 52:.1f} "
       f"{SX - 26:.1f},{SY - 50:.1f} {SX - 29:.1f},{SY - 38:.1f} "
       f"C{SX - 22:.1f},{SY - 38:.1f} {SX - 10:.1f},{SY - 32:.1f} "
       f"{SX - 4:.1f},{SY - 36:.1f} Z", "Ribbon loop L",
       fill="#E05A44", stroke="#5E1412", strokeWidth=1.6)
d.path(f"M{SX + 4:.1f},{SY - 36:.1f} C{SX + 16:.1f},{SY - 52:.1f} "
       f"{SX + 26:.1f},{SY - 50:.1f} {SX + 29:.1f},{SY - 38:.1f} "
       f"C{SX + 22:.1f},{SY - 38:.1f} {SX + 10:.1f},{SY - 32:.1f} "
       f"{SX + 4:.1f},{SY - 36:.1f} Z", "Ribbon loop R",
       fill="#C0392E", stroke="#5E1412", strokeWidth=1.6)
d.shape("ellipse", "Ribbon knot", x=SX - 6, y=SY - 42, width=12, height=10,
        fill="#F2705A", stroke="#5E1412", strokeWidth=1.4)
for sgn, nm in ((-1, "L"), (1, "R")):
    d.path(f"M{SX + sgn*4:.1f},{SY - 28:.1f} C{SX + sgn*10:.1f},{SY - 12:.1f} "
           f"{SX + sgn*16:.1f},{SY + 2:.1f} {SX + sgn*26:.1f},{SY + 8:.1f}",
           f"Ribbon tail {nm}", fill=NONE, stroke="#B8342C",
           strokeWidth=3.8, cap="round")

# --- hyacinth in a clay pot --------------------------------------------------
HX, HY = 690, 672

d.shape("ellipse", "Hyacinth shadow", x=HX - 74, y=HY + 22, width=148,
        height=22, fill=rad((0, INK, 40), (1, INK, 0)), stroke=NONE)
# strap leaves arching out
for sgn, hgt, bow in ((-1, 150, -44), (-1, 116, -70), (1, 158, 46),
                      (1, 122, 72), (0, 170, 8)):
    tipx = HX + bow + sgn * 16
    tipy = HY - hgt
    d.path(f"M{HX + sgn*4:.1f},{HY - 10:.1f} "
           f"C{HX + sgn*10 + bow*0.3:.1f},{HY - hgt*0.55:.1f} "
           f"{tipx - sgn*6:.1f},{tipy + 30:.1f} {tipx:.1f},{tipy:.1f}",
           f"Hyacinth leaf {sgn}-{hgt}", fill=NONE,
           stroke=[LEAF_LO, LEAF, "#467C3C"][(hgt // 30) % 3],
           strokeWidth=11 - abs(bow) * 0.04, cap="round", opacity=94)
    d.path(f"M{HX + sgn*4:.1f},{HY - 12:.1f} "
           f"C{HX + sgn*10 + bow*0.3:.1f},{HY - hgt*0.55:.1f} "
           f"{tipx - sgn*6:.1f},{tipy + 28:.1f} {tipx - sgn*2:.1f},{tipy + 4:.1f}",
           f"Hyacinth leaf hi {sgn}-{hgt}", fill=NONE, stroke=LEAF_HI,
           strokeWidth=2.6, cap="round", opacity=40)

# floret spike: dense cone of tiny 4-petal stars
stem_top = HY - 196
d.path(f"M{HX:.1f},{HY - 8:.1f} C{HX - 2:.1f},{HY - 80:.1f} "
       f"{HX + 2:.1f},{HY - 140:.1f} {HX:.1f},{stem_top:.1f}",
       "Hyacinth stem", fill=NONE, stroke="#3E6E34", strokeWidth=7,
       cap="round")
flor = 0
rows = [(0.00, 11, 22), (0.11, 10, 26), (0.22, 10, 29), (0.33, 9, 30),
        (0.44, 9, 29), (0.55, 8, 27), (0.66, 7, 24), (0.77, 6, 20),
        (0.88, 5, 15), (0.97, 4, 10)]
for rt, n, spread in rows:
    yy = HY - 40 - rt * (HY - 40 - stem_top)
    for i in range(n):
        a = math.tau * i / n + rt * 9
        rr = spread * (0.55 + rnd.random() * 0.45)
        fx = HX + math.cos(a) * rr
        fy = yy + math.sin(a) * rr * 0.24
        sz = 8.2 - rt * 2.2 + rnd.uniform(-0.6, 0.6)
        col = [HYA_LO, HYA, HYA_HI, "#9B8AE0"][flor % 4]
        for k in range(4):
            pa = a + k * math.pi / 2
            d.shape("ellipse", f"Hyacinth floret {flor}-{k}",
                    x=fx + math.cos(pa) * sz * 0.5 - sz * 0.34,
                    y=fy + math.sin(pa) * sz * 0.5 - sz * 0.34,
                    width=sz * 0.68, height=sz * 0.68, fill=col,
                    opacity=94, stroke="#3A2C66", strokeWidth=0.7)
        d.shape("ellipse", f"Hyacinth eye {flor}", x=fx - 1.3, y=fy - 1.3,
                width=2.6, height=2.6, fill="#E8DFF8", opacity=90, stroke=NONE)
        flor += 1
# terminal bud
d.shape("ellipse", "Hyacinth tip", x=HX - 5, y=stem_top - 14, width=10,
        height=12, fill=HYA_HI, stroke="#3A2C66", strokeWidth=0.8)

# clay pot
d.path(f"M{HX - 56:.1f},{HY - 6:.1f} C{HX - 52:.1f},{HY + 22:.1f} "
       f"{HX - 34:.1f},{HY + 46:.1f} {HX:.1f},{HY + 48:.1f} "
       f"C{HX + 34:.1f},{HY + 46:.1f} {HX + 52:.1f},{HY + 22:.1f} "
       f"{HX + 56:.1f},{HY - 6:.1f} Z", "Hyacinth pot",
       fill=lin((HX - 50, HY), (HX + 50, HY + 48),
                (0, POT_HI), (0.55, "#A05C30"), (1, POT_LO)),
       stroke=INK, strokeWidth=2.6)
d.shape("ellipse", "Hyacinth pot rim", x=HX - 58, y=HY - 18, width=116,
        height=24, fill=lin((0, HY - 18), (0, HY + 6),
                            (0, "#E8A06A"), (1, "#8E4A26")),
        stroke=INK, strokeWidth=2.4)
d.shape("ellipse", "Hyacinth soil", x=HX - 44, y=HY - 14, width=88,
        height=14, fill="#3A2414", stroke=NONE)
d.path(f"M{HX - 46:.1f},{HY + 16:.1f} C{HX - 30:.1f},{HY + 22:.1f} "
       f"{HX - 12:.1f},{HY + 24:.1f} {HX + 2:.1f},{HY + 24:.1f}",
       "Hyacinth pot sheen", fill=NONE, stroke="#F0B888",
       strokeWidth=3.4, opacity=36, cap="round")
# painted band on the pot
d.path(f"M{HX - 48:.1f},{HY + 30:.1f} Q{HX:.1f},{HY + 38:.1f} "
       f"{HX + 48:.1f},{HY + 30:.1f}", "Hyacinth pot band", fill=NONE,
       stroke="#E8D9A8", strokeWidth=2.2, opacity=52, cap="round")

# --- goldfish bowl ------------------------------------------------------------
BX, BY, BR = 500, 560, 128

d.shape("ellipse", "Bowl shadow", x=BX - BR - 20, y=BY + BR * 0.78,
        width=2 * (BR + 20), height=30,
        fill=rad((0, INK, 48), (0.6, INK, 24), (1, INK, 0)), stroke=NONE)

# back glass
d.shape("ellipse", "Bowl glass", x=BX - BR, y=BY - BR, width=2 * BR,
        height=2 * BR,
        fill=rad((0, "#EAF8F6", 30), (0.6, "#9ED0CC", 18), (1, "#4E8A8E", 24)),
        stroke="#BFE8E4", strokeWidth=2.8)

# water fill — slightly squashed, top edge is the surface
d.shape("ellipse", "Water", x=BX - BR + 9, y=BY - BR + 40,
        width=2 * (BR - 9), height=2 * (BR - 13),
        fill=rad((0, WATER_HI, 62), (0.55, WATER, 58), (1, WATER_LO, 72)),
        stroke=NONE)
# water surface ellipse, just under the mouth
d.shape("ellipse", "Water surface", x=BX - 62, y=BY - BR + 34,
        width=124, height=20,
        fill=rad((0, "#EAF8F6", 72), (1, "#8EC4C6", 48)),
        stroke="#CFEEEC", strokeWidth=1.8, opacity=88)
d.shape("ellipse", "Water rim dark", x=BX - 62, y=BY - BR + 34, width=124,
        height=20, fill=NONE, stroke=WATER_LO, strokeWidth=1.4, opacity=40)

# pebbles at the bowl floor
for i, (px, py, s, col) in enumerate([
        (BX - 52, BY + 84, 11, "#E8D9B0"), (BX - 22, BY + 92, 9, "#C8A868"),
        (BX + 6, BY + 88, 12, "#D8C090"), (BX + 34, BY + 82, 9, "#B89058"),
        (BX - 6, BY + 96, 8, "#A8804C"), (BX - 38, BY + 94, 8, "#E0CC9C"),
        (BX + 22, BY + 96, 7, "#D0B078")]):
    d.shape("ellipse", f"Pebble {i+1}", x=px - s, y=py - s * 0.62,
            width=s * 2, height=s * 1.24, fill=col, stroke="#5E4A28",
            strokeWidth=1.2)

# the goldfish — orange, flowing double tail, drifting left of centre
FX, FY = BX - 14, BY + 18
# tail: two flowing lobes
d.path(f"M{FX + 34:.1f},{FY - 2:.1f} C{FX + 62:.1f},{FY - 26:.1f} "
       f"{FX + 84:.1f},{FY - 30:.1f} {FX + 96:.1f},{FY - 44:.1f} "
       f"C{FX + 90:.1f},{FY - 20:.1f} {FX + 76:.1f},{FY - 8:.1f} "
       f"{FX + 58:.1f},{FY - 2:.1f} C{FX + 76:.1f},{FY + 6:.1f} "
       f"{FX + 88:.1f},{FY + 18:.1f} {FX + 94:.1f},{FY + 36:.1f} "
       f"C{FX + 76:.1f},{FY + 30:.1f} {FX + 58:.1f},{FY + 20:.1f} "
       f"{FX + 36:.1f},{FY + 8:.1f} Z", "Fish tail",
       fill=lin((FX + 30, FY), (FX + 98, FY), (0, FISH), (1, "#E86A2C")),
       opacity=88, stroke="#9A3A10", strokeWidth=1.4)
# tail fin rays
for k, (dy, ex) in enumerate(((-30, 88), (-14, 94), (4, 96), (20, 90))):
    d.path(f"M{FX + 40:.1f},{FY + 2:.1f} Q{FX + 66:.1f},{FY + dy*0.5:.1f} "
           f"{FX + ex:.1f},{FY + dy:.1f}", f"Fish tail ray {k+1}",
           fill=NONE, stroke="#B84A14", strokeWidth=1.2, opacity=50)
# body
d.shape("ellipse", "Fish body", x=FX - 34, y=FY - 15, width=72, height=34,
        fill=rad((0, "#F8BE7E"), (0.55, FISH), (1, FISH_LO)),
        stroke="#9A3A10", strokeWidth=1.8, rotation=-8)
# belly + head
d.shape("ellipse", "Fish belly", x=FX - 30, y=FY + 1, width=50, height=16,
        fill="#F8D8A8", opacity=60, stroke=NONE, rotation=-6)
# dorsal + pectoral fins
d.path(f"M{FX - 6:.1f},{FY - 14:.1f} C{FX + 4:.1f},{FY - 28:.1f} "
       f"{FX + 16:.1f},{FY - 30:.1f} {FX + 22:.1f},{FY - 24:.1f} "
       f"C{FX + 14:.1f},{FY - 18:.1f} {FX + 6:.1f},{FY - 12:.1f} "
       f"{FX - 2:.1f},{FY - 10:.1f} Z", "Fish dorsal",
       fill="#E86A2C", opacity=88, stroke="#9A3A10", strokeWidth=1.1)
d.path(f"M{FX - 14:.1f},{FY + 8:.1f} C{FX - 6:.1f},{FY + 20:.1f} "
       f"{FX + 4:.1f},{FY + 26:.1f} {FX + 2:.1f},{FY + 30:.1f} "
       f"C{FX - 8:.1f},{FY + 26:.1f} {FX - 18:.1f},{FY + 16:.1f} "
       f"{FX - 20:.1f},{FY + 10:.1f} Z", "Fish fin",
       fill="#F2A05C", opacity=80, stroke="#9A3A10", strokeWidth=1.1)
# eye + gill
d.shape("ellipse", "Fish eye", x=FX - 26, y=FY - 9, width=6.4, height=6.4,
        fill="#2A1410", stroke=NONE)
d.shape("ellipse", "Fish eye hi", x=FX - 25, y=FY - 8, width=2, height=2,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path(f"M{FX - 12:.1f},{FY - 8:.1f} Q{FX - 8:.1f},{FY + 1:.1f} "
       f"{FX - 12:.1f},{FY + 9:.1f}", "Fish gill", fill=NONE,
       stroke="#9A3A10", strokeWidth=1.4, opacity=60, cap="round")

# second small fish far side, lower right, facing right
GX, GY = BX + 62, BY + 66
d.path(f"M{GX - 10:.1f},{GY:.1f} C{GX - 22:.1f},{GY - 8:.1f} "
       f"{GX - 30:.1f},{GY - 12:.1f} {GX - 36:.1f},{GY - 17:.1f} "
       f"C{GX - 34:.1f},{GY - 6:.1f} {GX - 27:.1f},{GY - 2:.1f} "
       f"{GX - 36:.1f},{GY + 7:.1f} C{GX - 28:.1f},{GY + 9:.1f} "
       f"{GX - 19:.1f},{GY + 5:.1f} {GX - 10:.1f},{GY + 3:.1f} Z",
       "Fish2 tail", fill="#E07830", opacity=80, stroke="#9A3A10",
       strokeWidth=1.0)
d.shape("ellipse", "Fish2 body", x=GX - 14, y=GY - 7, width=30, height=15,
        fill=rad((0, "#F4B478"), (0.6, "#EA8438"), (1, "#C8521C")),
        stroke="#9A3A10", strokeWidth=1.3, rotation=6)
d.shape("ellipse", "Fish2 eye", x=GX + 8, y=GY - 4, width=4.2, height=4.2,
        fill="#2A1410", stroke=NONE)

# bubbles rising from the fish
for i, (bx, by, s) in enumerate([(BX + 30, BY - 4, 4.5), (BX + 44, BY - 26, 3.4),
                                 (BX + 34, BY - 46, 5.4), (BX + 52, BY - 62, 3.0),
                                 (BX + 20, BY - 30, 2.6)]):
    d.shape("ellipse", f"Bubble {i+1}", x=bx - s, y=by - s, width=s * 2,
            height=s * 2, fill="#EAF8F6", opacity=30,
            stroke="#CFEEEC", strokeWidth=1.0)
    d.shape("ellipse", f"Bubble hi {i+1}", x=bx - s * 0.4, y=by - s * 0.5,
            width=s * 0.5, height=s * 0.5, fill="#FFFFFF", opacity=55,
            stroke=NONE)

# front glass: mouth at the sphere's top + sheen arcs
d.shape("ellipse", "Bowl mouth", x=BX - 52, y=BY - BR - 4, width=104,
        height=22, fill=NONE, stroke="#EAF8F6", strokeWidth=2.8, opacity=72)
d.path(f"M{BX - 50:.1f},{BY - BR + 5:.1f} Q{BX:.1f},{BY - BR + 15:.1f} "
       f"{BX + 50:.1f},{BY - BR + 5:.1f}", "Bowl mouth inner", fill=NONE,
       stroke=WATER_LO, strokeWidth=1.6, opacity=55)
for k, (a0, a1, op) in enumerate(((132, 172, 26), (196, 232, 18))):
    r0 = BR - 10
    x0 = BX + r0 * math.cos(math.radians(a0))
    y0 = BY + r0 * math.sin(math.radians(a0))
    x1 = BX + r0 * math.cos(math.radians(a1))
    y1 = BY + r0 * math.sin(math.radians(a1))
    cx = BX + (r0 + 16) * math.cos(math.radians((a0 + a1) / 2))
    cy = BY + (r0 + 16) * math.sin(math.radians((a0 + a1) / 2))
    d.path(f"M{x0:.1f},{y0:.1f} Q{cx:.1f},{cy:.1f} {x1:.1f},{y1:.1f}",
           f"Glass sheen {k+1}", fill=NONE, stroke="#FFFFFF",
           strokeWidth=7 - k * 2, opacity=op, cap="round")
# sharp glint dots on the glass edge
for i, (gx, gy, s) in enumerate([(BX - BR + 18, BY - 44, 3.4),
                                 (BX + BR - 16, BY - 20, 2.6)]):
    d.shape("ellipse", f"Glass glint {i+1}", x=gx - s, y=gy - s, width=s * 2,
            height=s * 2, fill="#FFFFFF", opacity=62, stroke=NONE)

# --- drifting blossom petals ------------------------------------------------
for i, (px, py, ang, s, col) in enumerate([
        (238, 330, -30, 15, PETAL), (356, 236, 40, 12, "#F8E2E6"),
        (648, 220, -55, 14, PETAL), (764, 330, 20, 11, "#F0BCC6"),
        (820, 486, 65, 13, PETAL), (168, 512, -15, 12, "#F8E2E6"),
        (440, 168, 30, 10, PETAL), (596, 306, -40, 9, "#F0BCC6")]):
    leaf_at(d, px, py, ang, s * 1.9, s * 0.62, fill=col,
            stroke="#C87A8C", label=f"Petal {i+1}", vein=False)

# --- seal chop + caption ------------------------------------------------------
# horizontal vermilion chop, top right outside the disc: نوروز
CHX, CHY, CHW, CHH = 856, 104, 96, 58
d.shape("rectangle", "Chop shadow", x=CHX + 3, y=CHY + 4, width=CHW,
        height=CHH, radius=5, fill="#000000", opacity=30, stroke=NONE)
d.shape("rectangle", "Chop", x=CHX, y=CHY, width=CHW, height=CHH, radius=5,
        fill=lin((CHX, CHY), (CHX + CHW, CHY + CHH), (0, "#B23A30"),
                 (1, "#7E1F1B")), stroke="#5E1412", strokeWidth=2)
d.shape("rectangle", "Chop inner", x=CHX + 4, y=CHY + 4, width=CHW - 8,
        height=CHH - 8, radius=2, fill=NONE, stroke=GOLD_HI,
        strokeWidth=1.5, opacity=70)
d.text("نوروز", "Chop text", x=CHX + CHW / 2, y=CHY + CHH * 0.68, size=24,
       font=SS3, color=GOLD_HI, justify="center")

caption(p, "NOWRUZ", "نوروز · PERSIAN NEW YEAR · MAR 20",
        name_color="#F4EFD8", sub_color="#C8B478",
        name_size=52, tracking_name=110, sub_size=20, tracking_sub=44,
        sub_font=SS3)
p.finish(SLUG)
