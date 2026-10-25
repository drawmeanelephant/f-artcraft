#!/usr/bin/env python3
"""Remembrance Day — Festival Seal V1R00.

A Flanders-poppy wreath laid on a dark field at first light: nine poppies
ringed with rosemary sprigs (rosemary for remembrance), a mourning ribbon at
the bottom, and a pale dawn glow low behind the wreath. Sombre palette —
deep maroon, grey-green, dusk slate — with disciplined rim light on the lit
edges only. Vermilion chop with a drawn poppy. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin,
                          smooth, blend)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "remembrance-day-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

FIELD_HI = "#2C3A34"
FIELD_LO = "#0B1410"
POPPY_HI = "#C23B40"
POPPY = "#8E252B"
POPPY_LO = "#581418"
POPPY_DK = "#3A0E12"
ROSEMARY = "#4E6652"
ROSEMARY_LO = "#27362C"
RIM = "#F2E4BC"                # dawn rim light, used sparingly
DAWN = "#E8D2A0"

p = Plate("Remembrance Day — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def poppy(cx, cy, r, rot, label, rim_side=-135):
    """Flanders poppy: two staggered petal rows, black heart, pale stamens.

    rot tilts the whole flower (wreath poppies point outward); rim_side is
    the compass angle (deg) of the dawn-lit petal edge.
    """
    # soft ground shadow behind the bloom
    d.shape("ellipse", f"{label} shadow", x=cx - r * 1.05, y=cy - r * 0.30,
            width=r * 2.1, height=r * 0.9, fill="#000000", opacity=26,
            stroke=NONE)
    # back row: 3 broad petals
    for i, da in enumerate((-58, 0, 58)):
        a = math.radians(rot + da)
        px, py = cx + math.cos(a) * r * 0.40, cy + math.sin(a) * r * 0.40
        d.shape("ellipse", f"{label} back {i+1}", x=px - r * 0.62,
                y=py - r * 0.50, width=r * 1.24, height=r * 1.0,
                fill=rad((0, POPPY), (1, POPPY_DK)), opacity=96,
                stroke=INK, strokeWidth=1.6,
                rotation=round(math.degrees(a) + 90, 1))
    # front row: 4 petals offset between the back three
    for i, da in enumerate((-86, -29, 29, 86)):
        a = math.radians(rot + da)
        px, py = cx + math.cos(a) * r * 0.32, cy + math.sin(a) * r * 0.32
        d.shape("ellipse", f"{label} petal {i+1}", x=px - r * 0.56,
                y=py - r * 0.46, width=r * 1.12, height=r * 0.92,
                fill=rad((0, POPPY_HI), (0.6, POPPY), (1, POPPY_LO)),
                opacity=97, stroke=INK, strokeWidth=1.5,
                rotation=round(math.degrees(a) + 90, 1))
    # black heart + seed capsule + stamen ring
    d.shape("ellipse", f"{label} heart", x=cx - r * 0.30, y=cy - r * 0.26,
            width=r * 0.60, height=r * 0.52, fill="#14100C",
            stroke=POPPY_DK, strokeWidth=1.2)
    d.shape("ellipse", f"{label} capsule", x=cx - r * 0.11, y=cy - r * 0.15,
            width=r * 0.22, height=r * 0.18, fill="#4E5E44", stroke=NONE,
            opacity=90)
    for i in range(8):
        a = math.radians(i * 45 + 22)
        d.shape("ellipse", f"{label} stamen {i+1}",
                x=cx + math.cos(a) * r * 0.24 - r * 0.025,
                y=cy + math.sin(a) * r * 0.21 - r * 0.025,
                width=r * 0.05, height=r * 0.05, fill="#D8C89A",
                opacity=75, stroke=NONE)
    # rim light: one lit edge arc on the dawn side, nothing more
    a = math.radians(rim_side + rot)
    x0 = cx + math.cos(a - 0.55) * r * 0.86
    y0 = cy + math.sin(a - 0.55) * r * 0.70
    x1 = cx + math.cos(a + 0.55) * r * 0.86
    y1 = cy + math.sin(a + 0.55) * r * 0.70
    bx = cx + math.cos(a) * r * 1.16
    by = cy + math.sin(a) * r * 0.96
    d.path(f"M{x0:.1f},{y0:.1f} Q{bx:.1f},{by:.1f} {x1:.1f},{y1:.1f}",
           f"{label} rim", fill=NONE, stroke=RIM, strokeWidth=2.2,
           opacity=55, cap="round")


def rosemary(x, y, ang, h, label, op=88):
    """Rosemary sprig: thin stem + paired needle strokes."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    tx, ty = x + ca * h, y + sa * h
    mx, my = x + ca * h * 0.5 - sa * h * 0.06, y + sa * h * 0.5 + ca * h * 0.06
    d.path(f"M{x:.1f},{y:.1f} Q{mx:.1f},{my:.1f} {tx:.1f},{ty:.1f}",
           f"{label} stem", fill=NONE, stroke=ROSEMARY_LO, strokeWidth=2.6,
           opacity=op, cap="round")
    nx, ny = -sa, ca
    n_need = int(h / 9)
    for j in range(1, n_need + 1):
        t = j / (n_need + 1)
        qx = x + ca * h * t - sa * h * 0.06 * 4 * t * (1 - t)
        qy = y + sa * h * t + ca * h * 0.06 * 4 * t * (1 - t)
        L = 9.5 * (1 - 0.45 * t)
        for sgn in (-1, 1):
            d.shape("line", f"{label} needle {j}{'a' if sgn < 0 else 'b'}",
                    x1=round(qx, 1), y1=round(qy, 1),
                    x2=round(qx + (ca * 0.55 + nx * sgn) * L, 1),
                    y2=round(qy + (sa * 0.55 + ny * sgn) * L, 1),
                    stroke=ROSEMARY, strokeWidth=1.7, opacity=op - 6,
                    cap="round")


