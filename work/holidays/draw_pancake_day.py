#!/usr/bin/env python3
"""Pancake Day — Festival Seal V1R00.

Shrove Tuesday breakfast, food-holiday fun register: a wobbling stack of
five pancakes on a cream plate, a butter pat half-melted on top, a syrup
pitcher tipped mid-pour with a glossy amber ribbon landing on the stack,
a cut lemon half on the plate and steam wisps above. Deep maple field,
gold rim, vermilion chop with a drawn mini-stack. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin,
                          smooth, blend)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "pancake-day-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

FIELD_HI = "#54331C"
FIELD_LO = "#1E0E06"
CAKE_HI = "#D89A52"
CAKE = "#B8763A"
CAKE_LO = "#7E441C"
SYRUP = "#C87418"
SYRUP_HI = "#F2B45C"
BUTTER = "#FBE89E"
PLATE_COL = "#F6EBD2"
LEMON = "#F0C838"
LEMON_FL = "#F6DC62"

p = Plate("Pancake Day — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def wob_disc(cx, cy, rx, ry, wob, phase, fill, label, n=14, **kw):
    """Lumpy pancake: smoothed closed polygon around an ellipse."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1 + wob * math.sin(phase + i * 2.7)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    d.path(smooth(pts, closed=True), label, fill=fill, **kw)


def pancake(cx, cy, rx, ry, label, toast=("#D89A52", "#8E5224")):
    """One pancake: lumpy side wall + toasted top face + freckles."""
    wob_disc(cx, cy, rx, ry, 0.045, cx * 0.13,
             lin((cx - rx, cy - ry), (cx + rx, cy + ry),
                 (0, toast[0]), (1, toast[1])),
             f"{label} cake", stroke=INK, strokeWidth=2.6)
    # toasted top face, slightly inset
    d.shape("ellipse", f"{label} top", x=cx - rx * 0.78, y=cy - ry * 0.78,
            width=rx * 1.56, height=ry * 1.56,
            fill=rad((0, "#E4AC62"), (0.7, toast[0]), (1, toast[0])),
            stroke=NONE, opacity=55)
    # freckles
    for i, (fx, fy, fr) in enumerate(((-0.34, -0.1, 0.06), (0.12, -0.3, 0.045),
                                      (0.38, 0.08, 0.055))):
        d.shape("ellipse", f"{label} freckle {i+1}",
                x=cx + rx * fx - rx * fr, y=cy + ry * fy - ry * fr,
                width=rx * fr * 2, height=ry * fr * 2, fill="#8E5224",
                opacity=38, stroke=NONE)


def syrup_drip(x, y0, y1, w, label):
    """Glossy syrup dribble running down the stack side."""
    d.path(f"M{x - w / 2:.1f},{y0:.1f} "
           f"C{x - w * 0.7:.1f},{(y0 + y1) / 2:.1f} {x - w * 0.35:.1f},{y1 - 8:.1f} "
           f"{x:.1f},{y1:.1f} C{x + w * 0.35:.1f},{y1 - 8:.1f} "
           f"{x + w * 0.7:.1f},{(y0 + y1) / 2:.1f} {x + w / 2:.1f},{y0:.1f} Z",
           label, fill=lin((x, y0), (x, y1), (0, SYRUP_HI), (1, SYRUP)),
           stroke="#7E3E08", strokeWidth=1.8, opacity=94)
    d.path(f"M{x - w * 0.14:.1f},{y0 + 6:.1f} "
           f"Q{x - w * 0.28:.1f},{(y0 + y1) / 2:.1f} {x - w * 0.1:.1f},{y1 - 12:.1f}",
           f"{label} sheen", fill=NONE, stroke="#F8D894", strokeWidth=2.0,
           opacity=55, cap="round")


def steam(x, y, h, label, op=34):
    d.path(f"M{x:.1f},{y:.1f} C{x - 14:.1f},{y - h * 0.3:.1f} "
           f"{x + 14:.1f},{y - h * 0.55:.1f} {x - 4:.1f},{y - h * 0.85:.1f}",
           label, fill=NONE, stroke="#F8EFD8", strokeWidth=3.4, opacity=op,
           cap="round")


def seal_chop(cx=744, cy=214, s=62):
    """Vermilion chop inside the disc, top right; drawn mini pancake stack."""
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
    # mini stack: three gold pancakes + butter square
    for i, w in enumerate((34, 30, 26)):
        d.shape("ellipse", f"Chop cake {i+1}", x=cx - w / 2,
                y=cy + 8 - i * 9, width=w, height=8.5,
                fill="#FBE6B4", stroke="#4E100E", strokeWidth=1.3)
    d.shape("rectangle", "Chop butter", x=cx - 6, y=cy - 14, width=12,
            height=9, radius=2, fill="#FBE6B4", stroke="#4E100E",
            strokeWidth=1.3)


