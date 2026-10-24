#!/usr/bin/env python3
"""Hanukkah — Festival Seal V1R00.

Nine-branch chanukiah with the shamash raised at the centre, all nine
candles lit: the flames are the only light source, pooling warm gold over
deep sapphire. Gelt coins at the foot, a faint hexagram behind the arms.
Blue + gold, vermilion chop. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, NONE, INK, GOLD, GOLD_HI, GOLD_LO, PAPER, LATIN,
                          PCX, PCY, PR, lin, rad, gold_lin, smooth, blend)
from festival_kit import seal_disc, glow, dust, ring_dots, flame, caption

SLUG = "hanukkah-V1R00"
HEBREW = "Arial Hebrew"
DIGITS = "Source Sans 3"

p = Plate("Hanukkah — Festival Seal", 1000, 1000)
d = p.d


def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


# --- field ------------------------------------------------------------------
p.backdrop(top="#0B1322", bottom="#03050A", glow=("#223E6E", 14))
p.stars(n=30, color="#F6E3B8", seed=19, maxr=2.2)
seal_disc(p, "#2E528C", "#0A1A34", rim=GOLD, rim2="#4A3418")
# vignette pulls the rim dark so the candlelight reads centre-stage
d.shape("ellipse", "Vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.6, "#000000", 0), (1, "#000000", 58)),
        stroke=NONE)
dust(d, n=58, r=392, colors=("#F6E3B8", "#E8C074", "#9FC0E8"), seed=13,
     smin=1.0, smax=2.8, opmin=8, opmax=26, label="Disc dust")
ring_dots(d, r=396, n=60, size=2.4, color=GOLD, opacity=30)

# faint hexagram on the field, centred behind the arms
HX, HY, HR = 500, 476, 208
for i, a0 in enumerate((-90, 90)):
    pts = [(HX + HR * math.cos(math.radians(a0 + k * 120)),
            HY + HR * math.sin(math.radians(a0 + k * 120))) for k in range(3)]
    d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z",
           f"Hexagram {i+1}", fill=NONE, stroke=GOLD, strokeWidth=2.2,
           opacity=10)

# warm light: the nine flames are the source, pooling over the arms
glow(d, 500, 452, 335, "#FFC46B", a=24, label="Candle light", squash=1.06)
glow(d, 500, 455, 190, "#FFD98A", a=26, label="Candle core")

# --- chanukiah ---------------------------------------------------------------
# ground shadow first
d.shape("ellipse", "Menorah shadow", x=330, y=740, width=340, height=26,
        fill=rad((0, INK, 60), (0.6, INK, 26), (1, INK, 0)), stroke=NONE)

# stem rises base -> bar -> shamash cup, bar drawn across it
d.shape("rectangle", "Stem", x=492, y=496, width=16, height=208,
        fill=lin((492, 0), (508, 0), (0, "#8A5E20"), (0.5, GOLD_HI), (1, "#8A5E20")),
        stroke=INK, strokeWidth=2.6)
d.shape("ellipse", "Stem knop", x=486, y=626, width=28, height=24,
        fill=rad((0, GOLD_HI), (0.7, GOLD), (1, "#8A5E20")),
        stroke=INK, strokeWidth=2.4)

# foot: flared riser on an oval base
d.path("M488,694 C486,706 470,712 458,720 L542,720 C530,712 514,706 512,694 Z",
       "Foot riser", fill=lin((458, 694), (542, 722), (0, "#B8852F"),
                              (0.5, GOLD_HI), (1, "#8A5E20")),
       stroke=INK, strokeWidth=2.6)
d.shape("ellipse", "Foot base", x=444, y=716, width=112, height=20,
        fill=lin((444, 716), (556, 736), (0, "#8A5E20"), (0.45, GOLD_HI),
                 (1, "#7A4E18")), stroke=INK, strokeWidth=2.8)
d.shape("ellipse", "Foot sheen", x=458, y=719, width=52, height=7,
        fill="#FFF3D0", opacity=38, stroke=NONE)

# the arm bar, straight like a chanukiah's
d.shape("rectangle", "Arm bar", x=306, y=546, width=388, height=15, radius=7.5,
        fill=lin((306, 546), (306, 561), (0, "#8A5E20"), (0.5, GOLD_HI),
                 (1, "#8A5E20")), stroke=INK, strokeWidth=2.8)
for x in (314, 686):
    d.shape("ellipse", f"Bar cap {x}", x=x - 7, y=546.5, width=14, height=14,
            fill=rad((0, GOLD_HI), (1, "#8A5E20")), stroke=INK, strokeWidth=2.2)

# cups: little goblets on the bar; shamash cup crowning the stem
CUP_X = [332, 380, 428, 476, 524, 572, 620, 668]


def cup(cx, rim_y, w, label):
    d.path(f"M{cx - w*0.5:.1f},{rim_y:.1f} "
           f"C{cx - w*0.46:.1f},{rim_y + 12:.1f} {cx - w*0.28:.1f},{rim_y + 16:.1f} "
           f"{cx - w*0.18:.1f},{rim_y + 16:.1f} L{cx + w*0.18:.1f},{rim_y + 16:.1f} "
           f"C{cx + w*0.28:.1f},{rim_y + 16:.1f} {cx + w*0.46:.1f},{rim_y + 12:.1f} "
           f"{cx + w*0.5:.1f},{rim_y:.1f} Z",
           f"{label} bowl", fill=lin((cx - w * 0.5, rim_y), (cx + w * 0.5, rim_y + 16),
                                     (0, "#8A5E20"), (0.45, GOLD_HI), (1, "#9A6A24")),
           stroke=INK, strokeWidth=2.2)
    d.shape("ellipse", f"{label} rim", x=cx - w * 0.5, y=rim_y - 3.4,
            width=w, height=6.8, fill=lin(0, rim_y - 3, 0, rim_y + 4,
                                          (0, GOLD_HI), (1, "#9A6A24")),
            stroke=INK, strokeWidth=1.8)
    d.shape("ellipse", f"{label} well", x=cx - w * 0.34, y=rim_y - 2.2,
            width=w * 0.68, height=4.4, fill="#3A2410", opacity=85, stroke=NONE)


for i, cx in enumerate(CUP_X):
    cup(cx, 532, 26, f"Cup {i+1}")
cup(500, 486, 30, "Shamash cup")

# candles: cream and ice-blue alternating, shamash taller ivory
WAX_HI, WAX_LO = "#F8EFD8", "#D9C49A"
BLUE_HI, BLUE_LO = "#D4E7F6", "#8FB4D8"


def candle(cx, top, h, w, hi, lo, label):
    d.shape("rectangle", label, x=cx - w / 2, y=top, width=w, height=h,
            radius=w * 0.22, fill=lin((cx - w / 2, 0), (cx + w / 2, 0),
                                      (0, lo), (0.4, hi), (1, lo)),
            stroke=INK, strokeWidth=1.6)
    d.shape("ellipse", f"{label} top", x=cx - w / 2, y=top - 1.6, width=w,
            height=4.4, fill=hi, stroke=INK, strokeWidth=1.2)
    d.path(f"M{cx:.1f},{top - 1:.1f} L{cx:.1f},{top - 7:.1f}", f"{label} wick",
           fill=NONE, stroke="#2A180C", strokeWidth=2.2, cap="round")


for i, cx in enumerate(CUP_X):
    if i % 2:
        candle(cx, 468, 60, 10, BLUE_HI, BLUE_LO, f"Candle {i+1}")
    else:
        candle(cx, 468, 60, 10, WAX_HI, WAX_LO, f"Candle {i+1}")
candle(500, 416, 66, 12, "#FBF2DC", "#DCC692", "Shamash candle")

# flames last so they sit over every cup edge
for i, cx in enumerate(CUP_X):
    glow(d, cx, 452, 30, "#FFDD9A", a=30, label=f"Flame halo {i+1}")
    flame(d, cx, 461, 40, 17, lean=(i - 3.5) * 0.05, label=f"Flame {i+1}", smoke=0)
glow(d, 500, 396, 40, "#FFDD9A", a=36, label="Shamash halo")
flame(d, 500, 409, 52, 21, label="Shamash flame", smoke=2)

# --- gelt --------------------------------------------------------------------
def gelt(cx, cy, r, label):
    d.shape("ellipse", f"{label} shadow", x=cx - r, y=cy + r * 0.6,
            width=2 * r, height=r * 0.5, fill=INK, opacity=30, stroke=NONE)
    d.shape("ellipse", label, x=cx - r, y=cy - r, width=2 * r, height=2 * r,
            fill=lin((cx - r, cy - r), (cx + r, cy + r), (0, GOLD_HI),
                     (0.55, GOLD), (1, "#9A6A24")), stroke=INK, strokeWidth=2)
    d.shape("ellipse", f"{label} rim", x=cx - r * 0.78, y=cy - r * 0.78,
            width=r * 1.56, height=r * 1.56, fill=NONE, stroke="#8A5E20",
            strokeWidth=1.3, opacity=60)
    s = r * 0.42
    d.path(f"M{cx:.1f},{cy - s:.1f} L{cx + s * 0.88:.1f},{cy + s * 0.5:.1f} "
           f"L{cx - s * 0.88:.1f},{cy + s * 0.5:.1f} Z", f"{label} star a",
           fill=NONE, stroke="#8A5E20", strokeWidth=1.2, opacity=55)
    d.path(f"M{cx:.1f},{cy + s:.1f} L{cx + s * 0.88:.1f},{cy - s * 0.5:.1f} "
           f"L{cx - s * 0.88:.1f},{cy - s * 0.5:.1f} Z", f"{label} star b",
           fill=NONE, stroke="#8A5E20", strokeWidth=1.2, opacity=55)


for i, (x, y, r) in enumerate([(408, 762, 16), (452, 772, 14), (556, 770, 15),
                               (598, 760, 13)]):
    inside(x, y, r + 6, f"gelt {i}")
    gelt(x, y, r, f"Gelt {i+1}")

# --- sparks drifting off the flames ------------------------------------------
for i, (x, y, s) in enumerate([(360, 392, 2.2), (646, 372, 2.0), (414, 340, 1.8),
                               (588, 330, 2.4), (452, 300, 1.6), (548, 286, 1.8),
                               (500, 250, 2.0)]):
    glow(d, x, y, 10, "#FFD98A", a=34, label=f"Spark halo {i+1}")
    d.shape("ellipse", f"Spark {i+1}", x=x - s, y=y - s, width=2 * s,
            height=2 * s, fill="#FFF2C4", opacity=82, stroke=NONE)

# --- chop + caption ----------------------------------------------------------
CHX, CHY, CHW, CHH = 702, 148, 50, 178
inside(CHX + CHW, CHY, 6, "chop TR")
inside(CHX + CHW, CHY + CHH, 6, "chop BR")
d.shape("rectangle", "Chop shadow", x=CHX + 3, y=CHY + 4, width=CHW, height=CHH,
        radius=4, fill="#000000", opacity=30, stroke=NONE)
p.chop("חנוכה", x=CHX, y=CHY, w=CHW, h=CHH, size=25, font=HEBREW)

caption(p, "HANUKKAH", "25 KISLEV – 2 TEVET · DECEMBER",
        sub_font=DIGITS, name_color="#F6E7C8", sub_color="#C9A46A",
        name_size=52, tracking_name=90, sub_size=20, tracking_sub=40)

p.finish(SLUG)