def bud(x, y, ang, s, label):
    """Drooping poppy bud on a bent stalk."""
    a = math.radians(ang)
    d.path(f"M{x:.1f},{y:.1f} Q{x + math.cos(a)*s*1.6 - math.sin(a)*s*0.7:.1f},"
           f"{y + math.sin(a)*s*1.6 + math.cos(a)*s*0.7:.1f} "
           f"{x + math.cos(a)*s*2.4:.1f},{y + math.sin(a)*s*2.4 - s*0.4:.1f}",
           f"{label} stalk", fill=NONE, stroke=ROSEMARY_LO, strokeWidth=2.2,
           cap="round")
    hx = x + math.cos(a) * s * 2.4
    hy = y + math.sin(a) * s * 2.4 - s * 0.4
    d.shape("ellipse", f"{label} bud", x=hx - s * 0.42, y=hy - s * 0.30,
            width=s * 0.84, height=s * 0.60, fill=POPPY, stroke=INK,
            strokeWidth=1.3, rotation=round(math.degrees(a) + 20, 1))


def chop_poppy(cx, cy, r, label="Chop poppy"):
    """Tiny drawn poppy mark for the vermilion chop: 4 outlined petals."""
    for i in range(4):
        a = math.radians(-90 + i * 90)
        px, py = cx + math.cos(a) * r * 0.40, cy + math.sin(a) * r * 0.40
        d.shape("ellipse", f"{label} petal {i+1}", x=px - r * 0.60,
                y=py - r * 0.48, width=r * 1.20, height=r * 0.96,
                fill="#FBE6B4", opacity=94, stroke="#4E100E",
                strokeWidth=1.4,
                rotation=round(math.degrees(a) + 90, 1))
    d.shape("ellipse", f"{label} heart", x=cx - r * 0.24, y=cy - r * 0.22,
            width=r * 0.48, height=r * 0.44, fill="#14100C", stroke=NONE)


def seal_chop(cx=744, cy=214, s=62):
    x, y = cx - s / 2, cy - s / 2
    inside(cx + s / 2, cy + s / 2, 8, "chop BR")
    d.shape("ellipse", "Chop shadow", x=x + 3, y=y + 5, width=s, height=s,
            fill=INK, opacity=28, stroke=NONE)
    d.shape("rectangle", "Chop", x=x, y=y, width=s, height=s, radius=5,
            fill=lin((x, y), (x + s, y + s), (0, "#C0473A"), (1, "#7E1F1B")),
            stroke="#4E100E", strokeWidth=2.2)
    d.shape("rectangle", "Chop inner", x=x + 4.5, y=y + 4.5, width=s - 9,
            height=s - 9, radius=2.5, fill=NONE, stroke="#F6D9A0",
            strokeWidth=1.4, opacity=78)
    chop_poppy(cx, cy, 18)