# --- field -------------------------------------------------------------------
p.backdrop(top="#16100C", bottom="#070402", glow=("#54331C", 14))
dust(d, n=44, r=402, colors=("#F6E3B8", "#E8C074"), seed=29, smin=1.0,
     smax=2.4, opmin=8, opmax=22, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim=GOLD, rim2="#5E3A16")
ring_dots(d, r=397, n=56, size=2.4, color=GOLD, opacity=30)
# faint engraved field rings, medal-plate texture
for rr, op in ((170, 10), (262, 8), (340, 7)):
    d.shape("ellipse", f"Field ring {rr}", x=PCX - rr, y=PCY - rr,
            width=2 * rr, height=2 * rr, fill=NONE, stroke=GOLD,
            strokeWidth=1.4, opacity=op)
# warm breakfast glow behind the stack
glow(d, 500, 470, 330, "#F2B45C", a=16, label="Warm glow")
glow(d, 500, 480, 170, "#F8D894", a=18, label="Warm core")
# drifting sugar dust in the upper field
dust(d, n=26, r=330, colors=("#F8EFD8", "#F2B45C"), seed=41, smin=1.2,
     smax=3.0, opmin=14, opmax=34, label="Sugar dust")

# --- plate -------------------------------------------------------------------
PX, PY = 500, 692
d.shape("ellipse", "Plate shadow", x=PX - 236, y=PY + 26, width=472,
        height=52, fill=rad((0, "#000000", 40), (1, "#000000", 0)),
        stroke=NONE)
d.shape("ellipse", "Plate", x=PX - 232, y=PY - 44, width=464, height=96,
        fill=lin((0, PY - 44), (0, PY + 52), (0, "#FBF2DC"), (1, "#CBAE7E")),
        stroke="#6E4A1A", strokeWidth=3.4)
d.shape("ellipse", "Plate well", x=PX - 186, y=PY - 30, width=372, height=64,
        fill=NONE, stroke="#B8985E", strokeWidth=2.0, opacity=62)

# --- syrup pitcher, tipped mid-pour (upper left) -------------------------------
JCX, JCY, TILT = 310, 340, 32
def jug(pts_local, label, **kw):
    """Draw a closed path from pts local to jug centre, tilted TILT deg."""
    a = math.radians(TILT)
    ca, sa = math.cos(a), math.sin(a)
    pts = [(JCX + x * ca - y * sa, JCY + x * sa + y * ca)
           for x, y in pts_local]
    return d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z",
                  label, **kw)

# jug body (local frame: origin centre, spout +x)
jug([(-52, -58), (30, -58), (54, -30), (54, 40), (30, 56), (-52, 56)],
    "Jug body", fill=lin((JCX - 52, JCY), (JCX + 54, JCY + 56),
                         (0, "#F0DAB0"), (0.6, "#D9B987"), (1, "#A8814E")),
    stroke=INK, strokeWidth=3.0)
# glaze stripe
jug([(-52, -10), (54, -10), (54, 14), (-52, 14)],
    "Jug stripe", fill="#8E5224", opacity=88, stroke=NONE)
# spout lip
jug([(54, -34), (78, -22), (78, -6), (54, -16)], "Jug spout",
    fill=lin((JCX + 54, JCY - 30), (JCX + 78, JCY), (0, "#F0DAB0"),
             (1, "#C9A068")), stroke=INK, strokeWidth=2.6)
# handle
a = math.radians(TILT)
hca, hsa = math.cos(a), math.sin(a)
h0 = (JCX + (-52) * hca - (-30) * hsa, JCY + (-52) * hsa + (-30) * hca)
h1 = (JCX + (-52) * hca - (30) * hsa, JCY + (-52) * hsa + (30) * hca)
hm = (h0[0] - 40, (h0[1] + h1[1]) / 2 - 6)
d.path(f"M{h0[0]:.1f},{h0[1]:.1f} Q{hm[0]:.1f},{hm[1]:.1f} "
       f"{h1[0]:.1f},{h1[1]:.1f}", "Jug handle", fill=NONE, stroke="#D9B987",
       strokeWidth=9, cap="round")
d.path(f"M{h0[0]:.1f},{h0[1]:.1f} Q{hm[0]:.1f},{hm[1]:.1f} "
       f"{h1[0]:.1f},{h1[1]:.1f}", "Jug handle edge", fill=NONE, stroke=INK,
       strokeWidth=1.8, opacity=70, cap="round")

# --- the stack -----------------------------------------------------------------
# five pancakes, gently staggered, plate-sitting
STACK = [(478, 664, 150, 34), (470, 636, 156, 33), (482, 606, 148, 32),
         (472, 578, 152, 31), (480, 550, 144, 30)]
for i, (cx, cy, rx, ry) in enumerate(STACK):
    pancake(cx, cy, rx, ry, f"Layer {i+1}")

# syrup sheet on the top pancake + dribbles down the sides
d.shape("ellipse", "Syrup pool", x=480 - 118, y=550 - 26, width=236,
        height=52, fill=lin((0, 524), (0, 576), (0, SYRUP_HI), (1, "#9E520E")),
        stroke="#7E3E08", strokeWidth=2.0, opacity=95)
