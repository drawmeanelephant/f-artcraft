#!/usr/bin/env python3
"""Christmas — Festival Seal V1R00.

A lit fir in a snow drift: four drooping bough tiers in deep spruce green,
warm candle-lights along the tier edges, glass baubles in garnet and gold,
a four-point star topper and two small gifts at the trunk. Holly sprigs at
the lower rim. Deep green field, gold rim, vermilion chop with a drawn
star. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin, smooth)
from festival_kit import seal_disc, glow, dust, ring_dots, caption, leaf_at

SLUG = "christmas-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

PINE_HI = "#3C7A50"
PINE = "#1E4A34"
PINE_LO = "#0A2416"
FIELD_HI = "#173A2A"
FIELD_LO = "#06130C"
GARNET = "#B83A32"
CREAM = "#F4E7CE"
SNOW = "#EDF4EE"

p = Plate("Christmas — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def star4(x, y, r, col=GOLD_HI, op=95, label="Star", halo=26):
    """Four-point star with a soft halo and bright core."""
    if halo:
        d.shape("ellipse", f"{label} halo", x=x - r * 2.4, y=y - r * 2.4,
                width=r * 4.8, height=r * 4.8,
                fill=rad((0, col, halo), (0.5, col, halo * 0.35), (1, col, 0)),
                stroke=NONE)
    q = r * 0.20
    d.path(f"M{x:.1f},{y - r:.1f} Q{x + q:.1f},{y - q:.1f} {x + r:.1f},{y:.1f} "
           f"Q{x + q:.1f},{y + q:.1f} {x:.1f},{y + r:.1f} "
           f"Q{x - q:.1f},{y + q:.1f} {x - r:.1f},{y:.1f} "
           f"Q{x - q:.1f},{y - q:.1f} {x:.1f},{y - r:.1f} Z",
           f"{label} cross", fill=col, opacity=op, stroke=NONE)
    d.shape("ellipse", f"{label} core", x=x - r * 0.24, y=y - r * 0.24,
            width=r * 0.48, height=r * 0.48, fill="#FFFBE8", opacity=92,
            stroke=NONE)


def bough(cx, cy, hw, h, label, scallops=4):
    """One drooping fir bough: shallow arched top, scalloped needle edge."""
    d.path(f"M{cx - hw:.1f},{cy:.1f} Q{cx:.1f},{cy - h:.1f} {cx + hw:.1f},{cy:.1f} "
           + " ".join(f"Q{cx + hw - 2*hw*(j+0.5)/scallops:.1f},{cy + h*0.66:.1f} "
                      f"{cx + hw - 2*hw*(j+1)/scallops:.1f},{cy + h*0.30:.1f}"
                      for j in range(scallops)) + " Z",
           label,
           fill=lin((cx, cy - h * 0.5), (cx, cy + h * 0.7),
                    (0, PINE_HI), (0.45, PINE), (1, PINE_LO)),
           stroke=INK, strokeWidth=3)
    # needle texture strokes hanging from the top edge
    for j in range(scallops * 2):
        t = (j + 0.5) / (scallops * 2)
        bx = cx - hw + 2 * hw * t
        by = cy - h * 0.5 * (1 - (2 * t - 1) ** 2) * 0.5 + h * 0.10
        ln = h * (0.30 + 0.12 * math.sin(t * math.pi))
        d.path(f"M{bx:.1f},{by:.1f} Q{bx - 4:.1f},{by + ln*0.6:.1f} "
               f"{bx + 3:.1f},{by + ln:.1f}", f"{label} needle {j+1}",
               fill=NONE, stroke="#5E9A72", strokeWidth=1.6, opacity=38,
               cap="round")


def bauble(x, y, r, col, lo, label):
    d.shape("ellipse", label, x=x - r, y=y - r, width=2 * r, height=2 * r,
            fill=rad((0, "#F6D0B8"), (0.35, col), (1, lo)), stroke=INK,
            strokeWidth=1.8)
    d.shape("ellipse", f"{label} glint", x=x - r * 0.48, y=y - r * 0.55,
            width=r * 0.5, height=r * 0.34, fill="#FFFFFF", opacity=55,
            stroke=NONE)
    d.shape("rectangle", f"{label} cap", x=x - r * 0.26, y=y - r - 4.4,
            width=r * 0.52, height=5, radius=1.5, fill=GOLD, stroke=INK,
            strokeWidth=1.1)


def candle_dot(x, y, r=4.2, label="Light"):
    """Warm pinpoint light: halo + hot core."""
    glow(d, x, y, r * 3.2, "#FFC46B", a=40, label=f"{label} halo")
    d.shape("ellipse", label, x=x - r, y=y - r, width=2 * r, height=2 * r,
            fill="#FFE9AE", opacity=95, stroke=NONE)


def gift(cx, cy, w, h, col, lo, ribbon_col, label):
    d.shape("rectangle", f"{label} shadow", x=cx - w * 0.55, y=cy + h * 0.82,
            width=w * 1.1, height=h * 0.26, fill=INK, opacity=26, stroke=NONE)
    d.shape("rectangle", label, x=cx - w / 2, y=cy, width=w, height=h,
            radius=4, fill=lin((cx - w / 2, cy), (cx + w / 2, cy + h),
                               (0, col), (1, lo)),
            stroke=INK, strokeWidth=2.4)
    d.shape("rectangle", f"{label} ribbon v", x=cx - w * 0.09, y=cy,
            width=w * 0.18, height=h, fill=ribbon_col, stroke=NONE,
            opacity=90)
    d.shape("rectangle", f"{label} ribbon h", x=cx - w / 2, y=cy + h * 0.30,
            width=w, height=h * 0.20, fill=ribbon_col, stroke=NONE,
            opacity=90)
    for i, sx in enumerate((-1, 1)):
        d.path(f"M{cx:.1f},{cy:.1f} C{cx + sx*w*0.30:.1f},{cy - h*0.42:.1f} "
               f"{cx + sx*w*0.44:.1f},{cy - h*0.10:.1f} {cx:.1f},{cy + 2:.1f} Z",
               f"{label} bow {i+1}", fill=ribbon_col, stroke=INK,
               strokeWidth=1.4)


def holly(x, y, ang, s, label):
    """Two jagged leaves + three berries, leaning along the rim."""
    for i, da in enumerate((-26, 22)):
        leaf_at(d, x, y, ang + da, 46 * s, 15 * s, fill="#2E6B3C",
                stroke="#123A1E", label=f"{label} leaf {i+1}", vein=True)
    for i, (dx, dy) in enumerate(((-7, 4), (2, -3), (9, 6))):
        d.shape("ellipse", f"{label} berry {i+1}", x=x + dx - 5.4 * s,
                y=y + dy - 5.4 * s, width=10.8 * s, height=10.8 * s,
                fill=rad((0, "#E86A5A"), (0.6, GARNET), (1, "#6E1C18")),
                stroke=INK, strokeWidth=1.2)


def seal_chop(cx=744, cy=214, s=62):
    """Vermilion chop inside the disc, top right; drawn gold star mark."""
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
    star4(cx, cy, 15, col="#FBE6B4", halo=0, label="Chop star")


# --- field -------------------------------------------------------------------
p.backdrop(top="#0B1F16", bottom="#030907", glow=("#2A5A3C", 16))
dust(d, n=44, r=402, colors=("#F6E3B8", "#D8E8DC"), seed=29, smin=1.0,
     smax=2.4, opmin=8, opmax=24, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim=GOLD, rim2="#5E3A16")
dust(d, n=58, r=392, colors=("#F6E3B8", "#EDF4EE", "#E8C074"), seed=13,
     smin=1.0, smax=2.8, opmin=10, opmax=30, label="Disc dust")
ring_dots(d, r=397, n=56, size=2.6, color=GOLD, opacity=32)

# faint concentric field guides behind the tree
for rr, op in ((168, 12), (262, 10), (342, 8)):
    d.shape("ellipse", f"Field ring {rr}", x=PCX - rr, y=PCY - rr,
            width=2 * rr, height=2 * rr, fill=NONE, stroke=GOLD,
            strokeWidth=1.4, opacity=op)

# --- snow floor hugging the bottom of the disc ---------------------------------
# chord across the disc at y~790; lower edge follows the rim arc itself
d.path("M242,788 Q500,742 758,788 A420,420 0 0 0 242,788 Z",
       "Snow floor",
       fill=lin((0, 756), (0, 880), (0, "#FDFEFB", 66), (0.6, SNOW, 34),
                (1, SNOW, 12)), stroke=NONE)
d.path("M242,788 Q500,742 758,788", "Snow floor edge", fill=NONE,
       stroke="#F8FCFA", strokeWidth=3.2, opacity=55, cap="round")

# --- the tree ------------------------------------------------------------------
d.shape("ellipse", "Tree shadow", x=500 - 170, y=760, width=340, height=40,
        fill=rad((0, INK, 30), (0.6, INK, 14), (1, INK, 0)), stroke=NONE)
# trunk
d.path("M489,648 L486,706 Q500,714 514,706 L511,648 Z", "Trunk",
       fill=lin(486, 648, 514, 706, (0, "#6E4630"), (1, "#3A2014")),
       stroke=INK, strokeWidth=2.4)
# four tiers, narrow to wide
bough(500, 268, 96, 108, "Bough 1", scallops=3)
bough(500, 352, 152, 122, "Bough 2", scallops=4)
bough(500, 448, 208, 132, "Bough 3", scallops=5)
bough(500, 552, 262, 142, "Bough 4", scallops=6)

# snow caught on the tier edges
for i, (x, y, w) in enumerate([(436, 296, 30), (562, 290, 26), (396, 388, 34),
                               (604, 382, 30), (338, 486, 36), (662, 478, 32),
                               (298, 592, 34), (706, 584, 36), (500, 566, 30)]):
    d.shape("ellipse", f"Snow tuft {i+1}", x=x - w / 2, y=y - 9, width=w,
            height=18, fill=rad((0, "#FBFEFC", 80), (1, SNOW, 0)), stroke=NONE)

# star topper
star4(500, 196, 34, label="Topper")
d.path("M496,222 L500,236 L504,222 Z", "Topper stem", fill=GOLD_LO, stroke=NONE)

# candle-lights along the tier edges
for i, (x, y) in enumerate([(452, 300), (548, 296), (404, 390), (596, 384),
                            (466, 420), (534, 428), (352, 492), (648, 486),
                            (436, 530), (566, 538), (308, 600), (692, 592),
                            (404, 636), (596, 630)]):
    candle_dot(x, y, r=4.4, label=f"Light {i+1}")

# baubles: garnet, gold, cream
for i, (x, y, r, c, lo) in enumerate([
        (470, 330, 9, GARNET, "#5E1616"), (532, 338, 8, GOLD, GOLD_LO),
        (420, 428, 10, GOLD, GOLD_LO), (580, 424, 9, GARNET, "#5E1616"),
        (500, 452, 9, CREAM, "#9A8468"), (368, 536, 10, GARNET, "#5E1616"),
        (632, 528, 10, CREAM, "#9A8468"), (500, 560, 10, GOLD, GOLD_LO),
        (438, 596, 9, CREAM, "#9A8468"), (566, 604, 9, GARNET, "#5E1616")]):
    bauble(x, y, r, c, lo, f"Bauble {i+1}")

# gifts at the trunk, seated on the snow floor
gift(428, 706, 74, 56, "#A8352E", "#5E1616", GOLD, "Gift L")
gift(586, 714, 60, 46, "#2F6B4A", "#123A24", "#F6D9A0", "Gift R")

# holly sprigs low on the rim
holly(258, 716, 128, 0.9, "Holly L")
holly(742, 716, 52, 0.9, "Holly R")

# --- seal + caption -----------------------------------------------------------
seal_chop()
caption(p, "CHRISTMAS", "DECEMBER 25 · MIDWINTER FEAST",
        name_color="#F4EBD4", sub_color="#C9A46A",
        name_size=52, tracking_name=86, sub_size=21, tracking_sub=44,
        sub_font=SERIF)
p.finish(SLUG)
