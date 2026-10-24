#!/usr/bin/env python3
"""Mid-Autumn — Festival Seal V1R00.

The moon plate: a huge warm full moon fills the disc, soft craters on its
face, fine stars in the sky crescent above it. Osmanthus reaches in from the
upper left, silver clouds cross the moon, the jade rabbit sits on a cloud at
its foot with a small cake in its paws, and a patterned mooncake rests on a
round mat at the lower left. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, PAPER,
                          LATIN, CJK, lin, rad, gold_lin, smooth, blend)
from cn_kit import mooncake, osmanthus

SLUG = "mid-autumn-V1R00"
MOON_HI = "#F8EFD2"
MOON = "#F2DFAC"
MOON_LO = "#D8A85E"
SKY_HI = "#232344"
SKY_LO = "#0B0B1E"

p = Plate("Mid-Autumn — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def cloud_drift(d, cx, cy, w, label, color="#C8C4DC", opacity=16):
    for i, (dx, dy, r) in enumerate([(-0.32, 0.05, 0.28), (-0.08, -0.08, 0.34),
                                     (0.2, 0.0, 0.3), (0.4, 0.08, 0.2)]):
        d.shape("ellipse", f"{label} puff {i+1}", x=cx + dx * w - r * w,
                y=cy + dy * w - r * w * 0.6, width=r * 2 * w, height=r * 1.2 * w,
                fill=color, opacity=opacity, stroke=NONE)


def jade_rabbit2(d, cx, cy, s, label="Jade rabbit"):
    """Sitting jade rabbit facing left, ears connected, cake in its paws."""
    JADE_HI, JADE, JADE_LO = "#F4FBEE", "#D8ECD8", "#A8CCB4"
    # ears (drawn first, bases tucked into the head)
    for sign, nm in ((-1, "L"), (1, "R")):
        bx, by = cx + sign * 9 * s, cy - 44 * s
        tx, ty = cx + sign * 17 * s, cy - 96 * s
        d.path(f"M{bx - 8*s:.1f},{by:.1f} "
               f"C{bx - 12*s:.1f},{by - 26*s:.1f} {tx - 8*s:.1f},{ty + 18*s:.1f} {tx:.1f},{ty:.1f} "
               f"C{tx + 8*s:.1f},{ty + 18*s:.1f} {bx + 12*s:.1f},{by - 26*s:.1f} {bx + 8*s:.1f},{by:.1f} Z",
               f"{label} ear {nm}",
               fill=lin(0, ty, 0, by, (0, JADE_HI), (1, JADE)),
               stroke=INK, strokeWidth=2.6)
        d.path(f"M{bx + sign*2*s:.1f},{by - 8*s:.1f} "
               f"C{bx + sign*4*s:.1f},{by - 26*s:.1f} {tx + sign*2*s:.1f},{ty + 20*s:.1f} {tx + sign*1*s:.1f},{ty + 4*s:.1f}",
               f"{label} ear inner {nm}", fill=NONE, stroke="#E8A8B8",
               strokeWidth=4.5 * s, opacity=60, cap="round")
    # body bean
    d.path(f"M{cx - 30*s:.1f},{cy + 18*s:.1f} "
           f"C{cx - 34*s:.1f},{cy - 8*s:.1f} {cx - 16*s:.1f},{cy - 26*s:.1f} {cx + 4*s:.1f},{cy - 26*s:.1f} "
           f"C{cx + 24*s:.1f},{cy - 26*s:.1f} {cx + 36*s:.1f},{cy - 4*s:.1f} {cx + 33*s:.1f},{cy + 20*s:.1f} "
           f"C{cx + 31*s:.1f},{cy + 34*s:.1f} {cx - 27*s:.1f},{cy + 34*s:.1f} {cx - 30*s:.1f},{cy + 18*s:.1f} Z",
           f"{label} body", fill=rad((0, JADE_HI), (0.55, JADE), (1, JADE_LO)),
           stroke=INK, strokeWidth=3)
    # haunch shading
    d.shape("ellipse", f"{label} haunch", x=cx + 6 * s, y=cy - 2 * s,
            width=26 * s, height=30 * s, fill=rad((0, JADE_LO, 26),
                                                  (1, JADE_LO, 0)), stroke=NONE)
    # head circle overlapping the body
    d.shape("ellipse", f"{label} head", x=cx - 36 * s, y=cy - 56 * s,
            width=40 * s, height=38 * s,
            fill=rad((0, JADE_HI), (0.6, JADE), (1, JADE_LO)),
            stroke=INK, strokeWidth=3)
    # face
    for ex in (-26, -11):
        d.shape("ellipse", f"{label} eye {ex}", x=cx + ex * s - 2.4 * s,
                y=cy - 42 * s, width=4.8 * s, height=5.6 * s, fill="#2A1A18",
                stroke=NONE)
        d.shape("ellipse", f"{label} eye glint {ex}", x=cx + (ex + 0.8) * s - 0.9 * s,
                y=cy - 41 * s, width=1.8 * s, height=1.8 * s, fill="#FFFFFF",
                opacity=85, stroke=NONE)
    d.path(f"M{cx - 19*s:.1f},{cy - 34*s:.1f} L{cx - 16*s:.1f},{cy - 31.5*s:.1f} "
           f"L{cx - 13*s:.1f},{cy - 34*s:.1f}", f"{label} nose", fill=NONE,
           stroke="#C87A8A", strokeWidth=2 * s, cap="round")
    d.path(f"M{cx - 16*s:.1f},{cy - 31.5*s:.1f} Q{cx - 16*s:.1f},{cy - 28*s:.1f} "
           f"{cx - 20*s:.1f},{cy - 27.5*s:.1f} M{cx - 16*s:.1f},{cy - 31.5*s:.1f} "
           f"Q{cx - 16*s:.1f},{cy - 28*s:.1f} {cx - 12*s:.1f},{cy - 27.5*s:.1f}",
           f"{label} mouth", fill=NONE, stroke=INK, strokeWidth=1.5 * s,
           opacity=70, cap="round")
    for bx2 in (-30, -6):
        d.shape("ellipse", f"{label} blush {bx2}", x=cx + bx2 * s - 4 * s,
                y=cy - 34 * s, width=8 * s, height=4.5 * s, fill="#F2B8C0",
                opacity=42, stroke=NONE)
    # cake in the paws
    d.shape("ellipse", f"{label} cake", x=cx - 32 * s, y=cy + 12 * s,
            width=30 * s, height=24 * s,
            fill=rad((0, "#F6D48E"), (0.6, "#DCA452"), (1, "#A86A24")),
            stroke=INK, strokeWidth=2.4)
    d.shape("ellipse", f"{label} cake well", x=cx - 25 * s, y=cy + 17 * s,
            width=16 * s, height=12 * s, fill=NONE, stroke="#8A5A1E",
            strokeWidth=1.6, opacity=70)
    # front paws over the cake
    for px in (-30, -14):
        d.shape("ellipse", f"{label} paw {px}", x=cx + px * s - 8 * s,
                y=cy + 18 * s, width=17 * s, height=11 * s,
                fill=rad((0, JADE_HI), (0.65, JADE), (1, JADE_LO)),
                stroke=INK, strokeWidth=2.4)


# --- field ------------------------------------------------------------------
p.backdrop(top="#1A182E", bottom="#07060F", glow=("#5E4A28", 10))
p.disc(SKY_HI, SKY_LO, rim=GOLD, rim2="#241E3C")
d.shape("ellipse", "Vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.58, "#000000", 0), (1, "#000000", 64)),
        stroke=NONE)
d.shape("ellipse", "Rim relight", x=86, y=46, width=828, height=828, fill=NONE,
        stroke=lin((86, 46), (914, 874), (0, "#F0DCA0"), (0.5, "#A8864E"),
                   (1, "#E8CE8E")), strokeWidth=4)
p.ring_ticks(n=24, color="#9A8A66", r_in=378, r_out=396, width=2.2)

# --- fine stars in the sky crescent (outside the moon, inside the disc) ------
MX, MY, MR = 500, 400, 268
s = 17
for i in range(120):
    s = (1103515245 * s + 12345) % (2 ** 31)
    x = 120 + (s % 10000) / 10000 * 760
    s = (1103515245 * s + 12345) % (2 ** 31)
    y = 70 + (s % 10000) / 10000 * 660
    s = (1103515245 * s + 12345) % (2 ** 31)
    rr = 0.8 + (s % 1000) / 1000 * 1.7
    s = (1103515245 * s + 12345) % (2 ** 31)
    if math.hypot(x - PCX, y - PCY) > 392 or math.hypot(x - MX, y - MY) < 296:
        continue
    d.shape("ellipse", f"Sky star {i+1}", x=round(x - rr, 1), y=round(y - rr, 1),
            width=rr * 2, height=rr * 2, fill="#F2E6C0" if i % 3 else "#EDEAFA",
            opacity=16 + (s % 34), stroke=NONE)

# --- the full moon ------------------------------------------------------------
inside(MX, MY - MR, 12, "moon top")
inside(MX - MR, MY, 12, "moon L")
inside(MX + MR, MY, 12, "moon R")
d.shape("ellipse", "Moon halo", x=MX - MR - 34, y=MY - MR - 34,
        width=(MR + 34) * 2, height=(MR + 34) * 2,
        fill=rad((0, "#F6E3B8", 26), (0.72, "#E8C878", 9), (1, "#E8C878", 0)),
        stroke=NONE)
d.shape("ellipse", "Moon", x=MX - MR, y=MY - MR, width=MR * 2, height=MR * 2,
        fill=lin((MX - MR, MY - MR), (MX + MR * 0.6, MY + MR),
                 (0, MOON_HI), (0.55, MOON), (1, MOON_LO)),
        stroke=NONE)
# soft mare patches and craters
d.shape("ellipse", "Moon mare", x=MX - 190, y=MY - 150, width=230, height=190,
        fill=rad((0, "#D8B878", 16), (1, "#D8B878", 0)), stroke=NONE)
d.shape("ellipse", "Moon mare 2", x=MX + 40, y=MY + 10, width=180, height=150,
        fill=rad((0, "#D8B878", 12), (1, "#D8B878", 0)), stroke=NONE)
for i, (dx, dy, cr, op) in enumerate([(-120, -90, 30, 15), (-40, -140, 18, 13),
                                      (90, -60, 24, 14), (150, 40, 16, 12),
                                      (-150, 60, 20, 12), (30, -20, 14, 10),
                                      (110, 130, 22, 12), (-70, 110, 16, 11)]):
    d.shape("ellipse", f"Moon crater {i+1}", x=MX + dx - cr, y=MY + dy - cr,
            width=cr * 2, height=cr * 2, fill=blend(MOON, "#B89050", 0.35),
            opacity=op, stroke=NONE)
    d.shape("ellipse", f"Moon crater rim {i+1}", x=MX + dx - cr, y=MY + dy - cr,
            width=cr * 2, height=cr * 2, fill=NONE,
            stroke=blend(MOON_HI, "#FFFFFF", 0.4), strokeWidth=1.6,
            opacity=28)
# limb shading + thin bright rim on the upper left
d.shape("ellipse", "Moon limb", x=MX - MR, y=MY - MR, width=MR * 2,
        height=MR * 2, fill=rad((0, "#000000", 0), (0.78, "#8A6A30", 0),
                                (1, "#8A6A30", 22)), stroke=NONE)

# --- osmanthus branch ----------------------------------------------------------
osmanthus(d, 186, 216, 330, 148, "Osmanthus", n=26, color="#F2C05A")
osmanthus(d, 160, 300, 260, 240, "Osmanthus B", n=14, color="#E8B44E")

# --- clouds crossing the moon ---------------------------------------------------
cloud_drift(d, 372, 560, 240, "Cloud A", color="#B8B0D0", opacity=17)
cloud_drift(d, 668, 596, 210, "Cloud B", color="#A8A0C8", opacity=14)
cloud_drift(d, 560, 700, 190, "Cloud C", color="#B8B0D0", opacity=20)

# --- mooncake on its mat, lower left --------------------------------------------
MCX, MCY, MR2 = 322, 682, 86
inside(MCX - MR2 - 12, MCY + MR2 * 0.55, 12, "mooncake L")
inside(MCX, MCY + MR2 * 0.55, 12, "mooncake B")
d.shape("ellipse", "Mat shadow", x=MCX - 120, y=MCY + 24, width=240,
        height=104, fill=rad((0, "#000000", 40), (0.6, "#000000", 16),
                             (1, "#000000", 0)), stroke=NONE)
d.shape("ellipse", "Mat", x=MCX - 118, y=MCY + 6, width=236, height=94,
        fill=lin((MCX - 118, MCY), (MCX + 118, MCY + 100), (0, "#5E3A56"),
                 (1, "#2A1830")), stroke="#1A0E20", strokeWidth=3)
d.shape("ellipse", "Mat weave", x=MCX - 100, y=MCY + 16, width=200, height=74,
        fill=NONE, stroke="#8A6A80", strokeWidth=1.4, opacity=34)
mooncake(d, MCX, MCY, MR2, label="Mooncake")

# --- the jade rabbit on the cloud ------------------------------------------------
RX, RY, RS = 560, 640, 1.24
inside(RX + 17 * RS, RY - 96 * RS, 12, "rabbit ear R")
inside(RX - 32 * RS, RY + 34 * RS, 12, "rabbit base L")
jade_rabbit2(d, RX, RY, RS, label="Jade rabbit")

# --- falling osmanthus petals -----------------------------------------------------
s = 71
for i in range(14):
    s = (1103515245 * s + 12345) % (2 ** 31)
    x = 200 + (s % 10000) / 10000 * 560
    s = (1103515245 * s + 12345) % (2 ** 31)
    y = 220 + (s % 10000) / 10000 * 480
    s = (1103515245 * s + 12345) % (2 ** 31)
    rr = 2.2 + (s % 1000) / 1000 * 2.4
    if math.hypot(x - PCX, y - PCY) > 392:
        continue
    d.shape("ellipse", f"Falling petal {i+1}", x=round(x - rr, 1),
            y=round(y - rr * 0.6, 1), width=rr * 2, height=rr * 1.2,
            fill="#F2C05A", opacity=34 + (s % 30), stroke=NONE,
            rotation=round((s % 90) - 45, 1))

# --- seal + caption ----------------------------------------------------------------
CHX, CHY, CHW, CHH = 714, 148, 50, 136
inside(CHX + CHW, CHY + CHH, 6, "chop BR")
d.shape("rectangle", "Chop shadow", x=CHX + 3, y=CHY + 4, width=CHW, height=CHH,
        radius=4, fill="#000000", opacity=30, stroke=NONE)
p.chop("中秋", x=CHX, y=CHY, w=CHW, h=CHH, size=27)

p.caption("MID-AUTUMN FESTIVAL", "中秋節 · MOON FESTIVAL · DAY 15/8",
          name_color="#F4E8CC", sub_color="#C8A468",
          name_size=48, sub_size=20, tracking_name=56, tracking_sub=110)
p.finish(SLUG)
