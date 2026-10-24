#!/usr/bin/env python3
"""Navratri — Festival Seal V1R00.

Nine nights, nine lamps: a row of nine lit diyas follows the disc's lower
arc, one per night. Above them, the crossed dandiya sticks — lacquered wood,
painted bands, mirror studs and ribbon ends — crossed in the garba position.
Royal crimson and gold with green accents. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, PAPER,
                          LATIN, DEVA, lin, rad, gold_lin, smooth)
from festival_kit import seal_disc, glow, dust, ring_dots, lamp, deva_seal, caption

SLUG = "navratri-V1R00"
CRIMSON = "#5A1628"
CRIMSON_LO = "#1A050E"
GREEN = "#2E7A4A"
GREEN_HI = "#5AA878"
STICK = "#B87848"
STICK_HI = "#D8A068"
RIBBON = "#C23250"

p = Plate("Navratri — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def dandiya(cx, cy, length, width, rot, label):
    """One lacquered dandiya stick: rounded body, painted bands, capped ends."""
    a = math.radians(rot)
    ux, uy = math.cos(a), math.sin(a)
    half = length / 2
    d.shape("rectangle", label, x=cx - half, y=cy - width / 2,
            width=length, height=width, radius=width / 2,
            fill=lin((cx - half * ux, cy - half * uy),
                     (cx + half * ux, cy + half * uy),
                     (0, STICK_HI), (0.5, STICK), (1, "#7A4626")),
            stroke=INK, strokeWidth=3, rotation=rot)
    # painted bands along the axis
    for t, col in ((-0.72, GREEN), (-0.52, GOLD), (-0.32, GREEN),
                   (0.32, GREEN), (0.52, GOLD), (0.72, GREEN)):
        bx, by = cx + ux * half * t, cy + uy * half * t
        d.shape("rectangle", f"{label} band {t}", x=bx - 3.4, y=by - width / 2 + 1,
                width=6.8, height=width - 2, radius=3, fill=col,
                stroke=INK, strokeWidth=1.4, rotation=rot)
    for t in (-0.62, -0.42, 0.42, 0.62):
        bx, by = cx + ux * half * t, cy + uy * half * t
        d.shape("ellipse", f"{label} stud {t}", x=bx - 2.2, y=by - 2.2,
                width=4.4, height=4.4, fill=GOLD_HI, stroke=INK, strokeWidth=0.8,
                opacity=92)
    # gold caps + knotted ribbon tails at both ends
    for sign in (-1, 1):
        ex, ey = cx + ux * half * sign, cy + uy * half * sign
        d.shape("ellipse", f"{label} cap {sign}", x=ex - width * 0.42,
                y=ey - width * 0.42, width=width * 0.84, height=width * 0.84,
                fill=rad((0, GOLD_HI), (0.6, GOLD), (1, "#8E5A1E")),
                stroke=INK, strokeWidth=2.4)
        d.shape("ellipse", f"{label} knot {sign}", x=ex - 4, y=ey - 4,
                width=8, height=8, fill=RIBBON, stroke="#6E1428",
                strokeWidth=1.2)
        for k, swing in enumerate((-0.55, 0.5)):
            ex2 = ex + math.cos(a) * sign * 4 + swing * 10
            ey2 = ey + 30 + (6 if k else 0)
            mx2 = ex + swing * 4
            my2 = ey + 15
            inside(ex2, ey2, 12, f"{label} tail {sign}{k}")
            d.path(f"M{ex:.1f},{ey:.1f} Q{mx2:.1f},{my2:.1f} {ex2:.1f},{ey2:.1f}",
                   f"{label} ribbon {sign}-{k+1}", fill=NONE, stroke=RIBBON,
                   strokeWidth=3.2, cap="round")


# --- field ------------------------------------------------------------------
p.backdrop(top="#241018", bottom="#08030A", glow=("#7E2440", 12))
dust(d, n=40, r=402, colors=("#F6E3B8", "#F2A33C"), seed=29,
     smin=1.0, smax=2.4, opmin=8, opmax=22, label="Backdrop dust")
seal_disc(p, CRIMSON, CRIMSON_LO, rim=GOLD, rim2="#3E1020")
dust(d, n=60, r=390, colors=("#F6E3B8", "#F2A33C", "#E8C074"), seed=13,
     smin=1.0, smax=3.0, opmin=10, opmax=30, label="Disc dust")
d.shape("ellipse", "Rim relight", x=86, y=46, width=828, height=828, fill=NONE,
        stroke=lin((86, 46), (914, 874), (0, "#F2CC8E"), (0.5, "#B0804A"),
                   (1, "#E8BC78")), strokeWidth=4)
# faint garba rays
for i in range(36):
    a = math.radians(i * 10)
    x0, y0 = PCX + 130 * math.cos(a), PCY + 130 * math.sin(a)
    x1, y1 = PCX + 372 * math.cos(a), PCY + 372 * math.sin(a)
    d.shape("line", f"Field ray {i+1}", x1=round(x0, 1), y1=round(y0, 1),
            x2=round(x1, 1), y2=round(y1, 1), stroke=GOLD, strokeWidth=1.5,
            opacity=7, cap="round")
ring_dots(d, r=397, n=56, size=2.6, color=GOLD, opacity=32)
p.ring_ticks(n=24, color="#B08656", r_in=378, r_out=396, width=2.2)

# --- the nine lamps ------------------------------------------------------------
for i in range(9):
    a = math.radians(15 + i * 18.75)
    lx = PCX + 304 * math.cos(a)
    ly = PCY + 304 * math.sin(a)
    inside(lx + 40, ly + 30, 12, f"diya {i}")
    lamp(d, lx, ly, 68, label=f"Night lamp {i+1}", flame_h=58, glow_a=22)

# --- crossed dandiya -------------------------------------------------------------
DXC, DYC = 500, 402
inside(DXC - 180, DYC - 90, 12, "dandiya A end")
inside(DXC + 180, DYC + 90, 12, "dandiya B end")
glow(d, DXC, DYC, 190, "#E8A850", a=16, label="Dandiya glow")
dandiya(DXC, DYC, 356, 30, -28, "Dandiya A")
dandiya(DXC, DYC, 356, 30, 28, "Dandiya B")
# crossing knot
d.shape("ellipse", "Cross band", x=DXC - 17, y=DYC - 17, width=34, height=34,
        fill=rad((0, GOLD_HI), (0.6, GOLD), (1, "#8E5A1E")), stroke=INK,
        strokeWidth=2.6)
d.shape("ellipse", "Cross stud", x=DXC - 5, y=DYC - 5, width=10, height=10,
        fill="#FFF3CC", stroke=INK, strokeWidth=1.2)

# --- sparks ------------------------------------------------------------------------
for i, (x, y, s) in enumerate([(386, 300, 2.6), (616, 330, 2.2), (444, 520, 2.0),
                               (570, 486, 2.4), (500, 260, 1.8)]):
    glow(d, x, y, 12, "#FFD98A", a=38, label=f"Spark glow {i+1}")
    d.shape("ellipse", f"Spark {i+1}", x=x - s, y=y - s, width=s * 2,
            height=s * 2, fill="#FFF2C4", opacity=85, stroke=NONE)

# --- seal + caption ------------------------------------------------------------------
deva_seal(d, "नव", cx=744, cy=213, s=64, size=27)
caption(p, "NAVRATRI", "नवरात्रि · NINE NIGHTS · ASHWIN",
        name_color="#F8E8CC", sub_color="#D8A468",
        name_size=52, tracking_name=96, sub_size=20, tracking_sub=60)
p.finish(SLUG)