# --- field -------------------------------------------------------------------
p.backdrop(top="#10151A", bottom="#05070A", glow=("#2C3A34", 12))
dust(d, n=40, r=402, colors=("#D8C89A", "#8A9A8E"), seed=29, smin=1.0,
     smax=2.2, opmin=7, opmax=20, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim="#B8985E", rim2="#3E3018")
ring_dots(d, r=397, n=56, size=2.2, color="#C9A46A", opacity=26)

# faint rings on the field, like a medal engraving
for rr, op in ((170, 9), (262, 7), (340, 6)):
    d.shape("ellipse", f"Field ring {rr}", x=PCX - rr, y=PCY - rr,
            width=2 * rr, height=2 * rr, fill=NONE, stroke="#C9A46A",
            strokeWidth=1.4, opacity=op)

# --- low horizon + dawn glow ---------------------------------------------------
# dark ground band along the disc floor (closes on the inner arc, like
# golden-week's rim hills)
def rim_band(a0, a1, depth_mid, wob, phase, fill, label, n=30, r=PR - 4):
    arc = [(PCX + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            PCY + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
           for i in range(n + 1)]
    top = []
    for i in range(n + 1):
        a = math.radians(a1 - (a1 - a0) * i / n)
        t = i / n
        dep = depth_mid * (math.sin(math.pi * t) ** 0.85)
        dep *= 1 + wob * math.sin(phase + i * 0.8)
        rr = r - dep
        top.append((PCX + rr * math.cos(a), PCY + rr * math.sin(a)))
    d.path(smooth(arc) + smooth(top, move=False) + " Z", label,
           fill=fill, stroke=NONE)


rim_band(30, 150, 118, 0.05, 0.7,
         lin((0, 690), (0, 890), (0, "#1B2820"), (1, "#0A120C")),
         "Ground")
# dawn glow pooled low behind the wreath
glow(d, 500, 700, 300, DAWN, a=14, label="Dawn glow", squash=0.62)
glow(d, 500, 712, 150, "#F2E2B4", a=16, label="Dawn core", squash=0.5)
# furrows on the ground, sparse
for i, (x0, x1, cy) in enumerate([(290, 420, 742), (580, 706, 738),
                                  (360, 500, 788), (520, 650, 782)]):
    d.path(f"M{x0},{cy} Q{(x0 + x1) / 2},{cy + 12} {x1},{cy + 2}",
           f"Furrow {i+1}", fill=NONE, stroke="#060B08", strokeWidth=2.4,
           opacity=42, cap="round")

# --- the wreath ----------------------------------------------------------------
WX, WY, WR = 498, 428, 176
d.shape("ellipse", "Wreath shadow", x=WX - WR - 30, y=WY + WR * 0.62,
        width=2 * WR + 60, height=WR * 0.5,
        fill=rad((0, "#000000", 30), (0.6, "#000000", 12), (1, "#000000", 0)),
        stroke=NONE)
# inner green mass: the ring of foliage the blooms sit on
d.shape("ellipse", "Wreath mass", x=WX - WR, y=WY - WR, width=2 * WR,
        height=2 * WR, fill=NONE, stroke="#223026", strokeWidth=58,
        opacity=88)
d.shape("ellipse", "Wreath mass light", x=WX - WR, y=WY - WR, width=2 * WR,
        height=2 * WR, fill=NONE,
        stroke=lin((WX - WR, WY - WR), (WX + WR, WY + WR),
                   (0, "#3E5240"), (1, "#1A2620")),
        strokeWidth=44, opacity=80)

# rosemary sprigs between the blooms, leaning outward along the ring
NP = 9
for i in range(NP):
    a0 = -90 + (i + 0.5) * 360 / NP
    a = math.radians(a0)
    bx = WX + math.cos(a) * (WR + 30)
    by = WY + math.sin(a) * (WR + 30)
    inside(bx + math.cos(a) * 62, by + math.sin(a) * 62, 10, f"rosemary {i}")
    rosemary(bx, by, math.degrees(a) + (12 if i % 2 else -12), 58,
             f"Rosemary {i+1}", op=84)

# mourning ribbon at the bottom of the wreath
RBX, RBY = WX, WY + WR + 8
d.path(f"M{RBX - 64:.1f},{RBY - 26:.1f} C{RBX - 30:.1f},{RBY - 46:.1f} "
       f"{RBX + 30:.1f},{RBY - 46:.1f} {RBX + 64:.1f},{RBY - 26:.1f} "
       f"C{RBX + 40:.1f},{RBY - 6:.1f} {RBX - 40:.1f},{RBY - 6:.1f} "
       f"{RBX - 64:.1f},{RBY - 26:.1f} Z",
       "Ribbon knot band", fill=lin((RBX, RBY - 46), (RBX, RBY),
                                    (0, "#571C26"), (1, "#2E0C14")),
       stroke=INK, strokeWidth=2.2)
for sgn, lbl in ((-1, "L"), (1, "R")):
    d.path(f"M{RBX + sgn*14:.1f},{RBY - 14:.1f} "
           f"C{RBX + sgn*34:.1f},{RBY + 22:.1f} {RBX + sgn*40:.1f},{RBY + 58:.1f} "
           f"{RBX + sgn*30:.1f},{RBY + 92:.1f} "
           f"L{RBX + sgn*8:.1f},{RBY + 82:.1f} "
           f"C{RBX + sgn*12:.1f},{RBY + 48:.1f} {RBX + sgn*6:.1f},{RBY + 22:.1f} "
           f"{RBX - sgn*6:.1f},{RBY - 8:.1f} Z",
           f"Ribbon tail {lbl}",
           fill=lin((RBX, RBY - 10), (RBX, RBY + 92),
                    (0, "#4A1620"), (1, "#240810")),
           stroke=INK, strokeWidth=2.0)
d.shape("ellipse", "Ribbon knot", x=RBX - 22, y=RBY - 34, width=44, height=26,
        fill=lin((RBX, RBY - 36), (RBX, RBY - 8), (0, "#64222E"), (1, "#34101A")),
        stroke=INK, strokeWidth=2.0)
inside(RBX - 30, RBY + 92, 6, "ribbon tail L")
inside(RBX + 30, RBY + 92, 6, "ribbon tail R")

# the nine poppies, heads tilting outward, rim-lit from the upper left
for i in range(NP):
    a = math.radians(-90 + i * 360 / NP)
    x, y = WX + math.cos(a) * WR, WY + math.sin(a) * WR
    inside(x + math.cos(a) * 46, y + math.sin(a) * 46, 10, f"poppy {i+1}")
    poppy(x, y, 42 if i % 3 else 45, math.degrees(a) + 90,
          f"Poppy {i+1}", rim_side=-135 - (math.degrees(a) + 90))

# three small buds leaning out of the lower right of the ring
bud(WX + WR * 0.62, WY + WR * 0.66, 38, 22, "Bud 1")
bud(WX + WR * 0.30, WY + WR * 0.80, 62, 18, "Bud 2")

# fallen petals on the ground below the wreath
for i, (x, y, r_, rot) in enumerate([(388, 762, 9, -24), (596, 774, 8, 30),
                                     (482, 800, 7, 68)]):
    inside(x, y, 14, f"fallen petal {i}")
    d.shape("ellipse", f"Fallen petal {i+1}", x=x - r_, y=y - r_ * 0.62,
            width=2 * r_, height=r_ * 1.24, fill=POPPY_LO, opacity=80,
            stroke=NONE, rotation=rot)

# --- seal + caption --------------------------------------------------------------
seal_chop()
caption(p, "REMEMBRANCE DAY", "11 NOVEMBER · LEST WE FORGET",
        name_color="#EDE6D2", sub_color="#B89A6E",
        name_size=44, tracking_name=58, sub_size=20, tracking_sub=52,
        sub_font=SERIF)
p.finish(SLUG)
