#!/usr/bin/env python3
"""Easter — Festival Seal V1R00.

A wicker basket of dyed eggs on a spring dawn: five pastel eggs — rose,
sky, mint, lilac, cream — banded and dotted, nestled in a reed basket under
its arched handle. Grass tufts and fallen petals at the foot. Deep warm
plum-ink field, gold rim, vermilion chop with a drawn egg. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin, smooth,
                          blossom)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "easter-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

FIELD_HI = "#3A2A34"
FIELD_LO = "#140E12"
WICK_HI = "#D8A468"
WICK = "#B07840"
WICK_LO = "#5E3418"
ROSE = "#F2B8C6"
SKY = "#A8CCE8"
MINT = "#BFE3C0"
LILAC = "#D8C4E8"
BUTTER = "#F6E0A8"

p = Plate("Easter — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def egg(cx, cy, rx, ry, col, lo, label, lean=0.0):
    """Dyed egg: narrower at the top, rounded at the foot. lean tilts the top."""
    tx = cx + lean * ry
    d.path(f"M{tx:.1f},{cy - ry:.1f} "
           f"C{tx + rx*0.62:.1f},{cy - ry*0.98:.1f} {cx + rx:.1f},{cy - ry*0.18:.1f} "
           f"{cx + rx:.1f},{cy + ry*0.25:.1f} "
           f"C{cx + rx:.1f},{cy + ry*0.85:.1f} {cx + rx*0.55:.1f},{cy + ry:.1f} "
           f"{cx:.1f},{cy + ry:.1f} "
           f"C{cx - rx*0.55:.1f},{cy + ry:.1f} {cx - rx:.1f},{cy + ry*0.85:.1f} "
           f"{cx - rx:.1f},{cy + ry*0.25:.1f} "
           f"C{cx - rx:.1f},{cy - ry*0.18:.1f} {tx - rx*0.62:.1f},{cy - ry*0.98:.1f} "
           f"{tx:.1f},{cy - ry:.1f} Z", label,
           fill=lin((cx - rx, cy - ry), (cx + rx, cy + ry),
                    (0, "#FFF6EC"), (0.30, col), (1, lo)),
           stroke=INK, strokeWidth=2.6)
    # shaded lower-right
    d.path(f"M{cx + rx*0.30:.1f},{cy - ry*0.5:.1f} "
           f"C{cx + rx*0.88:.1f},{cy - ry*0.1:.1f} {cx + rx*0.80:.1f},{cy + ry*0.55:.1f} "
           f"{cx + rx*0.3:.1f},{cy + ry*0.85:.1f}",
           f"{label} shade", fill=NONE, stroke=INK, strokeWidth=rx * 0.16,
           opacity=13, cap="round")


def egg_half_width(rx, ry, dy):
    """Approx half-width of the egg outline at offset dy from centre."""
    t = max(-0.92, min(0.92, dy / ry))
    return rx * math.sqrt(1 - t * t) * 0.94


def band(cx, cy, rx, ry, dy, col, label, w=6):
    hw = egg_half_width(rx, ry, dy)
    d.path(f"M{cx - hw:.1f},{cy + dy:.1f} Q{cx:.1f},{cy + dy + ry*0.16:.1f} "
           f"{cx + hw:.1f},{cy + dy:.1f}", label, fill=NONE, stroke=col,
           strokeWidth=w, opacity=88, cap="round")


def dots_row(cx, cy, rx, ry, dy, col, label, n=5, r=3.4):
    hw = egg_half_width(rx, ry, dy) * 0.86
    for i in range(n):
        t = (i + 0.5) / n
        x = cx - hw + 2 * hw * t
        y = cy + dy + ry * 0.16 * (1 - (2 * t - 1) ** 2) * 0.8
        d.shape("ellipse", f"{label} {i+1}", x=x - r, y=y - r, width=2 * r,
                height=2 * r, fill=col, opacity=90, stroke=NONE)


def zigzag(cx, cy, rx, ry, dy, col, label, n=4, amp=7):
    hw = egg_half_width(rx, ry, dy)
    pts = []
    for i in range(2 * n + 1):
        x = cx - hw + 2 * hw * i / (2 * n)
        pts.append((x, cy + dy + (amp if i % 2 else -amp)))
    d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts), label,
           fill=NONE, stroke=col, strokeWidth=5, opacity=88, cap="round")


def blade(x, y, h, lean, col, label, w=4):
    d.path(f"M{x:.1f},{y:.1f} Q{x + lean*0.4:.1f},{y - h*0.55:.1f} "
           f"{x + lean:.1f},{y - h:.1f}", label, fill=NONE, stroke=col,
           strokeWidth=w, opacity=85, cap="round")


def petal(x, y, ang, s, col, label):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    tx, ty = -sa, ca
    tip = (x + ca * 14 * s, y + sa * 14 * s)
    d.path(f"M{x:.1f},{y:.1f} Q{x + ca*7*s + tx*6*s:.1f},{y + sa*7*s + ty*6*s:.1f} "
           f"{tip[0]:.1f},{tip[1]:.1f} "
           f"Q{x + ca*7*s - tx*6*s:.1f},{y + sa*7*s - ty*6*s:.1f} {x:.1f},{y:.1f} Z",
           label, fill=col, opacity=88, stroke=INK, strokeWidth=1.1)


def seal_chop(cx=744, cy=214, s=62):
    """Vermilion chop inside the disc, top right; drawn cream egg mark."""
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
    egg(cx, cy + 1, 9.5, 12.5, "#FBE6B4", "#D8A85E", "Chop egg")


# --- field -------------------------------------------------------------------
p.backdrop(top="#241A22", bottom="#0A0608", glow=("#4A2E3C", 15))
dust(d, n=40, r=402, colors=("#F6E3B8", "#E8D8E4"), seed=31, smin=1.0,
     smax=2.4, opmin=8, opmax=22, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim=GOLD, rim2="#5E3A16")
dust(d, n=54, r=392, colors=("#F6E3B8", "#F2B8C6", "#E8C074"), seed=17,
     smin=1.0, smax=2.8, opmin=10, opmax=28, label="Disc dust")
ring_dots(d, r=397, n=56, size=2.6, color=GOLD, opacity=30)

# faint concentric field guides
for rr, op in ((170, 11), (264, 9), (344, 7)):
    d.shape("ellipse", f"Field ring {rr}", x=PCX - rr, y=PCY - rr,
            width=2 * rr, height=2 * rr, fill=NONE, stroke=GOLD,
            strokeWidth=1.4, opacity=op)

# dawn glow behind the basket
glow(d, 500, 560, 280, "#E8B868", a=16, label="Dawn glow")
glow(d, 500, 330, 200, "#F2B8C6", a=9, label="Sky blush")

# drifting blossoms in the upper field
blossom(d, 272, 372, 24, petals=5, label="Blossom L", fill="#F2B8C6",
        core=GOLD_HI, stroke="#8A4E5E", rot=-14)
blossom(d, 724, 352, 20, petals=5, label="Blossom R", fill="#D8C4E8",
        core=GOLD_HI, stroke="#6A4E7A", rot=22)
blossom(d, 340, 246, 15, petals=5, label="Blossom hi", fill="#F6E0A8",
        core="#C2455A", stroke="#9A6A24", rot=-30, opacity=90)

# --- basket handle -------------------------------------------------------------
# arched handle behind the eggs: two reeds + lashing bands
d.path("M322,616 C330,380 400,296 500,296 C600,296 670,380 678,616",
       "Handle outer", fill=NONE, stroke=INK, strokeWidth=19, cap="round")
d.path("M322,616 C330,380 400,296 500,296 C600,296 670,380 678,616",
       "Handle", fill=NONE, stroke=WICK_HI, strokeWidth=14, cap="round")
d.path("M322,616 C330,380 400,296 500,296 C600,296 670,380 678,616",
       "Handle sheen", fill=NONE, stroke="#F2D0A0", strokeWidth=4,
       opacity=40, cap="round")

# --- eggs in the basket ---------------------------------------------------------
BCY = 636                       # basket rim line
for cx, cy, rx, ry, col, lo, dec, ln in [
        (392, 560, 52, 66, SKY, "#4E7494", "bands", -0.10),
        (466, 540, 54, 70, ROSE, "#9A4E62", "dots", 0.02),
        (540, 536, 54, 72, BUTTER, "#B08434", "zig", -0.02),
        (612, 558, 52, 66, MINT, "#4E7A52", "bands", 0.10),
        (500, 496, 46, 60, LILAC, "#7A5A94", "dots", 0.0)]:
    if dec == "bands":
        egg(cx, cy, rx, ry, col, lo, f"Egg {cx}", lean=ln)
        band(cx, cy, rx, ry, -0.30 * ry, "#FBE6B4", f"Egg {cx} band hi")
        band(cx, cy, rx, ry, 0.10 * ry, "#C0473A", f"Egg {cx} band lo")
    elif dec == "dots":
        egg(cx, cy, rx, ry, col, lo, f"Egg {cx}", lean=ln)
        band(cx, cy, rx, ry, -0.28 * ry, "#FBE6B4", f"Egg {cx} band", w=5)
        dots_row(cx, cy, rx, ry, 0.22 * ry, "#FBE6B4", f"Egg {cx} dots")
    else:
        egg(cx, cy, rx, ry, col, lo, f"Egg {cx}", lean=ln)
        zigzag(cx, cy, rx, ry, -0.28 * ry, "#C0473A", f"Egg {cx} zig hi")
        zigzag(cx, cy, rx, ry, 0.18 * ry, "#4E7494", f"Egg {cx} zig lo")

# --- basket body ----------------------------------------------------------------
BW, BH = 224, 158
d.shape("ellipse", "Basket shadow", x=500 - 250, y=BCY + BH + 4, width=500,
        height=44, fill=rad((0, INK, 34), (0.6, INK, 15), (1, INK, 0)),
        stroke=NONE)
# body: rim chord to narrowed base
d.path(f"M{500 - BW:.1f},{BCY:.1f} "
       f"C{500 - BW:.1f},{BCY + BH*0.55:.1f} {500 - BW*0.62:.1f},{BCY + BH:.1f} "
       f"{500:.1f},{BCY + BH:.1f} "
       f"C{500 + BW*0.62:.1f},{BCY + BH:.1f} {500 + BW:.1f},{BCY + BH*0.55:.1f} "
       f"{500 + BW:.1f},{BCY:.1f} Z", "Basket body",
       fill=lin((500, BCY), (500, BCY + BH),
                (0, WICK_HI), (0.55, WICK), (1, WICK_LO)),
       stroke=INK, strokeWidth=3.2)
# horizontal weft rows
for i, t in enumerate((0.18, 0.38, 0.58, 0.78)):
    y = BCY + BH * t
    hw = BW * (1 - t * 0.34)
    d.path(f"M{500 - hw:.1f},{y:.1f} Q500,{y + 16:.1f} {500 + hw:.1f},{y:.1f}",
           f"Weft {i+1}", fill=NONE, stroke="#5E3418", strokeWidth=4.4,
           opacity=55, cap="round")
    d.path(f"M{500 - hw:.1f},{y + 4.5:.1f} Q500,{y + 20:.1f} {500 + hw:.1f},{y + 4.5:.1f}",
           f"Weft {i+1} hi", fill=NONE, stroke="#EFC088", strokeWidth=2.0,
           opacity=40, cap="round")
# vertical warps
for i in range(9):
    t = (i + 0.5) / 9
    x0 = 500 - BW + 2 * BW * t
    x1 = 500 + (x0 - 500) * 0.58
    d.path(f"M{x0:.1f},{BCY + 8:.1f} Q{x0 + (x1 - x0)*0.3:.1f},{BCY + BH*0.5:.1f} "
           f"{x1:.1f},{BCY + BH*0.94:.1f}", f"Warp {i+1}", fill=NONE,
           stroke="#5E3418", strokeWidth=2.2, opacity=38, cap="round")
# rolled rim
d.path(f"M{500 - BW - 8:.1f},{BCY:.1f} Q500,{BCY + 30:.1f} {500 + BW + 8:.1f},{BCY:.1f}",
       "Basket rim", fill=NONE, stroke=INK, strokeWidth=22, cap="round")
d.path(f"M{500 - BW - 8:.1f},{BCY:.1f} Q500,{BCY + 30:.1f} {500 + BW + 8:.1f},{BCY:.1f}",
       "Basket rim reed", fill=NONE, stroke="#D89458", strokeWidth=16,
       cap="round")
d.path(f"M{500 - BW - 6:.1f},{BCY - 2:.1f} Q500,{BCY + 22:.1f} {500 + BW + 6:.1f},{BCY - 2:.1f}",
       "Basket rim sheen", fill=NONE, stroke="#F6DCA8", strokeWidth=4,
       opacity=45, cap="round")

# --- grass + petals at the foot -------------------------------------------------
grass_cols = ["#4E8A58", "#3C7048", "#6AA868"]
gi = 0
for x, h, ln in [(300, 46, -16), (322, 60, -4), (342, 42, 12), (662, 52, -10),
                 (684, 62, 4), (706, 44, 16), (382, 40, -12), (618, 42, 12),
                 (470, 36, -8), (530, 38, 8)]:
    blade(x, 800, h, ln, grass_cols[gi % 3], f"Grass {gi+1}")
    gi += 1
for i, (x, y, ang, s, c) in enumerate([
        (352, 778, 140, 1.0, ROSE), (648, 782, 40, 0.9, LILAC),
        (420, 800, 170, 0.85, BUTTER), (586, 796, 10, 0.9, ROSE),
        (296, 752, 120, 0.8, "#F6E7C8"), (704, 748, 60, 0.8, MINT)]):
    petal(x, y, ang, s, c, f"Petal {i+1}")

# --- seal + caption -------------------------------------------------------------
seal_chop()
caption(p, "EASTER", "MAR 22 – APR 25 · MOVEABLE FEAST",
        name_color="#F4EBD4", sub_color="#C9A46A",
        name_size=52, tracking_name=110, sub_size=20, tracking_sub=42,
        sub_font=SERIF)
p.finish(SLUG)
