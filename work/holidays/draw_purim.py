#!/usr/bin/env python3
"""Purim — Festival Seal V1R00.

Carnival objects, no figures: a domino masquerade mask up top, a wooden
gragger swung low on the left, three hamantaschen on a gold platter to
the right, confetti in the air. Royal violet + gold on deep ink.
1000x1000, Hebrew chop, Source Sans 3 date line.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, NONE, INK, GOLD, GOLD_HI, GOLD_LO, PAPER, LATIN,
                          PCX, PCY, PR, lin, rad, gold_lin, smooth, blend)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "purim-V1R00"
HEBREW = "Arial Hebrew"
DIGITS = "Source Sans 3"
ROSE = "#D45C74"
VIOLET = "#9A7AC8"

p = Plate("Purim — Festival Seal", 1000, 1000)
d = p.d


def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def rot(x, y, cx, cy, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)


def rpoly(pts, cx, cy, deg):
    return [rot(x, y, cx, cy, deg) for x, y in pts]


def poly(pts, label, **kw):
    return d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z",
                  label, **kw)


# --- field ------------------------------------------------------------------
p.backdrop(top="#150B22", bottom="#050309", glow=("#3A2260", 13))
p.stars(n=26, color="#E8D8B8", seed=31, maxr=2.0)
seal_disc(p, "#46286E", "#140826", rim=GOLD, rim2="#4A3418")
d.shape("ellipse", "Vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.6, "#000000", 0), (1, "#000000", 56)),
        stroke=NONE)
dust(d, n=54, r=392, colors=("#F6E3B8", "#E8C074", "#C9A8E8", "#F0A8B8"),
     seed=17, smin=1.0, smax=2.6, opmin=8, opmax=24, label="Disc dust")
ring_dots(d, r=396, n=60, size=2.4, color=GOLD, opacity=30)

# faint triple-corner echo on the field
for i, (cx, cy, r) in enumerate([(500, 372, 252), (216, 560, 96),
                                 (786, 560, 96)]):
    pts = [(cx, cy - r), (cx - r * 0.95, cy + r * 0.68),
           (cx + r * 0.95, cy + r * 0.68)]
    poly(pts, f"Field triangle {i+1}", fill=NONE, stroke=GOLD,
         strokeWidth=2.0, opacity=8)

glow(d, 500, 330, 290, "#C9A0F0", a=20, label="Mask aura", squash=0.9)
glow(d, 560, 690, 300, "#FFC46B", a=14, label="Warm pool", squash=0.7)

# --- gragger (drawn upright, swung -32deg about its head) --------------------
GC, GD = (372, 614), 32          # pivot, degrees (handle falls down-left)
d.shape("ellipse", "Gragger shadow", x=196, y=768, width=210, height=30,
        fill=rad((0, INK, 52), (0.6, INK, 22), (1, INK, 0)),
        rotation=14, stroke=NONE)
# handle: tapered grip + knob
poly(rpoly([(358, 636), (388, 636), (380, 788), (366, 788)], *GC, GD),
     "Gragger handle", fill=lin((358, 640), (390, 790), (0, "#9A6030"),
                                (0.55, "#7A4620"), (1, "#4A2410")),
     stroke=INK, strokeWidth=3)
hx, hy = rot(373, 790, *GC, GD)
d.shape("ellipse", "Gragger knob", x=hx - 15, y=hy - 12, width=30, height=26,
        fill=rad((0, "#B87A44"), (1, "#5E3018")), stroke=INK, strokeWidth=2.6,
        rotation=GD)
# head block
poly(rpoly([(320, 566), (424, 566), (424, 664), (320, 664)], *GC, GD),
     "Gragger head", fill=lin((320, 566), (424, 664), (0, "#B87A44"),
                              (0.5, "#8A5426"), (1, "#5E3018")),
     stroke=INK, strokeWidth=3.4)
# gear crest along the top edge: four bold teeth
for i in range(4):
    tx = 330 + i * 26
    tooth = rpoly([(tx, 568), (tx + 11, 546), (tx + 22, 568)], *GC, GD)
    poly(tooth, f"Gragger tooth {i+1}", fill="#7A4620", stroke=INK,
         strokeWidth=2.4)
# the slapper blade sticking out past the head's lower edge
poly(rpoly([(304, 640), (346, 652), (344, 662), (300, 650)], *GC, GD),
     "Gragger blade", fill="#D9A05E", stroke=INK, strokeWidth=2)
# gold bands across the head
for i, yy in enumerate((586, 630)):
    band = rpoly([(324, yy), (420, yy), (420, yy + 9), (324, yy + 9)], *GC, GD)
    poly(band, f"Gragger band {i+1}", fill=gold_lin(0, 1000), opacity=88,
         stroke="#5E3A16", strokeWidth=1.2)
# ratchet slat across the face
poly(rpoly([(330, 604), (414, 596), (414, 606), (330, 614)], *GC, GD),
     "Gragger slat", fill="#D9A05E", stroke=INK, strokeWidth=1.8, opacity=95)
# side crank + peg
cx_, cy_ = rot(430, 612, *GC, GD)
d.shape("ellipse", "Gragger crank", x=cx_ - 9, y=cy_ - 9, width=18, height=18,
        fill=gold_lin(cy_ - 9, cy_ + 9), stroke=INK, strokeWidth=2.2)
px_, py_ = rot(446, 622, *GC, GD)
d.shape("ellipse", "Gragger peg", x=px_ - 6, y=py_ - 6, width=12, height=12,
        fill="#5E3018", stroke=INK, strokeWidth=1.8)
# wood grain hints
for i, (x0, y0, x1, y1) in enumerate([(336, 616, 366, 648),
                                      (392, 574, 412, 606)]):
    a, b = rot(x0, y0, *GC, GD), rot(x1, y1, *GC, GD)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} Q{(a[0]+b[0])/2+4:.1f},{(a[1]+b[1])/2:.1f} "
           f"{b[0]:.1f},{b[1]:.1f}", f"Gragger grain {i+1}", fill=NONE,
           stroke="#3A1C0C", strokeWidth=1.4, opacity=45, cap="round")

# --- hamantaschen platter ----------------------------------------------------
PLC, PLR = 628, 748
d.shape("ellipse", "Platter shadow", x=PLC - 150, y=PLR + 16, width=300,
        height=34, fill=rad((0, INK, 55), (0.6, INK, 24), (1, INK, 0)),
        stroke=NONE)
d.shape("ellipse", "Platter", x=PLC - 148, y=PLR - 52, width=296, height=112,
        fill=lin((PLC - 148, PLR - 52), (PLC + 148, PLR + 60),
                 (0, GOLD_HI), (0.5, "#C99B4E"), (1, "#8A5E20")),
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Platter well", x=PLC - 124, y=PLR - 40, width=248,
        height=88, fill=lin((PLC - 124, PLR - 40), (PLC + 124, PLR + 48),
                            (0, "#F4E8CC"), (1, "#D9BE92")),
        stroke="#8A5E20", strokeWidth=1.8, opacity=96)
d.path(f"M{PLC - 130},{PLR - 30} Q{PLC},{PLR - 52} {PLC + 130},{PLR - 30}",
       "Platter sheen", fill=NONE, stroke="#FFF6DC", strokeWidth=3,
       opacity=45, cap="round")


def hamantasch(cx, cy, s, deg, label, jam="#6E1F30"):
    vt = (0, -s)
    vl = (-s * 0.95, s * 0.68)
    vr = (s * 0.95, s * 0.68)
    mid = lambda a, b, k=0.5, push=1.10: (
        cx + (a[0] + b[0]) * k * push, cy + (a[1] + b[1]) * k * push)
    m1 = mid(vt, vr)
    m2 = mid(vr, vl)
    m3 = mid(vl, vt)

    def pt(v, k=0.92):
        return rot(cx + v[0] * k, cy + v[1] * k, cx, cy, deg)

    p1, p2, p3 = (rot(*m1, cx, cy, deg), rot(*m2, cx, cy, deg),
                  rot(*m3, cx, cy, deg))
    cvr, cvl, cvt = pt(vr), pt(vl), pt(vt)
    dd = (f"M{p1[0]:.1f},{p1[1]:.1f} Q{cvr[0]:.1f},{cvr[1]:.1f} "
          f"{p2[0]:.1f},{p2[1]:.1f} Q{cvl[0]:.1f},{cvl[1]:.1f} "
          f"{p3[0]:.1f},{p3[1]:.1f} Q{cvt[0]:.1f},{cvt[1]:.1f} "
          f"{p1[0]:.1f},{p1[1]:.1f} Z")
    d.path(dd, label, fill=lin((cx - s, cy - s), (cx + s, cy + s),
                               (0, "#EDBE7E"), (0.55, "#D9A05E"), (1, "#A86828")),
           stroke="#6E3E14", strokeWidth=2.6)
    # folded-dough inner edge
    k = 0.62
    inner = [(cx + v[0] * k, cy + v[1] * k) for v in (vt, vr, vl)]
    inner = rpoly(inner, cx, cy, deg)
    poly(inner, f"{label} fold", fill=NONE, stroke="#8A5020", strokeWidth=2,
         opacity=50)
    # jam centre
    jx, jy = rot(cx, cy + s * 0.16, cx, cy, deg)
    d.shape("ellipse", f"{label} jam", x=jx - s * 0.27, y=jy - s * 0.24,
            width=s * 0.54, height=s * 0.48,
            fill=rad((0, blend(jam, "#FFFFFF", 0.25)), (0.7, jam),
                     (1, blend(jam, "#000000", 0.3))),
            stroke="#40101C", strokeWidth=1.6)
    d.shape("ellipse", f"{label} jam gloss", x=jx - s * 0.14, y=jy - s * 0.16,
            width=s * 0.16, height=s * 0.10, fill="#FFDCE8", opacity=40,
            stroke=NONE)


hamantasch(570, 736, 62, -12, "Hamantasch L")
hamantasch(682, 730, 60, 9, "Hamantasch R", jam="#4A1830")
hamantasch(626, 762, 64, 17, "Hamantasch F", jam="#7A2440")

# --- masquerade mask ----------------------------------------------------------
glow(d, 500, 330, 200, "#D8B4F8", a=18, label="Mask glow", squash=0.6)
# ribbon ties curling off the tips
for sgn in (-1, 1):
    x0 = 500 + sgn * 168
    d.path(f"M{x0},{330} C{x0 + sgn * 40},{342} {x0 + sgn * 58},{368} "
           f"{x0 + sgn * 46},{396}", f"Mask tie {'L' if sgn < 0 else 'R'}",
           fill=NONE, stroke=GOLD, strokeWidth=4.2, opacity=85, cap="round")
    d.path(f"M{x0},{330} C{x0 + sgn * 44},{336} {x0 + sgn * 62},{352} "
           f"{x0 + sgn * 68},{372}", f"Mask tie 2 {'L' if sgn < 0 else 'R'}",
           fill=NONE, stroke=ROSE, strokeWidth=3.2, opacity=70, cap="round")
# body
d.path("M332,330 C352,302 388,290 424,296 C456,301 480,312 500,318 "
       "C520,312 544,301 576,296 C612,290 648,302 668,330 "
       "C660,346 620,352 580,348 C556,346 528,342 512,352 "
       "C506,356 494,356 488,352 C472,342 444,346 420,348 "
       "C380,352 340,346 332,330 Z",
       "Mask", fill=lin((332, 288), (668, 356), (0, "#7A46AE"),
                        (0.5, "#4A2278"), (1, "#2A1050")),
       stroke=INK, strokeWidth=4)
# top-edge gold trim
d.path("M340,326 C360,302 392,294 424,299 C456,304 480,314 500,320 "
       "C520,314 544,304 576,299 C608,294 640,302 660,326",
       "Mask gold trim", fill=NONE, stroke=GOLD, strokeWidth=3.2,
       opacity=88, cap="round")
# sheen along the brow
d.path("M368,312 C420,300 470,308 500,316 C530,308 580,300 632,312",
       "Mask sheen", fill=NONE, stroke="#C9A0F0", strokeWidth=6,
       opacity=26, cap="round")
# eye holes: almond shapes
for cx, lab in ((424, "Eye L"), (576, "Eye R")):
    d.path(f"M{cx - 32},{321} Q{cx},{302} {cx + 32},{321} "
           f"Q{cx},{340} {cx - 32},{321} Z", f"Mask {lab}",
           fill="#160826", stroke=INK, strokeWidth=2.4)
    d.path(f"M{cx - 27},{319} Q{cx},{305} {cx + 27},{319}", f"{lab} glint",
           fill=NONE, stroke="#8A68C8", strokeWidth=2, opacity=50, cap="round")
# temple swirls
for sgn in (-1, 1):
    cx = 500 + sgn * 132
    d.path(f"M{cx},{332} c{sgn * 16},{-4} {sgn * 22},{-14} {sgn * 14},{-24} "
           f"c{sgn * -8},{-9} {sgn * -20},{-6} {sgn * -20},{4}",
           f"Mask swirl {'L' if sgn < 0 else 'R'}", fill=NONE, stroke=GOLD,
           strokeWidth=2.4, opacity=80, cap="round")
    for k in range(3):
        dx = sgn * (96 + k * 14)
        d.shape("ellipse", f"Mask dot {sgn}-{k}", x=500 + dx - 2.4,
                y=306 + k * 8, width=4.8, height=4.8, fill=GOLD_HI,
                opacity=75, stroke=NONE)
# centre jewel on the bridge
poly([(500, 300), (510, 312), (500, 324), (490, 312)], "Mask jewel",
     fill=rad((0, "#FFE9B8"), (0.7, "#E8B84E"), (1, "#9A6A24")),
     stroke="#5E3A16", strokeWidth=1.6)

# --- confetti -----------------------------------------------------------------
CONF = [(280, 250, 7, 20, GOLD), (726, 240, 8, -30, ROSE), (252, 420, 6, 45, VIOLET),
        (770, 430, 7, 12, GOLD), (322, 176, 5, -15, "#F4E7CE"), (692, 172, 6, 60, VIOLET),
        (200, 330, 6, 70, ROSE), (806, 330, 5, -40, "#F4E7CE"), (360, 216, 5, 35, ROSE),
        (640, 210, 6, -55, GOLD), (300, 500, 5, 25, "#F4E7CE"), (722, 520, 6, -20, VIOLET)]
for i, (x, y, s, ang, col) in enumerate(CONF):
    inside(x, y, 12, f"confetti {i}")
    d.shape("rectangle", f"Confetti {i+1}", x=x - s / 2, y=y - s / 3, width=s,
            height=s * 0.66, fill=col, opacity=82, rotation=ang, stroke=NONE)
for i, (x0, y0, x1, y1, col) in enumerate([
        (268, 300, 240, 372, ROSE), (748, 296, 782, 366, GOLD),
        (392, 168, 372, 226, GOLD), (612, 162, 632, 224, VIOLET),
        (420, 470, 396, 536, "#F4E7CE"), (586, 462, 610, 528, ROSE)]):
    d.path(f"M{x0},{y0} C{x0 - 18},{y0 + 30} {x1 + 18},{y1 - 34} {x1},{y1}",
           f"Streamer {i+1}", fill=NONE, stroke=col, strokeWidth=3.4,
           opacity=62, cap="round")
for i, (x, y, s, ang, col) in enumerate([
        (468, 500, 6, 30, GOLD), (548, 520, 5, -35, VIOLET),
        (502, 560, 6, 55, ROSE), (360, 560, 5, 10, "#F4E7CE")]):
    inside(x, y, 12, f"mid confetti {i}")
    d.shape("rectangle", f"Mid confetti {i+1}", x=x - s / 2, y=y - s / 3,
            width=s, height=s * 0.66, fill=col, opacity=78, rotation=ang,
            stroke=NONE)

# --- chop + caption -----------------------------------------------------------
CHX, CHY, CHW, CHH = 706, 150, 50, 142
inside(CHX + CHW, CHY, 6, "chop TR")
inside(CHX + CHW, CHY + CHH, 6, "chop BR")
d.shape("rectangle", "Chop shadow", x=CHX + 3, y=CHY + 4, width=CHW, height=CHH,
        radius=4, fill="#000000", opacity=30, stroke=NONE)
p.chop("פורים", x=CHX, y=CHY, w=CHW, h=CHH, size=26, font=HEBREW)

caption(p, "PURIM", "14 ADAR · MARCH",
        sub_font=DIGITS, name_color="#F6E7C8", sub_color="#C9A46A",
        name_size=52, tracking_name=90, sub_size=20, tracking_sub=40)

p.finish(SLUG)
