#!/usr/bin/env python3
"""Vesak — Festival Seal V1R00.

A string of lit paper lanterns sagging across the upper disc under the
full moon of Vaisakha, a gold lotus blooming on still water below.
Gold on deep sky. 1000x1000. The chop carries Devanagari वैशाख, set
horizontally — the script needs shaping, so it can't be stacked.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, NONE, INK, GOLD, GOLD_HI, GOLD_LO, PAPER, LATIN,
                          PCX, PCY, PR, lin, rad, gold_lin, smooth, blend)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "vesak-V1R00"
DEVA = "ITF Devanagari"
DIGITS = "Source Sans 3"

p = Plate("Vesak — Festival Seal", 1000, 1000)
d = p.d


def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


# --- field ------------------------------------------------------------------
p.backdrop(top="#0A1A2C", bottom="#02060C", glow=("#1E4E6E", 12))
p.stars(n=34, color="#F6E3B8", seed=23, maxr=2.2)
seal_disc(p, "#26547C", "#081C30", rim=GOLD, rim2="#4A3418")
d.shape("ellipse", "Vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.6, "#000000", 0), (1, "#000000", 54)),
        stroke=NONE)
dust(d, n=50, r=392, colors=("#F6E3B8", "#9FC0E8", "#E8C074"), seed=41,
     smin=1.0, smax=2.6, opmin=8, opmax=24, label="Disc dust")
ring_dots(d, r=396, n=60, size=2.4, color=GOLD, opacity=30)
# a scatter of larger stars inside the sky
for i, (x, y, s) in enumerate([(240, 300, 2.6), (760, 330, 2.2), (300, 180, 2.0),
                               (700, 150, 2.4), (176, 420, 1.8), (812, 470, 2.0),
                               (262, 560, 1.8), (756, 590, 1.6)]):
    inside(x, y, 12, f"sky star {i}")
    d.shape("ellipse", f"Sky star {i+1}", x=x - s, y=y - s, width=2 * s,
            height=2 * s, fill="#F6E3B8", opacity=70, stroke=NONE)
    d.shape("ellipse", f"Sky star halo {i+1}", x=x - s * 3, y=y - s * 3,
            width=6 * s, height=6 * s,
            fill=rad((0, "#F6E3B8", 22), (1, "#F6E3B8", 0)), stroke=NONE)

# --- the Vaisakha full moon ---------------------------------------------------
MX, MY, MR = 372, 226, 62
inside(MX, MY, MR + 40, "moon")
d.shape("ellipse", "Moon halo", x=MX - MR * 2.1, y=MY - MR * 2.1,
        width=MR * 4.2, height=MR * 4.2,
        fill=rad((0, "#FFE9B8", 26), (0.5, "#E8C074", 9), (1, "#E8C074", 0)),
        stroke=NONE)
d.shape("ellipse", "Moon", x=MX - MR, y=MY - MR, width=2 * MR, height=2 * MR,
        fill=rad((0, "#FBF0D4"), (0.7, "#F2DCA6"), (1, "#D9BC7E")),
        stroke="#B89A5E", strokeWidth=1.8)
for i, (dx, dy, r, op) in enumerate([(-18, -14, 9, 22), (12, 8, 13, 18),
                                     (-8, 22, 7, 20), (24, -18, 6, 16)]):
    d.shape("ellipse", f"Moon mark {i+1}", x=MX + dx - r, y=MY + dy - r,
            width=2 * r, height=2 * r, fill="#D9BC7E", opacity=op, stroke=NONE)

# --- lantern string ------------------------------------------------------------
# cord across the upper disc, sagging
CX0, CY0, CX1, CY1, SAG = 180, 216, 812, 206, 74
inside(CX0, CY0, 8, "cord L")
inside(CX1, CY1, 8, "cord R")
MXX, MYY = (CX0 + CX1) / 2, (CY0 + CY1) / 2 + SAG
d.path(f"M{CX0},{CY0} Q{MXX},{MYY} {CX1},{CY1}", "String cord",
       fill=NONE, stroke="#3A2410", strokeWidth=4, cap="round")
d.path(f"M{CX0},{CY0} Q{MXX},{MYY} {CX1},{CY1}", "String cord light",
       fill=NONE, stroke="#8A6A34", strokeWidth=1.6, opacity=80, cap="round")


def cord_pt(t):
    mt = 1 - t
    return (mt * mt * CX0 + 2 * mt * t * MXX + t * t * CX1,
            mt * mt * CY0 + 2 * mt * t * MYY + t * t * CY1)


def vesak_lantern(cx, top_y, w, h, label):
    """Pointed paper lantern, lit from within; hangs from top_y."""
    a, b = w / 2, h / 2
    cy = top_y + b
    # glow
    d.shape("ellipse", f"{label} glow", x=cx - w * 1.05, y=cy - h * 0.95,
            width=w * 2.1, height=h * 1.9,
            fill=rad((0, "#FFD08A", 30), (0.5, "#E8A84E", 10),
                     (1, "#E8A84E", 0)), stroke=NONE)
    # hanger line
    d.path(f"M{cx:.1f},{top_y - b - 26:.1f} L{cx:.1f},{cy - b - 8:.1f}",
           f"{label} hanger", fill=NONE, stroke="#8A6A34", strokeWidth=2.2,
           cap="round")
    # body: hexagonal paper lantern, wide mid, pointed top and bottom
    d.path(f"M{cx:.1f},{cy - b:.1f} "
           f"C{cx + a * 0.62:.1f},{cy - b * 0.94:.1f} {cx + a:.1f},{cy - b * 0.42:.1f} "
           f"{cx + a:.1f},{cy:.1f} "
           f"C{cx + a:.1f},{cy + b * 0.48:.1f} {cx + a * 0.5:.1f},{cy + b * 0.80:.1f} "
           f"{cx:.1f},{cy + b:.1f} "
           f"C{cx - a * 0.5:.1f},{cy + b * 0.80:.1f} {cx - a:.1f},{cy + b * 0.48:.1f} "
           f"{cx - a:.1f},{cy:.1f} "
           f"C{cx - a:.1f},{cy - b * 0.42:.1f} {cx - a * 0.62:.1f},{cy - b * 0.94:.1f} "
           f"{cx:.1f},{cy - b:.1f} Z",
           label, fill=lin((cx, cy - b), (cx, cy + b),
                           (0, "#FFE9B8"), (0.42, "#F2B45C"),
                           (0.8, "#D9903A"), (1, "#A86824")),
           stroke=INK, strokeWidth=2.6)
    # ribs converging to the points
    for k in (-0.62, -0.32, 0.0, 0.32, 0.62):
        x = cx + k * a * 0.92
        d.path(f"M{x:.1f},{cy - b * 0.86:.1f} Q{cx + k * a * 1.02:.1f},{cy:.1f} "
               f"{x:.1f},{cy + b * 0.86:.1f}", f"{label} rib {k}", fill=NONE,
               stroke="#8A5E20", strokeWidth=1.3, opacity=42, cap="round")
    # lit core
    d.shape("ellipse", f"{label} core", x=cx - w * 0.20, y=cy - h * 0.16,
            width=w * 0.40, height=h * 0.34,
            fill=rad((0, "#FFF6DC", 88), (0.7, "#FFD98A", 30),
                     (1, "#FFD98A", 0)), stroke=NONE)
    # caps
    for yy, lab in ((cy - b - 2, "top"), (cy + b - 8, "bottom")):
        d.shape("ellipse", f"{label} cap {lab}", x=cx - 9, y=yy, width=18,
                height=10, fill=gold_lin(yy, yy + 10), stroke=INK,
                strokeWidth=1.6)
    # tassel
    ty = cy + b + 2
    d.path(f"M{cx:.1f},{ty:.1f} C{cx - 4:.1f},{ty + 12:.1f} {cx + 5:.1f},{ty + 22:.1f} "
           f"{cx:.1f},{ty + 34:.1f}", f"{label} tassel", fill=NONE,
           stroke="#C0392E", strokeWidth=2.6, opacity=88, cap="round")
    d.shape("ellipse", f"{label} bead", x=cx - 4, y=ty + 30, width=8, height=8,
            fill=GOLD_HI, opacity=90, stroke=INK, strokeWidth=1)


for i, (t, w, h, drop) in enumerate([
        (0.14, 56, 64, 26), (0.32, 64, 74, 40), (0.50, 72, 84, 30),
        (0.68, 62, 70, 44), (0.86, 54, 62, 24)]):
    x, y = cord_pt(t)
    top = y + drop + (w * 0) + h / 2 + 0   # lantern centre sits below cord
    inside(x, top + h / 2 + 44, 8, f"lantern {i}")
    vesak_lantern(x, y + drop, w, h, f"Lantern {i+1}")

# --- water --------------------------------------------------------------------
# the still pond occupies the bottom of the disc
d.shape("ellipse", "Water line", x=150, y=706, width=700, height=60,
        fill=rad((0, "#16405E", 80), (0.7, "#0E2E48", 60), (1, "#0E2E48", 0)),
        stroke=NONE)
for i, (x0, w_, op) in enumerate([(330, 180, 34), (520, 210, 30),
                                  (390, 120, 26), (560, 140, 22)]):
    y = 748 + i * 16
    d.path(f"M{x0},{y} Q{x0 + w_ / 2},{y - 7} {x0 + w_},{y}", f"Ripple {i+1}",
           fill=NONE, stroke="#7EA4DC", strokeWidth=2.2, opacity=op,
           cap="round")
# lantern light caught on the water
glow(d, 500, 736, 210, "#F2B45C", a=14, label="Water light", squash=0.22)

# --- the lotus ----------------------------------------------------------------
glow(d, 500, 650, 190, "#F8D488", a=22, label="Lotus aura", squash=0.8)


def petal(bx, by, deg, ln, half, fill, label, edge="#8A5E20", sw=2.0,
          op=95):
    a = math.radians(deg)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    tx, ty = bx + dx * ln, by + dy * ln
    c1 = (bx + dx * ln * 0.44 + nx * half, by + dy * ln * 0.44 + ny * half)
    c2 = (bx + dx * ln * 0.44 - nx * half, by + dy * ln * 0.44 - ny * half)
    d.path(f"M{bx:.1f},{by:.1f} Q{c1[0]:.1f},{c1[1]:.1f} {tx:.1f},{ty:.1f} "
           f"Q{c2[0]:.1f},{c2[1]:.1f} {bx:.1f},{by:.1f} Z", label,
           fill=lin((bx, by), (tx, ty), (0, blend(fill, "#000000", 0.18)),
                    (0.55, fill), (1, blend(fill, "#FFFFFF", 0.22))),
           stroke=edge, strokeWidth=sw, opacity=op)


# bloom rises from a base sitting on the water
LB = (500, 712)
# outer ring: wide splayed petals
for i, a in enumerate(range(-166, -13, 19)):
    petal(*LB, a, 148, 46, "#D99434", f"Lotus outer {i+1}")
# mid ring
for i, a in enumerate(range(-152, -27, 21)):
    petal(*LB, a, 122, 44, "#F2B45C", f"Lotus mid {i+1}")
# inner ring, nearly upright
for i, a in enumerate((-118, -104, -90, -76, -62)):
    petal(*LB, a, 96, 38, "#FBE0A8", f"Lotus inner {i+1}")
# seed pod dome + stamen fringe
d.path("M472,700 C474,682 490,672 500,672 C510,672 526,682 528,700 "
       "C520,708 480,708 472,700 Z",
       "Lotus pod", fill=rad((0, "#FFF6DC"), (0.7, "#F2D08A"), (1, "#C99B4E")),
       stroke="#8A5E20", strokeWidth=1.8)
for i in range(9):
    a = math.radians(-168 + i * 21)
    x, y = LB[0] + math.cos(a) * 30, LB[1] - 14 + math.sin(a) * 20
    d.shape("ellipse", f"Lotus stamen {i+1}", x=x - 2.4, y=y - 2.4,
            width=4.8, height=4.8, fill="#FFF0C0", opacity=85, stroke=NONE)
# reflection on the water
d.shape("ellipse", "Lotus reflection", x=420, y=714, width=160, height=30,
        fill=rad((0, "#F8D488", 34), (0.6, "#E8A84E", 12), (1, "#E8A84E", 0)),
        stroke=NONE)

# pads flanking, resting on the water line
for sgn in (-1, 1):
    px = 500 + sgn * 178
    d.shape("ellipse", f"Pad {'L' if sgn < 0 else 'R'}", x=px - 52, y=726,
            width=104, height=30,
            fill=lin((px - 52, 726), (px + 52, 756), (0, "#3E7A5E"),
                     (1, "#1E4634")), stroke="#122E22", strokeWidth=2.2)
    d.path(f"M{px - 44},{734} Q{px},{742} {px + 44},{734}",
           f"Pad rim {'L' if sgn < 0 else 'R'}", fill=NONE, stroke="#8AC8A0",
           strokeWidth=2, opacity=55, cap="round")
    d.shape("ellipse", f"Pad shadow {'L' if sgn < 0 else 'R'}", x=px - 48,
            y=742, width=96, height=12, fill=INK, opacity=26, stroke=NONE)
# a drifting petal on the water
d.shape("ellipse", "Fallen petal", x=616, y=772, width=26, height=14,
        fill="#F8D488", opacity=88, stroke="#8A5E20", strokeWidth=1.4,
        rotation=-18)
d.shape("ellipse", "Fallen petal 2", x=378, y=784, width=20, height=11,
        fill="#E8A84E", opacity=80, stroke="#8A5E20", strokeWidth=1.2,
        rotation=24)

# --- chop + caption -----------------------------------------------------------
# Devanagari needs shaping: stamp it horizontally.
CHX, CHY, CHW, CHH = 658, 166, 118, 54
inside(CHX + CHW, CHY, 6, "chop TR")
inside(CHX + CHW, CHY + CHH, 6, "chop BR")
inside(CHX, CHY, 6, "chop TL")
d.shape("rectangle", "Chop shadow", x=CHX + 3, y=CHY + 4, width=CHW, height=CHH,
        radius=4, fill="#000000", opacity=30, stroke=NONE)
p.chop("वैशाख", x=CHX, y=CHY, w=CHW, h=CHH, size=22, font=DEVA, horizontal=True)

caption(p, "VESAK", "FULL MOON OF VAISAKHA · MAY",
        sub_font=DIGITS, name_color="#F6E7C8", sub_color="#C9A46A",
        name_size=52, tracking_name=90, sub_size=20, tracking_sub=40)

p.finish(SLUG)