syrup_drip(392, 560, 648, 26, "Drip L")
syrup_drip(588, 556, 690, 30, "Drip R")
syrup_drip(530, 566, 620, 20, "Drip mid")
# syrup pooling on the plate
d.shape("ellipse", "Syrup puddle", x=330, y=668, width=110, height=30,
        fill=rad((0, SYRUP_HI, 92), (0.6, SYRUP, 80), (1, SYRUP, 45)),
        stroke=NONE)

# --- pouring stream ------------------------------------------------------------
# spout tip in canvas coords; a clean parabolic arc landing left of the pat
ST = (JCX + 78 * hca - (-14) * hsa, JCY + 78 * hsa + (-14) * hca)
stream = [(ST[0] + 2, ST[1] + 8), (ST[0] + 34, ST[1] + 110),
          (448, 534)]
d.path(smooth(stream), "Syrup stream", fill=NONE, stroke="#9E520E",
       strokeWidth=12, cap="round")
d.path(smooth(stream), "Syrup stream mid", fill=NONE, stroke=SYRUP,
       strokeWidth=8, cap="round")
d.path(smooth(stream), "Syrup stream sheen", fill=NONE, stroke=SYRUP_HI,
       strokeWidth=3, opacity=70, cap="round")
# splash crown where the stream lands
for i, (dx, dy, r) in enumerate(((-18, -8, 5), (12, -12, 5.5), (26, 0, 4),
                                 (-4, -15, 4))):
    d.shape("ellipse", f"Splash {i+1}", x=448 + dx - r, y=534 + dy - r,
            width=2 * r, height=2 * r, fill=SYRUP_HI, opacity=80, stroke=NONE)

# butter pat, half-melted, sitting proud on the pool
d.shape("rectangle", "Butter pat", x=462, y=494, width=58, height=40,
        radius=6, fill=lin((462, 494), (462, 534), (0, "#FEF4C0"),
                           (1, "#E8C35E")), stroke="#9A7224", strokeWidth=2.2,
        rotation=-8)
d.shape("ellipse", "Butter melt", x=446, y=524, width=96, height=22,
        fill=rad((0, "#FBE89E", 85), (1, "#FBE89E", 0)), stroke=NONE)

# --- lemon half on the plate ----------------------------------------------------
LX, LY, LR = 652, 660, 46
d.shape("ellipse", "Lemon shadow", x=LX - LR - 6, y=LY + LR * 0.62,
        width=2 * LR + 12, height=LR * 0.4,
        fill=rad((0, "#000000", 34), (1, "#000000", 0)), stroke=NONE)
d.shape("ellipse", "Lemon rind", x=LX - LR, y=LY - LR, width=2 * LR,
        height=2 * LR, fill=lin((LX - LR, LY - LR), (LX + LR, LY + LR),
                                (0, "#F8DC50"), (1, "#C89A10")),
        stroke=INK, strokeWidth=2.6)
d.shape("ellipse", "Lemon pith", x=LX - LR * 0.80, y=LY - LR * 0.80,
        width=LR * 1.6, height=LR * 1.6, fill="#F8EFC8", stroke=NONE)
d.shape("ellipse", "Lemon flesh", x=LX - LR * 0.66, y=LY - LR * 0.66,
        width=LR * 1.32, height=LR * 1.32, fill=LEMON_FL,
        stroke="#D8B42E", strokeWidth=1.6)
# segment walls
for i in range(8):
    a = math.radians(i * 45 + 10)
    d.shape("line", f"Lemon segment {i+1}",
            x1=round(LX + math.cos(a) * LR * 0.14, 1),
            y1=round(LY + math.sin(a) * LR * 0.14, 1),
            x2=round(LX + math.cos(a) * LR * 0.62, 1),
            y2=round(LY + math.sin(a) * LR * 0.62, 1),
            stroke="#F8EFC8", strokeWidth=2.6, opacity=85, cap="round")
d.shape("ellipse", "Lemon heart", x=LX - 5, y=LY - 5, width=10, height=10,
        fill="#F8EFC8", stroke=NONE)

# --- steam + crumbs ---------------------------------------------------------------
steam(452, 486, 74, "Steam 1")
steam(520, 480, 88, "Steam 2", op=28)
steam(580, 492, 60, "Steam 3", op=22)
for i, (x, y, r) in enumerate([(306, 700, 4), (352, 716, 3), (606, 726, 3.4),
                               (700, 704, 2.8)]):
    d.shape("ellipse", f"Crumb {i+1}", x=x - r, y=y - r, width=2 * r,
            height=2 * r, fill="#D89A52", opacity=60, stroke=NONE)

# --- seal + caption --------------------------------------------------------------
seal_chop()
caption(p, "PANCAKE DAY", "SHROVE TUESDAY · 17 FEBRUARY",
        name_color="#F6EBD0", sub_color="#D8A85E",
        name_size=52, tracking_name=90, sub_size=21, tracking_sub=48,
        sub_font=SERIF)
p.finish(SLUG)
